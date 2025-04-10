![Logo](https://png.pngtree.com/png-vector/20220910/ourmid/pngtree-budgeting-icon-png-image_6145091.png)

# Budget Manager Web Project

This is Web version of Budget Manager, running on Apache.

## Table of Contents

1. [Introduction](#1-introduction)<br>
2. [Code Explanation](#2-code-explanation)<br>
   2.1. [Data Structure](#21-data-structure)<br>
   2.2. [Main Menu](#22-main-menu)<br>
   2.3. [Project Files](#23-project-files)<br>
   
3. [Implementation Steps](#3-implementation-steps)<br>
   3.1. [Adjust the Main File Code Into a Flask Web App](#31-adjust-the-main-file-code-into-a-flask-web-app)<br>
   3.2. [Adjust the Functions File Code](#32-adjust-the-functions-file-code)<br>
   3.3. [Create HTML Files for Each Function](#33-create-html-files-for-each-function)<br>
   3.4. [Create a WSGI File for Apache](#34-create-a-wsgi-file-for-apache)<br>
   3.5. [Adding Repository Files](#35-adding-repository-files)<br>
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.5.1. [Copy/Locate the Files](#35-adding-repository-files)<br>
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.5.2. [Clone Repository](#35-adding-repository-files)<br>
   3.6. [Configure Apache to Use WSGI](#36-configure-apache-to-use-wsgi)<br>
   3.7. [Update Virtual Host Configuration](#37-update-virtual-host-configuration)<br>
   3.8. [Install Flask](#38-install-flask)<br>
   3.9. [Perform the Required Changes for HTTPS Workability](#39-perform-the-required-changes-for-https-workability-in-case-if-needs)<br>
   3.10. [Restart Apache Web Server](#310-restart-apache-web-server)<br>
   
4. [License](#4-license)<br>
5. [Author](#5-author)<br>
6. [Feedback](#6-feedback)<br>


## 2. Code Explanation
### 2.1. Data Structure

The program maintains a dictionary that stores the user's balance and a list of transactions.<br>
Each transaction includes details like type (income/expense), amount, and description:

*```transactions_database = {"balance": 0, "transactions": []}```*
<br><br>Each transaction will be stored separately *(for example)*:

*```{"type": "expense", "amount": 500, "description": "Groceries"}```*<br>
<br>The user's balance value will be updated after each transaction.

### 2.2. Main Menu
- Add Income<br>
- Add Expense<br>
- Show Balance<br>
- Show Transaction History<br>

### 2.3. Project Files

- *[```app.py```](https://github.com/desmondcoacher/budget-manager-web/blob/main/app.py)* Main file

- *[```transactions.py```](https://github.com/desmondcoacher/budget-manager-web/blob/main/transactions.py)* Functions file

- *[```wsgi.py```](https://github.com/desmondcoacher/budget-manager-web/blob/main/wsgi.py)* WGSI file

- *[```templates```](https://github.com/desmondcoacher/budget-manager-web/tree/main/templates)* HTML Templates folder, which contains:
    - *[```index.html```](https://github.com/desmondcoacher/budget-manager-web/blob/main/templates/index.html)* Main Menu HTML file

    - *[```add_income.html```](https://github.com/desmondcoacher/budget-manager-web/blob/main/templates/add_income.html)* Add Income Transactions HTML file
    - *[```add_expense.html```](https://github.com/desmondcoacher/budget-manager-web/blob/main/templates/add_expense.html)* Add Expense Transactions HTML file
    - *[```balance.html```](https://github.com/desmondcoacher/budget-manager-web/blob/main/templates/balance.html)* Displaying Current Balance HTML file
    - *[```history.html```](https://github.com/desmondcoacher/budget-manager-web/blob/main/templates/history.html)* Showing Transactions History HTML file


## 3. Implementation Steps

### 3.1. Adjust the Main File Code Into a Flask Web App
Instead of a `while` loop with `input()` *(which is not relevant for HTML)*, endpoints that display HTML forms will be created. <br>Editing Main file including Flask Web App methon implementation.

```python
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
### 3.2. Adjust the Functions File Code
Instead of ```print``` function format ```return``` will be used.
```python
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
### 3.3. Create HTML Files for Each function
In this case, all ```.html``` files will be stored in **templates** folder, which will be created:
- ```index.html``` for the Main Menu
```python
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
- ```add_income.html``` for Adding Income Transactions
```python
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
- ```add_expense.html``` for Adding Expense Transactions
```python
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
- ```balance.html``` for Displaying Current Balance
```python
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
- ```history.html``` for Showing Transactions History
```python
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

### 3.4. Create a WSGI File for Apache
```python
# wsgi.py
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/<your-project-name>")  # adjust this to your project directory

from app import app as application

```

### 3.5. Adding Repository Files
Use ***ONLY*** One from The Methods Below:
- **3.5.1.** Copy/locate the files *```app.py```*, *```transactions.py```*, *```wsgi.py```* and *```templates```* folder to the project directory *(in case you created all the required files following the steps above)*

- **3.5.2.** Clone repository, copy files from the Repository to the project directory

    *```git clone https://github.com/desmondcoacher/budget-manager-web```*

    *```sudo cp -r budget-manager-web/templates budget-manager-web/app.py budget-manager-web/transactions.py budget-manager-web/wsgi.py /var/www/"your-project-name"```*

### 3.6. Configure Apache to Use WSGI
*```sudo apt-get install libapache2-mod-wsgi-py3```*

***Note:*** no need to run the command to enable mode because it will be automatically enabled when installation succeed.

### 3.7. Update Virtual Host Configuration
Add the lines below to your Virtual Host file:

*sudo nano /etc/apache2/sites-available/"your-project-name".conf*
```
    WSGIDaemonProcess budgetmanager python-path=/var/www/<your-project-name>
    WSGIScriptAlias / /var/www/<your-project-name>/wsgi.py
```

### 3.8. Install Flask
*```sudo apt install python3-flask```*

### 3.9. Perform the Required Changes for HTTPS Workability *(In Case if Needs)*
In most cases if you're modifying already running website with HTTPS and only migrated this one, the changes you need to perform located in the file:

```/etc/apache2/sites-available/"your-project-name".conf```

The path in ```Directory``` needs to be updated and ```DocumentRoot``` path in ```VirtualHost``` needs to be updated as well.

### 3.10. Restart Apache Web Server
*```sudo systemctl restart apache2```*

***Tip:*** use *```sudo tail -f /var/log/apache2/error.log```* command for debugging.

## 4. License

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://github.com/desmondcoacher/budget-manager-web/blob/main/LICENSE)

## 5. Author

- [@desmondcoacher](https://github.com/desmondcoacher)


## 6. Feedback

If you have any feedback, feel free to contact me: desmond.c@campus.technion.ac.il
