from confluent_kafka import Consumer, KafkaError
import json
from collections import defaultdict
from pymongo import MongoClient
from itertools import combinations

# Function to parse JSON message
def parse_message(msg_value):
    try:
        return json.loads(msg_value.decode('utf-8'))
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return None

# Function to save frequent itemsets to MongoDB
def save_to_mongodb(frequent_itemsets):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['frequent_itemsets']
    collection = db['pcy_results']
    collection.insert_many(frequent_itemsets)

# PCY Algorithm
def pcy(transactions, min_support, hash_size, bitmap_size):
    # Step 1: Counting
    counts = defaultdict(int)
    for transaction in transactions:
        for pair in combinations(transaction, 2):
            hash_index = hash(pair) % hash_size
            counts[hash_index] += 1

    # Step 2: Bitmap Filtering
    bitmap = [count >= min_support for count in counts.values()]

    # Step 3: Counting for Frequent Pairs
    freq_itemsets = set()
    for transaction in transactions:
        for pair in combinations(transaction, 2):
            hash_index = hash(pair) % hash_size
            if bitmap[hash_index]:
                freq_itemsets.add(pair)

    return freq_itemsets

def main():
    # Kafka consumer configuration
    kafka_conf = {
        'bootstrap.servers': 'localhost:9092',  # Change this to your Kafka broker
        'group.id': 'pcy_consumer_group',
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
                    transactions.append(set(data))
    except KeyboardInterrupt:
        pass
    finally:
        # Close consumer
        consumer.close()

    # Run PCY algorithm
    min_support = 0.2  # Adjust as needed
    hash_size = 1000  # Adjust as needed
    bitmap_size = 1000  # Adjust as needed
    frequent_itemsets = pcy(transactions, min_support, hash_size, bitmap_size)

    # Save frequent itemsets to MongoDB
    save_to_mongodb(frequent_itemsets)
    print("Frequent Itemsets saved to MongoDB.")

if __name__ == "__main__":
    main()