


import mysql.connector
import sys
sys.path.append('..')
from  settings import Settings

local_settings = Settings(None, "../settings/")
local_settings.load()



cnx = mysql.connector.connect(user=local_settings.sccbot_admin_user, password=local_settings.sccbot_admin_password,
                              host=local_settings.sccbot_admin_user,
                              database=local_settings.sccbot_db_name)
cnx.close()