# Databricks notebook source
import pyspark.sql.functions as F

# COMMAND ----------

def ingest_data(input_folder, file_name):
    df = spark.read.load(f"{input_folder}/{file_name}.csv", format="csv", inferSchema="true", header="true")
    return df.write.format('delta').mode("overwrite").save(f"/bronze_zone/{file_name}")

# COMMAND ----------

def execute_query(query_string):
    return spark.sql(query_string)

# COMMAND ----------

def enriched_flights():
    ENRICHED_FLIGHTS_view_creation_sql_string = """
    CREATE OR REPLACE TEMPORARY VIEW ENRICHED_FLIGHTS AS 
    SELECT f.ORIGIN_AIRPORT, f.AIRLINE, f.DEPARTURE_DELAY, p.AIRPORT as AIRPORT_NAME, a.AIRLINE as AIRLINE_NAME FROM delta.`/bronze_zone/flights_sample_10` f 
    INNER JOIN delta.`/bronze_zone/airports` p ON p.IATA_CODE = f.ORIGIN_AIRPORT 
    INNER JOIN delta.`/bronze_zone/airlines` a ON a.IATA_CODE = f.AIRLINE;
    """
    return execute_query(ENRICHED_FLIGHTS_view_creation_sql_string)

# COMMAND ----------

def max_delayer_airline_per_airport():
    max_delayer_airline_per_airport_sql_string = """
    CREATE OR REPLACE TEMPORARY VIEW max_delayer_airline_per_airport AS 
    SELECT * from( 
        SELECT ORIGIN_AIRPORT, AIRLINE, MAX(AIRPORT_NAME) AS AIRPORT_NAME, MAX(AIRLINE_NAME) AS AIRLINE_NAME, round(AVG(DEPARTURE_DELAY), 2) AS AVG_AIRLINE_DEPARTURE_DELAY, 
        ROW_NUMBER() OVER (PARTITION BY ORIGIN_AIRPORT ORDER BY AVG(DEPARTURE_DELAY) DESC) AS rn 
        FROM ENRICHED_FLIGHTS 
        GROUP BY ORIGIN_AIRPORT, AIRLINE
    )
    WHERE rn = 1
    """
    return execute_query(max_delayer_airline_per_airport_sql_string)

# COMMAND ----------

def delays_per_airport_combined():
    delays_per_airport_query_string = """
    with delays_per_airport AS (
        SELECT ORIGIN_AIRPORT, round(AVG(DEPARTURE_DELAY), 2) AS AVG_DEPARTURE_DELAY, MAX(DEPARTURE_DELAY) AS MAX_DEPARTURE_DELAY 
        FROM delta.`/bronze_zone/flights_sample_10` 
        GROUP BY ORIGIN_AIRPORT    
    )
    SELECT a.ORIGIN_AIRPORT, AIRPORT_NAME, AVG_DEPARTURE_DELAY, MAX_DEPARTURE_DELAY, AIRLINE, AIRLINE_NAME, AVG_AIRLINE_DEPARTURE_DELAY 
    FROM delays_per_airport a 
    INNER JOIN max_delayer_airline_per_airport b ON a.ORIGIN_AIRPORT = b.ORIGIN_AIRPORT;
    """
    return execute_query(delays_per_airport_query_string)
