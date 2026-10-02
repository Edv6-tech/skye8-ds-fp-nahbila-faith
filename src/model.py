"""Stage C: Model training and probability prediction.

Trains a Gradient Boosting model to predict the probability of recovery
given that an account has reached 15+ days in arrears.
"""
from pathlib import Path
from typing import Dict, Any, Tuple
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from src.features import FEATURE_COLUMNS

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"


def get_model(random_state: int = 42) -> HistGradientBoostingClassifier:
    """Instantiate a gradient boosted decision tree model."""
    return HistGradientBoostingClassifier(
        max_iter=150,
        learning_rate=0.05,
        max_leaf_nodes=31,
        min_samples_leaf=20,
        l2_regularization=1.0,
        class_weight="balanced",
        random_state=random_state,
    )


def train_prioritiser(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    calibrate: bool = True
) -> Any:
    """Train Gradient Boosting model to estimate P(recovery | arrears)."""
    base_clf = get_model()
    
    if calibrate:
        # Probability calibration via sigmoid/isotonic to guarantee realistic probabilities
        clf = CalibratedClassifierCV(estimator=base_clf, method="sigmoid", cv=3)
        clf.fit(X_train[FEATURE_COLUMNS], y_train)
    else:
        clf = base_clf
        clf.fit(X_train[FEATURE_COLUMNS], y_train)
        
    return clf


def predict_recovery_probability(model: Any, X: pd.DataFrame) -> np.ndarray:
    """Generate calibrated probability scores P(recovered = 1)."""
    return model.predict_proba(X[FEATURE_COLUMNS])[:, 1]


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
