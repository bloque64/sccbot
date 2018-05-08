
import data
from data import User


VS_PENDING = "PENDING"
VS_ACCEPTED = "ACCEPTED"
VS_REJECTED = "REJECTED"

class UserRegisterer():

    def __init__(self, sa_session):
        self.sa_session = sa_session
    
    def map_user(self,discord_member_id, discord_member_name, steem_account):
        new_user = User()
        new_user.discord_member_name = discord_member_name
        new_user.discord_member_id = discord_member_id
        new_user.steem_account = steem_account
        new_user.verification_status = VS_PENDING


        self.sa_session.add(new_user)
        self.sa_session.commit()

    def get_users(self):
        return(self.sa_session.query(User))
        #print("Mapping discord_user to steem user: %s -> %s " % (discord_member_name, steem_user))
