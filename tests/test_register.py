import sys
import unittest
sys.path.append("../sccbot")
import data as data
from data import User
from settings import Settings
from register import UserRegisterer

TEST_VERIFICATION_TOKEN = "74875725480c3eb46912c1bbbfbcc9d6"

settings_path = "../config/"
sa_session = data.return_session()
settings = Settings(sa_session, settings_path)

def create_test_user1():

    user1 = User()
    user1.discord_member_id = settings.sccbot_test_discord_id
    user1.discord_member_name = settings.sccbot_test_discord_member_name 
    user1.steem_account = settings.sccbot_test_steem_account
    user1.verification_status = data.VS_PENDING
    user1.verification_token = TEST_VERIFICATION_TOKEN

    return(user1)

def create_test_user2():

    user2 = data.User()
    user2.discord_member_id = "253584245790867457"
    user2.discord_member_name = "testdiscord"
    user2.steem_account = "testdiscord"
    user2.verification_status = data.VS_PENDING
    user2.verification_token = "1111111111"

    return(user2)

class TestAddUsers(unittest.TestCase):

        def test_add_user(self):

            data.drop_tables()
            data.create_tables()

            sa_session = data.return_session()
            settings = Settings(sa_session, settings_path)
            settings.load()

            user_registerer = UserRegisterer(settings)
            user1 = create_test_user1()
            user_registerer.add_user(user1)

            self.assertTrue(len(sa_session.query(data.User).all()) == 1)

            # self.assertTrue(len(sa_session.query(data.User).all()) == 2)
            # res = sa_session.query(data.User).filter(data.User.discord_member_id=="3333").all()
            # self.assertTrue(len(res) == 0)
            # res = sa_session.query(data.User).filter(data.User.discord_member_id == "253584245790867457").all()
            # self.assertTrue(len(res) == 1)
            # res = sa_session.query(data.User).filter(data.User.discord_member_id == "253584245790867457").one()
            # self.assertTrue(res.discord_member_id == "253584245790867457")

class TestValidateUsers(unittest.TestCase):

        def setUp(self):
            print("Setting up test")

        def test_validate_pending(self):

            data.drop_tables()
            data.create_tables()

            sa_session = data.return_session()
            settings = Settings(sa_session, settings_path)
            settings.load()

            user_registerer = UserRegisterer(settings)
            user1 = create_test_user1()
            user_registerer.add_user(user1)

            user_registerer.validate_pending()
            data.drop_tables()
            data.create_tables()


            sa_session.close()

        def tearDown(self):
            print("tear down test")

class TestDeleteUsers(unittest.TestCase):

        def test_del_all_users(self):

            data.drop_tables()
            data.create_tables()

            sa_session = data.return_session()
            settings = Settings(sa_session, settings_path)
            settings.load()

            user_registerer = UserRegisterer(settings)
            user2 = create_test_user2()
            user_registerer.add_user(user2)

            tmp_user = user_registerer.get_user(user2.discord_member_id)
            self.assertTrue(user2 == tmp_user)
            
            user_registerer.delete_users()

            self.assertTrue(len(user_registerer.get_users()) == 0)

            sa_session.close()



if __name__ == '__main__':

    suite = unittest.TestSuite()
    #suite.addTest(TestAddUsers("test_add_user"))
    #suite.addTest(TestDeleteUsers("test_del_all_users"))
    suite.addTest(TestValidateUsers("test_validate_pending"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    print("Exit Test Units")
