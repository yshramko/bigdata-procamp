# Databricks notebook source
# MAGIC %run ./utils_notebook

# COMMAND ----------

dbutils.widgets.text("input_folder", '/FileStore/tables')
dbutils.widgets.text("output_folder", '/gold_zone')

# COMMAND ----------

input_folder = dbutils.widgets.get("input_folder")
output_folder = dbutils.widgets.get("output_folder")
output_file_name = "flights_agg_statistics" 
for file_name in ["airlines", "airports", "flights_sample_10"]:
    print(file_name)
    ingest_data(input_folder, file_name)

# COMMAND ----------

enriched_flights()
max_delayer_airline_per_airport()
output = delays_per_airport_combined()
output.write.format('delta').mode("overwrite").save(f"{output_folder}/{output_file_name}")

# COMMAND ----------


execute_query(f"select * from delta.`{output_folder}/flights_agg_statistics/` limit 10").display()
