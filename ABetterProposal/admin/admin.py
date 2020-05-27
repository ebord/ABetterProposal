from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_paginate import Pagination, get_page_parameter

from ABetterProposal.model import db, Users, get_all_users, get_user_by_id, update_user_by_id 
from ABetterProposal.model import Logins,  get_all_logins, get_login_by_id, update_login_by_id
from ABetterProposal.model import Proposals, get_all_proposals, get_proposals_by_page, get_proposal_by_id, update_proposal_by_id
from ABetterProposal.model import ReferenceProposalStates,  get_all_proposalstates, get_proposalstates_by_page, get_proposalstates_count, update_proposalstate_by_id
from ABetterProposal.model import ReferenceProposalTypes,  get_all_proposaltypes, get_proposaltype_by_id, update_proposaltype_by_id

from ABetterProposal.tables import TableUsers, TableLogins, TableProposals, TableProposalStates, TableProposalTypes
from ABetterProposal.forms import FormUsers, FormLogins, FormProposals, FormProposalStates, FormProposalTypes

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

# this will be the profile page
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

# this will be the admin page for logins
@admin_bp.route('/logins', methods=["GET", "POST"])
def admin_logins():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        logins = get_all_logins()
        table = TableLogins(logins)
        
        # Show the admin logins page
        return render_template('/logins.html', username=session['username'], table=table, logins=logins)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the add page for logins
@admin_bp.route('/logins_add', methods=["GET", "POST"])
def logins_add():

    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Logins"
        header="Add Record To Logins"

        # add form
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

