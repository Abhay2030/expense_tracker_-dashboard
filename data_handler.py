import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"
FIELDNAMES = ["type", "amount", "category", "date"]

def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

def add_transaction(t_type, amount, category):
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow({
            "type": t_type,
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d")
        })

def get_all_transactions():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)