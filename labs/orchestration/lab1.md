# Orchestration Lab: Apache Airflow

## Prerequisites

- You have created a [GCP project](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-google-cloud-project)
- You have created a [Composer environment](https://github.com/gl-bigdata-procamp/bigdata-procamp/blob/master/infra/README.md#create-composer-cluster)
- Apache Spark Homework, where you implemented a batch job which:
    - Finds the most popular destination airport in each month and save to hdfs in TSV format.
    - Calculates percentage of canceled flights per origin airport per airline.

### Overview
The task is to orchestrate Apache Spark batch job that you implemented in one of your previous homeworks with Apache Airflow. 

### Task Description

1. Take the code from the official Google Cloud Composer tutorial - https://cloud.google.com/composer/docs/tutorials/hadoop-wordcount-job#airflow-1_1 (Make sure you copy Airflow 1.1 version of the code)
    - Try to run it and make sure words-count job is running successfully
    - navigate through the DAG to better understand how it's configured, explore how it looks on Airflow Web UI
2. Replace the hadoop word count job from the tutorial with Apache Spark job from your homework.
    - look through [the Airflow Dataproc operator's documentation](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/operators/dataproc_operator/index.html) and choose the operator you need for this step 
3. Before running all the Dataproc logic add step at the beginning which checks for a marker file presence:
    - [research sensor](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/sensors/gcs_sensor/index.html) that is required for this task
    - [create a bucket in Google Cloud Storage](https://cloud.google.com/storage/docs/creating-buckets)
    - bucket name should be passed to the DAG through Airflow variables
    - sensor should wait for a file by the following path: `gc://${your_bucket_name}/flights/${yyyy}/${MM}/${dd}/${HH}/_SUCCESS` where
        - `your_bucket_name` is the bucket you created in prev step
        - `flights` is a dummy name for some external dataset dependency
        - yyyy, MM, dd, HH are respectively year, month, day and hour of the time new data has arrived. 
        Your Airflow DAG constructs the path `/yyyy/MM/dd/HH/` using its 
        [execution date](https://airflow.apache.org/docs/apache-airflow/1.10.12/macros-ref.html) that you need to format.
        - `_SUCCESS` is a name of a success marker file
    - configure wait timeout to fail after two hours
4. Research DAG options and configure the DAG:
    - disable catchup
    - fix start_date in the tutorial code: https://airflow.apache.org/docs/apache-airflow/1.10.12/faq.html#what-s-the-deal-with-start-date
    - schedule hourly
