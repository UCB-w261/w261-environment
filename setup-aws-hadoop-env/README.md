# Setting Up your VM for Hadoop using AWS

## AWS Free-Tier Account

Follow the link to create your own AWS Free-Tier Account. You are free to use an existing account if you already have one.

[AWS Free-Tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc)

## AWS Educate

Follow the link to explore the AWS Educate account. You will need an `.edu` email.

[AWS Educate](https://aws.amazon.com/education/awseducate/)

## Create your Instance

### 1. Log into you AWS account using this link:

[AWS Console](https://signin.aws.amazon.com/signin?redirect_uri=https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3Fstate%3DhashArgs%2523%26isauthcode%3Dtrue&client_id=arn%3Aaws%3Aiam%3A%3A015428540659%3Auser%2Fhomepage&forceMobileApp=0&code_challenge=iPW1qTfgSh0ngwqgY3ljo6sBAWwR2_lyXzDJXjPTAY4&code_challenge_method=SHA-256)


### 2. Go to EC2 service and make sure you are in the N. Virginia region (us-east-1).

![EC2](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_01.png)


### 3. On the left menu, under IMAGES, click *AMIs*

![AMIs](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_02.png)


### 4. Search under Public Images: *w261*

![Search Public Images](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_03.png)  


### 5. Select the highlighted image.

![w261-hadoop-env](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_04_update.png)


### 6. Click the *Actions* button, and then click *Launch*.

![Launch](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_05.png)


### 7. Select the suggested Instance Type in the image at the bare minimum. Container will not run if you choose anything less. Click *Next*.

![Instance Type](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_06.png)


### 8. Keep the defaults and click *Next*.

![Instance Details](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_07.png)


### 9. Make sure you request 30 GB. Click *Next*

![Volume](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_08.png)


### 10. *Next*.

![Tags](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_09.png)


### 11. Create a new Security Group. Make sure you only activate port 22 `SSH` and Source is `0.0.0.0/0`. Highly recommended, if you have a fixed IP address where you will be working your HWs, to replace `0.0.0.0/0` with your `<IPv4-address>/32`. This way only someone in that IP address can ssh into your VM. Click *Next*.

![Security Group](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_11.png)


### 12. Review the details and click *Launch*.

![Review and Launch](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_12.png)


### 13. **Important:** After launch, you will get a pop-up window that asks you to create a key pair. Create a new one, name it as suggested `w261-ec2`, make sure you download it and save it in a safe location.

![Key Pair](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_13.png)


### 14. Click on *View Instances*.

![EC2](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_14.png)


### 15. Once the Status is changed to *Running*, select your instance and click the *Connect* button. Copy the line highlighted in red from the pop-up window.

![SSH](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_15.png)


### 16. Open your terminal. Create a directory in the home folder `w261-aws`, bring your `.pem` file to this folder.

```
mkdir w261-aws
cd w261-aws
mv ~/Downloads/w261-ec2.pem .
chmod 400 w261-ec2.pem
```

**Note:** If using windows, follow this instructions: [Connecting to your EC2 using Windows ](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html). Also, make sure on the *SSH* settings *8889, 8080, 19888* are being port-forward.


### 17. Connect to your Instance with the copied command from *Step 15*, and add the following port-forwarding options:

```
ssh -i w261-ec2.pem ec2-user@<vm-public-ip-address> \
-L8889:localhost:8889 \
-L8080:localhost:8080 \
-L19888:localhost:19888 \
-L4040:localhost:4040
```
**Note:** Replace `<vm-public-ip-address>` with your instance public ip address, i.e. *10-234-12-201*


### 18. Once you are logged in, locate the `run_this.sh` file, it should be in `/home/ec2-user/`. Execute this script like this:

```
. run_script.sh
```
This will prompt to clone the `main` repo and pull/launch the container for the first time. Please be patient.


### 19. After some output, your jupyter service should be up and accessible by clicking the following link:

[Jupyter Lab](http://localhost:8889 "Click here to open Jupyter Lab")


### 20. Once in JupyterLab, make sure *AutoSave* feature is enabled.

![Key Pair](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/jupyter_lab_autosave.png)

### 21. Go back to your terminal and `Ctrl + c` from the container and clone your personal repo. Make sure you do this outside the main folder.

```
cd ~
git clone https://github.com/ucb-w261/sp21-<section>-<github-username>.git
```
**Note:** Substitute section and github username accordingly.

### 22. Make sure you shutdown your instance when not working on your homeworks. You will be using compute resources at 4x the pace (t2.xlarge), and could cost more than expected if left unattended.

![Stop Instance](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_16.png)

 
