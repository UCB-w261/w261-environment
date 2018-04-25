#!/usr/bin/env bash
EXISTS=`conda env list | grep "dataproc " | wc -l`
if [ $EXISTS -eq "0" ]
then
  conda create --name=dataproc python=3.6
  source activate dataproc
  pip install -r requirements.txt
fi

export PROJECTNAME=`gcloud config get-value project`
gcloud iam service-accounts create w261-service --display-name "w261-service"
# TODO not the best security: limit roles
gcloud projects add-iam-policy-binding $PROJECTNAME \
  --member serviceAccount:w261-service@$PROJECTNAME.iam.gserviceaccount.com \
  --role "roles/owner"

gcloud iam service-accounts keys create ~/key.json \
  --iam-account w261-service@$PROJECTNAME.iam.gserviceaccount.com

export GOOGLE_APPLICATION_CREDENTIALS=~/key.json
