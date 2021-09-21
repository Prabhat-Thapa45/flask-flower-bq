from flask import Flask, redirect, url_for, render_template


app = Flask(__name__)


@app.route('/<string:name>')
def test(name):
    print(name)
    return render_template(test.html)

app.run(port=4000)
