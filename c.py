import os
import json
from datetime import datetime

# Path to local storage
DATA_FILE = os.path.join("data", "expenses.json")

def load_expenses():
    """safely load expense data from the json file"""
    dir_name = os.path.dirname(DATA_FILE)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # Ensure folder exists
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump([], file)
            return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)  # <-- FIXED: changed json.loads to json.load
    except (json.JSONDecodeError, PermissionError) as e:
        print(f"Error reading database: {e}. Starting fresh.")
        return []

def save_expenses(expenses):
    """save the current list of expenses back to json"""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(expenses, file, indent=4)
    except IOError as e:
        print(f"Could not save data: {e}")

def add_expenses(expenses, raw_description, amount, category="uncategorized"):
    """Creates a structured dictionary and updates local records."""
    record = {
        "id": len(expenses) + 1,
        "date": datetime.today().strftime("%Y-%m-%d %H:%M"),
        "description": raw_description,
        "amount": amount,  # <-- FIXED: added missing amount key
        "category": category
    }
    expenses.append(record)
    save_expenses(expenses)
    print(f"Logged: {raw_description} | Ksh {amount:.2f} ({category})")

def view_expenses(expenses):
    """Displays all currently logged items in a clean command line list."""
    if not expenses:
        print("\n No expenses recorded yet.")
        return

    print("\n--- Current Expense Log ---")
    for item in expenses:
        print(f"[{item['id']}] {item['date']} | {item['description']} -> Ksh {item['amount']:.2f} [{item['category']}]")

if __name__ == "_main_":
    # 1. Load active data
    my_wallet = load_expenses()

    # 2. Add sample transactions to verify write operations
    print("Testing entries...")
    add_expenses(my_wallet, "Uber trip to office", 450.00, "Transport")
    add_expenses(my_wallet, "Dinner at restaurant", 1250.50, "Food")

    # 3. View entries to verify read operations
    view_expenses(my_wallet)  # <-- FIXED: removed trailing raw string syntax error