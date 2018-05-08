from data import Post
import queue 
from evaluator import PostEvaluator


class Curator():

    def __init__(self):

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


    # Return True if the user is socially connected
    # Algorithm to be defind.
    def is_socially_connected(self, user, author):
        return(False)

    def promote_post(self, user, post):

        if(user not in self.registered_users):
            msg = "Could not promote post. User not registered: %s" % user   
        elif (user.steem_name == post.author):
            msg = "Could not promote post. User can not be the same as author"
        elif (is_socially_connected(user.steem_name, post.author)):
            msg = "Could not promote post. User and author are socially connected"

        



class Post():

    def __init__(self):
        
        self.post = Post()
    
    def evaluate_message(self, message):
        
        print(message.channel)
        print(message.channel.category)



if __name__ == "__main__":

    my_curator = Curator()
