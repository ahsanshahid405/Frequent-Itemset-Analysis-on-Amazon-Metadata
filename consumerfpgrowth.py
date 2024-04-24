from confluent_kafka import Consumer, KafkaError
import json
from pymongo import MongoClient
from pyfpgrowth import find_frequent_patterns

# Function to parse JSON message
def parse_message(msg_value):
    try:
        return json.loads(msg_value.decode('utf-8'))
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return None

# Function to save frequent itemsets to MongoDB
def save_to_mongodb(frequent_itemsets, algorithm):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['frequent_itemsets']
    collection = db[f'{algorithm}_results']
    collection.insert_many([{'itemset': list(itemset)} for itemset in frequent_itemsets])

def main():
    # Kafka consumer configuration
    kafka_conf = {
        'bootstrap.servers': 'localhost:9092',  # Change this to your Kafka broker
        'group.id': 'fpgrowth_consumer_group',
        'auto.offset.reset': 'earliest'
    }

    # Kafka topic to consume from
    topic = 'your_topic_name'

    # Create Kafka Consumer
    consumer = Consumer(kafka_conf)
    consumer.subscribe([topic])

    transactions = []

    # Consume messages
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            else:
                # Parse message
                data = parse_message(msg.value())
                if data:
                    # Assuming data is a list of items in each transaction
                    transactions.append(data)
    except KeyboardInterrupt:
        pass
    finally:
        # Close consumer
        consumer.close()

    # Run FP-Growth algorithm
    min_support = 0.2  # Adjust as needed
    frequent_itemsets = find_frequent_patterns(transactions, min_support * len(transactions))

    # Save frequent itemsets to MongoDB
    save_to_mongodb(frequent_itemsets, 'fpgrowth')
    print("Frequent Itemsets saved to MongoDB.")
    
if __name__ == "__main__":
    main()