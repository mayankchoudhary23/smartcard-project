from typing import List, Dict
import pandas as pd

from .cards import Card


def evaluate_card_for_row(row: pd.Series, card: Card) -> Dict:
    """
    Compute rewards for a specific transaction if a given card was used.
    """
    result = card.compute_reward(
        amount=row["amount_usd"],
        category=row["category"],
        is_foreign=row["is_foreign"],
    )
    result["card"] = card.name
    return result


def find_best_card(row: pd.Series, cards: List[Card]) -> Dict:
    """
    Find the card that gives the maximum net value for a transaction.
    """
    if not cards:
        raise ValueError("Card list is empty; cannot optimize.")

    evaluations = [evaluate_card_for_row(row, c) for c in cards]
    best = max(evaluations, key=lambda x: x["net_value"])
    return best


def analyze_transactions(df: pd.DataFrame, cards: List[Card]) -> pd.DataFrame:
    """
    Add actual vs optimal rewards & gaps to the transactions DataFrame.
    """
    if "card_used" not in df.columns:
        raise ValueError("DataFrame must contain 'card_used' column.")

    card_by_name = {c.name: c for c in cards}
    unknown_cards = set(df["card_used"]) - set(card_by_name.keys())
    if unknown_cards:
        raise ValueError(f"Transactions refer to unknown cards: {unknown_cards}")

    # Actual usage
    actual = df.apply(
        lambda row: evaluate_card_for_row(row, card_by_name[row["card_used"]]),
        axis=1,
        result_type="expand",
    )
    actual.columns = ["actual_gross_reward", "actual_fx_fee", "actual_net_value", "actual_card"]

    # Optimal usage
    optimal = df.apply(
        lambda row: find_best_card(row, cards),
        axis=1,
        result_type="expand",
    )
    optimal.columns = ["optimal_gross_reward", "optimal_fx_fee", "optimal_net_value", "optimal_card"]

    analysis_df = pd.concat([df.reset_index(drop=True), actual, optimal], axis=1)
    analysis_df["reward_gap"] = analysis_df["optimal_net_value"] - analysis_df["actual_net_value"]

    return analysis_df


def monthly_summary(analysis_df: pd.DataFrame) -> pd.DataFrame:
    """
    Time-series monthly summary (this is your time-series financial analysis part):
    - total spent
    - actual net rewards
    - optimal net rewards
    - gap (money left on table)
    """
    if "date" not in analysis_df.columns:
        raise ValueError("DataFrame must contain 'date' column for monthly summary.")

    monthly = (
        analysis_df.set_index("date")
        .resample("ME")
        .agg(
            amount_usd=("amount_usd", "sum"),
            actual_net_value=("actual_net_value", "sum"),
            optimal_net_value=("optimal_net_value", "sum"),
            reward_gap=("reward_gap", "sum"),
        )
    )

    return monthly
