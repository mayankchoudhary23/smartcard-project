import os
print("Current working directory:", os.getcwd())


from smartcard import (
    load_cards_from_csv,
    load_transactions,
    analyze_transactions,
    monthly_summary,
    plot_monthly_summary,
    plot_gap_by_category,
)

# TODO: create these CSVs later
cards = load_cards_from_csv("data/cards.csv")
tx = load_transactions("data/transactions.csv")

analysis = analyze_transactions(tx, cards)
print(analysis.head())
print("Total money left on the table: ", analysis["reward_gap"].sum())

monthly = monthly_summary(analysis)
print(monthly)

plot_monthly_summary(monthly)
plot_gap_by_category(analysis)
