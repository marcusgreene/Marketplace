from app import app, db
from flask import Flask, request, render_template, flash, redirect, url_for, Response, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, email_validator
from models import Listing, User
from flask_login import current_user, login_user, logout_user, login_required
from forms import Loginform, Signupform, Newlisting
from werkzeug.utils import secure_filename
import os

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
    if user is not None:
      flash("An account with this email already exists")
      render_template('register.html', title="Register", form=form)
    else:
      user = User(username = form.email.data)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      flash("you are now a registered user")
      return redirect(url_for('login'))
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

    if 'pic' not in request.files:
            print('No file part')
            return redirect(request.url)
    file = request.files['pic']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
    if file.filename == '':
      print('No selected file')
      return redirect(request.url)
    if file:
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    listing = Listing(title = form.title.data, description = form.description.data, price = form.price.data, user_id=current_user.id, images=filename)
    db.session.add(listing)
    db.session.commit()
    print(listing, listing.title, listing.description, listing.price, listing.id)
    flash("listing created")
  return render_template('selling.html', title = "My Account", form=form, listings = listings)

@app.route('/listings/user/<userid>')
def user(userid):
  listings = Listing.query.filter_by(id=userid)
  return render_template("user.html",listings=listings, title = "Listings", _external=True, _scheme = "https")

@app.route("/")
def index():
    listings = Listing.query.all()
    return render_template("listings.html", listings = listings, title="Listings", _external=True, _scheme="https")

@app.route("/listings/<listingid>")
def listing(listingid):
  listing = Listing.query.filter_by(id=listingid).first()
  user = User.query.filter_by(id=listing.id).first()
  return render_template("listing.html", title=listing.title, listing=listing, user=user)

@app.route("/uploads/<filename>")
def serve_image(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


