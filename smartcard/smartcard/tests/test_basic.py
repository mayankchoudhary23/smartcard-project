# tests/test_basic.py

import pandas as pd

from smartcard import (
    Card,
    analyze_transactions,
    monthly_summary,
)


def test_card_compute_reward_basic():
    card = Card(
        name="TestCard",
        base_rate=0.01,
        category_bonus={"groceries": 0.02},  # total 3% on groceries
        fx_fee=0.03,
    )

    result_domestic = card.compute_reward(
        amount=100.0,
        category="groceries",
        is_foreign=False,
    )
    # 3% of 100 = 3
    assert abs(result_domestic["gross_reward"] - 3.0) < 1e-9
    assert abs(result_domestic["fx_fee"] - 0.0) < 1e-9
    assert abs(result_domestic["net_value"] - 3.0) < 1e-9

    result_foreign = card.compute_reward(
        amount=100.0,
        category="groceries",
        is_foreign=True,
    )
    # gross 3, FX fee 3, net 0
    assert abs(result_foreign["gross_reward"] - 3.0) < 1e-9
    assert abs(result_foreign["fx_fee"] - 3.0) < 1e-9
    assert abs(result_foreign["net_value"] - 0.0) < 1e-9


def test_analyze_and_monthly_summary():
    # Create two simple cards
    cards = [
        Card("BaseCard", base_rate=0.01, category_bonus={}, fx_fee=0.03),
        Card("GroceriesPro", base_rate=0.01, category_bonus={"groceries": 0.02}, fx_fee=0.00),
    ]

    # Create a tiny transactions DataFrame
    data = {
        "date": pd.to_datetime(["2024-01-01", "2024-01-15"]),
        "description": ["Groceries A", "Groceries B"],
        "category": ["groceries", "groceries"],
        "amount_usd": [100.0, 200.0],
        "is_foreign": [False, False],
        "card_used": ["BaseCard", "BaseCard"],  # suboptimal choice
    }
    df = pd.DataFrame(data)

    # Run analysis
    analysis_df = analyze_transactions(df, cards)

    # We expect some positive reward_gap (GroceriesPro is better)
    assert "reward_gap" in analysis_df.columns
    assert analysis_df["reward_gap"].sum() > 0

    # Monthly summary should have one row (Jan 2024)
    monthly = monthly_summary(analysis_df)
    assert not monthly.empty
    assert "actual_net_value" in monthly.columns
    assert "optimal_net_value" in monthly.columns
    assert "reward_gap" in monthly.columns


if __name__ == "__main__":
    test_card_compute_reward_basic()
    test_analyze_and_monthly_summary()
    print("All tests passed.")
