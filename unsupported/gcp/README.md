## For additional walkthroughs, watch previous GCP Office Hour recordings.

You will need to login through the ISVC. Click on any recording to authenticate your zoom account. Then click these links:  
* First OH    
https://zoom.us/recording/play/rRDuG9DFGFZ8NNdkZL4SVGmlqcSARzvT3WA9ESH928Gdd0RfGYrVcbxm8UTPKgk8?continueMode=true   
* Second OH    
https://api.zoom.us/recording/play/RDDa_UeSzr7IDlMUkkO6furQ9IheCyTymdmDLoqaTgX2MmaSgv85wOMFa8M_zWCX

# Cloud Dataproc API Example

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=dataproc/README.md

Sample command-line programs for interacting with the Cloud Dataproc API.


Please see [the tutorial on the using the Dataproc API with the Python client
library](https://cloud.google.com/dataproc/docs/tutorials/python-library-example)
for more information.

Note that while this sample demonstrates interacting with Dataproc via the API, the functionality
demonstrated here could also be accomplished using the Cloud Console or the gcloud CLI.

`list_clusters.py` is a simple command-line program to demonstrate connecting to the
Dataproc API and listing the clusters in a region

`create_cluster_and_submit_job.py` demonstrates how to create a cluster, submit the
`pyspark_sort.py` job, download the output from Google Cloud Storage, and output the result.

`pyspark_sort.py_gcs` is the asme as `pyspark_sort.py` but demonstrates
 reading from a GCS bucket.

## Prerequisites to run locally:

* [pip](https://pypi.python.org/pypi/pip)

Go to the [Google Cloud Console](https://console.cloud.google.com).

Under API Manager, search for the Google Cloud Dataproc API and enable it.

## Set Up Your Local Dev Environment

To install, run the following commands. If you want to use  [virtualenv](https://virtualenv.readthedocs.org/en/latest/)
(recommended), run the commands within a virtualenv.

    * pip install -r requirements.txt

## Authentication

Please see the [Google cloud authentication guide](https://cloud.google.com/docs/authentication/).
The recommended approach to running these samples is a Service Account with a JSON key.

## Environment Variables

Set the following environment variables:

    GOOGLE_CLOUD_PROJECT=your-project-id
    REGION=us-central1 # or your region
    CLUSTER_NAME=waprin-spark7
    ZONE=us-central1-b

## Running the samples

To run list_clusters.py:

    python list_clusters.py $GOOGLE_CLOUD_PROJECT --region=$REGION

`submit_job_to_cluster.py` can create the Dataproc cluster, or use an existing one.
If you'd like to create a cluster ahead of time, either use the
[Cloud Console](console.cloud.google.com) or run:

    gcloud dataproc clusters create your-cluster-name

To run submit_job_to_cluster.py, first create a GCS bucket for Dataproc to stage files, from the Cloud Console or with
gsutil:

    gsutil mb gs://<your-staging-bucket-name>

Set the environment variable's name:

    BUCKET=your-staging-bucket
    CLUSTER=your-cluster-name

Then, if you want to rely on an existing cluster, run:

    python submit_job_to_cluster.py --project_id=$GOOGLE_CLOUD_PROJECT --zone=us-central1-b --cluster_name=$CLUSTER --gcs_bucket=$BUCKET

Otherwise, if you want the script to create a new cluster for you:

    python submit_job_to_cluster.py --project_id=$GOOGLE_CLOUD_PROJECT --zone=us-central1-b --cluster_name=$CLUSTER --gcs_bucket=$BUCKET --create_new_cluster

This will setup a cluster, upload the PySpark file, submit the job, print the result, then
delete the cluster.

You can optionally specify a `--pyspark_file` argument to change from the default
`pyspark_sort.py` included in this script to a new script.

