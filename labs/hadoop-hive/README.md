 # Hadoop Hive Lab
 
## Prerequisites

- You have created a [GCP project](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-google-cloud-project)
- You have created a [Dataproc cluster](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-dataproc-cluster)
- Your Dataproc cluster is up and running
 
## How to connect to Hive CLI

1. Start GCP console (if you don't have GCP CLI on your host machine)
2. Connect to your Dataproc cluster master node 

  >  \> git push --set-upstream origin HF-HIVE-1`gcloud compute ssh procamp-cluster-m --zone=us-east1-b --project=[YOUR PROJECT ID]`

**Note**: It is supposed your Dataproc cluster name is `procamp-cluster` and zone `us-east1-b`

3. Launch Hive CLI

 > \> hive

4. List existing database with `SHOW DATABASES;`

5. Create your own database with `CREATE DATABASE my_db;`

6. Visit [Hive LanguageManual Cli](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Cli)
    to find out more options


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

1. Find top 5 airlines with the greatest average DEPARTURE_DELAY. Show Airline code (IATA_CODE), Airline Name and average DEPARTURE_DELAY and save the result in another Hive table
   
 > Hint: You may want to create tables for the data files

 > Hint: Use DESCRIBE command to find out details about Hive entities

2. Describe how you would test the script (implemented solution is a great bonus)
