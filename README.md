# MIDS W261 - Cloudera Hadoop on Docker

---
This docker image consists of the Cloudera QuickStart image extended with miniconda, important python packages and Jupyter notebook configured with pyspark.

## Running this image on your machine

### Install Docker Engine
* Before we start using the image, please make sure the Docker Engine is installed on your machine.
* For instructions installing docker engine, refer to the link below:
> https://docs.docker.com/engine/installation/

* You can just stop at Step 1, i.e. "Install and Run Docker for Mac"
<br /><br />

### Pull the Docker Image
* Once you have the Docker Engine up and running, you can pull the **mids-cloudera-hadoop** image.

* You can navigate to the image at the Docker Hub link below:
> https://hub.docker.com/r/ankittharwani/mids-cloudera-hadoop/

* Refer to the Tags to find the latest image - usually it is the **latest** tag itself.

* On your machine, run the following command to pull the image:
```
docker pull ankittharwani/mids-cloudera-hadoop
```
<br />

### Create a Docker container with the pulled image
Once you have the Docker image pulled, you can create a container in one of the following two ways:

1. Create a container with the following command in your terminal:

```
docker run --hostname=quickstart.cloudera \
           --privileged=true \
           --name=cloudera \
           -t -i -d \
           -p 8889:8889 \
           -p 8887:8888 \
           -p 7180:7180 \
           -p 8088:8088 \
           -p 8042:8042 \
           -p 10020:10020 \
           -p 19888:19888 \
           -v <host-path-to-mount-inside-container>:/media/notebooks \
           ankittharwani/mids-cloudera-hadoop:latest \
           bash -c '/root/startup.sh; /usr/bin/docker-quickstart'
```
> `<host-path-to-mount-inside-container>` is the path on your local drive which would be made available inside the docker. This will also be the default notebook directory within Jupyter.

2. Use the docker-compose.yml file to start your container:

```
$ cd /path/to/docker-compose.yml
$ docker-compose up -d
```

The ports in the above terminal command may differ from those in the docker-compose.yml file. Feel free to add or remove ports as needed. For more details, you can refer to:
> https://www.cloudera.com/documentation/enterprise/5-6-x/topics/quickstart_docker_container.html

* Once you've created the container and has been ran, you can check running status by:
```
docker ps
```
<br />

### Accessing the container

* One of the configurations you can do on your host machine is to add a new hosts entry. This makes all reference to http://quickstart.cloudera/ resolve to http://localhost automatically.
Add **127.0.0.1 quickstart.cloudera** to **/etc/hosts**

* Important URLs:
	* Jupyter Notebook: http://quickstart.cloudera:8889
	* Resource Manager: http://quickstart.cloudera:8088
	* Node Manager: http://quickstart.cloudera:8042
	* MapReduce Job History Server: http://quickstart.cloudera:19888
	* Cloudera Manager (if enabled): http://quickstart.cloudera:7180
	* Hue (if enabled, details below): http://quickstart.cloudera:8887

* Once the container has been created, you can login to it (launch bash terminal):
```
docker exec -ti cloudera /bin/bash
```

* You can also run a few hadoop commands to test everything is okay:
```
[root@quickstart /]# hdfs dfs -ls /
Found 5 items
drwxrwxrwx   - hdfs  supergroup          0 2016-04-06 02:26 /benchmarks
drwxr-xr-x   - hbase supergroup          0 2017-01-24 20:49 /hbase
drwxrwxrwt   - hdfs  supergroup          0 2017-01-24 20:50 /tmp
drwxr-xr-x   - hdfs  supergroup          0 2016-04-06 02:27 /user
drwxr-xr-x   - hdfs  supergroup          0 2016-04-06 02:27 /var
```

* With the current Cloudera Docker image, you should also be able to access Hue, which is a web based interface to Hive/Impala/HDFS etc. To access:

> http://localhost:8887/

You can replace **8887** with the **hue-port** configured above

Username: cloudera

Password: cloudera
<br /><br />

### Conda and Python Packages

* The following python packages are installed under Conda:
	* bokeh
	* cython
	* ipython
	* ipython_genutils
	* ipython-qtconsole
	* ipython-notebook
	* libpng
	* jupyter
	* mrjob
	* nltk
	* notebook
	* numpy
	* pandas
	* pip
	* scipy
	* scikit-learn
	* scikit-image
	* setuptools
	* sympy
	* wheel
	* unicodecsv
	* ujson
	* zlib

* To use the miniconda environment outside of the notebook:
```
source /opt/anaconda/bin/activate
```


* To use all python packages (esp. numpy) within hadoop:
```
Add the following parameter to Map Reduce Streaming commands:
-cmdenv PATH=/opt/anaconda/bin:$PATH

Add the following parameter to MRJob commands:
--cmdenv PATH=/opt/anaconda/bin:$PATH
```

* To use PySpark within Jupyter, below is a sample notebook:
http://nbviewer.jupyter.org/urls/dl.dropbox.com/s/l4auzjcykgqirl0/PySpark%20Example.ipynb
