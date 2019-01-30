import sys 
sys.path.append('..')
import unittest
import data
from  settings import Settings
from manager import Manager
from register import UserRegisterer
import os

DB_FILE = "./sccbot.db"

class TestCuratorMethods(unittest.TestCase):

    def clear_database(self):
        try:
            os.remove(DB_FILE)
        except:
            print("Could not remove file. Possible not existing: %s" % DB_FILE)

    def test_add_curator(self):
        pass

    def test_get_curators(self):
        self.clear_database()
        sa_session = data.init()
        settings = Settings(sa_session)
        user_registerer = UserRegisterer(settings)
        user_registerer.add_user(discord_member_id=253584245790867457,
                                 discord_member_name="pgarcgo [cervantes]#0325",
                                 steem_account="pgarcgo",
                                 role=data.USER_ROLE_CURATOR,
                                 verification_status=data.VS_ACCEPTED)
        user_registerer.add_user(discord_member_id=2345, discord_member_name="test_user", steem_account="test_user")
        curator = Manager(settings)
        curators = curator.get_curators()
        print("Nr. of verified curators: %s" % len(curators))
        for c in curators:
            print(c)

if __name__ == '__main__':
    unittest.main()