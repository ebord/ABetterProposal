from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ABetterProposal.tables import TableUsers, TableLogins
from ABetterProposal.model import Users, Logins, db 
from ABetterProposal.forms import FormUsers, FormLogins

# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

# this will be the login page, we need to use both GET and POST requests
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
        try:
            account = Logins.get((Logins.UserName==username) & (Logins.Password==password))
        except Logins.DoesNotExist:
             msg = 'Incorrect username/password!'
        else:
             # Set session variables
            session['loggedin'] = True
            session['id'] = account.ID
            session['username'] = account.UserName
            # Redirect to home page
            return redirect(url_for('home'))   
   
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

# this will be the logout page
@auth_bp.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('auth_bp.login'))

# this will be the registration page, we need to use both GET and POST requests
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        firstname = request.form['firstname']
        lastname = request.form['lastname']       
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL

        try:
            account = Users.get(Users.UserName==username)
        except Users.DoesNotExist:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not firstname or not lastname or not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                newuser = Users(FirstName=firstname, 
                                LastName=lastname, 
                                EmailAddress=email,
                                UserName=username)
                newuser.save()
                newlogin = Logins(UserName=username, 
                                Password=password)
                newlogin.save()
                msg = 'You have successfully registered!'
        else:
            msg = 'Account already exists!'
                
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
