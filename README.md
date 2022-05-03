# w261 Environment
## Overview
Welcome to `w261 - Machine Learning at Scale`. In this Class, on top of learning about the Machine Learning models in the industry, you will be using production grade technology and infrastructure deployment best practices. About two thirds of the class, you will be using an environment orchestration in Google Cloud. The last third, you will get the opportunity to use Databricks on Azure.

## GitHub Repository
### Overview
A read-only GitHub repository will be used as a source of code for Homeworks and Live Session Labs. You will also create a private personal repository for submitting your homeworks and final project.

### Creating Personal Repository
Please subscribe to the following Slack channels where instructions and link to GitHub Classroom will be provided to create your personal private repo:
- data-sci-261-2022-summer-announcements
- data-sci-261-2022-summer-main
- data-sci-261-2022-summer-infrastructure

### Obtain GitHub Personal Token
While authenticated to GitHub, please navigate to [github/personal_tokens](https://github.com/settings/tokens) to obtain one. You will need it for the automatization script mentioned below. Add a note such as `w261 GCP` or similar to keep track of this token. Lastly, check the box on `repo` which provides full control of private repositories, automatically all the underneath boxes are shown as checked.

## Google Cloud
### Overview
Google Cloud is a top state of the art platform for Big Data Analytics and Orchestration. The main service used in w261 is Dataproc which is the main Cloud API for orchestration of Big Data Hadoop and Spark clusters.

### Why Dataproc?
Dataproc offers a plug-and-play kind of cluster orchestration for Hadoop and Spark. Jupyter Lab comes out of the box using the GoogleUserContent front-end which is highly secure, and prevents us from exposing our VM with an external IP address.

### Redeem Credits on GCP
Google offers $300 in credits for new accounts. Login to [GCP Console](https://console.cloud.google.com) to take advantage of this offer by clicking the top banner that shows the promotion. You can create a gmail account if you don't have an email account part of the Google Suite. You must have an account with a Billing Account set before running the automated orchestration.

*Note: Acepting this offer involves providing a credit card that will not be charged immediately after credits deplete. You will have an opportunity to decide to continue before GCP charging your credit card.*

### Automated Orchestration using GCP CloudShell
For this Class, we will be using two automation scripts that will help us navigate through some complexity in the Cloud and Compute World.

The first step is to open the [GCP Console](https://console.cloud.google.com), and click the terminal icon `>_` in the top blue bar.

![alt text](https://github.com/UCB-w261/w261-environment/blob/master/gcp-images/cloud_shell.png "Cloud Shell" | width = 100)

This will open a panel box at the bottom of the screen, and is your CloudShell. This is serverless compute, you are allocated 5 Gb of Storage, and is a great tool to act as a bridge for all the components we will be using in w261. From here, using the automation scripts, you will be able to deploy clusters, load data into Buckets, pull code and push Homeworks to GitHub. The best part of CloudShell is that it's free.

Running the automated scripts on CloudShell guarantees having the appropriate dependencies, packages and the right environment.

### GCP Infrastructure Deployment
The first script you need to run is to prepare a Google Project with all the artifacts needed to work in a secure environment with Dataproc. Please take a look at the documentation in [Create Dataproc Cluster](https://github.com/UCB-w261/w261-environment/edit/master/create-dataproc-cluster/README.md) to have a look inside of the orchestration under the covers.

Please follow the prompts:
```bash
gsutil cat gs://w261-hw-data/w261_env.sh | bash -euo pipefail
```
This script will take longer to run the first time. Once all the components are deployed, the subsequent runs will skip all orchestration and will create clusters on demand directly. Please run the script until you see in the prompts that a cluster was successfully created. You can safely delete this cluster as is missing the files from GitHub. Please navigate to [GCP Dataproc](https://console.cloud.google.com/dataproc/clusters) to delete it. If you don't see your cluster, switch to `w261-student` project in the top blue GCP bar. Remember you will be consuming credits on a per second basis. The orchestration that got put together had this in mind, and following best practices, $300 should be more than enough.

### GitHub Repositories
The second script will take care of the repository cloning and pushing, GitHub account setup. It will also make sure Jupyter notebooks and other scripts are properly loaded into your Dataproc cluster. Have that GitHub token handy when running the first time.

Please follow the prompts:
```bash
gsutil cat gs://w261-hw-data/w261_github.sh | bash -euo pipefail
```
This script will take longer to run the first time because of repository cloning. Subsequent runs will only pull from read-only source code, push changes to your personal repo or replace token.

Both scripts are meant to be run multiple times as you request an on-demand Dataproc cluster and when needing to pull or push to Github.

### Things to know

- Once you open JupyterLab, navigate to the root folder where you see to folders: `GCS` and `Local Disk`. We will work on `Local Disk` for HW1 and 2, and all first Labs before turning to Spark. The automation scripts make sure the files are properly loaded as long as you have run both scripts at least once. 

- When working on a Notebook, get the full path where this notebook is located, and then add a new cell at the very top like this one:
```
%cd /full/path/to/the/notebook
```

- To get the data for the HWs, add a new cell and comment the previous command that pulled the data such as `!curl`, `!wget` and similar, and obtain the data now from your GCS Data Bucket created in the first automation script:
```
!mkdir -p data/
!gsutil cp gs://<your-data-bucket>/main/Assignments/HW2/data/* data/
```
Feel free to explore where the data is for a specific HW with `gsutil ls gs://<your-data-bucket>/main/Assignments/HW*`
If you don't remember your GCS Data Bucket, run `gsutil ls` to get a list of Buckets in your account.

- For Hadoop, the new location of the `JAR_FILE` is:
```
JAR_FILE = '/usr/lib/hadoop/hadoop-streaming-3.2.2.jar'
```

- For debugging, go to Dataproc -> Clusters -> Web Interfaces and look for:
  - MapReduce Job History for Hadoop job logs.
  - Spark History Server for Spark job logs.

- In Jupyter, when running `mkdir` use `-p` to make sure you create the entire path, if inner folders doesn't exist.
  - `!hdfs dfs -mkdir -p {HDFS_DIR}`

- Spark UI for Current Notebook
  - The Spark UI for current jobs and Notebook can be accessed via SSH directly into the Master Node.
  - Open the Cloud Shell.
  - Get the zone where your Master node is located. Adjust the name of your instance. You can also assign the direct value if already known.
  ```
  ZONE=$(gcloud compute instances list --filter="name~w261" --format "value(zone)")
  ```
  - SSH into the VM using your Cloud Shell. It can also be done from your local terminal or Google Cloud SDK if running windows. Adjust the name of your instance if different.
  ```
  gcloud compute ssh w261-m --ssh-flag "-L 8080:localhost:42229" --zone $ZONE
  ```
  - Click the `Web Preview` button at the top right in the Cloud Shell panel. We mapped this port to 8080, which is the default port number that `Web Preview` uses.
  - By default, Dataproc runs the Spark UI on port `42229`. Adjust accordingly if using a different port. In order to get the port number, open a new cell and run the variable `spark` (if SparkSession already established). You'll see the UI link. Hover over the link and get the port number.
  - Keep the Cloud Shell alive by running `sleep 1800`, or a number you feel comfortable to keep the tunnel open.
  
