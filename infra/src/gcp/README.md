## GCP infrastructure

### Google Cloud Dataproc

- Cluster creation example
```bash
python dataproc.py create-cluster --project-id bigdata-procamp-env --region us-central1 --cluster-name test1 --create-buckets
```
- Cluster deletion example
```bash
python dataproc.py shutdown-cluster --project-id bigdata-procamp-env --region us-central1 --cluster-name test1 --delete-buckets
```