from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from ...models import User



class LoginForm(FlaskForm):
    #field name = DatatypeField('Label', validators=[LIST OF validators])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), 
        EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')
        # MUST BE LIKE THIS VALIDATE_FIELDNAME

    def validate_username(form, field):
        same_username_user = User.query.filter_by(username = field.data).first()
        if same_username_user:
            raise ValidationError('Username already registered')
    def validate_email(form, field):        
                                    # give me only the first result
        same_email_user = User.query.filter_by(email = field.data).first()
                                    # SELECT * FROM user WHERE email = ???
                                    #filter_by always gives a list (unless you use first())
        if same_email_user:
            raise ValidationError('Email already registered')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password', validators=[DataRequired(), 
        EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Update')