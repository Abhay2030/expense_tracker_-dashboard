from data_handler import get_all_transactions
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

BUDGET_LIMIT = 10000  # monthly budget limit

def monthly_summary():
    transactions = get_all_transactions()
    current_month = datetime.now().strftime("%Y-%m")

    income = 0
    expense = 0

    for t in transactions:
        if t["date"].startswith(current_month):
            if t["type"] == "income":
                income += float(t["amount"])
            else:
                expense += float(t["amount"])

    savings = income - expense

    print("\n=== Monthly Summary ===")
    print(f"Income: {income}")
    print(f"Expense: {expense}")
    print(f"Savings: {savings}")

    if expense > BUDGET_LIMIT:
        print("⚠ WARNING: Budget limit exceeded!")

def category_summary():
    transactions = get_all_transactions()
    categories = defaultdict(float)

    for t in transactions:
        if t["type"] == "expense":
            categories[t["category"]] += float(t["amount"])

    print("\n=== Category Summary ===")
    for cat, amount in categories.items():
        print(f"{cat}: {amount}")

def show_graph():
    transactions = get_all_transactions()
    categories = defaultdict(float)

    for t in transactions:
        if t["type"] == "expense":
            categories[t["category"]] += float(t["amount"])

    if not categories:
        print("No expense data to display.")
        return

    plt.bar(categories.keys(), categories.values())
    plt.title("Expense Breakdown by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
