import json
import os

class Settings():

    def __init__(self):

        self.discord_token = 'NDM0Mzc0NDEwNzcwNTc5NDYy.DbJgIQ.dggA7YLdly30MeSRto-8Z0gbyAE'

        self.channels = [{"name":"ciencia", "category":"PROMOCION", "id":0, "deletable":False},
           {"name":"gente_nueva", "category":"PROMOCION", "id":0, "deletable":True},
           {"name":"ciencia", "category":"POSTS_CURABLES", "id":0, "deletable":True},
           {"name":"gente_nueva", "category":"POSTS_CURABLES", "id":0, "deletable":True}]


        self.categories = [{"name":"PROMOCION", "id":0, "deletable":False}, {"name": "POSTS_CURABLES", "id":0, "deletable":True}]

        #self.channels = []
        #self.categories = []


        self.settings_file = "./sccbot.json"


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

    def get_json(self):
        
        d = dict()

        d["discord_token"] = self.discord_token
        d["channels"] = self.channels
        d["categories"] = self.categories

        return(json.dumps(d,indent=4, sort_keys=True))

    def save(self):

        print("Saving settings to file %s " % self.settings_file)
        file = open(self.settings_file,"w")
        file.write(self.get_json())    
        file.close() 

    def load(self):
        print("Loading settings from file: %s" % self.settings_file)
        file = open(self.settings_file,"r")
        st = json.load(file)

        try: 
            self.discord_token = os.environ['SCCBOT_TOKEN']
            self.channels = st["channels"]


        except KeyError as e:
            print('I got a KeyError - reason "%s"' % str(e))
            raise

    def __repr__(self):
        json = self.get_json()
        return(json)



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

if __name__ == "__main__":

    #test_set_channel_id()
    test_print_token_env()

