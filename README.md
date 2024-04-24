# Frequent-Itemset-Analysis-on-Amazon-Metadata

Our code begins by importing the JSON module which provides function for working with JSON data.

Preprocessing Function: 
preprocess_data(data): 
This function takes a list of records (data) as input and returns a preprocessed version of the data.
Inside the function:
It initializes an empty list preprocessed_data to store the preprocessed records.
It iterates over each record in the input data.
For each record, it creates a new dictionary (preprocessed_record) containing only selected columns: 'asin', 'brand', 'price', and 'also_buy'. This is achieved using a dictionary comprehension.
The preprocessed_record is then appended to the preprocessed_data list.
Finally, the function returns the preprocessed_data list.

Saving Preprocessed Data:
It specifies an output file path () where the preprocessed data will be saved as a JSON file.
It opens the specified file in write mode using open().
It uses json.dump() to write the preprocessed data (preprocessed_data) to the opened file in JSON format.
Finally, it prints a message confirming the path where the preprocessed data is saved.


Helper Functions:
In this function we Read JSON data from a file specified by filename and returns it as a Python dictionary.
Callback function to handle delivery reports from Kafka. It prints a message indicating whether the message delivery was successful or failed.
produce_data(producer, topic, data): Produces data to a Kafka topic using the provided Producer instance (producer). It iterates over each item in the data list, serializes it to a JSON string, and then produces the message to the Kafka topic.

Main Function:
The main function of the script.
Configures Kafka broker settings .
Specifies the Kafka topic to produce to .
Defines the filename from which to read JSON data .
Reads JSON data from the file using read_json_data() function.
Creates a Kafka Producer instance with the specified Kafka configuration.
Calls produce_data function to produce data to the Kafka topic.
Flushes the producer to ensure all messages are delivered.











Consumerfggrowth file:

function serves as the central component of the script, orchestrating the process of consuming messages from a Kafka topic, parsing these messages as JSON, applying the FP-Growth algorithm to find frequent itemsets in the transaction data, and finally saving these frequent itemsets to a MongoDB database. Initially, it configures the Kafka consumer with the necessary settings such as the broker address, group ID, and offset reset strategy. Then, it subscribes to the specified Kafka topic and initializes an empty list to store the transaction data. Within a continuous polling loop, it retrieves messages from Kafka, parses each message using the parse_message() function, and accumulates the resulting data into the transactions list. Upon interruption by a keyboard interrupt (Ctrl+C), it gracefully closes the Kafka consumer. After consuming all messages, it applies the FP-Growth algorithm to find frequent itemsets, using a specified minimum support threshold. Finally, it saves these frequent itemsets to a MongoDB database by invoking the save_to_mongodb() function and prints a confirmation message once the operation is complete. Through these steps, the main() function encapsulates the core functionality of the script, facilitating the real-time processing and analysis of streaming data.

This script provides a pipeline for processing streaming data from Kafka, applying a frequent pattern mining algorithm (FP-Growth), and persisting the results to a MongoDB database. It's a basic setup that can be expanded or modified to suit specific requirements, such as adjusting algorithm parameters, handling different data formats, or integrating with other data storage systems.

ConsumerPCY file:
in this file we go through with the PCY algorithum 
PCY Algorithm:

pcy(transactions, min_support, hash_size, bitmap_size): This function implements the PCY algorithm for finding frequent itemsets. It takes the transaction data, minimum support threshold, hash table size, and bitmap size as inputs.
Step 1: Counting - It counts the occurrences of pairs of items in the transactions using a hash table.
Step 2: Bitmap Filtering - It creates a bitmap indicating which hash buckets have counts greater than or equal to the minimum support threshold.
Step 3: Counting for Frequent Pairs - It scans the transactions again and counts the occurrences of pairs, considering only those pairs whose hash buckets are marked in the bitmap.
Finally, it returns the frequent itemsets found

Basically This file provides a pipeline for processing streaming data from Kafka, applying the PCY algorithm to find frequent item sets efficiently, and persisting the results to a MongoDB database for further analysis.

Consumer.py File :

Apriori Algorithm:

apriori(transactions, min_support): This function implements the Apriori algorithm for finding frequent itemsets. It takes the transaction data and minimum support threshold as inputs.
It initializes the candidate itemsets with individual items from transactions.
While there are still candidate itemsets, it generates new candidate itemsets by joining existing frequent itemsets.
It filters candidate itemsets based on support by counting occurrences in transactions and retaining those above the minimum support threshold.

This  provides a pipeline for processing streaming data from Kafka, applying the Apriori algorithm to find frequent itemsets efficiently, and persisting the results to a MongoDB database for further analysis

Bash file :
This Bash script automates the setup and teardown of a Kafka environment, streamlining the process for testing or development tasks. It starts essential components like Zookeeper and the Kafka broker, creates a Kafka topic, and optionally launches Kafka Connect. Additionally, it initiates a Python producer script along with multiple consumers, each tailored for different algorithms such as Apriori, PCY, and FP-Growth. After running, users can simply press a key to halt all processes, including consumers and Kafka Connect if utilized. The script offers flexibility by allowing users to adjust paths to configuration files and Python scripts as per their environment. Overall, it simplifies the management of Kafka ecosystems, enabling users to quickly set up and dismantle Kafka components, making it ideal for efficient testing and development workflows.


Contributors: Ahsan Abdul (i221870@nu.edu.pk) Awais Arshad (i221989@nu.edu.pk) Ali Zaib (i221900@nu.edu.pk)
