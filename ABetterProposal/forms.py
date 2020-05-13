from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput

# form definitions for users
class FormUsers(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    emailaddress = StringField('email', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField("Submit")

class FormLogins(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', widget=PasswordInput(hide_value=False))

    submit = SubmitField("Submit")

class FormLoginsDelete(FlaskForm):
    username = StringField('username')
    submit = SubmitField("Submit")

class FormUsersDelete(FlaskForm):
    firstname = StringField('firstname')
    lastname = StringField('lastname')
    emailaddress = StringField('email')
    username = StringField('username')
    submit = SubmitField("Submit") 