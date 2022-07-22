from app import app, db
from flask import Flask, request, render_template, flash, redirect, url_for, Response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, email_validator
from models import Listing, User
from flask_login import current_user, login_user, logout_user, login_required
from forms import Loginform, Signupform, Newlisting
from werkzeug.utils import secure_filename

@app.route('/login', methods=["GET", "POST"])
def login():
#check if current_user logged in, if so redirect to a page that makes sense
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = Loginform()
  if form.validate_on_submit():
    user = User.query.filter_by(username = form.email.data).first()
    print(form.password.data)
    if user is None or not user.check_password(pw = str(form.password.data)):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = Signupform()
  if form.validate_on_submit():
    user = User.query.filter_by(username = form.email.data).first()
    print(user)
    if user is not None:
      flash("An account with this email already exists")
      render_template('register.html', title="Register", form=form)
    else:
      user = User(username = form.email.data)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      print(user)
      flash("you are now a registered user")
      return redirect(url_for('login'))
  #does this work
  """else:  
    for field in form:
      for error in field.errors:
        flash(error)"""
  return render_template("register.html", title = "Register", form=form)


@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('login'))
    
@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
  listings = Listing.query.filter_by(user_id=current_user.id).all()
  print(listings)
  form = Newlisting()
  if form.validate_on_submit():

    pic = request.files["pic"]
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype


    listing = Listing(title = form.title.data, description = form.description.data, price = form.price.data, user_id=current_user.id, image = pic.read(), mimetype=mimetype)

    db.session.add(listing)
    db.session.commit()
    print(listing, listing.title, listing.description, listing.price, listing.id)
    flash("listing created")
  return render_template('selling.html', title = "My Account", form=form, listings = listings)


@app.route("/")
def index():
    listings = Listing.query.all()
    print(listings)
    return render_template("listings.html", listings = listings, title="Listings", _external=True, _scheme="https")

@app.route("/listings/<listingid>")
def listing(listingid):
  listing = Listing.query.filter_by(id=listingid).first()
  user = User.query.filter_by(id=listing.id).first()
  developed = Response(listing.image, mimetype=listing.mimetype)
  return render_template("listing.html", title=listing.title, listing=listing, user=user, image = developed)


@app.route("/listings/<listingid>/image")
def serve_image(listingid):
  listing = listing = Listing.query.filter_by(id=listingid).first()
  developed = Response(listing.image, mimetype=listing.mimetype)
  return Response(listing.image, mimetype=listing.mimetype)

