from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#assigns flask app name
app = Flask(__name__)
#config for flask sql
app.config['SECRET_KEY'] = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listingdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#database created
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


from routes import *
from models import *


if __name__ == "__main__":
    app.run()