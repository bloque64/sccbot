from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


print("Creating SQLAlchemy Engine...")
engine = create_engine('sqlite:///sccbot.db', echo=True)


base = declarative_base()

class User(base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    discord_name = Column(String)
    steem_name = Column(String)
    curation_rep = Column(Integer)
    curation_role = String()
    
    def __repr__(self):
        return "<User(discord_name='%s', steem_name='%s', curation_rep='%s')>" % (discord_name, steem_name, curation_rep)


class Post(base):

    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    permalink = Column(String)
    fulllink = Column(String)
    link_poster = Column(String)
    author = Column(String)
    category = Column(String)
    upvotes = Column(Integer)



base.metadata.create_all(engine)
print ("Creating Session")
Session = sessionmaker(bind=engine)
session = Session()
