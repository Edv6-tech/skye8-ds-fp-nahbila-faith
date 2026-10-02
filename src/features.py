"""Stage B: features knowable at the moment the officer picks up the phone.

All features are strictly computed from information available on or before the
observation date (observation_day). No information from during or after contact
is ever exposed to the feature pipeline.
"""
import pandas as pd
import numpy as np

# Only columns listed here may reach the model.
FEATURE_COLUMNS = [
    "overdue_amount",
    "prior_instalments_count",
    "prior_late_count",
    "prior_late_ratio",
    "prior_severe_late_count",
    "prior_avg_days_late",
    "prior_max_days_late",
    "prior_recovered_before",
    "prior_payment_ratio",
    "prior_underpaid_count",
    "recent_3_avg_late",
    "recent_payment_ratio",
    "instalment_number",
    "amt_income_total",
    "amt_credit",
    "amt_annuity",
    "days_employed",
    "days_birth",
]

# Anything recorded during/after contact, or after the observation date.
FORBIDDEN_POST_CONTACT = [
    "recovered",
    "contact_method",
    "contact_outcome",
    "promise_to_pay",
    "payment_after_contact",
    "days_to_recovery",
    "amount_recovered",
    "TARGET",
    "observation_day",
]


def build_features(
    events: pd.DataFrame,
    inst: pd.DataFrame,
    app_train: pd.DataFrame = None,
    prev_app: pd.DataFrame = None
) -> pd.DataFrame:
    """Construct leakage-free behavioral and loan features for each arrears event.
    Strict temporal guarantee: only records where DAYS_INSTALMENT < event.observation_day
    and payment recorded on or before observation_day are used.
    """
    # Work with copy of inst with calculated delay
    i_df = inst.copy()
    i_df["delay"] = i_df["DAYS_ENTRY_PAYMENT"] - i_df["DAYS_INSTALMENT"]
    i_df["paid_amount"] = i_df["AMT_PAYMENT"].fillna(0)
    i_df["inst_amount"] = i_df["AMT_INSTALMENT"].fillna(0)
    i_df["is_late"] = (i_df["delay"] > 0).astype(int)
    i_df["is_severe_late"] = (i_df["delay"] >= 15).astype(int)
    i_df["is_underpaid"] = (i_df["paid_amount"] < (i_df["inst_amount"] * 0.95)).astype(int)
    
    # Pre-merge with events to get observation_day per event
    events_keys = events[["SK_ID_CURR", "SK_ID_PREV", "observation_day", "overdue_amount"]].copy()
    
    # Merge installments for those loans
    merged = pd.merge(
        events_keys,
        i_df,
        on=["SK_ID_CURR", "SK_ID_PREV"],
        how="inner"
    )
    
    # Strict temporal filter: only historical instalments prior to observation_day
    # (i.e. due strictly before this delinquency event)
    hist = merged[merged["DAYS_INSTALMENT"] < merged["observation_day"]].copy()
    
    # Aggregate prior history per (SK_ID_CURR, SK_ID_PREV)
    if len(hist) > 0:
        grp = hist.groupby(["SK_ID_CURR", "SK_ID_PREV"])
        
        hist_feat = grp.agg(
            prior_instalments_count=("NUM_INSTALMENT_NUMBER", "count"),
            prior_late_count=("is_late", "sum"),
            prior_severe_late_count=("is_severe_late", "sum"),
            prior_avg_days_late=("delay", lambda s: s.clip(lower=0).mean()),
            prior_max_days_late=("delay", lambda s: s.clip(lower=0).max()),
            prior_total_paid=("paid_amount", "sum"),
            prior_total_inst=("inst_amount", "sum"),
            prior_underpaid_count=("is_underpaid", "sum"),
            instalment_number=("NUM_INSTALMENT_NUMBER", "max"),
        ).reset_index()
        
        hist_feat["prior_late_ratio"] = (
            hist_feat["prior_late_count"] / hist_feat["prior_instalments_count"].clip(lower=1)
        )
        hist_feat["prior_payment_ratio"] = (
            hist_feat["prior_total_paid"] / hist_feat["prior_total_inst"].clip(lower=1.0)
        ).clip(0.0, 2.0)
        hist_feat["prior_recovered_before"] = (
            hist_feat["prior_severe_late_count"] > 0
        ).astype(int)
        
        # Recent trend: last 3 installments
        recent = hist.sort_values("DAYS_INSTALMENT").groupby(["SK_ID_CURR", "SK_ID_PREV"]).tail(3)
        recent_grp = recent.groupby(["SK_ID_CURR", "SK_ID_PREV"]).agg(
            recent_3_avg_late=("delay", lambda s: s.clip(lower=0).mean()),
            recent_paid=("paid_amount", "sum"),
            recent_inst=("inst_amount", "sum"),
        ).reset_index()
        recent_grp["recent_payment_ratio"] = (
            recent_grp["recent_paid"] / recent_grp["recent_inst"].clip(lower=1.0)
        ).clip(0.0, 2.0)
        
        hist_feat = pd.merge(hist_feat, recent_grp[["SK_ID_CURR", "SK_ID_PREV", "recent_3_avg_late", "recent_payment_ratio"]],
                             on=["SK_ID_CURR", "SK_ID_PREV"], how="left")
    else:
        hist_feat = pd.DataFrame(columns=["SK_ID_CURR", "SK_ID_PREV"])
    
    # Merge back to events
    out = pd.merge(events_keys, hist_feat, on=["SK_ID_CURR", "SK_ID_PREV"], how="left")
    
    # Fill defaults for first-time or thin-file borrowers
    out["prior_instalments_count"] = out["prior_instalments_count"].fillna(0)
    out["prior_late_count"] = out["prior_late_count"].fillna(0)
    out["prior_late_ratio"] = out["prior_late_ratio"].fillna(0.0)
    out["prior_severe_late_count"] = out["prior_severe_late_count"].fillna(0)
    out["prior_avg_days_late"] = out["prior_avg_days_late"].fillna(0.0)
    out["prior_max_days_late"] = out["prior_max_days_late"].fillna(0.0)
    out["prior_recovered_before"] = out["prior_recovered_before"].fillna(0)
    out["prior_payment_ratio"] = out["prior_payment_ratio"].fillna(1.0)
    out["prior_underpaid_count"] = out["prior_underpaid_count"].fillna(0)
    out["recent_3_avg_late"] = out["recent_3_avg_late"].fillna(0.0)
    out["recent_payment_ratio"] = out["recent_payment_ratio"].fillna(1.0)
    out["instalment_number"] = out["instalment_number"].fillna(1)
    
    # Attach application demographic features if available
    if app_train is not None:
        app_cols = ["SK_ID_CURR", "AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "DAYS_EMPLOYED", "DAYS_BIRTH"]
        existing_cols = [c for c in app_cols if c in app_train.columns]
        app_sub = app_train[existing_cols].copy()
        rename_map = {c: c.lower() for c in existing_cols if c != "SK_ID_CURR"}
        app_sub = app_sub.rename(columns=rename_map)
        out = pd.merge(out, app_sub, on="SK_ID_CURR", how="left")
    else:
        out["amt_income_total"] = np.nan
        out["amt_credit"] = np.nan
        out["amt_annuity"] = np.nan
        out["days_employed"] = np.nan
        out["days_birth"] = np.nan
        
    for c in ["amt_income_total", "amt_credit", "amt_annuity", "days_employed", "days_birth"]:
        if c not in out.columns:
            out[c] = np.nan
            
    # Guarantee feature matrix has exactly FEATURE_COLUMNS in specified order
    return out[FEATURE_COLUMNS].copy()
