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
import vaderSentiment
import sqlalchemy
import psycopg2

import time
import logging

# Further Idea: Listen for changes on mongo replica https://stackoverflow.com/a/59251942

def extract(mongo_collection, seen_object_ids):
    ''' Extracts tweets from Mongo DB '''
    # https://stackoverflow.com/a/4425163
    extracted_tweets = []

    tweet_cursor = mongo_collection.find().sort('_id',-1).limit(50).sort('_id',1)
    for tweet in tweet_cursor:
        object_id = tweet['_id']
        logging.info('ObjectID ' + str(object_id) + ' text: ' + repr(tweet['text']))
        if not object_id in seen_object_ids:
            seen_object_ids.add(object_id)
            extracted_tweets.append(tweet)
    
    return extracted_tweets

def transform(extracted_tweets):
    '''Performs your desired transformations: sentiment analysis, text cleaning, emoji managmenet '''
    transformed_tweets = []
    for tweet in extracted_tweets:
        # TODO
        tweet['sentiment'] = 0.5
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
    engine = sqlalchemy.create_engine('postgresql://postgres:postgres@postgres/postgres', echo=True)
    create_query = """
        CREATE TABLE IF NOT EXISTS tweets (
            "id"        SERIAL PRIMARY KEY,
            "user"      VARCHAR(100),
            "text"      VARCHAR(500),
            "timestamp" NUMERIC,
            "sentiment" REAL
        );
        """
    result = engine.execute(create_query)
    logging.info(result)
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
    logging.info(pg_metadata.tables)
    pg_table = pg_metadata.tables['tweets']

    # etl
    seen_object_ids = set()
    while True:
        extracted_tweets = extract(mongo_collection, seen_object_ids)
        transformed_tweets = transform(extracted_tweets)
        load(transformed_tweets, pg_engine, pg_table)

        time.sleep(30)
    