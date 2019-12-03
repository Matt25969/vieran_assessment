from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Posts, User
from application import login_manager

class PostForm(FlaskForm):
    first_name = StringField("First Name",
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    last_name = StringField("Last Name",
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )
    
    title = StringField("Title",
        validators=[
            DataRequired(),
            Length(min=1, max=100)
         ]
    )

    content = StringField("Content",
        validators=[
            DataRequired(),
            Length(min=1, max=500)
        ]
    )

    submit = SubmitField("Post Content")

class RegistrationForm(FlaskForm):
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password',
        validators=[
            DataRequired()
        ]
    )

    confirm_password = PasswordField('Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use!')

class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
