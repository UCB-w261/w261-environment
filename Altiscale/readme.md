Altiscale
=========
https://documentation.altiscale.com/configure-ssh-from-mac-linux   
- Generate a SSH key pair
- Upload your Public Key to the Big Data Services Portal
- Set your SSH Configuration
- Download the Big Data Services's PAC file
- Configure your system for Proxy Auto Configuration


SSH Setup
---------

### SSH Key Creation

### Config File

You'll need to create a config file at `~/.ssh/config` with the following contents:

```
Host altiscale
     User <your altiscale username>
     Hostname ia.z42.altiscale.com
     Port 1589
     IdentityFile ~/.ssh/id_rsa
     Compression yes
     ServerAliveInterval 30
     TCPKeepAlive yes
     DynamicForward localhost:1080
     LocalForward <your assigned port> localhost:<your assigned port>
```

Environment Setup
-----------------

### Getting Setup Script

Use wget to download script from the master branch of the environment repo:

```
wget https://raw.githubusercontent.com/UCB-w261/w261-environment/master/Altiscale/runner.sh
```

### Running Setup Script

First make sure the script is executable:

```
chmod +x ./runner.sh
```

Then, from `./runner.sh -h`

```
How to use:
    Initial setup: ./runner.sh -s -p <port>
    Initial setup and run: ./runner.sh -sr -p <port>
    Run Notebook environment after setup: ./runner.sh -r
```

### What the `runner.sh` Setup Script Does

Be advised that the `runner.sh` script will, among other things, create a `~/.mrjob.conf` file in your home directory. This mrjob config file will set the `python_bin` property for MRjob, so you must NOT set that when you run MRjob with Hadoop. The `~/.mrjob.conf` will also set the `py_files` option to point to a zip archive of a Python virtual environment which will be added to all of the jobs' `PYTHONPATH`. Setting this property will eliminate the need to set the `PATH` option. This is contrary to the way you may be used to when using mrjob in the Docker container environment during the earlier part of this course. Read the mrjob documentation at https://pythonhosted.org/mrjob/guides/configs-all-runners.html for further details on these and other configuration options.

To summarize, here are some examples illustrating the differences between the environments on the course Docker container versus the Altiscale environment:

#### Previous method on W261 Docker Container:

```
!python similarity.py -r hadoop --cmdenv PATH={PATH} --python-bin /opt/anaconda/bin/python systems_test_index_1 > systems_test_similarities_1
```

#### New (example) method on Altiscale environment:

```
MOST_FREQUENT_20FILES = "{OUTPUT_PATH_BASE}/data/most_frequent_20files".format(OUTPUT_PATH_BASE=OUTPUT_PATH_BASE)
!hadoop fs -rm -r {MOST_FREQUENT_20FILES}
!python mostFrequentWords.py hdfs://{TEST_20} \
    -r hadoop \
    --output-dir={MOST_FREQUENT_20FILES} \
    --no-output
```

Be advised that the above is just an example for illustrative purposes and that your final implementation may differ (such as custom options you may choose to pass in to mrjob). The main takeaways are that the `--cmdenv PATH={PATH} --python-bin ...` options must NOT be set, as that is handled by `~/.mrjob.conf`, and that the `--output-dir=...` and `--no-output` options MUST be set.
