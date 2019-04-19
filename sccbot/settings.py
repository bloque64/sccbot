__author__ = "http://steemit.com/@cervantes"
__copyright__ = "Copyright (C) 2018 steem's @cervantes"
__license__ = "MIT"
__version__ = "1.0"


import json
import os
from data import User
import data

class Settings():

    def __init__(self, sa_session, path):

        self.sa_session = sa_session

        self.discord_token = os.environ["SCCBOT_TOKEN"]

        self.sccbot_admin_user = os.environ["SCCBOT_ADMIN_USER"]
        self.sccbot_admin_password = os.environ["SCCBOT_ADMIN_PASSWORD"]
        self.sccbot_db_host = os.environ["SCCBOT_DB_HOST"]
        self.sccbot_db_name = os.environ["SCCBOT_DB_NAME"]


        self.channels = [{"name":"ciencia", "category":"PROMOCION", "id":0, "deletable":False},
           {"name":"gente_nueva", "category":"PROMOCION", "id":0, "deletable":True},
           {"name":"ciencia", "category":"POSTS_CURABLES", "id":0, "deletable":True},
           {"name":"gente_nueva", "category":"POSTS_CURABLES", "id":0, "deletable":True}]


        self.categories = [{"name":"PROMOCION", "id":0, "deletable":False}, {"name": "POSTS_CURABLES", "id":0, "deletable":True}]

        #self.channels = []
        #self.categories = []

        self.registered_users = None

        self.bot_name = "sccbot"
        self.registrant_account = ""
        self.default_users = []
        self.default_users.append(User())


        self.settings_file = path + "sccbot.json"


    def get_rpc_nodes_list(self):
        l = []
        for e in self.steem_rpc_nodes:
            l.append(e["host"])

        return(l)

    def set_category_id(self, name, id):
        for c in self.categories:
            if(c["name"]==name):
                c["id"] = id
                continue

    def set_channel_id(self, channel_name=None, category_name=None, id=None):

        found = False

        for c in self.channels:
            if(c["name"]==channel_name and c["category"]==category_name):
                c["id"] = id
                found = True
                continue

        if not found:
            raise Exception("Could not found channel %s in category %s .." % (channel_name, category_name))

    
    def is_channel_deletable(self, id):
        for c in self.channels:
            if(c["id"]==id) and c["deletable"]==True:
                return True

        return(False)


    def get_category_by_channel_id(self, channel_id):

        result_category = None

        for c in self.channels:
            if c["id"] == channel_id:
                result_category = c["category"]

        return(result_category)                

    def get_deletable_channels_ids(self):

        output = [key["id"] for key in self.channels if key["deletable"]==True]
        return(output)


    def get_category_ids(self):

        output = [key["id"] for key in self.categories]
        return(output)


    def get_categories(self):
        return(self.categories)

    def get_channels(self):
        return(self.channels)


    def get_channels_by_cat(self, category_name):
        channels = list()
        for c in self.channels:
            if(c["category"]==category_name):
                channels.append(c)

        return(channels)

    def get_channels_level_0(self):
        channels = list()
        for c in self.channels:
            if(c["category"]==""):
                channels.append(c)

        return(channels)

    def print_database_info(self):

        print("user: %s" % self.sccbot_admin_user)
        print("pass: %s" % self.sccbot_admin_password)
        print("host: %s" % self.sccbot_db_host)
        print("db: %s" % self.sccbot_db_name)

    def get_json(self):
        
        d = dict()

        d["registrant_account"] = self.registrant_account
        d["steem_rpc_nodes"] = self.steem_rpc_nodes
        d["discord_token"] = self.discord_token
        d["channels"] = self.channels
        d["categories"] = self.categories
        d["default_users"] = self.default_users

        return(json.dumps(d,indent=4, sort_keys=True))

    def save(self):

        print("Saving settings to file %s " % self.settings_file)
        file = open(self.settings_file,"w")
        file.write(self.get_json())    
        file.close() 

    def load(self, settings_file=None):

        if settings_file != None:
            self.settings_file = settings_file

        print("Loading settings from file: %s" % self.settings_file)
        file = open(self.settings_file,"r")
        st = json.load(file)

        try: 

            self.registrant_account = st["registrant_account"]
            self.steem_rpc_nodes = st["steem_rpc_nodes"]
            self.channels = st["channels"]
            self.categories = st["categories"]

            file.close()


        except KeyError as e:
            print('I got a KeyError - reason "%s"' % str(e))
            raise

        except Exception as e:
            raise


    def get_log_channel_id(self):
        for c in self.channels:
            if c["name"] == "log" and c["category"]=="":
                return(c["id"])    
        
        raise Exception("Log channel not found")


    def get_admin_channel_id(self):
        for c in self.channels:
            if c["name"] == "admin" and c["category"]=="":
                return(c["id"])    
        
        raise Exception("Log channel not found")


    def __repr__(self):
        json = self.get_json()
        return(json)


    def is_user_registered(self, user):
        if user in self.registered_users:
            return(True)
        else:
            return(False)



def test_set_channel_id():

    my_settings = Settings()
    #my_settings.save()
    my_settings.load()
    #print(my_settings.get_channels_by_cat("PROMOCION"))
    my_settings.set_channel_id(channel_name="ciencia", category_name="PROMOCION", id=123455)
    print(my_settings)

    

def test_is_channel_deletable():

    my_settings = Settings()
    #my_settings.save()
    my_settings.load()
    my_settings.is_channel_deletable()


def test_print_token_env():
    #print(os.environ)
    print("Token: %s" % os.environ['SCCBOT_TOKEN'])


def test_print_sccbot_user_env():
    print("SSCBOT_ADMIN_USER: %s" % os.environ['SSCBOT_ADMIN_USER'])
    print("SSCBOT_ADMIN_PASSWORD: %s" % os.environ['SSCBOT_ADMIN_PASSWORD'])


def test_get_category_ids():
    sa_session = data.init()
    my_settings = Settings(sa_session)
    my_settings.load()
    print(my_settings.get_category_ids())

def test_get_deletable_channels_ids():
    sa_session = data.init()
    my_settings = Settings(sa_session)
    my_settings.load()
    print(my_settings.get_deletable_channels_ids())

if __name__ == "__main__":

    #test_set_channel_id()
    #test_print_token_env()
    #test_get_category_ids()
    #test_get_deletable_channels_ids()

    sa_session = data.return_session()
    my_settings = Settings(sa_session,"../settings/")
    my_settings.load()

