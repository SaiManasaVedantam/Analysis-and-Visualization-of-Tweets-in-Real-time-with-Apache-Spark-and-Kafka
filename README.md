# Analysis-and-Visualization-of-Tweets-in-Real-time-with-Apache-Spark-and-Kafka  (May 2022)

This project implements an end-to-end pipeline that:
- Read tweets in real-time
- Process & store tweets in a Kafka topic via Kafka producer
- Perform sentiment analysis on tweets by reading them from Kafka topic via Kafka consumer
- Create and store tweets & the sentiments associated with them using Elastic Search index
- Perform real-time visualization using Kibana with Elastic search
- Apply K-means clustering on the indexed data & view convergence

## Software & Version Information:
- Python --> 3.8
- Tweepy --> 3.10.0
- Kibana --> 7.15.2
- Kafka --> 2.13-3.1.0
- Elasticsearch --> 7.15.2

## Execution Instructions:
1. Start Kafka Zookeeper
- bin/zookeeper-server-start.sh config/zookeeper.properties

2. Start Kafka Broker service
- bin/kafka-server-start.sh config/server.properties

3. Start Elastic search
- ./bin/elasticsearch

4. Create a Kafka topic
bin/kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 1 \
    --topic tweepy-ukraine-output

5. Run producer code
python tweet_producer.py

6. Run consumer code
python tweet_consumer.py

7. Run K-means.ipynb

8. Visualization with kibana
- Check if elasticsearch & kibana are up & running
- Stack Management --> Index Patterns --> Create Index Pattern --> Link index with it
- Dashboard --> Create New Dashboard --> Create Visualization
- Select graph, Slice by & Size by values 

## Visualization with Kibana
The following are few sample outputs obtained in real-time using Kibana. There can be several other visualization techniques used with Kibana.
<img width="920" alt="Screen Shot 2022-05-17 at 7 52 31 PM" src="https://user-images.githubusercontent.com/28973352/168935230-47e7b2a9-3387-4a49-879b-c8db42ed9f59.png">

## Results obtained by K-means clustering with k=3
