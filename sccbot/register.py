__author__ = "http://steemit.com/@cervantes"
__copyright__ = "Copyright (C) 2018 steem's @cervantes"
__license__ = "MIT"
__version__ = "1.0"

import data
from data import User
from settings import Settings
from beem import Steem
from beem.account import Account
from datetime import datetime
from datetime import timedelta
#from steem import Steem



# define Python user-defined exceptions
class UserExistingError(Exception):
   pass

class UserRepeatedError(Exception):
   pass


class UserStillPendingError(Exception):
    pass

class UserAlreadyRegisteredError(Exception):
    pass

class UserValidator():

    def __init__(self, settings):
        self.settings = settings
        self.settings.load()

class UserRegisterer():

    def __init__(self, settings):
        self.settings = settings

    def delete_users(self):

        try:
            num_rows_deleted = self.settings.sa_session.query(User).delete()
            self.settings.sa_session.commit()
            print("User deleted: %s" % num_rows_deleted)
        except:
            self.settings.sa_session.rollback()
            raise Exception("Could not deleted users")



    def add_user(self, m_user):


        try:
            print("Adding user: %s" %m_user.steem_account)
            users = self.settings.sa_session.query(User).filter(User.discord_member_id == m_user.discord_member_id).all()
            for u in users:
                print(u)
            if (len(users) == 1):
                if users[0].verification_status ==  data.VS_PENDING:

                    raise UserStillPendingError("Discord user '%s' (id=%s) registration already iniciated with the steem account '%s' but still waiting confirmation." %
                                    (m_user.discord_member_name, m_user.discord_member_id, m_user.steem_account))
                elif users[0].verification_status ==  data.VS_ACCEPTED:
                    raise UserAlreadyRegisteredError("Discord user '%s' (id=%s) is already registered with the steem account '%s'" %
                                    (m_user.discord_member_name, m_user.discord_member_id, m_user.steem_account))


            self.settings.sa_session.add(m_user)
            self.settings.sa_session.commit()

        except Exception as e:
            raise e

    def get_users(self):
        return(self.settings.sa_session.query(User).all())

    def get_user(self, discord_id=None):
        if not id:
            return(self.settings.sa_session.query(User))
        else:
            return self.settings.sa_session.query(User).filter_by(discord_member_id=discord_id).first()
        #print("Mapping discord_user to steem user: %s -> %s " % (discord_member_name, steem_user))




    def get_user_by_discord_id(self, discord_member_id):

        users = self.settings.sa_session.query(User).filter_by(discord_member_id=discord_member_id).all()

        if(len(users)==0):
           raise Exception("There are NO registered user with discord_member_id = %s" % discord_member_id) 
        if(len(users)>1):
            raise Exception("There are more than one user with discord_member_id = %s" % discord_member_id)

        return(users[0])

    def is_registered(self, discord_member_id):

        try:
            user = self.get_user_by_discord_id(discord_member_id)
            return(True)
        except:
            return(False)

    def get_update_verification_token(discord_id, verification_token):
        try:
            user = self.get_user_by_discord_id(discord_id)
            user.verification_token = verification_token
            self.sa_session.commit()
        except Exception as e:
            raise e


    def get_transfer_ops(self, origin_account="",target_account = "", op_nr=100):

        steem = Steem(nodes=self.settings.get_rpc_nodes_list())
        account = Account(target_account,False)
        stop = datetime.utcnow() - timedelta(days=7)
        history = account.history_reverse(stop=stop, only_ops=["transfer"])
        for e in history:
            print(e)
        op_list = []
        for h in history:
            op = h[1]["op"]
            if op[0]=="transfer" and op[1]["from"] == origin_account and op[1]["to"] == target_account:
                op_list.append(op)

        return(op_list)


    def validate_pending(self):


        pending_users = self.settings.sa_session.query(User).filter(User.verification_status==data.VS_PENDING).all()
        for user in pending_users:

            print("Validating pending user: %s" % user.steem_account)
            print("Searching to transfer ops from %s to %s with memo:: '%s'" % (user.steem_account, self.settings.registrant_account, user.verification_token))
            ops = self.get_transfer_ops(origin_account = user.steem_account, target_account = self.settings.registrant_account, op_nr = 1000)
            #ops = self.get_transfer_ops(origin_account = user.steem_account, target_account = self.settings.registrant_account, op_nr = 10000)
            if len(ops)>0:

                for op in ops:
                    print(op)

                    # transfer op json format: ['transfer', {'from': 'pgarcgo', 'to': 'vota', 'amount': '0.001 STEEM', 'memo': '12345678910'}]
                    if(op[1]["memo"]==user.verification_token):
                        user.verification_status = data.VS_ACCEPTED
                        self.settings.sa_session.commit()
                        print("User registration sucessfully validated: %s" % user.steem_account)
                        break # if at least one transaction op existing with valid veritication token, no further scan needed.

            else:
                print("There as not beeing any recent transfer transaction from '@%s' to '@%s'" %(user.steem_account, self.settings.registrant_account))


if __name__ == "__main__":

    sa_session = data.return_session()
    settings = Settings(sa_session)
    r = UserRegisterer(settings=settings)
    r.validate_pending()
    pass