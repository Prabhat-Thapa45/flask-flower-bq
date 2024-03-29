from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from functools import wraps
from src.execute_sql import query_handler_no_fetch, query_handler_fetch
from src.check import check_flower_by_name, int_convertor

home_reg = Blueprint("store", __name__, template_folder="templates")


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


# About
@home_reg.route('/about')
@is_logged_in
def about():
    return render_template('about.html')


# contact
@home_reg.route('/contact')
@is_logged_in
def contact():
    return render_template('contact.html')


@home_reg.route('/menu')
@is_logged_in
def menu():
    return render_template('menu.html')


# adds flower to existing flowers and also adds new flower
@home_reg.route('/add_flower', methods=['Get', 'POST'])
@is_logged_in
def add_flower():
    query = "SELECT * FROM items"
    results = query_handler_fetch(query)

    if request.method == 'POST':
        quantity_to_add = int_convertor(request.form['number'])
        quantity_present = int_convertor(request.form.get('quantity'))
        if quantity_to_add < 0:
            flash("You can't pass negative value", "danger")
            return redirect(url_for('store.add_flower', articles=results))
        flower_name = request.form.get('flower_name')
        query = "UPDATE items SET quantity=%s WHERE flower_name=%s"
        values = (sum([quantity_to_add + quantity_present]), flower_name)
        query_handler_no_fetch(query, values)

        return redirect(url_for('store.add_flower'))
    return render_template('add_flower.html', articles=results)


# adds new flower
@home_reg.route('/add_new_flower', methods=['GET', 'POST'])
@is_logged_in
def add_new_flower():
    if request.method == 'POST':
        query = "SELECT * FROM items"
        results = query_handler_fetch(query)
        flower_name = request.form.get('new_flower')
        quantity = int(request.form.get('new_quantity'))
        try:
            price = float(request.form.get('new_price'))
        except ValueError:
            return redirect(url_for('store.add_new_flower'))
        else:
            if check_flower_by_name(results, flower_name):
                query = "UPDATE items SET quantity = quantity + %s, price = %s WHERE flower_name=%s"
                values = (quantity, price, flower_name)
                query_handler_no_fetch(query, values)
                return redirect(url_for('store.add_flower', articles=results))
            query = "INSERT INTO items(flower_name, price, quantity) VALUES(%s, %s, %s)"
            values = (flower_name, price, quantity)
            query_handler_no_fetch(query, values)
            return redirect(url_for('store.add_flower', articles=results))
    return render_template('add_new_flower.html')


@home_reg.route('/bouquet_size', methods=['GET', 'POST'])
@is_logged_in
def bouquet():
    if request.method == 'POST':
        query = "SELECT flower_name, price, quantity FROM items"
        results = query_handler_fetch(query)

        bouquet_size = int(request.form.get('bouquet_size'))
        if bouquet_size < 1:
            flash("bouquet size should more than zero", "danger")
            return render_template('bouquet_size.html')
        flash(f"You have {bouquet_size} flowers to be added into your bouquet", "success")
        return render_template('purchase_flower.html', bouquet_size=bouquet_size, articles=results)
    return render_template('bouquet_size.html')


# adds the flower with desired quantity in your cart
@home_reg.route('/purchase_flower/add_to_cart', methods=['GET', 'POST'])
@is_logged_in
def add_to_cart():
    """
    Fetches data from items and populates 'purchase_flower.html' with flowers to be bought
    bouquet size given by user is used as a constraint to avoid user from buying more than the confirmed quantity
    try except block is used in order to check if user adds empty value in the cart
    after each successful order bouquet size is reduced.
    """
    query = "SELECT flower_name, price, quantity FROM items"
    results = query_handler_fetch(query)

    if request.method == 'POST':
        bouquet_size = int(request.form.get('bouquet_size'))
        try:
            quantity = int(request.form['number'])
        except ValueError:
            flash("No items were added into your cart", "danger")
            quantity = 0
        available_in_stock = int(request.form.get('available'))
        if available_in_stock == 0:
            flash("We are out of stock", "danger")
        if available_in_stock < quantity:
            flash(f"We can't meet your demand, we only have {available_in_stock} of them in stock", "danger")
        elif bouquet_size >= quantity > 0:
            bouquet_size -= quantity
            flash("Item added to cart", "success")
            query = "INSERT INTO orders(username, flower_name, quantity, price) VALUES(%s, %s, %s, %s)"
            values = (session['username'], request.form.get("flower_name"), quantity, request.form.get("price"))
            query_handler_no_fetch(query, values)
        elif bouquet_size < quantity:
            flash("You have exceeded bouquet size", "danger")
        elif quantity < 0:
            flash("Order quantity cannot be less than zero", "danger")
        if bouquet_size > 0:
            flash(f"You have {bouquet_size} flowers to be added into your bouquet", "success")
        else:
            flash("You have successfully placed your all orders", "success")
        return render_template('purchase_flower.html', bouquet_size=bouquet_size, articles=results)
    return redirect(url_for('store.proceed_to_buy', articles=results))


