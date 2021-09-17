from flask import render_template, flash, redirect, url_for, session, request
from functools import wraps
from models.login_register import log_reg
from config import app
from config import mysql
from models.home import home_reg


app.register_blueprint(log_reg)
app.register_blueprint(home_reg)


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


# Index
@app.route('/home')
@is_logged_in
def index():
    cur = mysql.connection.cursor()
    # Get article
    cur.execute("SELECT * FROM items")
    results = cur.fetchall()
    print(type(results))
    return render_template('home.html', articles=results)


# About
@app.route('/about')
def about():
    return render_template('about.html')


# add button used to add flower
@app.route('/add_item/<string:id>', methods=['POST'])
@is_logged_in
def add_to_cart(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("UPDATE items SET quantity = quantity - 1, cart = cart + 1 WHERE id = %s", [id])
    cur.execute("SELECT * FROM items where id = %s", [id])
    result = cur.fetchall()
    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()

    flash('Item Added to Cart', 'success')

    return redirect(url_for('index'))


@app.route('/calculate', methods=['POST'])
def your_cart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT flower_name, cart, price from  items")
    result = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('bill.html', result=result)


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
