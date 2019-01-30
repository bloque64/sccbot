__author__ = "http://steemit.com/@cervantes"
__copyright__ = "Copyright (C) 2018 steem's @cervantes"
__license__ = "MIT"
__version__ = "1.0"

STATUS_KO = 0
STATUS_OK = 1

class Result():

    def __init__(self):

        self.content = None
        self.channel_id = None
        self.category_id = None
        self.curator_discord_id = None
        self.steem_account = None
        self.message1p = ""
        self.message3p = ""
        self.user = None
        self.status = STATUS_KO
        self.exception = None

    def __bool__(self):

        if(self.status == STATUS_KO):
            return(False)
        else:
            return(True)