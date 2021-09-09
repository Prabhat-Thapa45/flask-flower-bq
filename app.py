from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


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
    return render_template('home.html', articles=results)


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Register Form Cl
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('index'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE items SET cart = 0")
    mysql.connection.commit()
    cur.close()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


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
