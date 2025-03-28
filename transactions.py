# transactions.py

def menu_options():
    # This is now handled by the web interface (the index page)
    return {
        "1": "Add Income",
        "2": "Add Expense",
        "3": "Show Balance",
        "4": "Show Transaction History",
    }

def add_income(transactions_database: dict, amount: int, description: str) -> dict:
    # Update balance
    transactions_database["balance"] += amount

    # Add transaction
    transactions_database["transactions"].append({
        "type": "income",
        "amount": amount,
        "description": description
    })
    return transactions_database

def add_expense(transactions_database: dict, amount: int, description: str) -> dict:
    # Update balance
    transactions_database["balance"] -= amount

    # Add transaction
    transactions_database["transactions"].append({
        "type": "expense",
        "amount": amount,
        "description": description
    })
    return transactions_database

def show_balance(transactions_database: dict) -> int:
    # Return the current balance
    return transactions_database["balance"]

def show_transaction_history(transactions_database: dict) -> list:
    # Return the list of transactions
    return transactions_database["transactions"]
