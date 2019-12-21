from functools import wraps
from datetime import datetime, timedelta
import pymongo
import os
from flask import Flask, render_template, url_for, send_from_directory, \
    request, session, redirect, flash
from attendant import *

app = Flask(__name__)
a = os.environ.get("MONGO_URI")
b = os.environ.get("FLASK_SECRET_KEY")
mongo = pymongo.MongoClient(a)
app.secret_key = b


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'email' in session:
            return f(*args, **kwargs)
        else:
            flash("Login First!")
            return(redirect("/accounts"))
    return wrap


@app.route('/secret')
@login_required
def secret():
    return session['email']


@app.route('/attendant/signup', methods=['GET', 'POST'])
def operator_signup():
    '''Parking Interface'''
    if request.method == 'GET':
        return render_template('parkmycar.html')
    else:
        return "ok"


@app.route('/')
def index():
    '''Returns the homepage'''
    return render_template('index.html')


@app.route('/assets/<path:path>')
def css(path):
    '''Serve static content for the homepage'''
    return send_from_directory('assets', path)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Successfully Logged out")
    return redirect(url_for('index'))


@app.errorhandler(500)
def syserror(e):
    return render_template("404.html", error='500'), 500


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", error='404'), 404


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
