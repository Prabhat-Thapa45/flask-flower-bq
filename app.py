from flask import render_template, flash, redirect, url_for, session
from functools import wraps
from src.login_register import log_reg
from config import app
from src.home import home_reg


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


# About
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
