from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, PasswordField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, email_validator, EqualTo
import email_validator

class Signupform(FlaskForm):
    email = StringField(label = "Email", validators= [DataRequired(), Email()])
    password = PasswordField(label = "Password", validators = [DataRequired()])
    repeat = PasswordField(label = "repeat password", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField("register")


class Loginform(FlaskForm):
    email = StringField(label = "Email", validators= [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign in")

class Newlisting(FlaskForm):
    title = StringField(label = "title", validators=[DataRequired()])
    description = StringField(label= "description", validators=[DataRequired()])
    price = StringField(label= "Price", validators=[DataRequired()])
    submit = SubmitField("Create Listing")

# def upload(request):
#     form = UploadForm(request.POST)
#     if form.image.data:
#         image_data = request.FILES[form.image.name].read()
#         open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)

def validate_user(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
        raise ValidationError("Please use a different user name")

def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
        raise ValidationError("Please use a different email")


