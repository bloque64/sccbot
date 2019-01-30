import sys
sys.path.append('..')
import unittest
import data
from data import User
from  settings import Settings


class TestData(unittest.TestCase):


    def setUp(self):

        data.drop_tables()
        data.create_tables()


    def test_list_all_users(self):


        s = data.return_session()
        s.add(User(discord_member_name="user_test1"))
        s.add(User(discord_member_name="user_test2"))
        s.commit()
        users = s.query(data.User).all()
        print(len(users))
        self.assertEqual(len(users),2)
        assert isinstance(users, list)
        for u in users:
            assert isinstance(u,User)


    def tearDown(self):
        data.drop_tables()

if __name__ == '__main__':
    unittest.main()