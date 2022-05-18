# This module uses twitter API & scrapes tweets with given tag(s)
# Then, it saves the scraped data to the Kafka topic via the Kafka Producer

# Import all necessary packages
import time
import tweepy 
from tweepy import Stream
from tweepy import OAuthHandler
from kafka import KafkaProducer
from tweepy.streaming import StreamListener


# Set keys to access the twitter API
consumer_api_key = "Use your key here"
consumer_api_key_secret = "Use your key here"
access_token = "Use your key here"
access_secret = "Use your key here"


# Defines the Stream Listener class to update data as & when found/scraped
class MyStreamListener(StreamListener):

    # Event to be processed as & when we see data
    def on_data(self, data):
        producer.send('tweepy-ukraine-output', str.encode(data))
        return True

    # Event to handle errors
    def on_error(self, status):
        return True

# Creates Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(3, 0, 1))
tweet_counter = 1

# To get continuous data
while True:

    # Creates listener objct
    listener_object = MyStreamListener()

    # Handles authorization
    authorization = OAuthHandler(consumer_api_key, consumer_api_key_secret)
    authorization.set_access_token(access_token, access_secret)

    # Obtains streaming data & filters it
    twitter_stream_result = Stream(authorization, listener_object)
    twitter_stream_result.filter(track = ['#ukraine'])

    # Check counts
    tweet_counter += 1 
    if tweet_counter % 10 == 0:
        print("\nSleep...")
        time.sleep(30)
        tweet_counter = 0