# finally buys the product and clears the items from your cart
@home_reg.route('/purchase_flower/order_placed', methods=['GET', 'POST'])
@is_logged_in
def proceed_to_buy():
    """
    Populates the template with data fetched from table orders where username is equal to user logged in
    Inserts those data into separate table your_order with order_date added as the day you clicked buy
    this table can be later used to show orders history
    Updates the flowers quantity in table items, after the order is placed.
    Deletes data from table orders for the logged in user
    :return:
    """
    query = "SELECT flower_name, price, quantity FROM orders WHERE username=%s"
    values = (session['username'],)
    results = query_handler_fetch(query, values)
    if request.method == 'POST':
        try:
            reduce_amount = request.form['quantity']
        except KeyError:
            flash("You have nothing to order", "danger")
            return redirect(url_for('store.bouquet'))
        flower = request.form['flower_name']
        query = "INSERT INTO your_order (username, flower_name, price, quantity) VALUES (%s, %s, %s, %s)"
        values = (session['username'], request.form.get('flower_name'), request.form.get('price'),
                  request.form.get('quantity'))
        query_handler_no_fetch(query, values)

        query = "UPDATE items SET quantity=quantity-%s WHERE flower_name=%s"
        values = (reduce_amount, flower)
        query_handler_no_fetch(query, values)

        query = "DELETE FROM orders WHERE username=%s"
        values = (session['username'],)
        query_handler_no_fetch(query, values)

        flash("Your Order Has Been Placed Successfully", "success")

        query = "SELECT flower_name, quantity, order_date FROM your_order WHERE username=%s"
        values = (session['username'],)
        query_handler_fetch(query, values)
        return render_template('order_placed.html', articles=results)
    return render_template("go_to_cart.html", articles=results)


@home_reg.route('/check_order_bq', methods=['POST'])
@is_logged_in
def check_order_bq():
    if request.method == 'POST':
        bouquet_size = int(request.form['bouquet_size'])
        if bouquet_size == 0:
            return redirect(url_for('store.go_to_cart'))
        else:
            flash(f"You still have {bouquet_size} flowers to buy", "danger")
            query = "SELECT flower_name, price, quantity FROM items"
            results = query_handler_fetch(query)
            return render_template('purchase_flower.html', bouquet_size=bouquet_size, articles=results)


# displays your order details with total amount to be paid
@home_reg.route('/go_to_cart', methods=['GET', 'POST'])
@is_logged_in
def go_to_cart():
    """
    Populates go_to_cart template from data in orders table. This table is major table consisting orders from all users
    return: ('go_to_cart.html', articles: tuple)
    """
    query = "SELECT flower_name, price, quantity FROM orders WHERE username=%s"
    values = (session['username'],)
    results_1 = query_handler_fetch(query, values)
    query = "SELECT flower_name, price, quantity, order_date FROM your_order WHERE username=%s"
    values = (session['username'],)
    results_2 = query_handler_fetch(query, values)
    return render_template("go_to_cart.html", articles=results_1, order_history=results_2)


@home_reg.route('/cancel_order', methods=['GET', 'POST'])
@is_logged_in
def cancel_order():
    """
    Deletes from username
    """
    if request.method == "POST":
        query = "DELETE FROM orders WHERE username=%s"
        values = (session['username'],)
        query_handler_no_fetch(query, values)

        flash("Your order has been cancelled successfully", "success")
    return render_template("index.html")
