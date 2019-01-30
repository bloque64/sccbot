import sys
import pymysql.cursors
sys.path.append('..')
from  settings import Settings

local_settings = Settings(None, "../settings/")
local_settings.load()
local_settings.print_database_info()


# Connect to the database
connection = pymysql.connect(host=local_settings.sccbot_db_host,
                             user=local_settings.sccbot_admin_user,
                             password=local_settings.sccbot_admin_password,
                             db=local_settings.sccbot_db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

