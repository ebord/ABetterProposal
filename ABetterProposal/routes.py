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

# this will be the login page, we need to use both GET and POST requests
@app.route('/proposal-experiments/login', methods=['GET', 'POST'])
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
@app.route('/proposal-experiments/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# this will be the registration page, we need to use both GET and POST requests
@app.route('/proposal-experiments/register', methods=['GET', 'POST'])
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

# this will be the admin page, only accessible for administrators
@app.route('/proposal-experiments/admin')
def admin():

    # Check if user is loggedin
    if 'loggedin' in session:

        # Show the admin page with account info
        return render_template('admin.html', username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#----------------------------
# logins
#----------------------------

# this will be the admin page for logins, only accessible for administrators
@app.route('/proposal-experiments/admin/logins', methods=["GET", "POST"])
def admin_logins():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        logins = Logins.select()
        table = TableLogins(logins)
        
        # Show the admin logins page
        return render_template('/admin/logins.html', username=session['username'], table=table, logins=logins)

    # User is not loggedin redirect to admin page
    return redirect(url_for('login'))

# this will be the add page for logins, only accessible for administrators
@app.route('/proposal-experiments/logins_add', methods=["GET", "POST"])
def logins_add():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add form
        pagename="Admin: Logins"
        header="Add Record To Logins"
        addform = FormLogins(request.form)

        # add 
        if addform.validate_on_submit():
            try:
                logins = Logins()
                logins.UserName = addform.username.data
                logins.Password = addform.password.data            
                logins.save()
                flash ('successful save in logins', 'success')
            except:
                flash ('there was a problem adding to logins', 'warning')
            return redirect('/proposal-experiments/admin/logins')           
          
        return render_template('add-update-delete.html', username=session['username'], form=addform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('login'))

# this will be the delete page for logins, only accessible for administrators
@app.route('/proposal-experiments/logins_delete/<int:id>', methods=["GET", "POST"])
def logins_delete(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # delete form
        pagename="Admin: Logins"
        header="Delete Record From Logins"
        test = Logins.get(Logins.ID==id)
        deleteform = FormLoginsDelete()
        deleteform.username.data = test.UserName

        # delete 
        if deleteform.validate_on_submit():
            try:
                Logins.delete_by_id(id)
                flash ('successful delete in logins', 'success')
            except:
                flash ('there was a problem deleting in logins', 'warning')
            return redirect('/proposal-experiments/admin/logins')

        return render_template('add-update-delete.html', username=session['username'],form=deleteform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('login'))

# this will be the delete page for logins, only accessible for administrators
@app.route('/proposal-experiments/logins_update/<int:id>', methods=["GET", "POST"])
def logins_update(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        pagename="Admin: Logins"
        header="Update Record In Logins"
        updateform = FormLogins()
        # update 
        if updateform.validate_on_submit():

            user= Logins()
            updateform.populate_obj(user)
    
            try:
                query = Logins.update(
                    UserName=updateform.username.data,       
                    Password=updateform.password.data
                ).where(Logins.ID==id)
                query.execute()
                flash ('successful update in logins', 'success')
            except:
                flash ('there was a problem updating in logins', 'success')   

            return redirect('/proposal-experiments/admin/logins')
        else:
    
            # update form
            user = Logins.get(Logins.ID==id)
            updateform.username.data = user.UserName
            updateform.password.data = user.Password

        return render_template('add-update-delete.html', username=session['username'],form=updateform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('login'))

## this will allowing sorting of the logins table
@app.route('/proposal-experiments/sort_logins')
def sort_logins():
    
    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    #reverse = request.args.get('direction', 'direction')
    table = TableLogins(Logins.select().order_by(getattr(Logins, sort)),
                          sort_by=sort,
                          sort_reverse=reverse)

    return render_template('/admin/logins.html', table=table)

#----------------------------
# users
#----------------------------

# this will be the admin page for user, only accessible for administrators
@app.route('/proposal-experiments/admin/users')
def admin_users():
    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        #users = Users.select()
        users = find_all_users()
        table = TableUsers(users)

        # Show the admin users page
        return render_template('/admin/users.html', username=session['username'], table=table, users=users)

    # User is not loggedin redirect to admin page
    return redirect(url_for('login'))

# this will be the add page for users, only accessible for administrators
@app.route('/proposal-experiments/users_add', methods=["GET", "POST"])
def users_add():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add form
        pagename="Admin: Users"
        header="Add Record To Users"
        addform = FormUsers(request.form)

        # add 
        if addform.validate_on_submit():
            try:
                users = Users()
                users.FirstName = addform.firstname.data
                users.LastName = addform.lastname.data
                users.EmailAddress = addform.emailaddress.data
                users.UserName = addform.username.data            
                users.save()
                flash ('successful save in users', 'success')
            except:
                flash ('there was a problem adding to users', 'warning')
            return redirect('/proposal-experiments/admin/users')           
          
        return render_template('add-update-delete.html', username=session['username'], form=addform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('login'))

# this will be the delete page for users, only accessible for administrators
@app.route('/proposal-experiments/users_delete/<int:id>', methods=["GET", "POST"])
def users_delete(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # delete form
        #test = Users.get(Users.ID==id)
        pagename="Admin: Users"
        header="Delete Record From Users"
        test = find_user_by_id(id)
        deleteform = FormUsersDelete()
        deleteform.firstname.data = test.FirstName
        deleteform.lastname.data = test.LastName
        deleteform.emailaddress.data = test.EmailAddress
        deleteform.username.data = test.UserName

        # delete 
        if deleteform.validate_on_submit():
            try:
                Users.delete_by_id(id)
                flash ('successful delete in users', 'success')
            except:
                flash ('there was a problem deleting in users', 'warning')
            return redirect('/proposal-experiments/admin/users')

        return render_template('add-update-delete.html', username=session['username'],form=deleteform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('login'))

# this will be the delete page for logins, only accessible for administrators
@app.route('/proposal-experiments/users_update/<int:id>', methods=["GET", "POST"])
def users_update(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        pagename="Admin: Users"
        header="Update Record In Users"
        updateform = FormUsers()
        # update 
        if updateform.validate_on_submit():

            user= Users()
            updateform.populate_obj(user)
    
            try:
                query = Users.update(
                    FirstName=updateform.firstname.data,
                    LastName=updateform.lastname.data,
                    EmailAddress=updateform.emailaddress.data,            
                    UserName=updateform.username.data
                ).where(Users.ID==id)
                query.execute()
                flash ('successful update in users', 'success')
            except:
                flash ('there was a problem updating in users', 'success')   

            return redirect('/proposal-experiments/admin/users')
        else:
    
            # update form
            user = Users.get(Users.ID==id)
            updateform.firstname.data = user.FirstName
            updateform.lastname.data = user.LastName
            updateform.emailaddress.data = user.EmailAddress
            updateform.username.data = user.UserName
        return render_template('add-update-delete.html', username=session['username'],form=updateform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('login'))

## this will allowing sorting of the admin users table
@app.route('/proposal-experiments/sort_users')
def sort_users():
    
    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = TableUsers(Users.select().order_by(getattr(Users, sort)),
                          sort_by=sort,
                          sort_reverse=reverse)
    
    return render_template('/admin/users.html', table=table)

#----------------------------
# proposals
#----------------------------

# this will be the admin page for proposals, only accessible for administrators
@app.route('/proposal-experiments/admin/proposals', methods=["GET", "POST"])
def admin_proposals():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        proposals = Proposals.select()
        table = TableProposals(proposals)
        
        # Show the admin logins page
        return render_template('/admin/proposals.html', username=session['username'], table=table, proposals=proposals)

    # User is not loggedin redirect to admin page
    return redirect(url_for('login'))

#----------------------------
# proposal states
#----------------------------

# this will be the admin page for proposal states, only accessible for administrators
@app.route('/proposal-experiments/admin/proposalstates', methods=["GET", "POST"])
def admin_proposalstates():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        proposalstates = ReferenceProposalStates.select()
        table = TableProposalStates(proposalstates)
        
        # Show the admin logins page
        return render_template('/admin/proposalstates.html', username=session['username'], table=table, proposalstates=proposalstates)

    # User is not loggedin redirect to admin page
    return redirect(url_for('login'))

#----------------------------
# proposal types
#----------------------------

# this will be the admin page for proposal types, only accessible for administrators
@app.route('/proposal-experiments/admin/proposaltypes', methods=["GET", "POST"])
def admin_proposaltypes():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        proposaltypes = ReferenceProposalTypes.select()
        table = TableProposalTypes(proposaltypes)
        
        # Show the admin logins page
        return render_template('/admin/proposaltypes.html', username=session['username'], table=table, proposaltypes=proposaltypes)

    # User is not loggedin redirect to admin page
    return redirect(url_for('login'))

# this will be the profile page, only accessible for loggedin users
@app.route('/proposal-experiments/profile')
def profile():

    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the users info for the user so we can display it on the profile page
        account = Users.get(Users.UserName==session['username'])
 
        # Show the profile page with account info
        return render_template('profile.html', account=account, username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# this will be the experiment db dashboard page, only accessible for loggedin users
@app.route('/proposal-experiments/experiment_db_dashboard')
def experiment_db_dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the experimental db dashboard page
        return render_template('experiment_db_dashboard.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# this will be the experiment db proposals page, only accessible for loggedin users
@app.route('/proposal-experiments/experiment_db_proposals')
def experiment_db_proposals():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the experimental db proposals page
        return render_template('experiment_db_proposals.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# this will be the experiment db plans page, only accessible for loggedin users
@app.route('/proposal-experiments/experiment_db_plans')
def experiment_db_plans():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the experimental db plans page
        return render_template('experiment_db_plans.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# this will be the experiment db teams page, only accessible for loggedin users
@app.route('/proposal-experiments/experiment_db_teams')
def experiment_db_teams():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the experimental db teams page
        return render_template('experiment_db_teams.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# this will be the experiment repo page, only accessible for loggedin users
@app.route('/proposal-experiments/experiment_repo')
def experiment_repo():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('experiment_repo.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# this will be the experiment tools page, only accessible for loggedin users
@app.route('/proposal-experiments/experiment_tools')
def experiment_tools():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('experiment_tools.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
