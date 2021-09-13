# Spark Lab 2: Key Concepts and Optimization

## Prerequisites

- You have created a [GCP project](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-google-cloud-project)
- You have created a [Dataproc cluster](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-dataproc-cluster)
- Your Dataproc cluster is up and running


### Overview
The task is to create a production level Spark job, which is a replacement of existing SQL-based job in some Warehouse (let's call it BlueShift Data Warehouse)

### Prepare data

> Note: you can skip all or some of the steps if you have done that already during previous lab(s)

- Create a [Cloud Storage](https://cloud.google.com/storage/docs/creating-buckets) bucket
- Download [source data](https://www.kaggle.com/usdot/flight-delays)
- Upload extracted data to the created Cloud Storage bucket in some folder
- Check out URI to the files (ie `gs://globallogic-procamp-bigdata-datasets/2015_Flight_Delays_and_Cancellations/flights.csv`)

### Task Description
As a Data Engineer on a Next-Gen Data Platform, which is based on Spark, you have received the following task:
1. Migrate data aggregation job from legacy BlueShift Data Warehouse to Next Gen Data Platform
2. Your task is to translate the SQL statements of the legacy job to Spark code, following best practices in terms of code structure and job performance
3. All requirements you have - the SQL Query itself.
4. Consumers of your results - other Spark jobs
5. Corresponding data is ingested as CSV files (see Prepare Data section above) that have the following mapping to the legacy tables:
    1. FLIGHTS table - flights.csv file
    2. AIRPORTS table - airports.csv file
    3. AIRLINES table - airlines.csv file

### Legacy SQL Query
```
CREATE OR REPLACE TEMPORARY VIEW ENRICHED_FLIGHTS AS 
SELECT f.ORIGIN_AIRPORT, f.AIRLINE, f.DEPARTURE_DELAY, p.AIRPORT as AIRPORT_NAME, a.AIRLINE as AIRLINE_NAME FROM FLIGHTS f 
INNER JOIN AIRPORTS p ON p.IATA_CODE = f.ORIGIN_AIRPORT 
INNER JOIN AIRLINES a ON a.IATA_CODE = f.AIRLINE;

CREATE OR REPLACE TEMPORARY VIEW delays_per_airport_and_airline AS 
SELECT ORIGIN_AIRPORT, AIRLINE, MAX(AIRPORT_NAME) AS AIRPORT_NAME, MAX(AIRLINE_NAME) AS AIRLINE_NAME, AVG(DEPARTURE_DELAY) AS AVG_AIRLINE_DEPARTURE_DELAY, 
ROW_NUMBER() OVER (PARTITION BY ORIGIN_AIRPORT ORDER BY AVG(DEPARTURE_DELAY) DESC) AS rn 
FROM ENRICHED_FLIGHTS 
GROUP BY ORIGIN_AIRPORT, AIRLINE;

CREATE OR REPLACE TEMPORARY VIEW max_delayer_airline_per_airport AS 
SELECT * FROM delays_per_airport_and_airline 
WHERE rn = 1;

CREATE OR REPLACE TEMPORARY VIEW delays_per_airport AS 
SELECT ORIGIN_AIRPORT, AVG(DEPARTURE_DELAY) AS AVG_DEPARTURE_DELAY, MAX(DEPARTURE_DELAY) AS MAX_DEPARTURE_DELAY 
FROM FLIGHTS 
GROUP BY ORIGIN_AIRPORT;

CREATE OR REPLACE TEMPORARY VIEW final_result AS 
SELECT a.ORIGIN_AIRPORT, AIRPORT_NAME, AVG_DEPARTURE_DELAY, MAX_DEPARTURE_DELAY, AIRLINE, AIRLINE_NAME, AVG_AIRLINE_DEPARTURE_DELAY 
FROM delays_per_airport a 
INNER JOIN max_delayer_airline_per_airport b ON a.ORIGIN_AIRPORT = b.ORIGIN_AIRPORT;

CREATE TABLE lab2_results 
USING JSON 
LOCATION '{some_path_on_fs}/lab2_results_sql' 
AS SELECT * FROM final_result;
```

### Technical Constraints
- The solution should be written as PySpark job which can be executed on DataProc cluster
- The input of the job should be files in GCP Storage Bucket
- The output of the job should be a folder inside GCP Storage Bucket
- The GCP Storage Bucket(s) and folder inside the bucket(s) should be provided as a job parameters.

Example of the DataProc Submit Job command:

 <code>
gcloud dataproc jobs submit pyspark some_job.py --cluster=procamp-cluster --region=us-east1 -- procamp_labs_materials job_result result_folder
 </code>