# this will be the delete page for logins
@admin_bp.route('/logins_delete/<int:id>', methods=["GET", "POST"])
def logins_delete(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Logins"
        header="Delete Record From Logins"

        # delete form
        test = get_login_by_id(id)
        deleteform = FormLogins()
        deleteform.username.data = test.UserName
        deleteform.password.data = test.Password

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

# this will be the delete page for logins
@admin_bp.route('/logins_update/<int:id>', methods=["GET", "POST"])
def logins_update(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Logins"
        header="Update Record In Logins"
        
        updateform = FormLogins()
        # update 
        if updateform.validate_on_submit():

            user= Logins()
            updateform.populate_obj(user)
    
            try:
                update_login_by_id(updateform.username.data,
                                   updateform.password.data, 
                                   id)
                flash ('successful update in logins', 'success')
            except:
                flash ('there was a problem updating in logins', 'success')   

            return redirect('/logins')
        else:
    
            # update form
            user = get_login_by_id(id)
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

# this will be the admin page for users
@admin_bp.route('/users')
def admin_users():
    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        #users = Users.select()
        users = get_all_users()
        table = TableUsers(users)

        # Show the admin users page
        return render_template('/users.html', username=session['username'], table=table, users=users)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the add page for users
@admin_bp.route('/users_add', methods=["GET", "POST"])
def users_add():

    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Users"
        header="Add Record To Users"

        # add form
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

# this will be the delete page for users
@admin_bp.route('/users_delete/<int:id>', methods=["GET", "POST"])
def users_delete(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Users"
        header="Delete Record From Users"

        # delete form
        test = get_user_by_id(id)
        deleteform = FormUsers()
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

# this will be the delete page for users
@admin_bp.route('/users_update/<int:id>', methods=["GET", "POST"])
def users_update(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Users"
        header="Update Record In Users"

        # update form
        updateform = FormUsers()

        # update 
        if updateform.validate_on_submit():

            user= Users()
            updateform.populate_obj(user)
    
            try:
                update_user_by_id (updateform.firstname.data, 
                                   updateform.lastname.data,
                                   updateform.emailaddress.data,
                                   updateform.username.data,
                                   id)
                flash ('successful update in users', 'success')
            except:
                flash ('there was a problem updating in users', 'success')   

            return redirect('/users')
        else:
    
            # update form
            user = get_user_by_id(id)
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

# this will be the admin page for proposals
@admin_bp.route('/proposals', methods=["GET", "POST"])
def admin_proposals():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        proposals = get_all_proposals()
        table = TableProposals(proposals)
        
        # Show the admin logins page
        return render_template('/proposals.html', username=session['username'], table=table, proposals=proposals)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the add page for proposals
@admin_bp.route('/proposals_add', methods=["GET", "POST"])
def proposals_add():

    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Proposals"
        header="Add Record To Proposals"

        # add form
        addform = FormProposals(request.form)

        # add 
        if addform.validate_on_submit():
            try:
                proposals = Proposals()
                proposals.ProposalNumber = addform.proposalnumber.data
                proposals.ProposalRevision = addform.proposalrevision.data
                proposals.ProposalDescription = addform.proposaldescription.data
                proposals.ProposalLink = addform.proposallink.data
                proposals.ProposalState = addform.proposalstate.data
                proposals.ProposalType = addform.proposaltype.data          
                proposals.save()
                flash ('successful save in proposals', 'success')
            except:
                flash ('there was a problem adding to proposals', 'error')
            return redirect('/proposals')           

        return render_template('./add-update-delete.html', username=session['username'], form=addform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the delete page for proposals
@admin_bp.route('/proposals_delete/<int:id>', methods=["GET", "POST"])
def proposals_delete(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Proposals"
        header="Delete Record From Proposals"

        # delete form
        test = get_proposal_by_id(id)
        deleteform = FormProposals()
        deleteform.proposalnumber.data = test.ProsposalNumber
        deleteform.proposalrevision.data = test.ProposalRevision       
        deleteform.proposaldescription.data = test.ProposalDescription
        deleteform.proposallink.data = test.ProposalLink
        deleteform.proposalstate.data = test.ProposalState
        deleteform.proposaltype.data = test.ProposalType

        # delete 
        if deleteform.validate_on_submit():
            try:
                Proposals.delete_by_id(id)
                flash ('successful delete in proposals', 'success')
            except:
                flash ('there was a problem deleting in proposals', 'error')
            return redirect('/proposals')

        return render_template('./add-update-delete.html', username=session['username'],form=deleteform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the delete page for proposals
@admin_bp.route('/proposals_update/<int:id>', methods=["GET", "POST"])
def proposals_update(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Proposals"
        header="Update Record In Proposals"

        # update form
        updateform = FormProposals()

        # update 
        if updateform.validate_on_submit():

            proposal= Proposals()
            updateform.populate_obj(proposal)
    
            try:
                update_proposal_by_id (updateform.proposalnumber.data, 
                                       updateform.proposalrevision.data,
                                       updateform.proposaldescription.data,
                                       updateform.proposallink.data,
                                       updateform.proposalstate.data,
                                       updateform.proposaltype.data,
                                       id)
                flash ('successful update in proposals', 'success')
            except:
                flash ('there was a problem updating in proposals', 'error')   

            return redirect('/proposals')
        else:
    
            # update form
            proposal = get_proposal_by_id(id)
            updateform.proposalnumber.data = proposal.ProposalNumber
            updateform.proposalrevision.data = proposal.ProposalRevision
            updateform.proposaldescription.data = proposal.ProposalDescription
            updateform.proposallink.data = proposal.ProposalLink
            updateform.proposalstate.data = proposal.ProposalState
            updateform.proposaltype.data = proposal.ProposalType
        return render_template('./add-update-delete.html', username=session['username'],form=updateform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

#----------------------------
# reference proposal states
#----------------------------

# this will be the admin page for reference proposal states
@admin_bp.route('/proposalstates', methods=["GET", "POST"])
def admin_proposalstates():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add pagination        
        page = request.args.get(get_page_parameter(), type=int, default=1 )
        #page = request.args.get(get_page_parameter, type=int, default=1 )

        # add table
        proposalstates = get_proposalstates_by_page(page,5)
        table = TableProposalStates(proposalstates)
        pagination = Pagination(page=page, total=ReferenceProposalStates.select().count(), record_name='proposalstates',show_single_page=True)
        #pagination = Pagination(page=page,per_page=ITEMS_PER_PAGE,total=ReferenceProposalStates.select().count(),record_name='proposalstates',css_framework='bootstrap4')

        # Show the admin logins page
        return render_template('/proposalstates.html', username=session['username'], 
            table=table, proposalstates=proposalstates, pagination=pagination)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the add page for reference proposal states
@admin_bp.route('/proposalstates_add', methods=["GET", "POST"])
def proposalstates_add():

    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Reference Proposal States"
        header="Add Record To Reference Proposal States"

        # add form
        addform = FormProposalStates(request.form)

        # add 
        if addform.validate_on_submit():
            try:
                proposalstates = ReferenceProposalStates()
                #proposalstates.ID = addform.id.data
                proposalstates.State = addform.state.data         
                proposalstates.save()
                flash ('successful save in reference proposal states', 'success')
            except:
                flash ('there was a problem adding to reference proposal states', 'warning')
            return redirect('/proposalstates')           

        return render_template('./add-update-delete.html', username=session['username'], form=addform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the delete page for reference proposal states
@admin_bp.route('/proposalstates_delete/<int:id>', methods=["GET", "POST"])
def proposalstates_delete(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Reference Proposal States"
        header="Delete Record From Reference Proposal States"

        # delete form
        test = get_proposalstate_by_id(id)
        deleteform = FormProposalStates()
        deleteform.id.data = test.ID
        deleteform.state.data = test.State      

        # delete 
        if deleteform.validate_on_submit():
            try:
                ReferenceProposalStates.delete_by_id(id)
                flash ('successful delete in reference proposal states', 'success')
            except:
                flash ('there was a problem deleting in reference proposal states', 'warning')
            return redirect('/proposalstates')

        return render_template('./add-update-delete.html', username=session['username'],form=deleteform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the delete page for reference proposal states
@admin_bp.route('/proposalstates_update/<int:id>', methods=["GET", "POST"])
def proposalstates_update(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Reference Proposal States"
        header="Update Record In Reference Proposal States"

        # update form
        updateform = FormProposalStates()

        # update 
        if updateform.validate_on_submit():

            proposalstates= ReferenceProposalStates()
            updateform.populate_obj(proposalstates)
    
            try:
                update_proposalstate_by_id (updateform.state.data,id)
                flash ('successful update in reference proposal states', 'success')
            except:
                flash ('there was a problem updating in reference proposal states', 'success')   

            return redirect('/proposalstates')
        else:
    
            # update form
            proposalstate = get_proposalstate_by_id(id)
            updateform.id.data = proposalstate.ID
            updateform.state.data = proposalstate.State
        return render_template('./add-update-delete.html', username=session['username'],form=updateform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

#----------------------------
# reference proposal types
#----------------------------

# this will be the admin page for reference proposal types
@admin_bp.route('/proposaltypes', methods=["GET", "POST"])
def admin_proposaltypes():

    # Check if user is loggedin
    if 'loggedin' in session:

        # add table
        proposaltypes = get_all_proposaltypes()
        table = TableProposalTypes(proposaltypes)
        
        # Show the admin logins page
        return render_template('/proposaltypes.html', username=session['username'], table=table, proposaltypes=proposaltypes)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the add page for reference proposal types
@admin_bp.route('/proposaltypes_add', methods=["GET", "POST"])
def proposaltypes_add():

    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Reference Proposal Types"
        header="Add Record To Reference Proposal Types"

        # add form
        addform = FormProposalTypes(request.form)

        # add 
        if addform.validate_on_submit():
            try:
                proposaltypes = ReferenceProposalTypes()
                proposaltypes.Type = addform.type.data         
                proposaltypes.save()
                flash ('successful save in reference proposal types', 'success')
            except:
                flash ('there was a problem adding to reference proposal types', 'warning')
            return redirect('/proposaltypes')           

        return render_template('./add-update-delete.html', username=session['username'], form=addform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the delete page for reference proposal types
@admin_bp.route('/proposaltypes_delete/<int:id>', methods=["GET", "POST"])
def proposaltypes_delete(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Reference Proposal Types"
        header="Delete Record From Reference Proposal Types"

        # delete form
        test = get_proposaltype_by_id(id)
        deleteform = FormProposalTypes()
        deleteform.id.data = test.ID
        deleteform.type.data = test.Type     

        # delete 
        if deleteform.validate_on_submit():
            try:
                ReferenceProposalTypes.delete_by_id(id)
                flash ('successful delete in reference proposal types', 'success')
            except:
                flash ('there was a problem deleting in reference proposal types', 'warning')
            return redirect('/proposaltypes')

        return render_template('./add-update-delete.html', username=session['username'],form=deleteform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))

# this will be the delete page for reference proposal types
@admin_bp.route('/proposaltypes_update/<int:id>', methods=["GET", "POST"])
def proposaltypes_update(id):
    # Check if user is loggedin
    if 'loggedin' in session:

        # set pagename and header
        pagename="Admin: Reference Proposal Types"
        header="Update Record In Reference Proposal Types"

        # update form
        updateform = FormProposalTypes()

        # update 
        if updateform.validate_on_submit():

            proposaltypes = ReferenceProposalTypes()
            updateform.populate_obj(proposaltypes)
    
            try:
                update_proposaltype_by_id (updateform.type.data, id)
                flash ('successful update in reference proposal types', 'success')
            except:
                flash ('there was a problem updating in reference proposal types', 'error')   

            return redirect('/proposaltypes')
        else:
    
            # update form
            proposaltype = get_proposaltype_by_id(id)
            updateform.id.data = proposaltype.ID
            updateform.type.data = proposaltype.Type
        return render_template('./add-update-delete.html', username=session['username'],form=updateform, page=pagename, header=header)

    # User is not loggedin redirect to admin page
    return redirect(url_for('auth_bp.login'))
