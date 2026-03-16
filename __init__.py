"""
smartcard: Personal card usage & time-series rewards analyzer.
"""

from .cards import Card, load_cards_from_csv
from .transactions import load_transactions
from .optimizer import analyze_transactions, monthly_summary
from .plots import plot_monthly_summary, plot_gap_by_category

__all__ = [
    "Card",
    "load_cards_from_csv",
    "load_transactions",
    "analyze_transactions",
    "monthly_summary",
    "plot_monthly_summary",
    "plot_gap_by_category",
]
