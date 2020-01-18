# Setting Up your VM for Hadoop

## GCP Credits

Here is the URL you will need to access in order to request a Google Cloud Platform coupon. You will be asked to provide your school email address and name. An email will be sent to you to confirm these details before a coupon is sent to you:

- You will be asked for a name and email address, which needs to match the domain. A confirmation email will be sent to you with a coupon code.
- You can request a coupon from the URL and redeem it until: 5/6/2020
- Coupon valid through: 1/6/2021
- You can only request ONE code per unique email address.
- Please contact me if you have any questions or issues.

## Create your Instance

1. Log into you Google Cloud Console with you `berkeley.edu` using this link:

[GCP Console](http://console.cloud.google.com "Google Cloud")

2. Click on the Cloud Shell icon

![alt text](https://github.com/UCB-w261/w261-environment/tree/master/setup-new-hadoop-env/cloud_shell.png "Cloud Shell")

3. It might take a few minutes if it's the first time. Pay attention what `Project ID` is showing on top of the Cloud Shell window. This should match what you setup on your `gcloud init` configuration. Run the following command:

```
gcloud beta compute instances create w261-hadoop \
  --machine-type=n1-standard-4 \
  --subnet=default \
  --network-tier=PREMIUM \
  --metadata=startup-script=\#\!/bin/bash$'\n'$'\n'./home/idle-shutdown.sh \
  --maintenance-policy=MIGRATE \
  --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
  --tags=http-server,https-server \
  --image=image-w261-hadoop-shutdown \
  --image-project=w261-246901 \
  --boot-disk-size=50GB \
  --boot-disk-type=pd-standard \
  --boot-disk-device-name=w261-hadoop \
  --reservation-affinity=any \
  --zone us-central1-a
```
You might need to adjust the argument for `--zone`, again, to match what you set on `gcloud init`.

4. Close the Cloud Shell window by running `exit` once the you get the prompt back.

## Connect to Jupyter Lab

After the green check mark shows next to your newly instantiated VM, you can go back to your local Terminal shell window, Google Cloud Shell for Windows users, and run this command to connect to your VM:

```
gcloud compute ssh w261-hadoop \
  --ssh-flag="-L 8889:127.0.0.1:8889" \
  --ssh-flag="-L 8088:127.0.0.1:8088" \
  --ssh-flag="-L 19888:127.0.0.1:19888" \
  --ssh-flag="-L 4040:127.0.0.1:4040" \
  --ssh-flag="-L 41537:127.0.0.1:41537"
```

If is throwing you an error message that `GCP` cannot find the instance, it means that the project and/or zone on your Google Cloud SDK `gcloud init` setup and the VM do not match. Do not terminate your instance, re-run `gcloud init` and make them both match.

[Jupyter Lab](http://localhost:8889 "Click here to open Jupyter Lab")

Note: Make sure you don't have other services, like `jupyter notebook` or the w261 Docker container itself, running locally. You might be working in the wrong place.

## VM Automation

The instance contains a script that will spin the w261 Docker container at startup. If for some reason you think the service might be down, reboot the VM, or inside the VM `sudo docker ps` to check if the container is running, otherwise `sudo docker-compose -f /home/docker-compose.yml up`.

After 15 minutes of instance being idle, the same script will bring the Docker container down, and stop the instance from taking precious credits away from you.

![alt text](https://github.com/UCB-w261/w261-environment/tree/master/setup-new-hadoop-env/jupyter_lab_autosave.png)

Also, make sure this setting is active on Jupyter Lab, this way, even if you leave the instance unattended, chances of losing valuable progress are minimal.
