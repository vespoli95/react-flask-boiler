import requests 
import datetime
import keys
import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, logging, flash
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

ENV = 'dev'

app = Flask(__name__, template_folder='templates')
app.secret_key = keys.SECRET_KEY
# cors should not be for every endpoint
CORS(app, support_credentials=True)
# if ENV == 'prod':
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = keys.DB_STRING_PROD
# else:
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = keys.DB_STRING_DEV

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    return jsonify({'token':uuid.uuid4()})

if __name__ == '__main__':
    app.run()