## Spark Structured Streaming Lab

## Prerequisites

- You have created a [GCP project](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-google-cloud-project)
- You have created a [Dataproc cluster](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-dataproc-cluster)
- You have finished both [Nifi](https://github.com/gl-bigdata-procamp/bigdata-procamp/tree/master/labs/nifi) and [Kafka](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/labs/kafka/lab1.md) labs
- Your Dataproc cluster with NiFi and Kafka is up and running

### Overview
The task is to create Spark Streaming Job, which reads data from Kafka topic, executes windowed aggregation query on the data and writes result into the GCP Storage Bucket

### Task Description
On NiFi lessons, the NiFi workflow has been presented, which reads BitCoins transactions data and writes it into the Kafka.
A single transaction, converted to a string, looks like the following (where "value" is a default value for data field in Kafka):

<code>
{"value":"{\"data\":{\"id\":1295427768717315,\"id_str\":\"1295427768717315\",\"order_type\":0,\"datetime\":\"1605101520\",\"microtimestamp\":\"1605101519755000\",\"amount\":1.0101,\"amount_str\":\"1.01010000\",\"price\":15646.4,\"price_str\":\"15646.40\"},\"channel\":\"live_orders_btcusd\",\"event\":\"order_created\"}"}
</code>

<br/>The goal is to read the BitCoins Transactions data from Kafka, transform it into the DataFrame with suitable schema and for each 1 minute (base on event time), produce the following aggregations:

1. Count of the records within the time window
2. Average price of transactions within the time window
3. Sales Total (which is the amount multiplied by price) of transactions within the time window

Allowed latency - 3 minutes

### Technical Constraints
 - The solution should be written as PySpark job which can be executed on DataProc cluster
 - The input of the job should be Kafka topic
 - The output of the job should be a folder inside GCP Storage Bucket
 - The GCP Storage Bucket, folder inside the bucket as well as name of Kafka topic should be provided as a job parameters. 
 
 Example of the DataProc Submit Job command:
 
 <code>
gcloud dataproc jobs submit pyspark lab_streaming.py --cluster=procamp-cluster --region=us-east1 --properties spark.jars.packages=org.apache.spark:spark-sql-kafka-0-10_2.12:2.4.7 -- procamp_labs_materials streaming_result btc
 </code>    

<br/>Where `procamp_labs_materials` is a name of bucket, `streaming_result` is a folder within bucket and `btc` is a topic to read.

Please pay attention for the version of spark-sql-kafka library - it should match with version of the Spark installed on your DataProc cluster
