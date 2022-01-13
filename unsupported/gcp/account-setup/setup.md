For the below, run it on your computer and not in the Docker container. Remember that docker containers are immutable, so if you create a new one it'll delete everything you had installed previously.
1. Download gcloud command line
  - Windows https://cloud.google.com/sdk/docs/downloads-interactive#windows
  - Mac https://cloud.google.com/sdk/docs/downloads-interactive#mac
  - Linux (source) https://cloud.google.com/sdk/docs/downloads-interactive#linux
  - Linux (apt-get) https://cloud.google.com/sdk/docs/downloads-apt-get
  - Linux (yum) https://cloud.google.com/sdk/docs/downloads-yum
2. For the remainder of the instructions you'll be using bash or some bash emulator on windows such as git bash
3. Update gcloud to latest version `gcloud components update`   Note: this can take longer than you would expect
4. `gcloud auth login` use your `@Berkeley.edu` email since that's the account your funds are connected to.
5. Once authenticated run `gcloud projects list` and get the `project_id` associated with your project
6. Using the project_id from prior step run `gcloud config set project $PROJECT_ID`
7. Create a bucket with a name that you want. These names are unique across all of google, not just your account.  `gsutil mb gs://${BUCKET_NAME}/`. You can read more about best practices for naming buckets in the [documentation here](https://cloud.google.com/storage/docs/naming#requirements).
8. Create a service account which we'll run jobs with, instead of your root user. `gcloud iam service-accounts create sa-dataproc --display-name "[SA-DataProc]"`
9. Review that service account was created `gcloud iam service-accounts list`
10. Add the `role/dataproc.worker` role to the service account. `gcloud projects add-iam-policy-binding ${PROJECT_ID} --member serviceAccount:sa-dataproc@${PROJECT_ID}.iam.gserviceaccount.com --role roles/dataproc.worker` see https://cloud.google.com/dataproc/docs/concepts/iam/iam for details about the access level this service account has.
11. Add the `role/dataproc.editor` role to the service account. `gcloud projects add-iam-policy-binding ${PROJECT_ID} --member serviceAccount:sa-dataproc@${PROJECT_ID}.iam.gserviceaccount.com --role roles/dataproc.editor` see https://cloud.google.com/dataproc/docs/concepts/iam/iam for details about the access level this service account has.
12. Create an access key (this needs to be kept secret, do not commit to your repo) `gcloud iam service-accounts keys create $HOME/w261.json --iam-account sa-dataproc@${PROJECT-ID}.iam.gserviceaccount.com`
13. Enable the DataProc API by running `gcloud services enable dataproc.googleapis.com`
14. Create a new virtual environment however you would like and source this environment. If you don't know what this means use anaconda and see these instructions https://conda.io/docs/user-guide/tasks/manage-environments.html
15. cd to the w261-environment repo and go to the folder w261-environment/gcp-files/dataproc
16. `pip install -r requirements.txt`
17. Run our test script `python submit_job_to_cluster.py --project_id=${PROJECT_ID} --zone=us-central1-b --cluster_name=${SOME_NAME} --gcs_bucket=${BUCKET_CREATED_EARLIER_NAME} --key_file=$HOME/w261.json --create_new_cluster --pyspark_file=pyspark_sort.py` Note: cluster names need to start with a letter and be lowercase + numbers only
18. You should seem some nice output from the cluster after a few minutes when the job has run
19. To review logs go to `Jobs` in the `DataProc` UI on Google Cloud console
