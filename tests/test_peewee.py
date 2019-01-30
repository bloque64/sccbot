import sys
sys.path.append('..')
import unittest
import data
from  settings import Settings
import os
import peewee
from peewee import MySQLDatabase


class TestPeewee(unittest.TestCase):

    def test_mysql_connectivity(self):

        sccbot_admin_user = os.environ["SCCBOT_ADMIN_USER"]
        sccbot_admin_password = os.environ["SCCBOT_ADMIN_PASSWORD"]
        sccbot_db_host =os.environ["SCCBOT_DB_HOST"]
        sccbot_db_name = os.environ["SCCBOT_DB_NAME"]

        db = MySQLDatabase(host=sccbot_db_host, port=3306, user=sccbot_admin_user,passwd=sccbot_admin_password, database=sccbot_db_name)


        class User(peewee.Model):
            steem_name = peewee.CharField()
            discord_id = peewee.SmallIntegerField()

            class Meta:
                database = db


        db.connect()
        db.create_tables([User])

if __name__ == '__main__':
    unittest.main()