from pathlib import Path
import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"


def load_installments(nrows=None) -> pd.DataFrame:
    """Home Credit instalment payment history."""
    return pd.read_csv(RAW / "installments_payments.csv", nrows=nrows)


def load_previous_application(nrows=None) -> pd.DataFrame:
    return pd.read_csv(RAW / "previous_application.csv", nrows=nrows)


def load_application_train(nrows=None) -> pd.DataFrame:
    return pd.read_csv(RAW / "application_train.csv", nrows=nrows)
