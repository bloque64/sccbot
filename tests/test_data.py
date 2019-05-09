import sys 
import unittest
import data
from  settings import Settings
from register import UserRegisterer


settings_path = "../config/"

def create_test_user1():

    user1 = data.User()
    user1.discord_member_id = "253584245790867457"
    user1.discord_member_name = "pgarcgo [cervantes]#0325"
    user1.steem_account = "pgarcgo"
    user1.verification_status = data.VS_PENDING
    user1.verification_token = "12345678910"

    return(user1)


def create_test_user2():

    user1 = data.User()
    user1.discord_member_id = "253584245790867447"
    user1.discord_member_name = "sccbot_testuser_1 [sccbot_testuser_1]#0326"
    user1.steem_account = "sccbot_testuser_1"
    user1.verification_status = data.VS_PENDING
    user1.verification_token = "12345678910"

    return(user1)

class TestRegisterMethods(unittest.TestCase):

        def test_add_user(self):

            data.drop_tables()
            data.create_tables()

            sa_session = data.return_session()
            settings = Settings(sa_session, settings_path)
            settings.load()

            user_registerer = UserRegisterer(settings)
            user1 = create_test_user1()
            user2 = create_test_user2()

            user_registerer.add_user(user1)
            user_registerer.add_user(user2)

        def test_delete_users(self):

            data.drop_tables()
            data.create_tables()

            sa_session = data.return_session()
            settings = Settings(sa_session, settings_path)
            settings.load()

            user_registerer = UserRegisterer(settings)
            user1 = create_test_user1()
            user2 = create_test_user2()

            user_registerer.add_user(user1)
            user_registerer.add_user(user2)
            
            user_registerer.delete_users()


        def test_get_chanel_by_id(self):
            
            data.drop_tables()
            data.create_tables()

            sa_session = data.return_session()
            settings = Settings(sa_session, settings_path)
            settings.load()

            print(settings.get_categories())
            #data.get_channel_by_id():



if __name__ == '__main__':
    unittest.main()