import sys
sys.path.append('..')
import unittest
import data
from  settings import Settings


class TestSettings(unittest.TestCase):

    def test_init(self):
        sa_session = data.return_session()
        settings = Settings(sa_session)

    def test_get_rpc_nodes(self):
        data.drop_tables()
        data.create_tables()

        sa_session = data.return_session()
        settings = Settings(sa_session)
        settings.load(settings_file = "../sccbot.json")
        print(settings.steem_rpc_nodes)

if __name__ == '__main__':
    unittest.main()