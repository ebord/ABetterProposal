from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ABetterProposal.model import db, Users, find_all_users, find_user_by_id 
from ABetterProposal.model import Logins, Proposals, ReferenceProposalStates, ReferenceProposalTypes, db 

from ABetterProposal.tables import TableUsers, TableLogins, TableProposals, TableProposalStates, TableProposalTypes
from ABetterProposal.forms import FormUsers, FormLogins, FormLoginsDelete, FormUsersDelete


# Blueprint Configuration
admin_bp = Blueprint('admin_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


# this will be the admin page, only accessible for administrators
@admin_bp.route('/admin')
def admin():

    # Check if user is loggedin
    if 'loggedin' in session:

        # Show the admin page with account info
        return render_template('admin.html', username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('auth_bp.login'))

#----------------------------
# profile
#----------------------------

# this will be the profile page, only accessible for loggedin users
@admin_bp.route('/profile')
def profile():

    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the users info for the user so we can display it on the profile page
        account = Users.get(Users.UserName==session['username'])
 
        # Show the profile page with account info
        return render_template('profile.html', account=account, username=session['username'])

        # User is not loggedin redirect to login page
        return redirect(url_for('auth_bp.login'))

#----------------------------
# logins
#----------------------------

# this will be the admin page for logins, only accessible for administrators
@admin_bp.route('/logins', methods=["GET", "POST"])
def admin_logins():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        logins = Logins.select()
        table = TableLogins(logins)
        
        # Show the admin logins page
        return render_template('/logins.html', username=session['username'], table=table, logins=logins)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the add page for logins, only accessible for administrators
@admin_bp.route('/logins_add', methods=["GET", "POST"])
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
            return redirect('/logins')           
          
        return render_template('./add-update-delete.html', username=session['username'], form=addform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the delete page for logins, only accessible for administrators
@admin_bp.route('/logins_delete/<int:id>', methods=["GET", "POST"])
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
            return redirect('/logins')

        return render_template('./add-update-delete.html', username=session['username'],form=deleteform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the delete page for logins, only accessible for administrators
@admin_bp.route('/logins_update/<int:id>', methods=["GET", "POST"])
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

            return redirect('/logins')
        else:
    
            # update form
            user = Logins.get(Logins.ID==id)
            updateform.username.data = user.UserName
            updateform.password.data = user.Password

        return render_template('./add-update-delete.html', username=session['username'],form=updateform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

## this will allowing sorting of the logins table
@admin_bp.route('/sort_logins')
def sort_logins():
    
    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    #reverse = request.args.get('direction', 'direction')
    table = TableLogins(Logins.select().order_by(getattr(Logins, sort)),
                          sort_by=sort,
                          sort_reverse=reverse)

    return render_template('admin_bp.logins.html', table=table)

#----------------------------
# users
#----------------------------

# this will be the admin page for user, only accessible for administrators
@admin_bp.route('/users')
def admin_users():
    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        #users = Users.select()
        users = find_all_users()
        table = TableUsers(users)

        # Show the admin users page
        return render_template('/users.html', username=session['username'], table=table, users=users)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the add page for users, only accessible for administrators
@admin_bp.route('/users_add', methods=["GET", "POST"])
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
            return redirect('/users')           
          
        return render_template('./add-update-delete.html', username=session['username'], form=addform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the delete page for users, only accessible for administrators
@admin_bp.route('/users_delete/<int:id>', methods=["GET", "POST"])
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
            return redirect('/users')

        return render_template('./add-update-delete.html', username=session['username'],form=deleteform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the delete page for logins, only accessible for administrators
@admin_bp.route('/users_update/<int:id>', methods=["GET", "POST"])
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

            return redirect('/users')
        else:
    
            # update form
            user = Users.get(Users.ID==id)
            updateform.firstname.data = user.FirstName
            updateform.lastname.data = user.LastName
            updateform.emailaddress.data = user.EmailAddress
            updateform.username.data = user.UserName
        return render_template('./add-update-delete.html', username=session['username'],form=updateform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

## this will allowing sorting of the admin users table
@admin_bp.route('/sort_users')
def sort_users():
    
    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = TableUsers(Users.select().order_by(getattr(Users, sort)),
                          sort_by=sort,
                          sort_reverse=reverse)
    
    return render_template('/users.html', table=table)

#----------------------------
# proposals
#----------------------------

# this will be the admin page for proposals, only accessible for administrators
@admin_bp.route('/proposals', methods=["GET", "POST"])
def admin_proposals():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        proposals = Proposals.select()
        table = TableProposals(proposals)
        
        # Show the admin logins page
        return render_template('/proposals.html', username=session['username'], table=table, proposals=proposals)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

#----------------------------
# proposal states
#----------------------------

# this will be the admin page for proposal states, only accessible for administrators
@admin_bp.route('/proposalstates', methods=["GET", "POST"])
def admin_proposalstates():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        proposalstates = ReferenceProposalStates.select()
        table = TableProposalStates(proposalstates)
        
        # Show the admin logins page
        return render_template('/proposalstates.html', username=session['username'], table=table, proposalstates=proposalstates)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

#----------------------------
# proposal types
#----------------------------

# this will be the admin page for proposal types, only accessible for administrators
@admin_bp.route('/proposaltypes', methods=["GET", "POST"])
def admin_proposaltypes():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        proposaltypes = ReferenceProposalTypes.select()
        table = TableProposalTypes(proposaltypes)
        
        # Show the admin logins page
        return render_template('/proposaltypes.html', username=session['username'], table=table, proposaltypes=proposaltypes)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

