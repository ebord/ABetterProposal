import peewee
from peewee import MySQLDatabase, Model, PrimaryKeyField, TextField

# Intialize MySQL
db = MySQLDatabase('proposalexperiments', user='root',
    passwd='Emerson#20', host='localhost' )

class BaseModel(Model):
    class Meta:
        database = db

# ----------------------
# users
# ----------------------

class Users(BaseModel):
    ID = PrimaryKeyField(null=False)
    FirstName = TextField()
    LastName = TextField() 
    EmailAddress= TextField()
    UserName = TextField()

    class Meta:
        db_table = "users"

# common functions
def find_all_users():
    query = Users.select()
    return query

def find_user_by_id(attr):
    query = Users.get(Users.ID == attr)
    return query

def update_user_by_id(firstname, lastname, emailaddress, username, id):
    query = Users.update(
        FirstName=firstname,
        LastName=lastname,
        EmailAddress=emailaddress,            
        UserName=username
    ).where(Users.ID==id)
    query.execute()

# ----------------------
# logins
# ----------------------

class Logins(BaseModel):
    ID = PrimaryKeyField(null=False) 
    UserName = TextField()
    Password = TextField()

    class Meta:
        db_table = "logins"

# common functions
def find_all_logins():
    query = Logins.select()
    return query

def find_login_by_id(attr):
    query = Logins.get(Logins.ID == attr)
    return query

def update_login_by_id(username, password, id):
    query = Logins.update(
        UserName=username,       
        Password=password
    ).where(Logins.ID==id)
    query.execute()

# ---------------------------
# proposals
# ---------------------------

class Proposals(BaseModel):
    ID = PrimaryKeyField(null=False)
    ProposalNumber = TextField()
    ProposalRevision = TextField() 
    ProposalDescription = TextField()
    ProposalLink = TextField()
    ProposalState = TextField()
    ProposalType = TextField()

    class Meta:
        db_table = "proposals"

# common functions
def find_all_proposals():
    query = Proposals.select()
    return query

def find_proposal_by_id(attr):
    query = Proposals.get(Proposals.ID == attr)
    return query

def update_proposal_by_id(number, revision, description, link, state, type, id):
    query = Proposals.update(
        ProposalNumber=number,
        ProposalRevision=revision,
        ProposalDescription=description,
        ProposalLink=link,
        ProposalState=state,
        ProposalType=type
    ).where(Proposals.ID==id)
    query.execute()

# ---------------------------
# reference-proposalstates
# ---------------------------

class ReferenceProposalStates(BaseModel):
    ID = PrimaryKeyField(null=False) 
    State = TextField()

    class Meta:
        db_table = "referenceproposalstates"

# common functions
def find_all_proposalstates():
    query = ReferenceProposalStates.select()
    return query

def find_proposalstate_by_id(attr):
    query = ReferenceProposalStates.get(ReferenceProposalStates.ID == attr)
    return query

def update_proposalstate_by_id(id, state):
    query = ReferenceProposalStates.update(
        ID=id,       
        State=state
    ).where(ReferenceProposalStates.ID==id)
    query.execute()

# ---------------------------
# reference-proposaltype
# ---------------------------

class ReferenceProposalTypes(BaseModel):
    ID = PrimaryKeyField(null=False) 
    Type = TextField()

    class Meta:
        db_table = "referenceproposaltypes"

# common functions
def find_all_proposaltypes():
    query = ReferenceProposalTypes.select()
    return query

def find_proposaltype_by_id(attr):
    query = ReferenceProposalTypes.get(ReferenceProposalTypes.ID == attr)
    return query

def update_proposaltype_by_id(id, type):
    query = ReferenceProposalTypes.update(
        ID=id,       
        Type=type
    ).where(ReferenceProposalTypes.ID==id)
    query.execute()