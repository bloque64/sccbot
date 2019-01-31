__author__ = "http://steemit.com/@cervantes"
__copyright__ = "Copyright (C) 2018 steem's @cervantes"
__license__ = "MIT"
__version__ = "1.0"

from data import Post
import queue 
from evaluator import PostEvaluator
from settings import Settings
import data
from data import User
from register import UserRegisterer
from result import Result
import result
import register



class Manager():
    '''Class to manage the curation tasks'''

    def __init__(self, settings):

        self.max_nr_of_curated_posts = 50
        self.max_nr_of_good_posts = 25
        self.max_nr_of_excelent_post = 10
        self.max_nr_of_master_post =5

        self.promoted_round_duration = 12 # in Hours
        self.curable_round_duration = 6
        self.good_round_duration = 3
        self.excelent_round_duration = 2
        self.master_round_duration = 1

        self.settings = settings
        self.registered_users = None
        self.curators_level_1 = None
        self.curators_level_2 = None
        self.curators_level_2 = None


        self.promoted_posts = queue.Queue()
        self.curable_posts = queue.Queue()
        self.good_posts = queue.Queue()
        self.master_posts = queue.Queue()
        self.excelent_posts = queue.Queue()

        self.evaluator = PostEvaluator()
        self.user_registerer = UserRegisterer(settings)

        self.settings = settings


    # Return True if the user is socially connected
    # Algorithm to be defind.
    def is_socially_connected(self, user, author):
        return(False)

    def promote_post(self, user = None, url = None):

        r = Result()
        r.steem_account = user.steem_account
        r.curator_discord_id = user.discord_member_id

        if(not self.user_registerer.is_registered(user.discord_member_id)):

            r.message3p = "Could not promote post. User not registered: %s" % user
            r.message1p = "Could not promote post. User not registered: %s" % user
            r.status = result.STATUS_KO

        elif (user.steem_name == post.author):
            r.messsage3p = "Could not promote post. User can not be the same as author"
            r.messsage1p = "Could not promote post. User can not be the same as author"
            r.status = result.STATUS_KO
        elif (self.is_socially_connected(user.steem_name, post.author)):
            r.message3p = "Could not promote post. User and author are socially connected"
            r.message1p = r.message3p
            r.status = result.STATUS_KO

        else:

            session = settings.sa_session

            post = data.Post()
            post.fulllink
            session.add(post)
            session.commit()

            r.message3p = "Post successfully promoted: %s" % url
            r.message1p = r.message3p
            r.status = result.STATUS_OK

        return(r)


    def evaluate_promoted_posts(self):
        pass

    def curate_post(self, user, post, message_evaluator_result):
        """Do X """
        pass

    def get_curators(self):
        return(self.settings.sa_session.query(User).filter(User.role==data.USER_ROLE_CURATOR, User.verification_status == data.VS_ACCEPTED).all())

class Post():

    def __init__(self):
        
        self.post = Post()
    
    def evaluate_message(self, message):
        
        print(message.channel)
        print(message.channel.category)



if __name__ == "__main__":
    
    sa_session = data.init()
    settings = Settings(sa_session)
    my_curator = Manager(settings)
