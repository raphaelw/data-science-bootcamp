import config
import logging
from time import time
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import pymongo

def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called config.py
       which stores the 4 required authentication tokens:

       1. API_KEY
       2. API_SECRET
       3. ACCESS_TOKEN
       4. ACCESS_TOKEN_SECRET

    See course material for instructions on getting your own Twitter credentials.
    """
    auth = OAuthHandler(config.API_KEY, config.API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class MaxTweetsListener(StreamListener):

    def __init__(self, max_tweets, *args, **kwargs):
        # initialize the StreamListener
        super().__init__(*args, **kwargs)
        # set the instance attributes
        self.max_tweets = max_tweets
        self.counter = 0

        # database
        self.client = pymongo.MongoClient(host='mongodb'
                                         ,port=27017
                                         ,username='user'
                                         ,password='pass')

        database_name = 'twitter'
        self.db = self.client[database_name]
        
        collection_name = 'tweets'
        self.db_collection = self.db[collection_name]

    def on_connect(self):
        logging.info('connected. listening for incoming tweets')


    def on_status(self, status):
        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""
        
        # increase the counter
        self.counter += 1        

        tweet = {
            'text': status.text,
            'username': status.user.screen_name,
            'followers_count': status.user.followers_count,
            'timestamp_received': int(time())
        }

        self.db_collection.insert_one(tweet)
        
        # log
        truncated = lambda s,lim: s[:lim] if len(s) > lim else s
        truncated_tweet = repr( truncated(tweet["text"],60) )
        logging.info(f'New tweet arrived: {truncated_tweet}')
        
        # check if we have enough tweets collected
        if self.max_tweets == self.counter:
            # reset the counter
            self.counter=0
            # return False to stop the listener
            return False


    def on_error(self, status):
        if status == 420:
            logging.info(f'Rate limit applies. Stop the stream.')
            return False


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    auth = authenticate()
    listener = MaxTweetsListener(max_tweets=100)
    stream = Stream(auth, listener)
    stream.filter(track=['jazz'], languages=['en'], is_async=False)