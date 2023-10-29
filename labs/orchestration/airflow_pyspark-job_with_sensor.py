
import datetime
import pendulum
import os

from airflow import models
from airflow.contrib.operators import dataproc_operator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStorageObjectSensor
from airflow.utils import trigger_rule


# Path to PySpark Job for flights statistics calculation.
PYSPARK_SCRIPT_PATH = "gs://bigdata_procamp/labs/lab_5/hw5.py"


default_dag_args = {
    # Setting start date 
    "start_date": pendulum.datetime(2023, 10, 28),
    # To email on failure or retry set 'email' arg to your email and enable
    # emailing here.
    "email_on_failure": False,
    "email_on_retry": False,
    # If a task fails, retry it once after waiting at least 5 minutes
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
    "project_id": "{{ var.value.gcp_project }}",
}

with models.DAG(
    "flights_statistics_calcualtion_with_sensor",
    # Continue to run DAG hourly
    schedule_interval='@hourly',
    catchup=False,
    default_args=default_dag_args,
) as dag:

    # Wait for file been uploded into  GCS bucket
    wait_for_obj_create = GoogleCloudStorageObjectSensor(
        task_id='wait_for_obj_create',
        bucket='{{ var.value.gcs_sensor_bucket }}',
        object="sensor/{{ execution_date.strftime('%Y/%m/%d/%H') }}/_SUCCESS",
        google_cloud_conn_id='google_cloud_default'
    )

    # Create a Cloud Dataproc cluster.
    create_dataproc_cluster = dataproc_operator.DataprocClusterCreateOperator(
        task_id="create_dataproc_cluster",
        # Give the cluster a unique name by appending the date scheduled.
        # See https://airflow.apache.org/docs/apache-airflow/stable/macros-ref.html
        cluster_name="composer-hadoop-tutorial-cluster-{{ ds_nodash }}",
        num_workers=2,
        region="{{ var.value.gce_region }}",
        master_machine_type="n1-standard-2",
        worker_machine_type="n1-standard-2",
    )

    # Run the PySpark job for flights stat calculation
    run_dataproc_hadoop = dataproc_operator.DataProcPySparkOperator(
        task_id="run_dataproc_pyspark_job",
        main=PYSPARK_SCRIPT_PATH,
        region="{{ var.value.gce_region }}",
        cluster_name="composer-hadoop-tutorial-cluster-{{ ds_nodash }}",
    )

    # Delete Cloud Dataproc cluster.
    delete_dataproc_cluster = dataproc_operator.DataprocClusterDeleteOperator(
        task_id="delete_dataproc_cluster",
        cluster_name="composer-hadoop-tutorial-cluster-{{ ds_nodash }}",
        region="{{ var.value.gce_region }}",
        # Setting trigger_rule to ALL_DONE causes the cluster to be deleted
        # even if the Dataproc job fails.
        trigger_rule=trigger_rule.TriggerRule.ALL_DONE,
    )

    # Define DAG dependencies.
    wait_for_obj_create >> create_dataproc_cluster >> run_dataproc_hadoop >> delete_dataproc_cluster