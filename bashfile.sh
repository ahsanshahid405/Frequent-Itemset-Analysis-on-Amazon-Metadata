#!/bin/bash

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Start Zookeeper
echo "Starting Zookeeper..."
zookeeper-server-start.sh -daemon path/to/zookeeper.properties

# Start Kafka broker
echo "Starting Kafka broker..."
kafka-server-start.sh -daemon path/to/server.properties

# Create Kafka topic
echo "Creating Kafka topic..."
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic your_topic_name

# Start Kafka Connect (if needed)
if command_exists "connect-distributed.sh"; then
    echo "Starting Kafka Connect..."
    connect-distributed.sh path/to/connect-distributed.properties &
elif command_exists "connect-standalone.sh"; then
    echo "Starting Kafka Connect..."
    connect-standalone.sh path/to/connect-standalone.properties &
else
    echo "Kafka Connect not found. Skipping..."
fi

# Start producerconsumerfpgrowth.py
python producer.py &

# Start Apriori consumer
echo "Starting Apriori consumer..."
python consumeraapriori.py &

# Start PCY consumer
echo "Starting PCY consumer..."
python consumerpcy.py &

# Start FP-Growth consumer
echo "Starting FP-Growth consumer..."
python consumerfpgrowth.py &

# Wait for a key press to stop consumers and clean up
echo "Press any key to stop consumers and clean up..."
read -n 1 -s

# Stop consumers
echo "Stopping consumers..."
pkill -f "python producer.py"
pkill -f "python consumeraapriori.py"
pkill -f "python consumerpcy.py"
pkill -f "python consumerfpgrowth.py"

# Stop Kafka Connect (if needed)
echo "Stopping Kafka Connect..."
pkill -f "connect-distributed.sh"
pkill -f "connect-standalone.sh"

# Stop Kafka broker
echo "Stopping Kafka broker..."
kafka-server-stop.sh

# Stop Zookeeper
echo "Stopping Zookeeper..."
zookeeper-server-stop.sh

echo "Cleanup completed."