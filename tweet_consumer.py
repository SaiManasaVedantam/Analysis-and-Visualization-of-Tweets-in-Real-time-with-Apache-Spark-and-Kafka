# This module works as a Consumer of the data produced to the kafka topic
# Then, processes data to be able to store with ElasticSearch index in a format usable by Kibana

# Import all necessary packages
import json, time, sys, re
from textblob import TextBlob
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

# Import NLP related packages
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.tokenize import word_tokenize


# Preprocess obtained data
def preprocess_tweets(tweet_input):
    format_mentions = ' '.join(re.sub("(@[A-Za-z0-9_.]+)|([^A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet_input.lower()).split())
    format_rts = ' '.join(subword for subword in format_mentions.split() if subword!= 'rt')
    word_tokens = word_tokenize(format_rts)
    filtered_tokens = [w for w in word_tokens if not w in stop_words]
    processed_tweet = " ".join(filtered_tokens)
    return processed_tweet


# Creates ElasticSearch instance
elastic_search = Elasticsearch([{ 'host': 'localhost', 'port': 9200, 'use_ssl': False, 'ssl_verify': False,}], timeout=30, max_retries=10)

# Sets up Kafka consumer
consumer = KafkaConsumer('tweepy-ukraine-output', auto_offset_reset='earliest')


# Helper variable to create ElasticSearch indexing
idx, iterator = 1, 1
    
# To get continuous data
while True:

    # Loops through the data, processes it & adds to the index
    for data in consumer:

        # Sleeps after every 10 tweets
        if iterator % 10 == 0:
            print("\n", "Sleep...")
            time.sleep(10)
            
        value_associated_with_data = json.loads(data.value)

        # Obtains sentiment using polarity : neutral by default
        tweet_sentiment = 'NEUTRAL'

        if value_associated_with_data["lang"] == 'en':
            preprocessed_tweets = preprocess_tweets(value_associated_with_data["text"])
            tweet_text = TextBlob(preprocessed_tweets)
            tweet_polarity = tweet_text.sentiment.polarity

            # Assign sentiment to the tweet
            if tweet_polarity > 0:
                tweet_sentiment = 'POSITIVE'

            elif tweet_polarity < 0:
                tweet_sentiment = 'NEGATIVE'
                     
            # Processes & adds results to elastic_search
            current_data = {'date' : value_associated_with_data['created_at'],
                            'author' : value_associated_with_data['user']['screen_name'],
                            'tweet_text' : value_associated_with_data['text'],
                            'sentiment' : tweet_sentiment,
                            'processed_tweet' : preprocess_tweets(value_associated_with_data['text'])
                        }

            print(current_data)

            elastic_search.index(index='ukraine_index', id=idx, body=current_data)
            idx += 1
            iterator += 1

            # Tracks results
            print("*****  "+str(tweet_sentiment)+"  ******", "\n", str(tweet_text), "\n\n")
               
