# Introduction
This project performs frequent itemset analysis on the Amazon Metadata dataset using streaming data techniques. The main goal is to extract valuable insights and associations from product data, which can be used to understand consumer behavior and improve recommendation systems. The dataset includes various product attributes such as ID, title, features, description, price, images, related products, sales rank, brand, categories, and technical details.

# Dataset Description
* asin: ID of the product
* title: Name of the product
* feature: Bullet-point format features of the product
* description: Description of the product
* price: Price in US dollars (at time of crawl)
* imageURL: URL of the product image
* related: Related products (also bought, also viewed, bought together, buy after viewing)
* salesRank: Sales rank information
* brand: Brand name
* categories: List of categories the product belongs to
* tech1: First technical detail table of the product
* tech2: Second technical detail table of the product
* similar: Similar product table
# Dependencies
* Python
* Kafka
* MongoDB
* Confluent Kafka
* JSON
# Pre-Processing
Load the Sampled Amazon Dataset:
Load the sampled Amazon dataset from a JSON file.

# Clean and Format the Data:

Select relevant columns such as 'asin', 'brand', 'price', and 'also_buy'.
Handle missing values and standardize text fields.
Convert the cleaned data to a new JSON file.
Batch Processing (Bonus):
Perform batch processing to execute pre-processing in real time.

# Streaming Pipeline Setup
Producer Application:
Develop a producer application that streams the preprocessed data in real time to Kafka topics.

# Consumer Applications:
Create three consumer applications that subscribe to the producer's data stream:

Consumer 1: Implements the Apriori algorithm.
Consumer 2: Implements the PCY algorithm.
Consumer 3: Implements a custom algorithm for innovative analysis.
# Frequent Itemset Mining
Apriori Algorithm:

Implement the Apriori algorithm in one consumer.
Print real-time insights and associations.
PCY Algorithm:

Implement the PCY algorithm in another consumer.
Print real-time insights and associations.
Custom Analysis:

Implement a custom algorithm for innovative analysis in the third consumer.
Ensure the analysis is beyond straightforward calculations and provides significant insights.
# Database Integration
Database Choice: Use a NoSQL database like MongoDB for storing results.
Modify Consumers: Connect each consumer to the database and store the results.
