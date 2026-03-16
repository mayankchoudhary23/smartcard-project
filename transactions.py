from typing import List
from datetime import datetime
import pandas as pd

REQUIRED_TX_COLUMNS: List[str] = [
    "date",         # YYYY-MM-DD
    "description",
    "category",
    "amount_usd",
    "is_foreign",
    "card_used",
]


def load_transactions(csv_path: str) -> pd.DataFrame:
    """
    Load and validate transaction data from CSV.

    Required columns: date, description, category, amount_usd, is_foreign, card_used
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Transactions file not found: {csv_path}") from e
    except Exception as e:
        raise RuntimeError(f"Error reading transactions file '{csv_path}': {e}") from e

    missing = [c for c in REQUIRED_TX_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in transactions file: {missing}")

    # Parse dates
    try:
        df["date"] = pd.to_datetime(df["date"])
    except Exception as e:
        raise ValueError("Could not parse 'date' column to datetime.") from e

    # Validate amounts
    if (df["amount_usd"] < 0).any():
        raise ValueError("Found negative amounts in 'amount_usd'; must be non-negative.")

    # Ensure boolean
    if df["is_foreign"].dtype != bool:
        try:
            df["is_foreign"] = df["is_foreign"].astype(bool)
        except Exception as e:
            raise ValueError("Column 'is_foreign' must be convertible to bool.") from e

    return df
