
import data

class MessageEvaluator():

    def __init__(self, settings):
        self.settings = settings
    
    def check_message(self, message):

        #print(message.channel)
        #print(message.channel.category)

        # Example of valid message.content: https://steemit.com/spanish/@cervantes/comunidad-de-cervantes-podcasts-educativos


        result = {"content": message.content, 
                  "channel_id": message.channel.id, 
                  "category_id": message.channel.category_id,
                  "check_status": "OK",
                  "check_message": ""}
       
        if (message.channel.category_id not in self.settings.get_category_ids()):
           result["check_status"] = "KO"
           result["check_message"] = "This channel do not belong to a valid category"
           return(result)

        if(message.content[0:20] != "https://steemit.com/"):
            result["check_status"] = "KO"
            result["check_message"] = "Message is not a valid steemit.com url"
            return(result)


        return(result)


class PostEvaluator():

    def __init__(self):
        pass
    
    def evaluate_post(self, post):
        pass


    