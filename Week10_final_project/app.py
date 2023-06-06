import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


# configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///store.db")

# home page route
@app.route("/")
def index():
    items = db.execute("SELECT * FROM item")
    return render_template("index.html", items=items)

# register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # get the inputs
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        shipping_address = request.form.get("shipping_address")
        # ensure data is submitted
        if not email:
            return render_template("apology.html", error="Must provide an email")
        elif not username:
           return render_template("apology.html", error="Must provide an username")
        elif not password:
            return render_template("apology.html", error="Must provide a password")
        elif not confirmation:
            return render_template("apology.html", error="Must confirm your password")
        elif password != confirmation:
            return render_template("apology.html", error="confirmation not the same as password")
        # check if the username used
        rows = db.execute("SELECT * FROM customer WHERE username = ?", username)
        if rows:
            return render_template("apology.html", error="username is alredy taken")
        # hash the password
        password = generate_password_hash(password)
        # save data
        db.execute("INSERT INTO customer (username, password, email, shipping_address) VALUES (?, ?, ?, ?)", username, password, email, shipping_address)
        return redirect("/login")

# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    # forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:
        # get inputs
        username = request.form.get("username")
        password = request.form.get("password")

        # ensure data is submitted
        if not username:
           return render_template("apology.html", error="Must provide an username")
        elif not password:
            return render_template("apology.html", error="Must provide a password")

        # query database for username
        rows = db.execute("SELECT * FROM customer WHERE username = ?", username)

        # ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            return render_template("apology.html", error="invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect("/")


# item_detail route
@app.route("/item/<int:item_id>")
def item_detail(item_id):
    # get the data of the item
    item = db.execute("SELECT * FROM item WHERE id = ?", (item_id))

    # render a template to display the item details
    return render_template("item_detail.html", item=item)

# add to cart route
@app.route("/Addtocart", methods=["GET","POST"])
def Addtocart():
    if request.method == "POST":

        # Check if user is loged in
        if 'user_id' not in session:
            return redirect(url_for('login'))
        else:
            user_id = session["user_id"]

        # get inputs
        item_id = int(request.form.get("item_id"))
        sold_quantity = int(request.form.get("sold_quantity"))

        # get info of item
        item = db.execute("SELECT name,quantity,price FROM item WHERE id = ?", item_id)

        # ensure data is valid
        if sold_quantity <= 0:
            return render_template("apology.html", error="Enter a valid quantity")
        elif sold_quantity > item[0]['quantity']:
            return render_template("apology.html", error=f"Sorry We Have Only  {item[0]['quantity']} Available In Stock")

        # add to cart
        db.execute("INSERT INTO orders (customer_id, item_id, sold_quantity) VALUES (?, ?, ?)", user_id, item_id, sold_quantity)

        # go to cart
        orders=db.execute(""" SELECT orders.item_id, item.image, item.name, SUM(orders.sold_quantity) AS totalQ, item.price
                          FROM orders
                          INNER JOIN item ON orders.item_id = item.id
                          WHERE orders.customer_id = ?
                          GROUP BY item_id""", user_id)
        Total = 0.00
        for order in orders:
            Total += order['price']*order['totalQ']

        return render_template("cart.html", orders=orders, Total=round(Total, 2))
    else:
        return redirect("/")


# get the cart route
@app.route("/cart")
def cart():
    user_id = session["user_id"]
    # go to cart
    orders=db.execute(""" SELECT orders.item_id, item.image, item.name, SUM(orders.sold_quantity) AS totalQ, item.price
                          FROM orders
                          INNER JOIN item ON orders.item_id = item.id
                          WHERE orders.customer_id = ?
                          GROUP BY item_id""", user_id)
    Total = 0.00
    for order in orders:
        Total += order['price']*order['totalQ']

    return render_template("cart.html", orders=orders, Total=round(Total, 2))

# remove from cart
@app.route("/remove_from_cart/<int:item_id>")
def remove_from_cart(item_id):
    user_id = session["user_id"]
    db.execute("DELETE FROM orders WHERE item_id = ?",item_id)
    # go to cart
    orders=db.execute(""" SELECT orders.item_id, item.image, item.name, SUM(orders.sold_quantity) AS totalQ, item.price
                          FROM orders
                          INNER JOIN item ON orders.item_id = item.id
                          WHERE orders.customer_id = ?
                          GROUP BY item_id""", user_id)

    Total = 0.00
    for order in orders:
        Total += order['price']*order['totalQ']

    return render_template("cart.html", orders=orders, Total=round(Total, 2))

# checkout route
@app.route("/checkout")
def checkout():
    user_id = session["user_id"]
    # go to cart
    orders=db.execute(""" SELECT orders.id, orders.item_id, item.image, item.name, item.quantity, SUM(orders.sold_quantity) AS totalQ, item.price
                          FROM orders
                          INNER JOIN item ON orders.item_id = item.id
                          WHERE orders.customer_id = ?
                          GROUP BY item_id""", user_id)
    # check the quantity of item
    for order in orders:
        if order['totalQ'] > order['quantity']:
            return render_template("apology.html", error=f"Sorry about: {order['name']} We Have Only  {order['quantity']} Available In Stock")
    # if the quantity is valid update quantity
    for order in orders:
        db.execute("UPDATE item SET quantity = quantity - ? WHERE id = ?", order['totalQ'], order['item_id'])

    # delelte the items that the customer buy
    db.execute("DELETE FROM orders WHERE orders.customer_id = ?", user_id)
    return render_template("success.html")

# user profile
@app.route("/profile")
def profile():
    user_id = session["user_id"]
    # get user info
    user=db.execute("SELECT * FROM customer WHERE id = ?", user_id)

    return render_template("profile.html", user=user)

# change password
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    user_id = session["user_id"]
    if request.method == "GET":
        return render_template("changePassword.html")
    else:
        # get the new password
        Newpassword = request.form.get("Newpassword")
        confirmation = request.form.get("confirmation")
        # ensure new password is submitted
        if not Newpassword:
            return render_template("apology.html", error="Must provide a New password")
        elif not confirmation:
            return render_template("apology.html", error="Must confirm your New password")
        elif Newpassword != confirmation:
            return render_template("apology.html", error="confirmation not the same as New password")
        # hash the new password
        Newpassword = generate_password_hash(Newpassword)
        # update the password
        db.execute("UPDATE customer SET password = ? WHERE id = ?", Newpassword, user_id)

        # get user info
        user=db.execute("SELECT * FROM customer WHERE id = ?", user_id)

        return render_template("profile.html", user=user)


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")