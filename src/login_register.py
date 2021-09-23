from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from passlib.hash import sha256_crypt
from config import mysql
from functools import wraps
from src.execute_sql import query_handler_no_fetch


log_reg = Blueprint("login_register", __name__, template_folder="templates")


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login_register.login'))
    return wrap


@log_reg.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        if str(password) != str(request.form['confirm']):
            flash("password doesn't match", "danger")
            return render_template('register.html')
        password = sha256_crypt.hash(str(password))
        query = "INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)"
        values = (name, email, username, password)
        # Execute query Commit to DB
        query_handler_no_fetch(query, values)
        flash('You are now registered and can log in', 'success')
        return render_template('login.html')
    return render_template('register.html')


# User login
@log_reg.route('/login', methods=['GET', 'POST'])
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
                cur.close()
                return redirect(url_for('store.home'))
            else:
                error = 'Invalid login'
                cur.close()
                return render_template('login.html', error=error)
            # Close connection
        else:
            cur.close()
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# Logout
@log_reg.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for("login_register.login"))
