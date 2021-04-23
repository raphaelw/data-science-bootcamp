'''
1. Extract tweets from MongoDB
    - Connect to databse
    - Extract data
2. Transform:
    - Possibly text cleaning stuff
    - Senstiment analysis
    - Possibly changing types
3. Load: 
    - Connect to postgres
    - Insert transformed data into postgres
'''

## put these into your requirement.txt file
import pymongo
import sqlalchemy
import psycopg2

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import time
import logging

# Further Idea: Listen for changes on mongo replica https://stackoverflow.com/a/59251942

truncated = lambda s,lim: s[:lim] if len(s) > lim else s

def extract(mongo_collection, seen_object_ids):
    ''' Extracts tweets from Mongo DB '''
    # https://stackoverflow.com/a/4425163
    extracted_tweets = []

    tweet_cursor = mongo_collection.find().sort('_id',-1).limit(50).sort('_id',1)
    for tweet in tweet_cursor:
        object_id = tweet['_id']
        if not object_id in seen_object_ids:
            logging.info('ObjectID {} text: {}'.format(str(object_id), repr(truncated(tweet['text'],60))))
            seen_object_ids.add(object_id)
            extracted_tweets.append(tweet)
    
    return extracted_tweets

def transform(extracted_tweets, vader_analyzer):
    '''Performs your desired transformations: sentiment analysis, text cleaning, emoji managmenet '''
    transformed_tweets = []
    for tweet in extracted_tweets:
        tweet['sentiment'] = vader_analyzer.polarity_scores(tweet['text'])['compound']
        transformed_tweets.append(tweet)

    return transformed_tweets

def load(transformed_tweets, postgres_engine, postgres_table):
    '''Loads transformed tweets and analysis into postgres'''
    for tweet in transformed_tweets:
        ins = postgres_table.insert().values(user = tweet['username']
                                            , text = tweet['text']
                                            , timestamp = tweet['timestamp_received']
                                            , sentiment = tweet['sentiment'])
        postgres_engine.execute(ins)
        logging.info('Written to RDMS, Tweet from ' + str(tweet['username']))

def connect_to_mongo():
    mongo_client = pymongo.MongoClient(host='mongodb'
                                      ,port=27017
                                      ,username='user'
                                      ,password='pass')
    return mongo_client

def connect_to_postgres():
    engine = sqlalchemy.create_engine('postgresql://postgres:postgres@postgres/postgres', echo=False)
    create_query = """
        CREATE TABLE IF NOT EXISTS tweets (
            "id"        SERIAL PRIMARY KEY,
            "user"      VARCHAR(100),
            "text"      VARCHAR(500),
            "timestamp" NUMERIC,
            "sentiment" REAL
        );
        """
    engine.execute(create_query)
    return engine

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # mongo db
    mongo_client = connect_to_mongo()
    mongo_collection = mongo_client.twitter.tweets

    # postgres
    pg_engine = connect_to_postgres()
    # https://docs.sqlalchemy.org/en/14/core/reflection.html#reflecting-all-tables-at-once
    pg_metadata = sqlalchemy.MetaData()
    pg_metadata.reflect(bind=pg_engine)
    pg_table = pg_metadata.tables['tweets']

    # sentiment model
    vader_analyzer = SentimentIntensityAnalyzer()

    # etl
    seen_object_ids = set()
    while True:
        extracted_tweets = extract(mongo_collection, seen_object_ids)
        transformed_tweets = transform(extracted_tweets, vader_analyzer)
        load(transformed_tweets, pg_engine, pg_table)

        time.sleep(5)