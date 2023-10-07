# Spark Lab 2: Databricks

## Prerequisites

- You have created a [Community Databricks Account](https://community.cloud.databricks.com/login.html)
    - Navigate to https://www.databricks.com/ -> Click "Try Databrick" -> Fill out the form and click "Continue" -> Click on "Get Started With Community Edition"
- You have created a Databricks cluster in your Databricks Community Edition
- Your Databricks cluster is up and running


### Overview
The task is to create a production-level Spark job in the form of a Databricks notebook, which is a replacement for an existing SQL-based job in some Warehouse (let's call it BlueShift Data Warehouse)

### Prepare data

- Download [source data](https://www.kaggle.com/usdot/flight-delays)
- For flights.csv file, extract some sample of the data (to do not overload the free version of Databricks)
- Upload extracted data to the Databricks in some folder (use sampled flights.csv instead of the original one)
- Check out URI to the files (ie `/FileStore/table/flights.csv`)

### Task Description
As a Data Engineer on a Next-Gen Data Platform, which is based on Spark, you have received the following task:
1. Migrate the ingested data from CSV format to the Delta format
2. Migrate data aggregation job from legacy BlueShift Data Warehouse to Next Gen Data Platform
3. Your task is to translate the SQL statements of the legacy job to Spark code, following best practices in terms of code structure and job performance
4. All requirements you have - the SQL Query itself.
5. Consumers of your results - other Spark jobs in the form of Databricks notebook
6. Corresponding data is ingested as CSV files (see Prepare Data section above) that have the following mapping to the legacy tables:
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
- The solution should be written as Databricks notebook using Python language and can be executed on Databricks
- The input of the job should be the files in DBFS
- The output of the job should be a folder in DBFS
- The input and output locations should be provided as notebook parameters (via [Widget](https://docs.databricks.com/en/notebooks/widgets.html) functionality).

