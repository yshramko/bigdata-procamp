 # Spark Lab 1: RDDs
 
## Prerequisites

- You have created a [GCP project](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-google-cloud-project)
- You have created a [Dataproc cluster](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-dataproc-cluster)
- Your Dataproc cluster is up and running
 
## How to connect to Spark Shell

1. Start GCP console (if you don't have GCP CLI on your host machine)
2. Connect to your Dataproc cluster master node 

  >  \> `gcloud compute ssh procamp-cluster-m --zone=us-east1-b --project=[YOUR PROJECT ID]`

**Note**: It is supposed your Dataproc cluster name is `procamp-cluster` and zone `us-east1-b`

3. Start Spark shell

	- python
	
    > /usr/lib/spark/bin/pyspark

	- scala 
	
	> spark-shell
	

 It will take some time to start
 
 
 ## How to connect to Zeppelin
 
 1. Go to Dataproc in GCP console
 2. Select `Clusters`
 3. In the clusters list select your running Dataproc cluster
 4. Navigate to `WEB INTERFACES` tab
 5. Find link to `Zeppelin` UI
 
  > Hint: Check out how to activate your preferable Spark interpreter https://zeppelin.apache.org/docs/latest/interpreter/spark.html
 
 
 
 ## How to connect to submit a Spark job
 
1. Start GCP console (if you don't have GCP CLI on your host machine)
2. Connect to your Dataproc cluster master node 
3. Submit your Spark job

 > ./spark-submit --master yarn-cluster  \
 >  --num-executors 20 --executor-memory 1G --executor-cores 3 \
 > --driver-memory 1G \
 > --conf spark.yarn.appMasterEnv.SPARK_HOME=/dev/null \
 > --conf spark.executorEnv.SPARK_HOME=/dev/null \
 > --files  /home/user/script.py

## Lab Homework

### Prepare data

 > Note: you can skip all or some of the steps if you have done that with Hadoop MapReduce lab and have the data available on Dataproc HDFS

- Create a [Cloud Storage](https://cloud.google.com/storage/docs/creating-buckets) bucket 
- Download [source data](https://www.kaggle.com/usdot/flight-delays)
- Upload extracted data to the created Cloud Storage bucket in some folder
- Check out URI to the files (ie `gs://globallogic-procamp-bigdata-datasets/2015_Flight_Delays_and_Cancellations/flights.csv`)
- Ssh to Hadoop master node

  > `gcloud compute ssh procamp-cluster-m --zone=us-east1-b --project=[YOUR PROJECT ID]`

- Copy the data from Cloud Storage to Hadoop (Dataproc) HDFS 

 > Hint: Use `hadoop discp` or `hadoop fs -cp` or `hdfs dfs -cp`

 > Reminder: Don't forget to recall the commands from the first lecture on Hadoop fundamentals

### Tasks

Using RDDs API:

1. Find the most popular destination airport in each month and save to hdfs in TSV format. Record should contain the destination airport name and number of visits. Gather statistics per each of the airports for debugging
2. Calculate percentage of canceled flights per origin airport per airline. Save the result to HDFS in json format sorted by airline name and percentage for all airports but 'Waco Regional Airport' which shold be stored in CSV format. Record should contain airline name, origin airport name, percentage, number of canceled flights, number of processed flights. Gather total number of flights  per airline for debbuging
