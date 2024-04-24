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
def save_to_mongodb(frequent_itemsets, algorithm):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['frequent_itemsets']
    collection = db[f'{algorithm}_results']
    collection.insert_many([{'itemset': list(itemset)} for itemset in frequent_itemsets])

# Apriori Algorithm
def apriori(transactions, min_support):
    itemsets = [{item} for transaction in transactions for item in transaction]
    frequent_itemsets = []

    num_transactions = len(transactions)
    while itemsets:
        candidate_itemsets = generate_candidates(itemsets)
        freq_itemsets = filter_candidates(transactions, candidate_itemsets, min_support, num_transactions)
        frequent_itemsets.extend(freq_itemsets)
        itemsets = freq_itemsets

    return frequent_itemsets

# Function to generate candidate itemsets
def generate_candidates(prev_itemsets):
    candidates = set()
    for itemset1 in prev_itemsets:
        for itemset2 in prev_itemsets:
            union_set = itemset1.union(itemset2)
            if len(union_set) == len(itemset1) + 1:
                candidates.add(union_set)
    return candidates

# Function to filter candidate itemsets based on support
def filter_candidates(transactions, candidates, min_support, num_transactions):
    freq_itemsets = set()
    item_counts = defaultdict(int)
    for transaction in transactions:
        for candidate in candidates:
            if candidate.issubset(transaction):
                item_counts[candidate] += 1

    for itemset, count in item_counts.items():
        support = count / num_transactions
        if support >= min_support:
            freq_itemsets.add(itemset)

    return freq_itemsets

def main():
    # Kafka consumer configuration
    kafka_conf = {
        'bootstrap.servers': 'localhost:9092',  # Change this to your Kafka broker
        'group.id': 'apriori_consumer_group',
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

    # Run Apriori algorithm
    min_support = 0.2  # Adjust as needed
    frequent_itemsets = apriori(transactions, min_support)

    # Save frequent itemsets to MongoDB
    save_to_mongodb(frequent_itemsets, 'apriori')
    print("Frequent Itemsets saved to MongoDB.")
if __name__ == "__main__":
    main()