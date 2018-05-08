from data import Post
import queue 


class Curator():

   def __init__(self):

        self.promoted_posts = queue.Queue()
        self.good_posts = queue.Queue()
        self.master_posts = queue.Queue()
        self.excelent_posts = queue.Queue()


class Post():

    def __init__(self):
        
        self.post = Post()
    
    def evaluate_message(self, message):
        
        print(message.channel)
        print(message.channel.category)



if __name__ == "__main__":

    my_curator = Curator()
