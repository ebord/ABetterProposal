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

# ----------------------
# logins
# ----------------------
class Logins(BaseModel):
    ID = PrimaryKeyField(null=False) 
    UserName = TextField()
    Password = TextField()

    class Meta:
        db_table = "logins"

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

# ---------------------------
# reference-proposalstates
# ---------------------------
class ReferenceProposalStates(BaseModel):
    ID = PrimaryKeyField(null=False) 
    State = TextField()

    class Meta:
        db_table = "referenceproposalstates"

# ---------------------------
# reference-proposaltype
# ---------------------------
class ReferenceProposalTypes(BaseModel):
    ID = PrimaryKeyField(null=False) 
    Type = TextField()

    class Meta:
        db_table = "referenceproposaltypes"