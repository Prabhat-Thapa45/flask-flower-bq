from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from config import mysql
from functools import wraps

# from src.bouquet.order import take_order


home_reg = Blueprint("home", __name__, template_folder="templates")


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


@home_reg.route('/home')
@is_logged_in
def home():
    return render_template('index.html', username=session['username'])


@home_reg.route('/menu')
@is_logged_in
def menu():
    return render_template('menu.html')


# adds flower to existing flowers and also adds new flower
@home_reg.route('/add_flower', methods=['Get', 'POST'])
def add_flower():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    results = cur.fetchall()
    if request.method == 'POST':
        quantity_present = request.form.get('quantity')
        quantity_to_add = int(request.form.get('number')) + int(quantity_present)
        flower_name = request.form.get('flower_name')
        cur.execute("UPDATE items SET quantity=%s WHERE flower_name=%s", [quantity_to_add, flower_name])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home.add_flower'))
    cur.close()
    return render_template('add_flower.html', articles=results)


# adds new flower
@home_reg.route('/add_new_flower', methods=['GET', 'POST'])
def add_new_flower():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        flower_name = request.form.get('new_flower')
        quantity = request.form.get('new_quantity')
        try:
            price = float(request.form.get('new_price'))
        except ValueError:
            return redirect(url_for('home.add_new_flower'))
        else:
            cur.execute("INSERT INTO items(flower_name, price, quantity) VALUES(%s, %s, %s)",
                        (flower_name, quantity, price))
            mysql.connection.commit()
            cur.close()
    return render_template('add_new_flower.html')


# renders template showing list of flowers available
@home_reg.route('/purchase_flower')
def purchase_flower():
    cur = mysql.connection.cursor()
    cur.execute("SELECT flower_name, price, quantity FROM items")
    results = cur.fetchall()
    return render_template('purchase_flower.html', articles=results)


# adds the flower with desired quantity in your cart
@home_reg.route('/purchase_flower/add_to_cart', methods=['GET', 'POST'])
@is_logged_in
def add_to_cart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT flower_name, price, quantity FROM items")
    results = cur.fetchall()
    if request.method == 'POST':
        quantity = request.form['number']
        flash("Item added to cart", "success")
        cur.execute("INSERT INTO orders(username, flower_name, quantity, price) VALUES(%s, %s, %s, %s)",
                    (session['username'], request.form.get("flower_name"), quantity, request.form.get("price")))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home.add_to_cart', articles=results))
    return render_template('purchase_flower.html', articles=results)


# displays your order details with total amount to be paid
@home_reg.route('/purchase_flower/your_cart', methods=['GET', 'POST'])
@is_logged_in
def your_cart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT flower_name, price, quantity FROM orders WHERE username=%s", [session['username']])
    results = cur.fetchall()
    cur.close()
    return render_template("your_cart.html", articles=results)


# finally buys the product and clears the items from your cart
@home_reg.route('/purchase_flower/proceed_to_buy', methods=['GET', 'POST'])
@is_logged_in
def proceed_to_buy():
    cur = mysql.connection.cursor()
    cur.execute("SELECT flower_name, price, quantity FROM orders WHERE username=%s", [session['username']])
    results = cur.fetchall()
    if request.method == 'POST':
        cur.execute("INSERT INTO your_order (username, flower_name, price, quantity) VALUES (%s, %s, %s, %s)",
                    (session['username'], request.form.get('flower_name'), request.form.get('price'),
                     request.form.get('quantity')))
        cur.execute("DELETE FROM orders WHERE username=%s", [session['username']])
        mysql.connection.commit()
        cur.close()
        return render_template('order_placed.html', articles=results)

    return render_template("your_cart.html", articles=results)
