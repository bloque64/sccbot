__author__ = "http://steemit.com/@cervantes"
__copyright__ = "Copyright (C) 2018 steem's @cervantes"
__license__ = "MIT"
__version__ = "1.0"

import data
from register import UserRegisterer
from register import UserExistingError
from register import UserRepeatedError
import result
from result import Result


class MessageEvaluator():

    def __init__(self, settings):

        self.settings = settings
        self.user_registerer = UserRegisterer(settings)
        self.bot_name = settings.bot_name
        self.result = Result()
    
    def check_message(self, message):



        self.result.content = message.content
        self.result.channel_id = message.channel.id
        self.result.category_id = message.channel.category_id
        self.result.curator_discord_id = message.author.id
        self.result.steem_account = None
        self.result.status = result.STATUS_OK
        self.result.message1p = ""
        self.result.message3p = ""
        self.result.exception = None


        try:

            reg_user = self.user_registerer.get_user_by_discord_id(message.author.id)
            self.result.user = reg_user

        except UserExistingError as e:

            self.result.status = result.STATUS_KO
            self.result.message3p= "User not registered: %s (%s)" % (message.author.name, message.author.id)
            self.result.message1p = "Your user (**%s**, %s) is not registered to use **%s**, please use the command **!reg new** to register as a new user" % (message.author.name, message.author.id, self.bot_name)
            self.result.exception = e

            return(self.result)

        except UserRepeatedError as e:

            self.result.status = result.STATUS_KO
            self.result.message3p = "Duplicated User: %s (%s)" % (message.author.name, message.author.id)
            self.result.message1p = "Your user is duplicated, please contact administrator: %s (%s)" % (message.author.name, message.author.id)
            self.result.exception = e
            return(self.result)

        except Exception as e:
            self.result.status = result.STATUS_KO
            self.result.message3p = "Trying to get a user resulted in an unknown exception: %s" % str(e)
            self.result.message1p = "Trying to get a user resulted in an unknown exception: %s" % str(e)
            self.result.exception = e
            return(self.result)

               
        if (message.channel.category_id not in self.settings.get_category_ids()):
           self.result.status = result.STATUS_KO
           self.result.message3p = "Message check failed: This channel do not belong to a valid category"
           self.result.message1p = self.result.message3p
           return(self.result)

        elif(message.content[0:20] != "https://steemit.com/"):
            self.result.status = result.STATUS_KO
            self.result.message3p = "Message check failed: Message is not a valid steemit.com url"
            self.result.message1p = "Message check failed: Message is not a valid steemit.com url"
            return(self.result)


        return(self.result)


class PostEvaluator():

    def __init__(self):
        pass
    
    def evaluate_post(self, post):
        pass


    