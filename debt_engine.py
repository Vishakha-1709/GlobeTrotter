"""
GlobeSplit — Multi-Currency Group Expense & Debt Settlement Engine
(WOW Factor 1)

Features:
1. Live / Static Multi-Currency Normalization (EUR, JPY, GBP, INR, USD, etc.)
2. Min-Cash-Flow Debt Settlement Algorithm: Computes the minimum number of
   financial transactions required to settle all debts among travel group members.
"""

from typing import List, Dict, Any


# Standard exchange rates relative to USD base
FX_RATES_TO_USD: Dict[str, float] = {
    "USD": 1.0,
    "EUR": 1.08,     # 1 EUR = 1.08 USD
    "GBP": 1.27,     # 1 GBP = 1.27 USD
    "INR": 0.012,    # 1 INR = 0.012 USD
    "JPY": 0.0065,   # 1 JPY = 0.0065 USD
    "AUD": 0.65,
    "CAD": 0.74,
    "CHF": 1.13,
    "SGD": 0.74,
    "AED": 0.27,
    "THB": 0.028,
}


def convert_currency(amount: float, from_curr: str, to_curr: str) -> float:
    """Converts an amount from one currency to another using exchange rates."""
    from_curr = from_curr.upper()
    to_curr = to_curr.upper()

    if from_curr == to_curr:
        return round(amount, 2)

    usd_rate_from = FX_RATES_TO_USD.get(from_curr, 1.0)
    usd_rate_to = FX_RATES_TO_USD.get(to_curr, 1.0)

    amount_in_usd = amount * usd_rate_from
    converted = amount_in_usd / usd_rate_to
    return round(converted, 2)


def normalize_name(name: str) -> str:
    return name.strip().title() if name else "Traveler"


def compute_net_balances(expenses: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Computes net balance for each member across a list of expenses.
    Positive value: Person is owed money (creditor).
    Negative value: Person owes money (debtor).

    Each expense dictionary should contain:
    - paid_by: str (name of person who paid)
    - converted_amount: float (amount in base currency)
    - splits: List[Dict] with {"name": str, "share": float}
    """
    balances: Dict[str, float] = {}

    for exp in expenses:
        payer = normalize_name(exp["paid_by"])
        total = float(exp["converted_amount"])
        splits = exp.get("splits", [])

        if payer not in balances:
            balances[payer] = 0.0
        balances[payer] += total

        if splits:
            for s in splits:
                person = normalize_name(s["name"])
                share = float(s["share"])
                if person not in balances:
                    balances[person] = 0.0
                balances[person] -= share
        else:
            # If no explicit split provided, assume self-payment
            balances[payer] -= total

    return {k: round(v, 2) for k, v in balances.items() if abs(v) > 0.01}


def settle_debts_min_cash_flow(balances: Dict[str, float]) -> List[Dict[str, Any]]:
    """
    Minimizes the number of cash transactions among members using a greedy matching algorithm.
    Returns:
    [
        {"from_user": "Bob", "to_user": "Alice", "amount": 34.50},
        {"from_user": "Charlie", "to_user": "Alice", "amount": 12.00}
    ]
    """
    creditors = [[name, balance] for name, balance in balances.items() if balance > 0.01]
    debtors = [[name, -balance] for name, balance in balances.items() if balance < -0.01]

    # Sort to greedily match the largest balances first
    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)

    transactions = []
    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        debtor_name, debt_amt = debtors[i]
        creditor_name, cred_amt = creditors[j]

        # Ignore accidental same-person settlement
        if debtor_name.lower() == creditor_name.lower():
            if debt_amt <= cred_amt:
                creditors[j][1] -= debt_amt
                i += 1
            else:
                debtors[i][1] -= cred_amt
                j += 1
            continue

        settled = min(debt_amt, cred_amt)
        transactions.append({
            "from_user": debtor_name,
            "to_user": creditor_name,
            "amount": round(settled, 2)
        })

        debtors[i][1] -= settled
        creditors[j][1] -= settled

        if debtors[i][1] < 0.01:
            i += 1
        if creditors[j][1] < 0.01:
            j += 1

    return transactions
