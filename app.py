# app.py

from flask import Flask, render_template, request, redirect, url_for
import transactions

app = Flask(__name__)

# In-memory database (in a production app you’d use a persistent storage)
transactions_database = {"balance": 0, "transactions": []}

@app.route("/")
def index():
    # Show the main menu
    menu = transactions.menu_options()
    return render_template("index.html", menu=menu)

@app.route("/add-income", methods=["GET", "POST"])
def add_income():
    if request.method == "POST":
        try:
            amount = int(request.form["amount"])
            description = request.form["description"]
            transactions.add_income(transactions_database, amount, description)
            return redirect(url_for("show_balance"))
        except ValueError:
            error = "Invalid amount. Please enter a number."
            return render_template("add_income.html", error=error)
    return render_template("add_income.html")

@app.route("/add-expense", methods=["GET", "POST"])
def add-expense():
    if request.method == "POST":
        try:
            amount = int(request.form["amount"])
            description = request.form["description"]
            transactions.add-expense(transactions_database, amount, description)
            return redirect(url_for("show_balance"))
        except ValueError:
            error = "Invalid amount. Please enter a number."
            return render_template("add-expense.html", error=error)
    return render_template("add-expense.html")

@app.route("/show-balance")
def show_balance():
    balance = transactions.show_balance(transactions_database)
    return render_template("balance.html", balance=balance)

@app.route("/show-history")
def show_history():
    history = transactions.show_transaction_history(transactions_database)
    return render_template("history.html", transactions=history)

@app.route("/exit")
def exit_app():
    # Since a web app doesn’t “exit” the same way a CLI does, redirect to the home page.
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
