# Setting Up your VM for Hadoop using AWS

## AWS Free-Tier Account

Follow the link to create your own AWS Free-Tier Account. You are free to use an existing account if you already have one.

[AWS Free-Tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc)

## Create your Instance

1. Log into you AWS account using this link:

[AWS Console](https://signin.aws.amazon.com/signin?redirect_uri=https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3Fstate%3DhashArgs%2523%26isauthcode%3Dtrue&client_id=arn%3Aaws%3Aiam%3A%3A015428540659%3Auser%2Fhomepage&forceMobileApp=0&code_challenge=iPW1qTfgSh0ngwqgY3ljo6sBAWwR2_lyXzDJXjPTAY4&code_challenge_method=SHA-256)

2. Go to EC2 service and make sure you are in the N. California region (us-west-1).

![EC2](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_01.png)

3. On the left menu, under IMAGES, click *AMIs*

![AMIs](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_02.png)

4. Search under Public Images: *w261*

![Search Public Images](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_03.png)  

5. Select the highlighted image.

![w261-linux-hadoop](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_04.png)

6. Click the *Actions* button, and then click *Launch*.

![Launch](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_05.png)

7. Select the suggested Instance Type, and then click *Next*.

![Instance Type](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_06.png)

8. Keep the defaults and click *Next*.

![Instance Details](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_07.png)

9. Make sure you request 30 GB. Click *Next*

![Volume](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_08.png)

10. *Next*.

![Tags](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_09.png)

11. Create a new Security Group. Make sure you only activate port 22 `SSH` and Source is `0.0.0.0/0`. Click *Next*.

![Security Group](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_11.png)

12. Review the details and click *Launch*.

![Review and Launch](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_12.png)

13. **Important:** After launch, you will get a pop-up window that asks you to create a key pair. Create a new one, name it as suggested `w261-ec2`, make sure you download it and save it in a safe location.

![Key Pair](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_13.png)

14. Click on *View Instances*.

![EC2](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_14.png)

15. Once the Status is changed to *Running*, select your instance and click the *Connect* button. Copy the line highlighted in red from the pop-up window.

![SSH](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_15.png)

16. Open your terminal. Create a directory in the home folder `w261-aws`, bring your `.pem` file to this folder.

```
mkdir w261-aws
cd w261-aws
mv ~/Downloads/w261-ec2.pem .
chmod 400 w261-ec2.pem
```

**Note:** If using windows, follow this instructions: [Connecting to your EC2 using Windows ](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html). Also, make sure on the *SSH* settings *8889, 8080 and 19888* are being port-forward.

17. Connect to your Instance with the copied command from *Step 15*, and add the following port-forwarding options:

```
ssh -i w261-ec2.pem ec2-user@ec2-public-ip-address.us-west-1.compute.amazonaws.com \
-L8889:ec2-public-ip-address.us-west-1.compute.amazonaws.com:8889 \
-L8080:ec2-public-ip-address.us-west-1.compute.amazonaws.com:8080 \
-L19888:ec2-public-ip-address.us-west-1.compute.amazonaws.com:19888
```

18. Once you are logged in, locate and go to the *main* repo, it should be in `/home/ec2-user/`. Next, run the docker container.

```
cd main
docker-compose up
```

19. After some output, your jupyter service should be up and accessible by clicking the following link:

[Jupyter Lab](http://localhost:8889 "Click here to open Jupyter Lab")

20. Once in JupyterLab, make sure *AutoSave* feature is enabled.

![Key Pair](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/jupyter_lab_autosave.png)

21. Make sure you shutdown your instance when not working on your homeworks. You will be using compute resources at 4x the pace (t2.xlarge), and the Free-Tier account only has a certain amount of hrs for free in a month.

![Stop Instance](https://github.com/UCB-w261/w261-environment/blob/master/setup-aws-hadoop-env/step_16.png)
