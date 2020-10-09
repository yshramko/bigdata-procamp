# uncomment for local execution
# import findspark
# findspark.init()

import sys
from pyspark.sql import SparkSession
from pyspark.sql import Window
from pyspark.sql.functions import col, avg, row_number, broadcast, max as s_max
import pyspark as ps

if len(sys.argv) != 2:
    raise Exception("Exactly 1 argument is required: <bucket_name>")

# path_prefix = "f:/local/ProCamp"
path_prefix = "gs://" + sys.argv[1]

airports_path = path_prefix + "/dataSetFlightDelays/airports.csv"
airlines_path = path_prefix + "/dataSetFlightDelays/airlines.csv"
flights_path = path_prefix + "/dataSetFlightDelays/flights.csv"

airlines_delays_out_path = path_prefix + "/Lab1Results/AirlinesDelays"
state_airlines_delays_out_path = path_prefix + "/Lab1Results/StateAirlinesDelays"
spark = SparkSession \
    .builder \
    .master("yarn") \
    .appName("Lab1") \
    .getOrCreate()
# # .master("local[*]") \
# # .master("yarn") \

# sc = ps.SparkContext()
# sc.setLogLevel("ERROR")
# spark = ps.sql.SQLContext(sc)

airports = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(airports_path)
airlines = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(airlines_path)
flights = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(flights_path)

enriched_flights = flights\
    .join(broadcast(airlines)
          .withColumnRenamed("AIRLINE", "AIRLINE_NAME")
          .withColumnRenamed("IATA_CODE", "AIRLINE"), "AIRLINE")\
    .join(airports
          .withColumnRenamed("IATA_CODE", "ORIGIN_AIRPORT")
          .select("STATE", "ORIGIN_AIRPORT"), "ORIGIN_AIRPORT")
# 1. Find the top 5 airlines with greatest average DEPARTURE_DELAY. Show Airline code (IATA_CODE), Airline Name and
# average DEPARTURE_DELAY, sorted by average DEPARTURE_DELAY, descending

airlines_delays = enriched_flights.groupby("AIRLINE").agg(avg("DEPARTURE_DELAY").alias("AVERAGE_DEPARTURE_DELAY")) \
    .orderBy("AVERAGE_DEPARTURE_DELAY", ascending=False).limit(5)

# airlines_delays.show(10)
airlines_delays.repartition(1).write.format("json").mode("overwrite").save(airlines_delays_out_path)
# 2. For each state, find the top 5 airlines with greatest average DEPARTURE_DELAY. Show State, Airline code,
# Airline Name and average DEPARTURE_DELAY, sorted by State, and then - by average DEPARTURE_DELAY, descending.
window = Window.partitionBy("STATE")
state_airlines_delays = enriched_flights.groupBy("STATE", "AIRLINE")\
    .agg(avg("DEPARTURE_DELAY").alias("AVERAGE_DEPARTURE_DELAY"), s_max("AIRLINE_NAME").alias("AIRLINE_NAME"))\
    .withColumn("rn", row_number().over(window.orderBy(col("AVERAGE_DEPARTURE_DELAY").desc())))\
    .filter(col("rn") <= 5)\
    .select("STATE", "AIRLINE", "AIRLINE_NAME", "AVERAGE_DEPARTURE_DELAY")\
    .orderBy(col("STATE"), col("AVERAGE_DEPARTURE_DELAY").desc())

# state_airlines_delays.show(50)
state_airlines_delays.repartition(1).write.format("json").mode("overwrite").save(state_airlines_delays_out_path)