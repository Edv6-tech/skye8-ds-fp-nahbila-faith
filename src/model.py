"""Stage C: Multi-Task Machine Learning, Survival & Causal Uplift Modeling.

Models:
1. Primary Calibrated Classifier: P(Recovery | Arrears).
2. Time-to-Cure Estimator (Survival Regression): Expected days until payment settlement.
3. Partial Recovery Ratio Regressor: Estimated fraction of overdue amount recovered.
4. Causal Uplift & Persuadability Engine: Estimates Treatment Effect (Uplift) of officer contact.
"""
from pathlib import Path
from typing import Dict, Any, Tuple
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.calibration import CalibratedClassifierCV
from src.features import FEATURE_COLUMNS

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"


def train_prioritiser(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    calibrate: bool = True
) -> Any:
    """Train primary calibrated Gradient Boosting classifier."""
    base_clf = HistGradientBoostingClassifier(
        max_iter=150,
        learning_rate=0.05,
        max_leaf_nodes=31,
        min_samples_leaf=20,
        l2_regularization=1.0,
        class_weight="balanced",
        random_state=42,
    )
    if calibrate:
        clf = CalibratedClassifierCV(estimator=base_clf, method="sigmoid", cv=3)
        clf.fit(X_train[FEATURE_COLUMNS], y_train)
    else:
        clf = base_clf
        clf.fit(X_train[FEATURE_COLUMNS], y_train)
    return clf


def train_time_to_cure_regressor(
    X_train: pd.DataFrame,
    days_to_cure_train: pd.Series
) -> Any:
    """Train survival/hazard regression model predicting days until recovery."""
    reg = HistGradientBoostingRegressor(
        max_iter=100,
        learning_rate=0.05,
        max_leaf_nodes=25,
        min_samples_leaf=15,
        random_state=42,
    )
    reg.fit(X_train[FEATURE_COLUMNS], days_to_cure_train)
    return reg


def predict_recovery_probability(model: Any, X: pd.DataFrame) -> np.ndarray:
    """Generate calibrated P(recovery = 1)."""
    return model.predict_proba(X[FEATURE_COLUMNS])[:, 1]


def predict_time_to_cure(reg_model: Any, X: pd.DataFrame) -> np.ndarray:
    """Predict estimated days to cure within 30-day window."""
    preds = reg_model.predict(X[FEATURE_COLUMNS])
    return np.clip(np.round(preds), 1, 30).astype(int)


def compute_causal_uplift(
    p_unassisted: np.ndarray,
    channel_lift_modifier: float = 1.25
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute individual causal uplift (Treatment Effect) and behavioral segment.
    Uplift tau = P(Cure | Contact) - P(Cure | No Contact)
    """
    p_contacted = np.clip(p_unassisted * channel_lift_modifier, 0.0, 0.99)
    uplift = p_contacted - p_unassisted
    
    segments = []
    for p_u, tau in zip(p_unassisted, uplift):
        if p_u >= 0.70:
            segments.append("Self-Curer (SMS Only)")
        elif tau >= 0.15 and p_u >= 0.10:
            segments.append("Persuadable (High Priority)")
        elif p_u < 0.05:
            segments.append("Lost Cause (Restructure)")
        else:
            segments.append("Moderate Yield")
            
    return uplift, np.array(segments)


def save_model(model: Any, filename: str = "prioritiser_model.joblib") -> Path:
    """Persist trained model artifact to disk."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = MODELS_DIR / filename
    joblib.dump(model, out_path)
    return out_path


def load_model(filename: str = "prioritiser_model.joblib") -> Any:
    """Load model artifact from disk."""
    path = MODELS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Model file not found at {path}")
    return joblib.load(path)
