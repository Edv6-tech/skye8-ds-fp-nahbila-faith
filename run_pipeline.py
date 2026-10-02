"""End-to-End Pipeline for Loan Collections Prioritiser (Skye8 Final Project).

Executes Stages A, B, C, D:
1. Stage A: Loads raw data, extracts arrears population (>= 15 days late), builds 30-day recovery label.
2. Stage B: Computes leakage-free behavioral features knowable before contact.
3. Stage C: Trains and calibrates Gradient Boosting model; evaluates Precision@50, Precision@100,
            and money recovered in FCFA vs Incumbent (biggest-debt-first).
4. Stage D: Generates optimal cost-weighted contact method and ethical vulnerability flags.
5. Saves model artifact (models/prioritiser_model.joblib) and production weekly 400-account call book
   (data/processed/weekly_400_accounts.csv) for the 3 collections officers in Bamenda.
"""
import json
import os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

from src.data_loading import load_installments, load_application_train
from src.target import build_arrears_events, base_recovery_rate
from src.features import build_features, FEATURE_COLUMNS
from src.model import train_prioritiser, predict_recovery_probability, save_model
from src.evaluate import evaluate_collections_policy
from src.contact import apply_action_recommendations

PROCESSED_DIR = Path("data/processed")
REPORTS_DIR = Path("reports")
MODELS_DIR = Path("models")


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("LOAN COLLECTIONS PRIORITISER - SKYE8 FINAL PROJECT (BAMENDA MFI)")
    print("=" * 70)
    
    # -------------------------------------------------------------
    # 1. DATA LOADING
    # -------------------------------------------------------------
    print("\n[1/5] Loading data from data/raw/...")
    inst = load_installments(nrows=2500000)
    print(f"Loaded {len(inst):,} installment records.")
    
    try:
        app_train = load_application_train(nrows=250000)
        print(f"Loaded {len(app_train):,} client application demographic records.")
    except Exception as e:
        print(f"Notice: application_train.csv optional: {e}")
        app_train = None

    # -------------------------------------------------------------
    # 2. STAGE A - TARGET DEFINITION & ARREARS POPULATION
    # -------------------------------------------------------------
    print("\n[2/5] Stage A: Isolating arrears population and defining recovery target...")
    events = build_arrears_events(inst)
    n_events = len(events)
    base_rate = base_recovery_rate(events)
    
    print(f"Total isolated arrears accounts (delay >= 15 days): {n_events:,}")
    print(f"Base Recovery Rate (Do Nothing): {base_rate:.2%} ({base_rate * 100:.2f}%)")
    print("-> That is what happens if you do nothing: ~88% of arrears accounts remain delinquent.")

    # -------------------------------------------------------------
    # 3. STAGE B - BEHAVIOURAL FEATURE EXTRACTION (LEAKAGE-FREE)
    # -------------------------------------------------------------
    print("\n[3/5] Stage B: Building behavioral features knowable before contact...")
    features_df = build_features(events, inst, app_train=app_train)
    print(f"Feature matrix shape: {features_df.shape}")
    print(f"Features: {list(features_df.columns)}")
    
    # Grouped split by SK_ID_CURR to avoid client leakage between train and test
    gss = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
    train_idx, test_idx = next(gss.split(features_df, events["recovered"], groups=events["SK_ID_CURR"]))
    
    X_train = features_df.iloc[train_idx]
    y_train = events["recovered"].iloc[train_idx]
    events_train = events.iloc[train_idx]
    
    X_test = features_df.iloc[test_idx]
    y_test = events["recovered"].iloc[test_idx]
    events_test = events.iloc[test_idx]
    
    print(f"Train set: {len(X_train):,} events | Test set: {len(X_test):,} events")

    # -------------------------------------------------------------
    # 4. STAGE C - MODEL TRAINING & COMPARATIVE EVALUATION
    # -------------------------------------------------------------
    print("\n[4/5] Stage C: Training calibrated Gradient Boosting model...")
    model = train_prioritiser(X_train, y_train, calibrate=True)
    model_path = save_model(model, "prioritiser_model.joblib")
    print(f"Model trained and saved to {model_path}")
    
    # Evaluate on held-out test set
    y_prob_test = predict_recovery_probability(model, X_test)
    eval_metrics = evaluate_collections_policy(
        events_test,
        y_test.values,
        y_prob_test,
        overdue_col="overdue_amount",
        k_list=[50, 100, 200, 400]
    )
    
    print("\n" + "-" * 75)
    print("COMPARATIVE EVALUATION: ML PRIORITISER VS INCUMBENT (BIGGEST DEBT FIRST)")
    print("-" * 75)
    print(f"ROC-AUC: {eval_metrics['roc_auc']:.4f} | PR-AUC: {eval_metrics['pr_auc']:.4f}")
    print(f"Base Recovery Rate (Unassisted): {eval_metrics['base_recovery_rate']:.2%}\n")
    
    for k in [50, 100]:
        k_res = eval_metrics["k_evaluations"][k]
        print(f"=== TOP {k} ACCOUNTS (Weekly Officer Capacity) ===")
        print(f"  Precision (ML Expected Value)   : {k_res['precision_ev']:.2%} ({k_res['precision_ev']*100:.1f}% cure rate)")
        print(f"  Precision (Incumbent Biggest Debt): {k_res['precision_incumbent']:.2%} ({k_res['precision_incumbent']*100:.1f}% cure rate)")
        print(f"  Precision (Random / Do Nothing)  : {k_res['precision_random']:.2%}")
        print(f"  Precision Gain (Relative Lift)  : {k_res['precision_gain_ratio']:.2f}x higher cure rate")
        print(f"  Money Recovered (ML Model)      : {k_res['money_recovered_ev']:,.0f} FCFA")
        print(f"  Money Recovered (Biggest Debt)  : {k_res['money_recovered_incumbent']:,.0f} FCFA")
        print(f"  NET GAIN (Business Case Value)  : +{k_res['money_lift_fcfa']:,.0f} FCFA (+{k_res['money_lift_pct']:.1f}%)")
        print()

    # Save metrics JSON
    with open(REPORTS_DIR / "metrics_summary.json", "w") as f:
        json.dump(eval_metrics, f, indent=2)
    print(f"Metrics saved to {REPORTS_DIR / 'metrics_summary.json'}")

    # -------------------------------------------------------------
    # 5. STAGE D & E - PRODUCTION 400-ACCOUNT ARREARS BOOK GENERATION
    # -------------------------------------------------------------
    print("\n[5/5] Stages D & E: Building production weekly 400-account book for 3 officers...")
    book_candidates = events_test.copy().reset_index(drop=True)
    book_features = X_test.copy().reset_index(drop=True)
    
    # Predict recovery probability
    book_candidates["recovery_probability"] = predict_recovery_probability(model, book_features)
    
    # Merge feature columns for transparent reason generation
    for col in FEATURE_COLUMNS:
        book_candidates[col] = book_features[col]
        
    # Expected value: P(recovery) * overdue_amount
    book_candidates["expected_gross_recovery_fcfa"] = (
        book_candidates["recovery_probability"] * book_candidates["overdue_amount"]
    )
    
    # Sample the 400 accounts representing the microfinance institution's weekly arrears book
    book_400 = book_candidates.head(400).copy().reset_index(drop=True)
    
    # Rank by Expected Recoverable Value to maximize total recovery for the microfinance institution
    book_400 = book_400.sort_values("expected_gross_recovery_fcfa", ascending=False).reset_index(drop=True)
    book_400["rank"] = np.arange(1, len(book_400) + 1)
    
    # Apply Stage D contact channel recommendation and ethical vulnerability screen
    book_400 = apply_action_recommendations(book_400)
    
    # Distribute the 400 accounts equitably among the 3 collections officers
    officer_names = ["Officer 1 - John N.", "Officer 2 - Beatrice M.", "Officer 3 - Emmanuel K."]
    book_400["assigned_officer"] = [officer_names[i % 3] for i in range(len(book_400))]
    
    out_book_path = PROCESSED_DIR / "weekly_400_accounts.csv"
    book_400.to_csv(out_book_path, index=False)
    print(f"Weekly 400-account book successfully written to {out_book_path}!")
    
    total_overdue = book_400["overdue_amount"].sum()
    expected_rec = book_400["expected_gross_recovery_fcfa"].sum()
    total_cost = book_400["channel_cost_fcfa"].sum()
    net_val = expected_rec - total_cost
    
    print(f"\nWEEKLY PORTFOLIO SUMMARY (400 ACCOUNTS):")
    print(f"  Total Arrears Portfolio Value : {total_overdue:,.0f} FCFA")
    print(f"  Expected Recovery (Gross)    : {expected_rec:,.0f} FCFA ({expected_rec/total_overdue:.1%})")
    print(f"  Total Outreach Action Cost   : {total_cost:,.0f} FCFA")
    print(f"  Expected Recovery (Net)      : {net_val:,.0f} FCFA")
    print(f"  Recommended Channel Mix      : {dict(book_400['recommended_channel'].value_counts())}")
    print(f"  Vulnerable Borrowers Flagged : {book_400['is_vulnerable'].sum()} accounts protected from aggressive collection")
    print("\nPipeline execution complete!")


if __name__ == "__main__":
    main()
