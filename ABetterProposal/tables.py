from flask_table import Table,Col,LinkCol
from flask import url_for

# ------------------------------------
# table definitions for users
# ------------------------------------
class TableUsers(Table):
    classes = ['table', 'table-sm']
    thead_classes = ['thead-light']
    ID = Col ('Id')
    FirstName = Col('First Name')
    LastName = Col('Last Name')
    EmailAddress = Col('Email')
    UserName = Col ('User Name')

    allow_sort = True
    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction =  'desc'
        else:
            direction = 'asc'
        return url_for('sort_users', sort=col_key, direction=direction)   

# ------------------------------------
# table definitions for logins
# ------------------------------------
class TableLogins(Table):
    classes = ['table', 'table-sm']
    thead_classes = ['thead-light']
    ID = Col ('Id')
    UserName = Col ('User Name')
    Password = Col('Password')
    
    #update = LinkCol('update', 'logins_update', url_kwargs=dict(id='ID'))
    #delete = LinkCol('delete', 'logins_delete', url_kwargs=dict(id='ID'))

    allow_sort = True
    def sort_url(self, col_key, reverse=True):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('sort_logins', sort=col_key, direction=direction)

# --------------------------------------------------
# table definitions for proposals
# --------------------------------------------------
class TableProposals(Table):
    classes = ['table', 'table-sm']
    thead_classes = ['thead-light']
    ID = Col ('Id')
    ProposalNumber = Col('Number')
    ProposalRevision = Col('Revision')
    ProposalDescription = Col('Description')
    ProposalLink = Col('Link')
    ProposalState = Col('State')
    ProposalType = Col('Type')

# --------------------------------------------------
# table definitions for reference-proposalstates
# --------------------------------------------------
class TableProposalStates(Table):
    classes = ['table', 'table-sm']
    thead_classes = ['thead-light']
    ID = Col ('Id')
    State = Col('State')

# --------------------------------------------------
# table definitions for reference-proposaltypes
# --------------------------------------------------
class TableProposalTypes(Table):
    classes = ['table', 'table-sm']
    thead_classes = ['thead-light']
    ID = Col ('Id')
    Type = Col('Type')
