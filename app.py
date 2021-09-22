from flask import render_template, flash, redirect, url_for, session
from functools import wraps
from src.login_register import log_reg
from config import app
from src.store import home_reg


app.register_blueprint(log_reg)
app.register_blueprint(home_reg)


# stat page
@app.route('/')
def start():
    return render_template('start.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
