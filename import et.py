import csv
from datetime import datetime
import os

# Predefined expense categories
CATEGORIES = [
    "Food", 
    "Transportation", 
    "Entertainment", 
    "Utilities", 
    "Other"
]

DATA_FILE = "expenses.csv"

def initialize_data_file():
    """Create CSV file with headers if it doesn't exist"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Amount", "Category", "Description"])
            writer.writeheader()

def add_expense():
    """Add a new expense to the tracker"""
    print("\n=== Add New Expense ===")
    
    # Date input with validation
    while True:
        date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date_str:
            date = datetime.today().strftime("%Y-%m-%d")
            break
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            date = date_str
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # Amount input with validation
    while True:
        try:
            amount = float(input("Enter amount spent: ₹"))
            if amount <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive number.")

    # Category selection
    print("\nSelect a category:")
    for i, category in enumerate(CATEGORIES, 1):
        print(f"{i}. {category}")
    
    while True:
        try:
            choice = int(input("Enter category number: "))
            if 1 <= choice <= len(CATEGORIES):
                category = CATEGORIES[choice-1]
                break
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Please enter a valid number.")

    description = input("Enter a brief description: ").strip()

    # Save to CSV
    with open(DATA_FILE, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Amount", "Category", "Description"])
        writer.writerow({
            "Date": date,
            "Amount": f"{amount:.2f}",
            "Category": category,
            "Description": description
        })
    
    print("\nExpense added successfully!")

def view_summary():
    """Display expense summaries"""
    print("\n=== Expense Summary ===")
    
    # Load existing expenses
    expenses = []
    with open(DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append(row)

    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n1. Monthly Summary\n2. Category Summary")
    choice = input("Select summary type (1/2): ").strip()

    if choice == '1':
        # Monthly summary
        year = input("Enter year (YYYY): ").strip()
        month = input("Enter month (MM): ").strip()
        total = 0.0
        
        for expense in expenses:
            expense_date = datetime.strptime(expense['Date'], "%Y-%m-%d")
            if expense_date.year == int(year) and expense_date.month == int(month):
                total += float(expense['Amount'])
        
        print(f"\nTotal expenses for {month}/{year}: ₹{total:.2f}")

    elif choice == '2':
        # Category summary
        category_totals = {category: 0.0 for category in CATEGORIES}
        
        for expense in expenses:
            category = expense['Category']
            if category in category_totals:
                category_totals[category] += float(expense['Amount'])
        
        print("\nCategory-wise Expenditure:")
        for category, total in category_totals.items():
            print(f"{category}: ₹{total:.2f}")

    else:
        print("Invalid choice.")

def main_menu():
    """Display main menu and handle user input"""
    initialize_data_file()
    
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add New Expense")
        print("2. View Expense Summary")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            print("\nThank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()