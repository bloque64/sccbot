import sys
sys.path.append('../sccbot')
import unittest
import data
from  settings import Settings

settings_path = "../config/"

class TestSettings(unittest.TestCase):

    def test_init(self):
        sa_session = data.return_session()
        settings = Settings(sa_session, settings_path)

    def test_get_rpc_nodes(self):
        data.drop_tables()
        data.create_tables()

        sa_session = data.return_session()
        settings = Settings(sa_session, settings_path)
        settings.load(settings_file = "../config/sccbot.json")
        print(settings.steem_rpc_nodes)


    def test_save_settings(self):
        data.drop_tables()
        data.create_tables()
        sa_session = data.return_session()
        settings = Settings(sa_session, settings_path)
        settings.load(settings_file = "../config/sccbot.json")
        settings.settings_file = "test_settings.json"


    def test_get_chanel_by_id(self):
            
        data.drop_tables()
        data.create_tables()

        sa_session = data.return_session()
        settings = Settings(sa_session, settings_path)
        settings.load()

        print(settings.get_categories())



if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestSettings("test_get_chanel_by_id"))
    runner = unittest.TextTestRunner()
    runner.run(suite)