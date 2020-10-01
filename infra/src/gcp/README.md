# GCP infrastructure

## Installation steps:
There are two options for executing python scripts that spin up/shutdown GCP infrastructure:
1. Use Google Cloud Shell
2. Execute them from your local machine

Due to differences in local machines i.e. OS's, hardware, software the recommended option is execution of this scripts
from Google Cloud Shell.

### Google Cloud Shell installation
1. Activate Google Cloud Shell
2. [Download this project](https://cloud.google.com/shell/docs/uploading-and-downloading-files) into cloud shell machine
by zipping the project folder and uploading it directly or via `git clone`
3. Install Python3 on Google Cloud Shell
```bash
sudo apt update
sudo apt install python3 python3-dev python3-venv
pip3 install --upgrade pip
python3 -m pip install --upgrade setuptools
cd <project-root>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Installation on your local machine

Pre-requisites:
- install [Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstart)
- [setup service account with enough permissions and create GOOGLE_APPLICATION_CREDENTIALS env variable](https://cloud.google.com/docs/authentication/production#passing_variable) 
- Python >= 3.6

Execute from command line in project root:
```$bash
python3 -m venv .venv
source .venv/bin/activate # or on Windows execute .venv/activate.bat
pip install -r requirements.txt
```


### Google Cloud Dataproc

- Cluster creation example
```bash
python dataproc.py create-cluster --project-id bigdata-procamp-env --region us-central1 --cluster-name test1 --create-buckets
```
- Cluster deletion example
```bash
python dataproc.py shutdown-cluster --project-id bigdata-procamp-env --region us-central1 --cluster-name test1 --delete-buckets
```

### Google Cloud Composer

- Env creation example
```bash
python composer.py create-env --region us-central1 --env-name test1
```
- Env deletion example
```bash
python composer.py shutdown-env --region us-central1 --env-name test1
```
