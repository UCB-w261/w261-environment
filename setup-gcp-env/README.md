# Setting Up your VM for Hadoop/Spark

## GCP Credits

GCP is offering $300 in credits for new accounts. Strongly recommended to use your `berkeley.edu` account, otherwise use another Google Account (gmail) if you already used the offer.

## Create your Instance

1. Log into you Google Cloud Console with you `berkeley.edu` using this link:

[GCP Console](http://console.cloud.google.com "Google Cloud")

2. Create a new Project, if you don't have one, by clicking the box next to "Google Cloud Platform" on the top blue bar of the screen. Then click on "New Project" in the top right corner of the popup screen. Follow the prompts.

![alt text](https://github.com/UCB-w261/w261-environment/blob/master/gcp-images/project-id.png "Project ID")

3. Click on the Cloud Shell icon.

![alt text](https://github.com/UCB-w261/w261-environment/blob/master/gcp-images/cloud_shell.png "Cloud Shell")

4. It might take a few minutes if it's the first time. Pay attention what `Project ID` is showing on top of the Cloud Shell window. This should match when you setup your `gcloud init` configuration locally (see the [Jupyter Lab section below](#Connect-to-Jupyter-Lab) for more details on `gcloud init`). If you don't see a project id in the output from the Cloud Shell, then you need to select a project in your web console by clicking the item circled in red as shown in the image from Step 2.

The real project id is obtained in the pop-up window.

5. Run the following command:

```
gcloud compute instances create w261 \
  --project=$GOOGLE_CLOUD_PROJECT \
  --zone=us-central1-a \
  --machine-type=n2-standard-4 \
  --network-interface=subnet=default,no-address \
  --maintenance-policy=MIGRATE \
  --create-disk=auto-delete=yes,boot=yes,device-name=w261,image=projects/w261-trusted-images/global/images/w261-image,mode=rw,size=10 \
  --no-shielded-secure-boot \
  --shielded-vtpm \
  --shielded-integrity-monitoring \
  --reservation-affinity=any
```

You might need to adjust the argument for `--zone`, again, to match what you set on `gcloud init`.

Note: If using an account other than your `berkeley.edu`, drop the `--create-disk` line, and follow the instructions in step 8 to install Docker and Docker Compose once you are inside the VM:

6. Close the Cloud Shell window by running `exit` once you get the prompt back.

7. GCP isolates your VM from the outside world if you don't provide an External IP to your VM. This is the setup that we want to follow best practices in Cloud Security. We could always get tighter, but it's enough to keep unwanted Crypto-Miners out of your VM.
   Setup a NAT Gateway to open a secure channel for your VM to access the internet. This is needed for updating the Debian packages, install Docker, clone your repos, etc.

- Go to [console](console.cloud.google.com) Main Menu -> Networking -> Network Services -> Cloud NAT. Click on the "Get Started" button in the central window.
- Name it `nat-us-central-1`
- Select `default` network
- Region `us-central1`, or the one that matches your VM region
- Create a new Cloud Router
    - Name it `router-us-central1`
    - Keep default values for the rest of the settings
    - Create Cloud Router
- Keep default values for the rest of the settings
- Create NAT Gateway
- Make sure the NAT gateway is shown as `Running` before completing the next steps.

8. OPTIONAL: Install Docker if needed (i.e. if you are using a non-Berkeley gmail).

* [Install Docker](https://docs.docker.com/engine/install/debian/ "Install Docker")
* [Install Docker Compose](https://docs.docker.com/compose/install/ "Install Docker Compose")

9. Go to the main menu -> Compute Engine. Once the VM is showing as `Running`, click on the SSH button showing on the right. Click on "Connect".

10. As a best practice, you should always run an update on your VM. Since it's a Debian distro, run the following command:

```
sudo apt-get update
```

11. Run this command in order to be able to run `docker` without `sudo`:

```
sudo usermod -aG docker $USER
```

  - Type `exit` and re-open the web-SSH in order to put the change into effect.
  - OPTIONAL: Test by running `docker run hello-world`

12. Create 2 Environment Variables with the values from `id` command:

```
id

# Number showing for the UID
export ID=1001

# Number showing for the GID
export GID=1000
```

12a. Only for berkeley.edu accounts. Create your `docker-compose.yaml` file.
```
cat ../w261/docker-compose.tmp | envsubst > docker-compose.yaml
```

12b. Copy and run the following command in the web-SSH:
```
cat > docker-compose.yaml << EOF
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
EOF
```

13. Confirm you don't have missing values in the yaml:

```
cat docker-compose.yaml
```

14. Test it!
```
docker-compose up
```

15. Exit container by pressing `ctrl + c`, and exit shell by typing `exit`.

## Non-Google-Workspace Accounts

This goes mostly for students that had to use their `gmail` account in order to get the credits.

1. Find you ssh Public Key, typically in `~/.ssh/google_compute_engine.pub`

2. Upload the key to the Metadata server:
```
gcloud compute os-login ssh-keys add \
    --project PROJECT_ID \
    --key-file /home/$USER/.ssh/google_compute_engine.pub
```

3. Specify key, if necessary, when ssh'ing to the VM:
```
gcloud compute ssh w261 --ssh-key-file=/home/$USER/.ssh/google_compute_engine ...
```

## Connect to Jupyter Lab
### Important: Use your local computer for the rest of the steps.

1. Install Google Cloud SDK, follow the instructions that correspond to your system:

[MacOS](https://cloud.google.com/sdk/docs/install#mac "MacOS")

[Windows](https://cloud.google.com/sdk/docs/install#windows "Windows")

[Linux](https://cloud.google.com/sdk/docs/install#linux "Linux")

2. Open your Terminal (MacOS, Linux) or click on the Google Cloud SDK icon installed in your Desktop (Windows)

3. Run `gcloud init` to authenticate and configure Project, Zone, etc. Follow the prompts.

4. SSH into your VM with this command:
```
gcloud compute ssh w261 --ssh-flag="-L 8889:127.0.0.1:8889" --ssh-flag="-L 4040:127.0.0.1:4040"
```

Note: If it's throwing you an error message that `GCP` cannot find the instance, it means that the project and/or zone on your Google Cloud SDK `gcloud init` setup and on the VM do not match. Do not terminate your instance, re-run `gcloud init` and make them both match. As an alternative, you can set the project and zone directly, without having to re-run gcloud init, with the commands:

`gcloud config set project [my-project-id]`

`gcloud config set compute/zone us-central1-a`

Make sure you run either or both, if necessary, where you installed the Google Cloud SDK locally. Project `w261-trusted-images` is only acting as a resource to share the disk image needed to deploy your instance with the right tools for class. You should use/create your own project.

After you connect successfully to your VM, you should get the instance prompt at your user home folder, showing like:

`your-username@w261:~$`

Here is the best place to `git clone https://github.com/UCB...` the repos needed for HW and to run the demos. This operation is only needed once. Afterwards, you only need to `git pull` or go through the process of committing and pushing changes explained in week 1.

For students using Windows, the Google Cloud SDK opens a PuTTY window, sometimes might be behind your active windows.

5. You might need to repeat Steps 7-10 from above if a different user is created in the VM (most likely this will happen). Either or, re-launch your container by running:
```
docker-compose up
```

6. Open Jupyter by clicking the link below:

[Jupyter Lab](http://localhost:8889 "Click here to open Jupyter Lab")

Note: Make sure you don't have other services, like `jupyter notebook` or the w261 Docker container itself, running locally. You might be working in the wrong place.

## Discipline

Remember, these are your credits, make the most of them. Please be responsible and make sure you turn off your instance after a stopping point. You will be consuming around $50 a month if instance left on.
