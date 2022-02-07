# Create a Dataproc Cluster

## Important

All notebooks can be run using this cluster, you can run Bash/Python and Spark notebooks locally or in the Cloud just as we will show you in here. However, the Hadoop notebooks, our only reliable option right now is using this Dataproc cluster given the `log4j` CVE. More information [here](https://logging.apache.org/log4j/2.x/security.html#CVE-2021-44832). It's your option to keep this setup until we move to Databricks for HW5. Just be cautious of your GCP credits or credit card charges. Switch your cluster on/off as you work on the class material. Keep in mind that you'll be charged at 20 cents/hr while cluster on. Then, charges drop dramatically while off (You still get charged for Disk and Storage, but minimal). For more information on GCP pricing:

[GCP Calculator](https://cloud.google.com/products/calculator) 

## Instructions

### Create a New GCP Project

- Login to [GCP Console](https://console.cloud.google.com) with your Berkeley.edu account, or gmail account if taking the $300 credit offer, and click on the top blue bar next to *Google Cloud Platform* where it says "Select Project". Skip if you have a Project already.
- From the popup window, click on *NEW PROJECT*.
- Follow the prompts.
- If using Berkeley account, you need to place this Project under the *Learning* folder.
- Create.

![alt text](https://github.com/UCB-w261/w261-environment/blob/master/gcp-images/project-id.png "Project")

### Setup Cluster Using Cloud Shell

NOTE: Feel free to skip some of the steps if you already setup some of the items if you went through the instructions to setup a VM for class.

Once your Project is ready...

- Open the *Cloud Shell* by clicking the `>_` icon near the top right corner. It might take a few minutes if this is the first time. *Cloud Shell* is a Serverless shell that has your individual permissions (in this case you are a project owner), so it really simple and fast to run `gcloud` commands to deploy cloud services.

![alt text](https://github.com/UCB-w261/w261-environment/blob/master/gcp-images/cloud_shell.png "Cloud Shell")

- Enable APIs
```
gcloud services enable compute.googleapis.com
gcloud services enable dataproc.googleapis.com
```

- Choose a Region. I will show case with `us-central1`, but feel free to use any other available.
```
REGION=us-central1
```

- Create a Cloud Router.
```
gcloud compute routers create router-${REGION} \
  --project=${GOOGLE_CLOUD_PROJECT} \
  --region=${REGION} \
  --network=default
```

- Create a NAT Gateway
```
gcloud compute routers nats create nat-${REGION} \
  --router=router-${REGION} \
  --nat-all-subnet-ip-ranges \
  --region ${REGION} \
  --auto-allocate-nat-external-ips
```

- Enable Google Private Access in the subnet we will use for cluster
```
gcloud compute networks subnets update default \
  --region=${REGION} \
  --enable-private-ip-google-access 
```

- Create Cluster
```
gcloud dataproc clusters create w261 \
  --enable-component-gateway \
  --region ${REGION} \
  --subnet default \
  --no-address \
  --single-node \
  --master-machine-type n1-standard-4 \
  --master-boot-disk-size 100 \
  --image-version 2.0-debian10 \
  --optional-components JUPYTER \
  --project $GOOGLE_CLOUD_PROJECT \
  --max-idle 3600s \
  --async
```

Wait a few minutes until it's ready, it might take 3-5 minutes.

> NOTE: Add a `--max-idle 3600s` to the command above if you will store your notebooks in the Dataproc staging bucket, and have the data loaded in a personal GCS Bucket. This will terminate your cluster after 1 hr of being idle, keeping you on budget.

- Once you get back control at the prompt, run this command and click on the link to open your Jupyter Lab web interface.
```
gcloud dataproc clusters describe w261 --region ${REGION} | grep JupyterLab
``` 

### Things to know

- Once you open JupyterLab, navigate to the root folder where you see to folders: `GCS` and `Local Disk`. We will work on `Local Disk`.

- Locate the `media` folder once you are in `Local Disk`, and clone the main repo in `Local Disk/media`. You can use the GitHub integration for JupyterLab or you can open a terminal inside Jupyter, change directory to `media` and then `git clone ...`

- When working on a Notebook, get the full path where this notebook is located, and then add a new cell at the very top like this one:
```
%cd /full/path/to/the/notebook
```

- To get the data for the HWs, add a new cell and comment the previous command that pulled the data such as `!curl`, `!wget` and similar, and obtain the data now from here:
```
!mkdir -p data/
!gsutil cp gs://w261-hw-data/main/Assignments/HW2/data/* data/
```
Feel free to explore where the data is for a specific HW with `gsutil ls gs://w261-hw-data/main/Assignments/HW*`

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
  
