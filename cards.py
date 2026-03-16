from dataclasses import dataclass, field
from typing import Dict, List
import pandas as pd


REQUIRED_CARD_COLUMNS = ["name", "base_rate", "fx_fee"]


@dataclass
class Card:
    """
    Represents a credit/debit card with cashback and FX fee rules.
    """
    name: str
    base_rate: float              # e.g. 0.01 for 1%
    category_bonus: Dict[str, float] = field(default_factory=dict)
    fx_fee: float = 0.0           # e.g. 0.03 for 3%

    def __post_init__(self):
        if self.base_rate < 0:
            raise ValueError("base_rate must be non-negative.")
        if self.fx_fee < 0:
            raise ValueError("fx_fee must be non-negative.")

    def effective_rate(self, category: str) -> float:
        """
        Base + category bonus (if any).
        """
        bonus = self.category_bonus.get(category, 0.0)
        return self.base_rate + bonus

    def compute_reward(self, amount: float, category: str, is_foreign: bool = False) -> Dict[str, float]:
        """
        Compute gross reward, FX fee, and net value for a given purchase.
        """
        if amount < 0:
            raise ValueError("Amount must be non-negative.")

        rate = self.effective_rate(category)
        gross_reward = amount * rate
        fx_fee_amount = amount * self.fx_fee if is_foreign else 0.0
        net_value = gross_reward - fx_fee_amount

        return {
            "gross_reward": gross_reward,
            "fx_fee": fx_fee_amount,
            "net_value": net_value,
        }


def load_cards_from_csv(csv_path: str) -> List[Card]:
    """
    Load card definitions from a CSV file.

    Required columns:
      - name
      - base_rate
      - fx_fee
    Optional bonus columns:
      - bonus_groceries, bonus_travel, etc.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Card file not found: {csv_path}") from e
    except Exception as e:
        raise RuntimeError(f"Error reading card file '{csv_path}': {e}") from e

    missing = [c for c in REQUIRED_CARD_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in card file: {missing}")

    cards: List[Card] = []
    for _, row in df.iterrows():
        try:
            name = str(row["name"])
            base_rate = float(row["base_rate"])
            fx_fee = float(row["fx_fee"])
        except Exception as e:
            raise ValueError(f"Invalid numeric values in card row: {row.to_dict()}") from e

        # bonus_* columns → category_bonus dict
        category_bonus: Dict[str, float] = {}
        for col in df.columns:
            if col.startswith("bonus_") and not pd.isna(row[col]):
                category = col.replace("bonus_", "")
                try:
                    category_bonus[category] = float(row[col])
                except Exception as e:
                    raise ValueError(
                        f"Invalid bonus value for card '{name}', column '{col}'."
                    ) from e

        cards.append(Card(name=name, base_rate=base_rate,
                          category_bonus=category_bonus, fx_fee=fx_fee))

    if not cards:
        raise ValueError("No cards loaded from file; check input CSV.")

    return cards
