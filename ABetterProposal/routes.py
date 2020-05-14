from flask import render_template, request, redirect, url_for, session, flash
import re
import os
#from tables import TableUsers, TableLogins, TableProposals, TableProposalStates, TableProposalTypes
#from models import Users, Logins, Proposals, ReferenceProposalStates, ReferenceProposalTypes, db 
#from models import find_all_users, find_user_by_id
#from forms import FormUsers, FormLogins, FormLoginsDelete, FormUsersDelete
#from flask_bootstrap import Bootstrap

#app = Flask(__name__)
#bootstrap = Bootstrap(app)

# Change this to your secret key (can be anything, it's for extra protection)
#app.secret_key = os.urandom(24)

# this will be the home page, only accessible for loggedin users
@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():

    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the users info for the user so we can display it on the profile page
        account = Users.get(Users.UserName==session['username'])
 
        # Show the profile page with account info
        return render_template('/admin/profile.html', account=account, username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('admin_bp.login'))



