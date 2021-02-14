import requests 
import datetime
import keys
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, logging, flash
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


ENV = 'dev'

app = Flask(__name__, template_folder='templates')
app.secret_key = keys.SECRET_KEY
CORS(app)
# if ENV == 'prod':
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = keys.DB_STRING_PROD
# else:
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = keys.DB_STRING_DEV

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    PK_user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    height = db.Column(db.String(200))
    age = db.Column(db.Integer)
    primary_role = db.Column(db.String(200))
    secondary_role = db.Column(db.String(200))
    country = db.Column(db.String(200))
    province = db.Column(db.String(200))
    city = db.Column(db.String(200))
    reliability = db.Column(db.String(200))
    
    def __init__(self, email, password, first_name, last_name, height, age, primary_role, secondary_role, country, province, city, reliability):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.height = height
        self.age = age
        self.primary_role = primary_role
        self.secondary_role = secondary_role
        self.country = country
        self.province = province
        self.city = city
        self.reliability = reliability



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# A route to return all of the available entries in our catalog.
@app.route('/api/register', methods=['POST'])
def register():
    req = request.get_json()
    print(req)
    if session:
        session.clear()
    if request.method == 'POST':
        password = sha256_crypt.hash((str(req['password'])))
        if db.session.query(Users).filter(Users.email == req['email']).count() == 0:
            data = Users(
                req['email'],
                password,
                req['first_name'], 
                req['last_name'], 
                req['height'], 
                req['age'], 
                req['primary_role'], 
                req['secondary_role'], 
                req['country'], 
                req['province'],
                req['city'], 
                req['reliability']
            )
            db.session.add(data)
            db.session.commit()
            return jsonify({'success': 'account created.'})
    return jsonify({'error': 'email already exists!'})

@app.route('/api/login', methods=['POST'])
def login():
    req = request.get_json()
    if request.method == 'POST':
        email = req['email']
        password_candidate = req['password']
        db_record = Users.query.filter_by(email=email).first()
        record_password = db_record.password
        if sha256_crypt.verify(password_candidate, record_password):
            session['logged_in'] = True
            return jsonify({'loggedIn':True})
        return jsonify({'loggedIn':False})


# signout
@app.route('/api/logout')
def logout():
    session.clear()
    return jsonify({'success':'signed out'})

@app.route('/api/isLoggedIn')
def isLoggedIn():
    return {'logged_in':session['logged_in']}

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({'error':'not logged in'})
    return wrap

if __name__ == '__main__':
    app.run()
