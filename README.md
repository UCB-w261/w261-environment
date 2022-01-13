# Docker FAQ

## What is Docker? 

Docker is a container management platform for automating deployments of re-usable environemnets. 
https://towardsdatascience.com/learn-enough-docker-to-be-useful-b7ba70caeb4b

## What are Containers? Containers vs VM

Containers are a type of virtualization. They virtualize environments at the operating system level by sharing the base libraries. This removes the need for boot drives and hardware interfaces for each environment. This makes a container use much less resources than a virtual machine (VM) which can make environments more efficient because lack of duplication of resources.

![alt text](http://zdnet2.cbsistatic.com/hub/i/r/2017/05/08/af178c5a-64dd-4900-8447-3abd739757e3/resize/770xauto/78abd09a8d41c182a28118ac0465c914/docker-vm-container.png "Container vs VM")

## Why Docker?

Using Docker we can keep a fresh deployment of our Hadoop/Jupyter/Spark environment readily avaliable. Taking around 2 minutes to remove and launch a new environment with the same initial configuration everytime.

## Installing Docker

Download Docker Community Edition from [Docker](https://docs.docker.com/engine/installation/ "Docker Install Documentation")

## Things to know

We will use `docker-compose` to deploy our container with the proper configuration of user ownership, volume mounts, etc.

- version: this item says use v3 syntax
- services: list of containers
  - spark: the name of a container, the label being spark
    - image: use this base container
    - hostname: DNS name for the container
    - privledged: allow access to other machines such as the local machine
    - user: root user privileges
    - environment:
      - values to not conflict ownership of files both inside and outisde the container
    - commands: runs this commands on start
    - ports: map ports so that services running on the container are accessible from the local computer
      - remote port:local port
    - tty: allow a shell to be initiated
    - stdin_open: allow interactivity with the shell
    - volumes: location to map from local computer to the docker container so they can share. 
      - /local/path:/media/notebook

```
version: '3'
services:
  spark:
    image: jupyter/pyspark-notebook
    hostname: docker.w261
    privileged: true
    user: root
    environment:
      - NB_USER=$USER
      - CHOWN_HOME=yes
      - GRANT_SUDO=yes
      - NB_UID=$ID
      - NB_GID=$GID
    command: bash -c "start.sh jupyter lab --ServerApp.token='' --ServerApp.authenticate_prometheus=False --ServerApp.port=8889"
    ports:
      - "8889:8889"
      - "4040:4040"
    tty: true
    stdin_open: true
    volumes:
      - .:/home/$USER
```

[This only apply to linux-based systems]
If you are planning to use this locally, copy the yaml text from above into `temp-docker.yaml`, then inject the environment variables with the following commands:

```
#IF YOU DON'T HAVE UID OR GID ENV VARS, RUN THIS COMMAND. SKIP OTHERWISE.
export $(id | cut -d ' ' -f 1,2 | sed -e 's/([^()]*)//g' | tr '[:lower:]' '[:upper:]')

eval "echo \"$(sed 's/"/\\"/g' temp-docker.yaml)\"" > docker-compose.yaml

#SAFELY REMOVE TEMP YAML
rm temp-docker.yaml
```

## NOTE: For all notebooks related to Hadoop, please follow this instructions to create a Dataproc cluster.

[Create a Dataproc cluster](https://github.com/UCB-w261/w261-environment/create-dataproc-cluster/README.md)]

## How to Use

1. Install Docker (Restart as needed)
2. Go to your class repo folder on your computer
3. Run `docker-compose up`
4. Open your browser and go to `localhost:8889`

## General Issues

Using python packages against HDFS

Add the following parameter to Map Reduce Streaming commands:
`-cmdenv PATH=/opt/anaconda/bin:$PATH`

### Hostname mapping

Apply the `docker.w261` alias for `127.0.0.1` aka `localhost`
- Linux & Mac
  1. Open Terminal
  2. Open hostfile by running `sudo nano /etc/hosts`
  3. Append the following line, then save: `127.0.0.1    docker.w261`
  4. Refresh DNS with `sudo killall -HUP mDNSResponder`
- Windows:
  1. Open notepad as administrator (otherwise you'll not be able to save the file)
  2. Open `C:\Windows\System32\drivers\etc\hosts` in notepad.  Note the file has no extension
  3. Append the following line, then save: `127.0.0.1    docker.w261`
  4. Refresh DNS by running `ipconfig /flushdns` in command prompt or powershell

*Note on Windows:*
> On win10, the hosts file is read only and can not be edited directly
> There are 2 methods to edit it in this case, 1) change the file to read/write and edit or 2) make a copy of the hosts file, move original out of way, then copy edited file to correct folder. Either method should work. 
> https://superuser.com/questions/958991/windows-10-cant-edit-hosts-file
  
### Minimum System Requirements for MIDS W261 Cloudera Hadoop Container

Docker needs 2 CPUs and 4 GB of RAM to ensure resource managers don't crash during normal operation. 
- Linux
  1. By default Docker shares the same resources as the local computer.
- Windows
  1. Right click Docker in the notification area
  2. Click Settings
  3. Click Advanced
  4. Slide Memory to 4096 MB
- Mac OS
  1. Click Docker in the menu bar (near day/time at top-right)
  2. Click Preferences
  3. Click Advanced
  4. Slide Memory to 4096 MB

### Using Spark inside the notebook

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

`spark` is the general session manager for dataframes and the newer style introduced in Spark 2.0

`sc` is a Spark context sets up internal services and establishes a connection to a Spark execution environment.

## Linux Issues

## Windows Issues
Running Docker in WSL: https://github.com/UCB-w261/w261-environment/wiki/Linux-on-Windows   
See the wiki for common issues: https://github.com/UCB-w261/w261-environment/wiki/Troubleshooting-Docker

### Minimum OS requirement

- Windows 10 Pro/Education is required to run Docker on Windows. A free license of Windows 10 Education is avaliable to all students through [UCB Software Central](https://software.berkeley.edu/operating-systems#Microsoft)

- See the wiki for common issues and solutions: https://github.com/UCB-w261/w261-environment/wiki/Troubleshooting-Docker

## Mac Issues

- Macs require a computer capable of virtualization to test this run `sysctl kern.hv_support` in a terminal.
  - If 1 then good to go
  - If 0 then you need a new computer

