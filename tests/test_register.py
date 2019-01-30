import sys 
sys.path.append('..')
import unittest
import data
from  settings import Settings
from register import UserRegisterer


settings_path = "../settings/"

def create_test_user1():

    user1 = data.User()
    user1.discord_member_id = "253584245790867457"
    user1.discord_member_name = "pgarcgo [cervantes]#0325"
    user1.steem_account = "pgarcgo"
    user1.verification_status = data.VS_PENDING
    user1.verification_token = "12345678910"

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
    suite.addTest(TestDeleteUsers("test_del_all_users"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
