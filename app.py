from functools import wraps
from datetime import datetime, timedelta
import pymongo
import os
import json
import bcrypt
# import simplejson as json
from flask import Flask, render_template, url_for, send_from_directory, \
    request, session, redirect, flash, jsonify
from attendant import ParkingLot
from map_my_india import geocode

app = Flask(__name__)
# CORS(app)
a = os.environ.get("MONGO_URI")
b = os.environ.get("FLASK_SECRET_KEY")
mongo = pymongo.MongoClient(a)
app.secret_key = b
TOKEN = '282cf477-f3b8-400f-918b-183fb2c54b8a'
objectEndpoint = ''


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            flash("Login First!")
            return(redirect("/operator/login"))
    return wrap


@app.route('/secret')
@login_required
def secret():
    return session['username']


@app.route('/operator/signup', methods=['GET', 'POST'])
def operator_signup():
    '''Parking Interface'''
    if request.method == 'GET':
        return render_template('parkmycar.html')
    else:
        print("ENTERING THE ONE")
        username = request.form["username"]
        password = request.form["password"]
        address = request.form["address"]
        cost_per_hour = request.form["cost_per_hour"]
        total_capacity = request.form["capacity"]
        users = mongo.parking.lot
        print(users)
        existing_user = users.find_one({'username': username})
        if existing_user is None:
            hashpass = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt())
            session['username'] = username
        else:
            "User already Exists"
            return redirect('/operator/signup')
        print("done")

        coordinates = geocode(address, token=TOKEN)
        latitude = coordinates[0]
        longitude = coordinates[1]
        operator = ParkingLot(username, latitude,
                              longitude, total_capacity, cost_per_hour)
        # print(operator)
        print('================================================')
        users.insert(
            {'username': username, 'password': hashpass, 'latitude': latitude,
             'longitude': longitude, 'totalSpace': total_capacity,
             'available_space': total_capacity,
             'cost_per_hour': cost_per_hour})

        global objectEndpoint
        objectEndpoint = json.dumps(operator.__dict__)
        print(objectEndpoint)
        # return objectEndpoint
        return "DONNEEE"


@app.route('/operator/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form["username"]
        password = request.form["password"]
        users = mongo.parking.lot
        login_user = users.find_one({"username": username})

        if login_user:
            orig_pass = login_user['password']
            if bcrypt.hashpw(password.encode('utf-8'), orig_pass) == orig_pass:
                session['username'] = username
                return redirect('/operator/dashboard')
            return "Invalid username/password combination"
        return "invalid username"


@app.route('/public')
def public():
    return render_template('public.html')


@app.route('/list')
def list():
    json_list = []
    users = mongo.parking.lot
    a = users.find({})

    for doc in a:
        # print(type(doc))
        del doc['_id']
        del doc['password']
        json_list.append(doc)

        # print(doc)
    # print(json_list)
    return jsonify(json_list), {'Access-Control-Allow-Origin': '*'}
    # print(a)


@app.route('/address', methods=['POST'])
def address_tbf():
    address = request["address"]


@app.route('/')
def index():
    '''Returns the homepage'''
    return render_template('index.html')


@app.route('/assets/<path:path>')
def css(path):
    '''Serve static content for the homepage'''
    return send_from_directory('assets', path)


@app.route('/coordinates', methods=['POST'])
def coordinates():
    if request.method == 'POST':
        req = request.get_json()
        print(req)
    return jsonify({"received": "true"})


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


@app.route('/operator/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
