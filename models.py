from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(20))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, pw):
        return check_password_hash(self.password, pw)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.String(30), index = True, unique=False)
    title = db.Column(db.String(50), index=True, unique=False)
    description = db.Column(db.String(500), unique= False, index=False)
    images = db.Column(db.Text)

    # allows each listing to be linked to a user who created it
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
