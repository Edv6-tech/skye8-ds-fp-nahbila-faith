"""Unit tests for multi-task modeling, spatial clustering, and bilingual scripts."""
import numpy as np
import pandas as pd
import pytest
from src.features import FEATURE_COLUMNS
from src.model import (
    train_prioritiser,
    train_time_to_cure_regressor,
    train_partial_recovery_regressor,
    predict_recovery_probability,
    predict_time_to_cure,
    predict_partial_recovery_ratio,
    compute_causal_uplift,
    compute_xai_waterfall
)
from src.contact import (
    assign_bamenda_quarter,
    generate_bilingual_scripts,
    calculate_benskin_route_savings,
    apply_action_recommendations
)


@pytest.fixture
def dummy_data():
    np.random.seed(42)
    n = 60
    X = pd.DataFrame(np.random.randn(n, len(FEATURE_COLUMNS)), columns=FEATURE_COLUMNS)
    X["overdue_amount"] = np.random.uniform(10000, 200000, size=n)
    X["prior_payment_ratio"] = np.random.uniform(0.5, 1.2, size=n)
    X["prior_avg_days_late"] = np.random.uniform(0, 20, size=n)
    X["harvest_season"] = np.random.choice([0, 1], size=n)
    X["school_fee_shock"] = np.random.choice([0, 1], size=n)
    X["bureau_total_debt"] = np.random.uniform(0, 400000, size=n)
    X["bureau_active_loans"] = np.random.choice([0, 1, 2], size=n)
    y = pd.Series(np.random.choice([0, 1], size=n, p=[0.7, 0.3]))
    ttc = pd.Series(np.random.randint(3, 28, size=n))
    ratio = pd.Series(np.random.uniform(0.4, 1.0, size=n))
    return X, y, ttc, ratio


def test_model_training_and_inference(dummy_data):
    X, y, ttc, ratio = dummy_data
    # 1. Calibrated Classifier
    clf = train_prioritiser(X, y, calibrate=True)
    probs = predict_recovery_probability(clf, X)
    assert len(probs) == len(X)
    assert np.all((probs >= 0.0) & (probs <= 1.0))

    # 2. Survival Regressor
    reg_ttc = train_time_to_cure_regressor(X, ttc)
    days = predict_time_to_cure(reg_ttc, X)
    assert len(days) == len(X)
    assert np.all((days >= 1) & (days <= 30))

    # 3. Partial Recovery Ratio
    reg_ratio = train_partial_recovery_regressor(X, ratio)
    ratios = predict_partial_recovery_ratio(reg_ratio, X)
    assert len(ratios) == len(X)
    assert np.all((ratios >= 0.35) & (ratios <= 1.00))


def test_causal_uplift_and_segmentation():
    p = np.array([0.85, 0.40, 0.02, 0.15])
    uplift, segments = compute_causal_uplift(p)
    assert len(uplift) == 4
    assert len(segments) == 4
    assert "Self-Curer (SMS Only)" in segments[0]
    assert "Persuadable (High Priority)" in segments[1]
    assert "Lost Cause (Restructure)" in segments[2]


def test_xai_waterfall():
    sample_row = pd.Series({
        "prior_payment_ratio": 0.98,
        "prior_avg_days_late": 1.0,
        "harvest_season": 1,
        "bureau_total_debt": 0.0,
        "bureau_active_loans": 0,
        "overdue_amount": 25000.0,
        "school_fee_shock": 0
    })
    res = compute_xai_waterfall(sample_row)
    assert "top_positive" in res
    assert "top_negative" in res
    assert len(res["top_positive"]) > 0
    assert any("Repayment" in d["factor"] or "Punctual" in d["factor"] for d in res["top_positive"])


def test_bamenda_quarters_and_bilingual_scripts():
    qtr = assign_bamenda_quarter(103380)
    assert any(z in qtr for z in ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"])

    eng, pid = generate_bilingual_scripts(
        account_id=103380,
        loan_id=204551,
        overdue_amount=75000,
        assigned_officer="Officer 2 - Beatrice M.",
        is_vulnerable=False,
        segment="Persuadable"
    )
    assert "Beatrice" in eng
    assert "75,000" in eng
    assert "di salute you" in pid or "Credit Union" in pid


def test_benskin_route_savings():
    df_field = pd.DataFrame({
        "recommended_channel": ["FIELD_VISIT"] * 6,
        "bamenda_quarter": [
            "Commercial Avenue / Food Market (Zone 1)",
            "Commercial Avenue / Food Market (Zone 1)",
            "Nkwen / Mile 2 - Mile 4 (Zone 2)",
            "Nkwen / Mile 2 - Mile 4 (Zone 2)",
            "Mankon / Small Mankon (Zone 4)",
            "Mankon / Small Mankon (Zone 4)"
        ]
    })
    savings = calculate_benskin_route_savings(df_field)
    assert savings["km_saved"] > 0
    assert savings["fuel_cash_saved_fcfa"] > 0
    assert savings["pct_distance_saved"] > 30.0
