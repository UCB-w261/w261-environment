# w261 Environment (Under Construction)
## Overview

## Google Cloud Dataproc
### Overview
### Why Dataproc?
### Redeem Credits on GCP
### Automated Orchestration using GCP CloudShell

## GitHub Repository
### Overview
### Creating Personal Repository
### Automation using GCP CloudShell

## Using Hadoop inside the Jupyter Notebook
## Using Spark inside the Jupyter Notebook

```
from pyspark.sql import SparkSession
app_name = "example_notebook"
master = "local[*]"
spark = SparkSession\
        .builder\
        .appName(app_name)\
        .master(master)\
        .getOrCreate()
sc = spark.sparkContext
```

`spark` is the general Session Manager for dataframes.

`sc` is a Spark context sets up internal services and establishes a connection to a Spark execution environment.
