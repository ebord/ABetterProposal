from flask_table import Table,Col,LinkCol
from flask import url_for

# ------------------------------------
# users
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
# logins
# ------------------------------------

class TableLogins(Table):
    classes = ['table', 'table-sm']
    thead_classes = ['thead-light']
    ID = Col ('Id')
    UserName = Col ('User Name')
    Password = Col('Password')

    allow_sort = True
    def sort_url(self, col_key, reverse=True):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('sort_logins', sort=col_key, direction=direction)

# --------------------------------------------------
# proposals
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
# referenceproposalstates
# --------------------------------------------------

class TableProposalStates(Table):
    classes = ['table', 'table-sm']
    thead_classes = ['thead-light']
    ID = Col ('Id')
    State = Col('State')

# --------------------------------------------------
# referenceproposaltypes
# --------------------------------------------------
class TableProposalTypes(Table):
    classes = ['table', 'table-sm']
    thead_classes = ['thead-light']
    ID = Col ('Id')
    Type = Col('Type')
