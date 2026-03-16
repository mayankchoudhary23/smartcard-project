# SmartCard 💳

A modular Python package for **time-series financial analysis of personal card spending** — quantifying actual rewards earned, comparing them against optimal alternatives, and identifying inefficiencies across time and spending categories.

---

## Features

- 📊 Compare **actual vs optimal** card rewards per transaction
- 📅 **Monthly time-series** aggregation of reward performance
- 💸 Quantify **reward gaps** — money left on the table
- 🗂️ Category-level breakdown of missed opportunities
- 🔒 Robust data validation and error handling throughout

---

## Project Structure
```
smartcard-project/
├── smartcard/
│   ├── __init__.py
│   ├── cards.py          # Card abstraction & CSV loader
│   ├── transactions.py   # Transaction ingestion & validation
│   ├── optimizer.py      # Actual vs optimal reward analysis
│   └── plots.py          # Visualization utilities
├── data/
│   ├── cards.csv         # Card definitions (user-provided)
│   └── transactions.csv  # Transaction history (user-provided)
├── examples/
│   └── example_usage.py
├── tests/
│   └── test_basic.py
├── requirements.txt
└── README.md
```

---

## Installation
```bash
git clone https://github.com/YOUR_USERNAME/smartcard-project.git
cd smartcard-project
pip install -r requirements.txt
```

---

## Quick Start
```python
from smartcard import load_cards_from_csv, load_transactions
from smartcard import analyze_transactions, monthly_summary
from smartcard import plot_monthly_summary, plot_gap_by_category

# Load data
cards = load_cards_from_csv("data/cards.csv")
transactions = load_transactions("data/transactions.csv")

# Analyze
analysis = analyze_transactions(transactions, cards)
monthly = monthly_summary(analysis)

# Visualize
plot_monthly_summary(monthly)
plot_gap_by_category(analysis)
```

---

## Data Format

### `data/cards.csv`
| name  | base_rate | fx_fee | bonus_groceries | bonus_travel |
|-------|-----------|--------|-----------------|--------------|
| CardA | 0.01      | 0.03   | 0.04            | 0.02         |
| CardB | 0.02      | 0.00   | 0.00            | 0.03         |

### `data/transactions.csv`
| date       | description  | category  | amount_usd | is_foreign | card_used |
|------------|--------------|-----------|------------|------------|-----------|
| 2024-01-15 | Whole Foods  | groceries | 85.00      | False      | CardA     |
| 2024-01-20 | Delta Flight | travel    | 420.00     | True       | CardB     |

---

## Dependencies

- `pandas`
- `numpy`
- `matplotlib`

---

## License

MIT License
