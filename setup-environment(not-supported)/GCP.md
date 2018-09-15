Setting-up W261 Docker on Google Cloud Platform Compute Engine Instance
=======================================================================

Why Bother Using a Cloud Instance in W261
-----------------------------------------
Why would you bother with all of the extra work outlined below when you can just set-up the W261 Class Image on your own machine? Three reasons:
1. You can connect to it from any machine that has a browser.
2. You can quickly scale your GCP resources according to the needs of the assignment. (This should probably be the top reason but nearly ubiquitous access is always useful. This will be your top reason, though, if you try to run the last Spark assignment on your own machine. _Consider yourself warned._)
3. You will feel _just a little bit more_ like a legit data scientist, if you don't already.
4. **(BONUS REASON)** You have GCP credits. Put them to use!


High Level Steps
----------------
1. Skim the Google Cloud [overview of using containers on Compute Engine](https://cloud.google.com/compute/docs/containers/).
   * You can ignore everything after "Installing Docker on Windows Server 2016 images". This set-up guide covers using Docker on a GCP Linux VM.
2. Ensure you complete all the pre-requisites (see below).
2. Set-up GCP and Linux VM (a pre-req but worth reiterating).
3. Download and install Docker CE.
4. Set-up the W261 class image.


Pre-requisites
--------------
* Access to GCP Compute Engine (see below)
* Set-up a Linux VM on Google GCP (see below)
* An appropriate browser, e.g. Google Chrome or Mozilla Firefox (I'll leave this to you)


GCP and Linux VM Set-up
-----------------------
1. First, set-up your local machine to interact with GCP. 
   * You already have a Google account through Berkeley. 
   * You need to install the [gcloud compute command-line tool](https://cloud.google.com/compute/docs/gcloud-compute/) on your local machine, which is part of the [Google Cloud SDK](https://cloud.google.com/sdk/). Installing Google Cloud SDK will install gcloud compute command-line tool.
2. Set-up a Linux VM instance on GCP. 
   * You will need to [create a GCP project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) and [enable billing](https://cloud.google.com/billing/docs/how-to/modify-project) for your project.
   * If you need to set-up a billing account, you can follow [these instructions](https://cloud.google.com/billing/docs/how-to/manage-billing-account).
   * You should have access to credits through MIDS. Please see one of your course instructors for details on how to obtain them. 
   * You can follow the [quickstart guide](https://cloud.google.com/compute/docs/quickstart-linux) or 
   * This more [detailed set of instructions](https://cloud.google.com/compute/docs/instances/create-start-instance).
   
   Keep in mind that, while the guides suggest various operating systems configurations, you can customize your instance to your liking. I found success in W261 using:
   * OS: Ubuntu 16.04
   * 2 vCPUs and 7.5 GB memory (to start)
   * _The class minimum is 2 CPUs and 4 GB RAM but I found the above to be a better minimum on GCP._
   * 150 GB Standard persistent disk (I used about half for W261 but I also made copies of certain directories to locations outside my GitHub repo directory)


Download and Install Docker CE
------------------------------
1. Skim the [Docker CE overview](https://docs.docker.com/install/).
   * I will cover installation on Ubuntu 16.04. For installation to other platforms follow the link corresponding to your OS, which may be found under "Supported platforms" on the page above (or use this [direct link](https://docs.docker.com/install/#supported-platforms)).
2. Follow the instructions to install Docker on Ubuntu 14.04 or above at [Install Docker CE](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce).
   * I recommend following the directions under [Install using the repository](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository).
3. Follow the [Post-installation steps for Linux](https://docs.docker.com/install/linux/linux-postinstall/) of your choosing.
   * I only recommend [Manage Docker as a non-root user](https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user) but others may want to do more. Proceed at your own risk because none of the other post-installation steps have been field tested.


Set-up the W261 Class Image
---------------------------
1. Follow the [instructions found on the W261 Environment repo](https://github.com/UCB-w261/w261-environment) beginning with "Pull the Class Image"
   * _**Do not reinstall Docker.**_ You have already completed this step.
   * See _**One important note about volumes**_ below **BEFORE you set-up your class Github repo**.
2. Configure your `docker-compose.yml` file. I found success using the following configuration:
```
version: '3'
services:
  quickstart.cloudera:
    image: w261/w261-environment:latest
    hostname: docker.w261
    privileged: true
    command: bash -c "/root/start-notebook.sh;/usr/bin/docker-quickstart"
    ports:
      - "8887:8888"   # Hue server
      - "8889:8889"   # jupyter
      - "10020:10020" # mapreduce job history server
      - "8022:22"     # ssh
      - "7180:7180"   # Cloudera Manager
      - "11000:11000" # Oozie
      - "50070:50070" # HDFS REST Namenode
      - "50075:50075" # hdfs REST Datanode
      - "8088:8088"   # yarn resource manager webapp address
      - "19888:19888" # mapreduce job history webapp address
      - "8983:8983"   # Solr console
      - "8032:8032"   # yarn resource manager access
      - "8042:8042"   # yarn node manager
      - "60010:60010" # hbase
      - "4040:4040"   # Spark UI
      - "8080:8080"   # Hadoop Job Tracker
    tty: true
    stdin_open: true
    volumes:
      #- .:/media/notebooks
      - /home/my_username/w261:/media/notebooks
```

   * _my_username_ corresponds to your the Linux user you created for yourself on your GCP Linux VM.
   * _**One important note about volumes:**_ the path that you specify before the `:` in the argument above, e.g. mine is `/home/my_username/w261` becomes your default "base" directory when you launch JupyterLab. If you want to be able to navigate to other directories above your GitHub directory from JupyterLab, be sure to install your GitHub directory 
   
3. Disconnect from your instance and reconnect using the following command: `gcloud compute --project "your_project_name" ssh --ssh-flag="-L 8889:127.0.0.1:8889" --ssh-flag="-L 8088:127.0.0.1:8088" --ssh-flag="-L 19888:127.0.0.1:19888" --ssh-flag="-L 4040:127.0.0.1:4040" --ssh-flag="-L 41537:127.0.0.1:41537" --zone "zone_of_your_instance" "your_instance_name"` where:
   * _your_project_name_ corresponds to your GCP project
   * _zone_of_your_instance_ corresponds to the zone of your GCP instance, e.g. mine was `us-east1-b`
   * _your_instance_name_ corresponds to the name of your instance.

   You can vary the ports that you open using the `--ssh-flag` argument. Opening all of the ports above should guarantee full functionality for JupyterLab, Hadoop, and Spark for W261's purposes. 

4. Follow the W261 Environment Repo instructions under "How to Use".

5. Enjoy and good luck in W261!

If you run into any trouble with any of the above, please contact the W261 class image administrator at `ADD EMAIL ADDRESS HERE` or post a question to `ADD REFERENCE TO APPROPRIATE SLACK CHANNEL`.