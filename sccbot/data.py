__author__ = "http://steemit.com/@cervantes"
__copyright__ = "Copyright (C) 2018 steem's @cervantes"
__license__ = "MIT"
__version__ = "1.0"

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import os



USER_ROLE_REGISTERED = "REGISTERED"
USER_LEVEL_BEGGINER = "BEGINNER"
USER_LEVEL_GOOD = "GOOD"
USER_LEVEL_EXCELENT = "EXCELENT"
USER_LEVEL_MASTER = "MASTER"

VS_PENDING = "PENDING"
VS_ACCEPTED = "ACCEPTED"
VS_REJECTED = "REJECTED"

sscbot_admin_user = os.environ["SCCBOT_ADMIN_USER"]
sccbot_admin_password = os.environ["SCCBOT_ADMIN_PASSWORD"]
sccbot_db_host = os.environ["SCCBOT_DB_HOST"]
sccbot_db_name = os.environ["SCCBOT_DB_NAME"]

connection_string = "mysql+pymysql://%s:%s@%s/%s" % (sscbot_admin_user, sccbot_admin_password, sccbot_db_host, sccbot_db_name)
#connection_string = "mysql://%s:%s@%s/%s" % (sscbot_admin_user, sccbot_admin_password, sccbot_db_host, sccbot_db_name)

session_instance = None

base = declarative_base()

class User(base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    discord_member_name = Column(String(50))
    discord_member_id = Column(String(50))
    steem_account = Column(String(30))
    role = Column(String(10))          # "CURATOR", "CLEANER"
    level = Column(String(10))         # "BEGNNER, GOOD, EXCELENT, MASTER
    verification_status = Column(String(10))   # "PENDING", "ACCEPTED", "REJECTED"
    verification_token = Column(String(100))
    reputation = Column(Integer)               # Integer 0 to 100

    
    def __repr__(self):
        return "<User(discord_name='%s' (%s), steem_name='%s')>" % (self.discord_member_name, self.discord_member_id, self.steem_account)
    
    def __init__(self, discord_member_name = None, discord_member_id = None, steem_account=None):

        self.discord_member_name = discord_member_name
        self.discord_member_id = discord_member_id
        self.steem_account = steem_account

    

class Post(base):

    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    permalink = Column(String(256))
    fulllink = Column(String(256))
    link_poster = Column(String(256))
    author = Column(String(30))
    category = Column(String(50))
    upvotes = Column(Integer)
    #promoted_by = Column(User)

class Category(base):

    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    description = Column(String(256))

def return_session():

    engine = create_engine(connection_string, echo=False)
    Session = sessionmaker(bind=engine)
    session_instance = Session()
    return(session_instance)

def drop_tables():

    engine = create_engine(connection_string, echo=False)
    base.metadata.bind = engine
    base.metadata.drop_all()


def create_tables():

    engine = create_engine(connection_string, echo=False)
    base.metadata.create_all(engine)

def get_users():
    return(session_instance.query(User))


def reset_and_inicialize():
    drop_tables()
    create_tables()
    populate_default_categories()


def populate_default_categories()

if __name__ == "__main__":

    #s = init()
    #print("%s" % sscbot_admin_user)
    create_tables()
