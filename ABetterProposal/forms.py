from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput

# ---------------------------
# users
# ---------------------------

class FormUsers(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    emailaddress = StringField('email', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField("Submit")

# ---------------------------
# logins
# ---------------------------

class FormLogins(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', widget=PasswordInput(hide_value=False))
    submit = SubmitField("Submit")

# ---------------------------
# proposals
# ---------------------------

class FormProposals(FlaskForm):
    proposalnumber = StringField('proposalnumber', validators=[DataRequired()])
    proposalrevision = StringField('proposalnumber', validators=[DataRequired()])
    proposaldescription = StringField('proposaldescription', validators=[DataRequired()])
    proposallink = StringField('proposallink', validators=[DataRequired()])
    proposalstate = StringField('proposalstate', validators=[DataRequired()])
    proposaltype = StringField('proposaltype', validators=[DataRequired()])
    submit = SubmitField("Submit")

# ---------------------------
# reference proposal states
# ---------------------------

class FormProposalStates(FlaskForm):
    #id = StringField('id', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    submit = SubmitField("Submit")

# ---------------------------
# reference proposal types
# ---------------------------

class FormProposalTypes(FlaskForm):
    id = HiddenField('id')
    type = StringField('type', validators=[DataRequired()])
    submit = SubmitField("Submit")
