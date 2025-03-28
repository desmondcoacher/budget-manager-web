
# Budget Manager Web
This is Budget Manager Web version, running on Apache.

## Implementation Steps
1. Adjust the Main File Code into a Flask Web App (app.py will be created)
Note: Instead of a while loop with input() (which is not relevant for html), endpoints that display HTML forms will be created.

```
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
def add_expense():
    if request.method == "POST":
        try:
            amount = int(request.form["amount"])
            description = request.form["description"]
            transactions.add_expense(transactions_database, amount, description)
            return redirect(url_for("show_balance"))
        except ValueError:
            error = "Invalid amount. Please enter a number."
            return render_template("add_expense.html", error=error)
    return render_template("add_expense.html")

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

```

2. Adjust the Functions File Code (transactions.py will be modified)
**Note:** Instead of ```print``` function format ```return``` will be used.

```
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

```

3. Create HTML Files for Each Function (folder templates will be created)
- index.html for main menu
```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Budget Manager</title>
  </head>
  <body>
    <h1>Welcome to Budget Manager</h1>
    <ul>
      <li><a href="{{ url_for('add_income') }}">Add Income</a></li>
      <li><a href="{{ url_for('add_expense') }}">Add Expense</a></li>
      <li><a href="{{ url_for('show_balance') }}">Show Balance</a></li>
      <li><a href="{{ url_for('show_history') }}">Show Transaction History</a></li>
    </ul>
  </body>
</html>

```
- add_income.html for adding income transaction
```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Add Income</title>
  </head>
  <body>
    <h1>Add Income</h1>
    {% if error %}
      <p style="color:red;">{{ error }}</p>
    {% endif %}
    <form method="post">
      <label for="amount">Amount:</label>
      <input type="number" name="amount" id="amount" required><br><br>
      <label for="description">Description:</label>
      <input type="text" name="description" id="description" required><br><br>
      <input type="submit" value="Add Income">
    </form>
    <p><a href="{{ url_for('index') }}">Back to Menu</a></p>
  </body>
</html>

```
- add_expense.html for adding expense transaction
```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Add Expense</title>
  </head>
  <body>
    <h1>Add Expense</h1>
    {% if error %}
      <p style="color:red;">{{ error }}</p>
    {% endif %}
    <form method="post">
      <label for="amount">Amount:</label>
      <input type="number" name="amount" id="amount" required><br><br>
      <label for="description">Description:</label>
      <input type="text" name="description" id="description" required><br><br>
      <input type="submit" value="Add Expense">
    </form>
    <p><a href="{{ url_for('index') }}">Back to Menu</a></p>
  </body>
</html>

```
- balance.html for displaying current balance
```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Current Balance</title>
  </head>
  <body>
    <h1>Your Current Balance</h1>
    <p>{{ balance }} ₪</p>
    <p><a href="{{ url_for('index') }}">Back to Menu</a></p>
  </body>
</html>

```
- history.html for showing transactions history
```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Transaction History</title>
  </head>
  <body>
    <h1>Transaction History</h1>
    {% if transactions %}
      <ul>
      {% for t in transactions %}
        <li>
          Type: {{ t.type|capitalize }}, Amount: {{ t.amount }} ₪, Description: {{ t.description }}
        </li>
      {% endfor %}
      </ul>
    {% else %}
      <p>No transactions available.</p>
    {% endif %}
    <p><a href="{{ url_for('index') }}">Back to Menu</a></p>
  </body>
</html>

```

4. Create a WSGI File for Apache (wsgi.py will be created)
```
# wsgi.py
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/<your-project-name>")  # adjust this to your project directory

from app import app as application

```

5. Use only One from Two Methods Below:
5.1 Copy/locate the files app.py, transactions.py, wsgi.py and templates folder to the project directory (in case you created all the required files following the steps above)

5.2 Clone repository, copy files from the Repository to the project directory

*git clone https://github.com/desmondcoacher/budget-manager-web*

*sudo cp -r budget-manager-web/templates budget-manager-web/app.py budget-manager-web/transactions.py budget-manager-web/wsgi.py /var/www/* <your-project-name>

6. Configure Apache to Use WSGI
```sudo apt-get install libapache2-mod-wsgi-py3```

**Note:** no need to run the command to enable mode because it will be automatically enabled when installation succeed.

7. Update Virtual Host Configuration
Add the lines below to your Virtual Host file

*/etc/apache2/sites-available/* <your-project-name>.conf
```
    WSGIDaemonProcess budgetmanager python-path=/var/www/<your-project-name>
    WSGIScriptAlias / /var/www/<your-project-name>/wsgi.py

```

8. Install Flask
```python
sudo apt install python3-flask
```

9. Perform Requeired Changes for HTTPS Workability for the new wbsite *(In Case if Needs)*

10. Restart Apache Web Server
*sudo systemctl restart apache2*

