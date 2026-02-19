from utils import print_menu, validate_amount
from data_handler import initialize_file, add_transaction, get_all_transactions
from reports import monthly_summary, category_summary, show_graph

def view_transactions():
    transactions = get_all_transactions()
    print("\n=== All Transactions ===")
    for t in transactions:
        print(f"{t['date']} | {t['type']} | {t['category']} | {t['amount']}")

def main():
    initialize_file()

    while True:
        print_menu()
        choice = input("Select an option: ")

        if choice == "1":
            amount = validate_amount(input("Enter expense amount: "))
            if not amount:
                print("Invalid amount.")
                continue
            category = input("Enter category: ")
            add_transaction("expense", amount, category)
            print("Expense added successfully.")

        elif choice == "2":
            amount = validate_amount(input("Enter income amount: "))
            if not amount:
                print("Invalid amount.")
                continue
            category = input("Enter source: ")
            add_transaction("income", amount, category)
            print("Income added successfully.")

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            monthly_summary()

        elif choice == "5":
            category_summary()

        elif choice == "6":
            show_graph()

        elif choice == "7":
            print("Exiting program.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
