 # Hadoop MapReduce Lab
 
## Prerequisites

- You have created a [GCP project](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-google-cloud-project)
- You have created a [Dataproc cluster](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-dataproc-cluster)
- Your Dataproc cluster is up and running
 
## How to start example applications

1. Start GCP console (if you don't have GCP CLI on your host machine)
2. Connect to your Dataproc cluster master node 

  > `gcloud compute ssh procamp-cluster-m --zone=us-east1-b --project=[YOUR PROJECT ID]`

**Note**: It is supposed your Dataproc cluster name is `procamp-cluster` and zone `us-east1-b`

3. Clone this repository 

> git clone https://github.com/gl-bigdata-procamp/bigdata-procamp.git

4. Navigate to Hadoop MapReduce labs

> cd bigdata-procam/labs/hadoop-mr

5. There are 4 demo applications (projects):
- failing
- stuck
- word_counter
- word_counter_python

6. Check out their readme to find out the way to run the examples
7. Check out their `source` folders to find out their implementation details

## How to rebuild example applications

Java based application use Maven package manage:
- failing
- stuck
- word_counter

In order to reasseble an application jar you need:
>- go to an example source dir 
>- execute `mvn clean package`
>- find output artifact under `target` in an example `source` dir 


## Lab Homework

### Prepare data

- Create a [Cloud Storage](https://cloud.google.com/storage/docs/creating-buckets) bucket 
- Download [source data](https://www.kaggle.com/usdot/flight-delays)
- Upload extracted data to the created Cloud Storage bucket in some folder
- Check out URI to the files (ie `gs://globallogic-procamp-bigdata-datasets/2015_Flight_Delays_and_Cancellations/flights.csv`)
- ssh to Hadoop master node

  > `gcloud compute ssh procamp-cluster-m --zone=us-east1-b --project=[YOUR PROJECT ID]`

- Use `hadoop discp` or `hadoop fs -cp` or `hdfs dfs -cp` to copy the data from Cloud Storage to Hadoop (Dataproc) HDFS
- Don't forget to experiment with all the commands from the lecture

### Tasks

1. Find top 5 airlines with the greatest average DEPARTURE_DELAY. Show Airline code (IATA_CODE), Airline Name and average DEPARTURE_DELAY
2. Unit tests will give you extra points
