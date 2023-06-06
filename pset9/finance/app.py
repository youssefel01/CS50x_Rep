import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    stocks = db.execute("SELECT symbol, name, price, SUM(shares) as sumshares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    total = cash
    for stock in stocks:
        total += stock["price"] * stock["sumshares"]


    return render_template("index.html", stocks=stocks, total=total, cash=cash, usd=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares_num = request.form.get("shares")

        # if the user leave someting empty
        if not symbol:
            apology("must provide a symbol")
        if not shares_num:
            apology("must provide Number")

        # check if the value of shares_num is numeric 1 2 4 ...
        if shares_num.isnumeric():
            shares_num = int(shares_num)
        else:
            try:
                shares_num = float(shares_num)
                return apology("Shares must be a valid number float")
            except ValueError:
                return apology("Shares must be a valid number text")

        # check if the value is positiv
        shares_num = int(shares_num)
        if shares_num <= 0:
            return apology("must provide a positif Number")

        # check if the symbol is valid
        stock = lookup(symbol)
        if not stock:
            return apology("symbol not valid")
        user_id = session["user_id"]
        # this return a dictionary of one element [{'cash'=10000}] but we want to return just 10000
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        # get the name of the share and his price
        stock_name = stock["name"]
        stock_price = stock["price"]
        # calculate the total price of shares
        total_price = stock_price * shares_num
        # check if the user have that much
        if cash < total_price:
            return apology("you don't have enough money to buy that stock")
        else:
            # subtract total price
            # from user's cash
            cash = cash - total_price
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)
            # insert in transactions
            db.execute("INSERT INTO transactions (user_id, name, shares, price, symbol) VALUES ( ?, ?, ?, ?, ?)",
                       user_id, stock["name"], shares_num, stock_price, stock["symbol"])
            return redirect('/')
    # GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    stocks = db.execute("SELECT symbol, shares, price, time FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        # Ensure symbol not null
        if not symbol:
            return apology("Please enter a symbol")
        # getting the stock quote with lookup()
        stock = lookup(symbol.upper())
        # check if stock = None
        if not stock:
            return apology("symbol not valid")
        # sent dictionary to quoted.html
        usd_price = usd(stock["price"]) # Format value as USD
        return render_template("quoted.html", stock=stock, usd_price=usd_price)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # POST
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        # Ensure pass = conf
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("confirmation not the same as password")

        # Ensure that the username not taken before
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if rows:
            return apology("username is alredy taken")

        # add user to db
        # hash the user's password
        password_hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), password_hash)

        # Redirect user to home page
        return redirect("/login")
    # GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # get the user id
    user_id = session["user_id"]
    # Post
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_num = request.form.get("shares")

        # if the user leave someting empty
        if not symbol:
            apology("must provide a symbol")
        if not shares_num:
            apology("must provide Number")

        # check if the value of shares_num is numeric 1 2 4 ...
        if shares_num.isnumeric():
            shares_num = int(shares_num)
        else:
            try:
                shares_num = float(shares_num)
                return apology("Shares must be a valid number float")
            except ValueError:
                return apology("Shares must be a valid number text")

        # check if the value is positiv
        shares_num = int(shares_num)
        if shares_num <= 0:
            return apology("must provide a positif Number")

        # check if the user already have the shares
        # next line return a list with dictionaries / in this case will be one dictionary
        nser_shares = db.execute("SELECT SUM(shares) as sumshares FROM transactions WHERE user_id = ? AND symbol = ?",
                                  user_id, symbol)[0]["sumshares"]
        if nser_shares < shares_num:
            return apology("you don't have that many shares")
        # if the user have the shares
        else:  # SELECT SUM(shares) as sumshares FROM transactions WHERE user_id = 1 AND symbol = 'AAPL';
            # check the price and the of shares
            sharePrice = lookup(symbol)["price"]
            total_price = sharePrice * shares_num
            shareName = lookup(symbol)["name"]

            # subtract total price from user's cash
            # import cash
            cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
            cash = cash + total_price
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)

            # insert in transactions
            db.execute("INSERT INTO transactions (user_id, name, shares, price, symbol) VALUES ( ?, ?, ?, ?, ?)",
                      user_id, shareName, -(shares_num), sharePrice, symbol)
            return redirect('/')

    # GET
    else:
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        return render_template("sell.html", symbols=symbols)

# PERSONAL TOUCH
# add cash
@app.route("/AddCash", methods=["GET", "POST"])
@login_required
def AddCash():
    # POST
    if request.method == "POST":
        # get the user id
        user_id = session["user_id"]
        # get input from the AddCash page
        cash = float(request.form.get("cash"))
        # check the input
        if not cash:
            return apology("you didn't enter any amount")
        if cash <= 0:
            return apology("enter a positif amount")
        # update cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", cash, user_id)
        return redirect('/')
    # GET
    else:
        return render_template("addcash.html")


# change password
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":

        # get the user id
        user_id = session["user_id"]

        # get the new password
        Newpassword = request.form.get("N_password")
        confirmation = request.form.get("confirmation")

        # check
        if not Newpassword:
            return apology("Enter A Password")
        if not confirmation:
            return apology("confirm your password")
        if Newpassword != confirmation:
            return apology("confirm your password again")

        # hash the user's password
        Newpassword = generate_password_hash(Newpassword)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", Newpassword, user_id)
        return redirect('/')
    # GET
    else:
        return render_template("password.html")


