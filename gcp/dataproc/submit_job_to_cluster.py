#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Sample command-line program for listing Google Dataproc Clusters"""

import argparse
import os

from google.cloud import storage
import googleapiclient.discovery

DEFAULT_FILENAME = 'pyspark_sort.py'


def get_default_pyspark_file():
    """Gets the PySpark file from this directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(current_dir, DEFAULT_FILENAME), 'rb')
    return f, DEFAULT_FILENAME


def get_pyspark_file(filename):
    f = open(filename, 'rb')
    return f, os.path.basename(filename)


def upload_pyspark_file(project_id, bucket_name, filename, file):
    """Uploads the PySpark file in this directory to the configured
    input bucket."""
    print('Uploading pyspark file to GCS')
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(file)


def download_output(project_id, cluster_id, output_bucket, job_id):
    """Downloads the output file from Cloud Storage and returns it as a
    string."""
    print('Downloading output file')
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(output_bucket)
    output_blob = (
        'google-cloud-dataproc-metainfo/{}/jobs/{}/driveroutput.000000000'
        .format(cluster_id, job_id))
    return bucket.blob(output_blob).download_as_string()


# [START create_cluster]
def create_cluster(dataproc, project, zone, region, cluster_name,
                   instance_type, master_nodes, worker_nodes):
    print('Creating cluster...')
    zone_uri = \
        'https://www.googleapis.com/compute/v1/projects/{}/zones/{}'.format(
            project, zone)
    cluster_data = {
        'projectId': project,
        'clusterName': cluster_name,
        'config': {
            'gceClusterConfig': {
                'zoneUri': zone_uri,
                "metadata": {
                    "CONDA_PACKAGES": "\"numpy pandas\"",
                    "MINICONDA_VARIANT": "3",
                    "MINICONDA_VERSION": "latest"
                }
            },
            "softwareConfig": {
                'properties': {
                    'spark:spark.jars.packages': 'graphframes:graphframes:0.7.0-spark2.3-s_2.11,com.databricks:spark-avro_2.11:4.0.0'
                }
            },
            'masterConfig': {
                'numInstances': master_nodes,
                'machineTypeUri': instance_type
            },
            'workerConfig': {
                'numInstances': worker_nodes,
                'machineTypeUri': instance_type
            },
            "initializationActions": [
                {
                    "executableFile": "gs://dataproc-initialization-actions/conda/bootstrap-conda.sh"
                },
                {
                    "executableFile": "gs://dataproc-initialization-actions/conda/install-conda-env.sh"
                }
            ]
        }
    }
    result = dataproc.projects().regions().clusters().create(
        projectId=project,
        region=region,
        body=cluster_data).execute()
    return result
# [END create_cluster]


def wait_for_cluster_creation(dataproc, project_id, region, cluster_name):
    print('Waiting for cluster creation...')

    while True:
        result = dataproc.projects().regions().clusters().list(
            projectId=project_id,
            region=region).execute()
        cluster_list = result['clusters']
        cluster = [c
                   for c in cluster_list
                   if c['clusterName'] == cluster_name][0]
        if cluster['status']['state'] == 'ERROR':
            raise Exception(result['status']['details'])
        if cluster['status']['state'] == 'RUNNING':
            print("Cluster created.")
            break


# [START list_clusters_with_detail]
def list_clusters_with_details(dataproc, project, region):
    result = dataproc.projects().regions().clusters().list(
        projectId=project,
        region=region).execute()
    cluster_list = result['clusters']
    for cluster in cluster_list:
        print("{} - {}"
              .format(cluster['clusterName'], cluster['status']['state']))
    return result
# [END list_clusters_with_detail]


def get_cluster_id_by_name(cluster_list, cluster_name):
    """Helper function to retrieve the ID and output bucket of a cluster by
    name."""
    cluster = [c for c in cluster_list if c['clusterName'] == cluster_name][0]
    return cluster['clusterUuid'], cluster['config']['configBucket']


# [START submit_pyspark_job]
def submit_pyspark_job(dataproc, project, region,
                       cluster_name, bucket_name, filename):
    """Submits the Pyspark job to the cluster, assuming `filename` has
    already been uploaded to `bucket_name`"""
    job_details = {
        'projectId': project,
        'job': {
            'placement': {
                'clusterName': cluster_name
            },
            'pysparkJob': {
                'mainPythonFileUri': 'gs://{}/{}'.format(bucket_name, filename)
            }
        }
    }
    result = dataproc.projects().regions().jobs().submit(
        projectId=project,
        region=region,
        body=job_details).execute()
    job_id = result['reference']['jobId']
    print('Submitted job ID {}'.format(job_id))
    return job_id
# [END submit_pyspark_job]


# [START delete]
def delete_cluster(dataproc, project, region, cluster):
    print('Tearing down cluster')
    result = dataproc.projects().regions().clusters().delete(
        projectId=project,
        region=region,
        clusterName=cluster).execute()
    return result
# [END delete]


# [START wait]
def wait_for_job(dataproc, project, region, job_id):
    print('Waiting for job to finish...')
    while True:
        result = dataproc.projects().regions().jobs().get(
            projectId=project,
            region=region,
            jobId=job_id).execute()
        # Handle exceptions
        if result['status']['state'] == 'ERROR':
            raise Exception(result['status']['details'])
        elif result['status']['state'] == 'DONE':
            print('Job finished.')
            return result
# [END wait]


# [START get_client]
def get_client():
    """Builds an http client authenticated with the service account
    credentials."""
    dataproc = googleapiclient.discovery.build('dataproc', 'v1')
    return dataproc
# [END get_client]


def main(project_id, zone, cluster_name, bucket_name,
         instance_type, master_nodes, worker_nodes,
         pyspark_file=None, create_new_cluster=True):
    dataproc = get_client()
    region = 'global'
    try:
        if pyspark_file:
            spark_file, spark_filename = get_pyspark_file(pyspark_file)
        else:
            spark_file, spark_filename = get_default_pyspark_file()

        if create_new_cluster:
            create_cluster(
                dataproc, project_id, zone, region, cluster_name,
                instance_type, master_nodes, worker_nodes)
            wait_for_cluster_creation(
                dataproc, project_id, region, cluster_name)

        upload_pyspark_file(
            project_id, bucket_name, spark_filename, spark_file)

        cluster_list = list_clusters_with_details(
            dataproc, project_id, region)['clusters']

        (cluster_id, output_bucket) = (
            get_cluster_id_by_name(cluster_list, cluster_name))

        # [START call_submit_pyspark_job]
        job_id = submit_pyspark_job(
            dataproc, project_id, region,
            cluster_name, bucket_name, spark_filename)
        # [END call_submit_pyspark_job]
        wait_for_job(dataproc, project_id, region, job_id)

        output = download_output(project_id, cluster_id, output_bucket, job_id)
        print('Received job output {}'.format(output))
        return output
    finally:
        if create_new_cluster:
            delete_cluster(dataproc, project_id, region, cluster_name)
        spark_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
            '--project_id', 
            help='Project ID you want to access.',
            required=True
        ),
    parser.add_argument(
            '--zone',
            help='Zone to create clusters in/connect to.',
            required=True
        ),
    parser.add_argument(
            '--cluster_name',
            help='Name of the cluster to create/connect to',
            required=True
        )
    parser.add_argument(
            '--gcs_bucket',
            help='Bucket to upload Pyspark file to',
            required=True
        )
    parser.add_argument(
            '--pyspark_file',
            help='Pyspark filename. Defaults to pyspark_sort.py'
        )
    parser.add_argument(
            '--create_new_cluster',
            action='store_true',
            help='States if the cluster should be created'
        )
    parser.add_argument(
            '--key_file',
            help='Location of your key file for service account'
        )
    parser.add_argument(
            '--instance_type',
            help='Instance types used for this cluster',
            default='n1-standard-4'
        )
    parser.add_argument(
            '--master_nodes',
            help='Number of master nodes',
            default=1
        )
    parser.add_argument(
            '--worker_nodes',
            help='Number of worker nodes',
            default=2
        )

    args = parser.parse_args()

    if args.key_file is not None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.key_file

    main(
        args.project_id, args.zone, args.cluster_name,
        args.gcs_bucket, args.instance_type, args.master_nodes, args.worker_nodes,
        args.pyspark_file, args.create_new_cluster)
