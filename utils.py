from datetime import datetime

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def validate_amount(amount):
    try:
        value = float(amount)
        if value <= 0:
            return None
        return value
    except ValueError:
        return None

def print_menu():
    print("\n==== SMART EXPENSE TRACKER ====")
    print("1. Add Expense")
    print("2. Add Income")
    print("3. View All Transactions")
    print("4. Monthly Summary")
    print("5. Category Summary")
    print("6. Show Expense Graph")
    print("7. Exit")
