from confluent_kafka import Producer
import json

def read_json_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_data(producer, topic, data):
    for item in data:
        # Serialize the dictionary to JSON string
        json_string = json.dumps(item)
        # Produce the message to Kafka
        producer.produce(topic, json_string.encode('utf-8'), callback=delivery_report)
        # Wait for the message to be sent
        producer.poll(0.5)

def main():
    # Kafka broker configuration
    kafka_conf = {
        'bootstrap.servers': 'localhost:9092',  # Change this to your Kafka broker
        # Other configurations like security, etc. can be added here
    }

    # Kafka topic to produce to
    topic = 'alizaib'

    # JSON data file
    filename = '/home/ahsan/kafka/Preprocessed_Amazon.json'
    # Read JSON data from file
    data = read_json_data(filename)

    # Create Kafka Producer
    producer = Producer(kafka_conf)

    # Produce data to Kafka
    produce_data(producer, topic, data)

    # Flush producer to ensure all messages are delivered
    producer.flush()

if __name__ == "__main__":
    main()

    