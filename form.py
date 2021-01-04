from wtforms import *
from flask_wtf import *
from wtforms.validators import *


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=30)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    con_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    mobile = StringField('Mobile Number', validators=[DataRequired()])
    location = StringField('Location', validators=[data_required()])
    submit = SubmitField('SignUp')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class Sell_form(FlaskForm):
    name = StringField("Product Name:", validators=[DataRequired()])
    image = FileField("Image Of Product")
    price = FloatField("Price:", validators=[DataRequired()])
    details = TextAreaField("Product Details:", validators=[DataRequired()])
    code = StringField('Code:', validators=[DataRequired()])
    mobile = StringField('Mobile Number')
    submit = SubmitField("Create Product")


class Username(FlaskForm):
    username = StringField('Username')
    email = StringField('Email')
    submit = SubmitField('Update Account')


class Password(FlaskForm):
    email = StringField('Email')
    oldpassword = PasswordField('Old Password')
    password = PasswordField('Password')
    submit = SubmitField('Update Account')


class Mobile(FlaskForm):
    email = StringField('Email')
    mobile = StringField('Mobile Number')
    submit = SubmitField('Update Account')


class Location(FlaskForm):
    email = StringField('Email')
    location = StringField('Location')
    submit = SubmitField('Update Account')
