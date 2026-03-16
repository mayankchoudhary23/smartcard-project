import pandas as pd
import matplotlib.pyplot as plt


def plot_monthly_summary(monthly_df: pd.DataFrame) -> None:
    """
    Plot actual vs optimal net rewards per month.
    """
    if monthly_df.empty:
        raise ValueError("Monthly summary DataFrame is empty; nothing to plot.")

    ax = monthly_df[["actual_net_value", "optimal_net_value"]].plot(kind="bar")
    ax.set_ylabel("Net rewards ($)")
    ax.set_title("Actual vs Optimal Rewards by Month")
    plt.tight_layout()
    plt.show()


def plot_gap_by_category(analysis_df: pd.DataFrame) -> None:
    """
    Plot 'money left on the table' by category.
    """
    if "reward_gap" not in analysis_df.columns:
        raise ValueError("DataFrame must contain 'reward_gap' column.")

    grouped = (
        analysis_df.groupby("category")["reward_gap"]
        .sum()
        .sort_values(ascending=False)
    )

    if grouped.empty:
        raise ValueError("No reward gaps to plot; check analysis DataFrame.")

    ax = grouped.plot(kind="bar")
    ax.set_ylabel("Extra rewards possible ($)")
    ax.set_title("Money Left on the Table by Category")
    plt.tight_layout()
    plt.show()
