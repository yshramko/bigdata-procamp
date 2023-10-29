from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window


if __name__ == "__main__":
    print("job_started...")    
    
    spark = (SparkSession.builder.appName('hm5').enableHiveSupport().getOrCreate())
    print("reading data...")
    ### reading row data
    airlines = spark.read.load("gs://bigdata_procamp/labs/lab_1/flights/airlines.csv", format="csv", inferSchema="true", header="true")
    airports = spark.read.load("gs://bigdata_procamp/labs/lab_1/flights/airports.csv", format="csv", inferSchema="true", header="true")
    flights = spark.read.load("gs://bigdata_procamp/labs/lab_1/flights/flights.csv", format="csv", inferSchema="true", header="true")
    print("calculation starts")
    ## finding most popular destnation
    total_flights = flights.groupby('YEAR', 'MONTH', 'DESTINATION_AIRPORT').agg(count('AIRLINE').alias('total_flights'))
    ### output ranked destination airport
    ranked = total_flights.withColumn("rank", dense_rank().over(Window.partitionBy('MONTH').orderBy(desc("total_flights")))).orderBy('Month', 'rank')
    filtered = ranked.filter("rank == 1")
    ### output most popular destination for month
    filtered.coalesce(1).write.mode('overwrite').format("csv").option("header", "true").save("gs://bigdata_procamp/labs/lab_5/most_popular_dest.tsv")
    ### output overall statistics for debugging
    ranked.coalesce(1).write.mode('overwrite').format("csv").option("header", "true").save("gs://bigdata_procamp/labs/lab_5/ranked_dest.tsv")
    print("calculations starts part 2")
    ## calculating statistics for canceled flights
    aggregated = flights.select("AIRLINE","ORIGIN_AIRPORT","CANCELLED").filter("CANCELLED is Not Null").groupby("AIRLINE","ORIGIN_AIRPORT").agg(sum("CANCELLED").alias("total_canceled"), count('AIRLINE').alias('total_flights'))
    aggregated = aggregated.select("AIRLINE","ORIGIN_AIRPORT", 
                                   round((aggregated.total_canceled*100 / aggregated.total_flights), 2).alias('canceled_percentage'), 
                                   "total_canceled", 
                                   (aggregated.total_flights - aggregated.total_canceled).alias("processed_flights"), 'total_flights')
                                   
    ### finding wako airport code
    waco_code = airports.filter("AIRPORT == 'Waco Regional Airport'").select('IATA_CODE').first()[0]
    
    ### writing statistics for all airport except waco
    aggregated.select("AIRLINE", "ORIGIN_AIRPORT", "canceled_percentage").filter(aggregated["ORIGIN_AIRPORT"] != waco_code).orderBy("AIRLINE", 'canceled_percentage').\
            coalesce(1).write.mode('overwrite').json('gs://bigdata_procamp/labs/lab_5/canceled_flights.json')
            
    ### output statistics for waco       
    aggregated.filter(aggregated["ORIGIN_AIRPORT"] == waco_code).orderBy("AIRLINE", 'canceled_percentage').\
            coalesce(1).write.mode('overwrite').format("csv").option("header", "true").save("gs://bigdata_procamp/labs/lab_5/waco_canceled_flights.csv")  
    
    spark.stop()    
		