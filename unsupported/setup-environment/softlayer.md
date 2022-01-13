# Setting up a remote system for w261
Josh Lee  
MIDS 18'  
2018-08-08 rev 2  

## Objective
Upon completing this guide you will have a  cloud server provisioned with the w261 docker components downloaded and ready to be used for your assignments.
I addition you will also have developed some basic skills that you can use in your future work to simplify your workflow and enable you to work more comfortably with remote systems.

## Skills
This guide presupposes basic familiarity with the command line and running jupyter locally.  One essential attribute and an essential skill is tenacity and googling.  I learned the ensuing material from googling and was not detered when seemingly insurmountable problems presented themselves.  The pay off will be a robust and powerful remote computing instance as well as an improvement in your devops skills.  Think of it as getting better at statistics or writing.  

If you wildly uncomfortable with docker I would recommend the docker tutorial.  
https://docs.docker.com/get-started/


## Setup: Provisioning

Instructions are for Softlayer. They are based on my own server I provisioned.  Feel free to change as you see fit. 

### Hardware

Note: All prices are as of the writing of the document, for SJC04, and are for a monthly basis.  As our w251 instructor likes to say “Your millage may vary."  
  
<screen shots and instructions for softlayer>
#### Security to be set at Provisioning

On the subsequent page we can set our security policies. For the “Public Network Interface” I’m allowing incoming traffic on port 22, ssh, and allowing all outbound traffic.  I’m allowing all outbound traffic because I didn’t know at the time if there were any other services needed for the docker container.  Plus also by doing so I can also use Git.

Preview of things to come, we’re going to use a ssh tunnel to connect to the server.

I have not set any policies for the “Private Network Interface”.

I didn’t set up any backend vLAN.  
I used my key that already made and registered with SoftLayer.  

## Setup: Post-Provisioning 

#### Harden Server

Before going any further please note that this document was written in a word processing program which means the quotes are smart quotes and there may be some other formatting to the text.  When you copy and paste a command it may not work correctly because smart quotes and plain quotes are different.  You want plain quotes.  One solution is to paste the command from this document into a text editor such as sublime text.  The editor will replace the smart quotes with plain quotes.

#### Some things to keep in mind…  
1. The command `service` is deprecated in CentOS 7.  Use `systemctl` instead.  
2. Some of the instructions will ask you to create a ssh key.  You really don’t need to, just use your existing key.  
3. With all that... The goal is to close off the more common attack vectors which are  
    a. weak root passwords  
    b. allowing root to login  
    c. not using ssh key for authentication  

##### A. Change root password
Note: you will still need root for system maintenance and installing additional packages etc. 
ssh as root
change root’s password  

Here's a link for instructions for changing the root password:  
https://www.tldp.org/LDP/lame/LAME/linux-admin-made-easy/changing-user-passwords.html

##### B. Disable root login
ssh as non-root
change to root user, so you don’t have to keep typing sudo.
Careful after doing this you will not be able to login as root.
change settings in sshd to disable root login.  

Here's a link for instructions for disabling root login:   
https://mediatemple.net/community/products/dv/204643810/how-do-i-disable-ssh-login-for-the-root-user

##### C. Require ssh key for logon
ssh as non-root
change to root user, so you don’t have to keep typing sudo.  

Here's a link for instructions for requiring ssh key for logon:   
https://www.liberiangeek.net/2014/07/enable-ssh-key-logon-disable-password-password-less-logon-centos/

Appendix XXX is an example of my sshd file I used for my server.
Appendix YYY contains instructions for setting up passwordless ssh so you don't have to type so much.

#### Update system, mount drives, install software
At this point you have changed root password, disabled root login, and require ssh key for logon.  Optionally you have setup passwordless ssh to your remote system.  We will now go through some additional devops to prepare your server for running the course docker container.

##### Update system
First you update your system
for centOS, REHEL, and Fedora type distributions
```
yum makecache 
#go get some coffee

yum update 
#go check email

yum install bzip2 
#you’ll need it later for when you install anaconda
```
##### Mount your data drive  
  
__Learn from my mistakes:__  
Switch to `root` or some other `privilaged account` after loggin in to avoid having to type `sudo` a lot.  
Format the drive as `ext3` not `ext4` so as to not get some odd cross file system errors.  
After you format the drive, create a place to `mount` the directory change back to `non-root` user so that when you make directories or files they’ll be owned by the `non-root` user.  This avoids having to do a `chown` on a bunch of files.

If you are sharing a system with another `user` verify that the `user` can create files on the data drive. 

Instructions for setting up and mounting your data drive:  
https://ubccr.freshdesk.com/support/solutions/articles/13000019293-mounting-a-volume-in-centos-or-ubuntu  

Instructions for ascertaining the file system type:  
https://www.tecmint.com/find-linux-filesystem-type/

##### Install Anaconda or Something else that has pip

We need `pip` to install `docker-compose` later.  Ok so this may be overkill but in general I personally don’t like having inconsistencies across my platforms with respects to versions of python and other tools, this is why we’re installing anaconda.  Anaconda has `pip`, plus also I like the way anaconda manages packages and some of its other features as well.  If you don’t want to install anaconda then update your `pip` and move on.

###### Get the latest version of anaconda
The latest version can be found here: https://www.anaconda.com/download/#linux
```
su root #Switch to root
cd ~ # change to home directory
wget <the version you want to get>
```
Screen shot anaconda

From the terminal run the command (paste the url from above into the terminal).  
For example:
```
wget https://repo.anaconda.com/archive/Anaconda3-5.1.0-Linux-x86_64.sh
```
###### Install anaconda
You’re `root`.  If you install anaconda as root only `root` will be able to use it.  
We need to install anaconda to a directory that can be accessed by other users.  
The canonical location is `/opt`.  
When prompted specify `/opt/anaconda` for the installation `path`.  
Instructions from stackoverflow for where to install:  
https://stackoverflow.com/questions/27263620/how-to-install-anaconda-python-for-all-users  
Instructions for installing anaconda on linux:  
https://docs.anaconda.com/anaconda/install/linux

When prompted change the path but also agree to adding a path variable to your `.bash_profile`.  

When the install is completed do the following:
```
#To be performed as root...
cd ~
source .bash_profile
which python
```
You should see something like `/opt/anaconda/bin/python`.  This is a good sign.  
Your anaconda directory maybe named something like `anaconda3`.  This is imaterial.

##### Modify the python path 
Exit from `root` back to `non-root`
```
#To be performed as non-root.
cd ~ # change to home directory
vi .bash_profile 

#Add the following to the end of the profile but before the export PATH.
export PATH=“/opt/anaconda/bin:$PATH”

#Save changes and then reload your session settings.
source .bash_profile

#Verify the correct version of python is being used.
which python.
```
Once again you should see something like `/opt/anaconda/bin/python`.  

##### Upgrade your anaconda and installed packages (more coffee and email checking)
```
#To be performed as root.
conda upgrade --conda
conda update --all
```
##### Install docker
Follow the instructions from docker:  
https://docs.docker.com/install/#supported-platforms

##### Install docker-compose
Follow the instructions from docker:  
https://docs.docker.com/compose/install/

##### Get docker jupyter lab to run via ssh tunnel
At this point you should have a hardened server, anaconda installed, docker and docker-composed installed.
You will need git access to the course enviroment repo.

Pull the w261 environment to your data directory.
We need to ensure that when we start the docker container that jupyter will start in no-browser mode and on a specified port.

From your data directory examine the start-notebook.sh file in the w261-enviroment's folder...
```
vi w261-environment/docker/start-notebook.sh
```
You should see something like...
```
jupyter lab --port=8889 --no-browser &
```
This is promising. The port on which jupyter lab will be operating is `8889` and it will be operating in a `no-browser` configuration.

Even though we will be using an ssh tunnel I personally still want to require a password for the server.
Here are the instructions for configuring a password on a jupyter server.  Note we want to use the preparing a hashed password instructions http://jupyter-notebook.readthedocs.io/en/stable/public_server.html.

Follow the instructions for preparing a hashed password using a local jupyter notebook. 
Your hashed password should look something like `'sha1:5cd7c15e9bae:8b9d830a738c5b58109156e6fda7a99072d7f757'` which by the way is the hash, with salt, for the word 'foobar'.  

Note the salt ensures that even if you know the plain text password the hash still cannot be cracked because you don't know the additional characters, or salt, that have been appened to the plain text.  A classic example of salting plain text can be found if you google "The world wonders leyte gulf". But you know that I used python's password generator and you know the plain text so... you have all the pieces to crack the password hash.

Next we need to add the hashed password to the file jupyter_notebook_config.py.
```
vi w261-environment/docker/jupyter_notebook_config.py
```
You will see that the password field is blank:
`c.NotebookApp.password = ''`.

Add the hashed password to the field:
`c.NotebookApp.password = 'sha1:5cd7c15e9bae:8b9d830a738c5b58109156e6fda7a99072d7f757'`.

Be careful about copying and pasting quotes. When in doubt use a plain text editor.

We are now ready to launch the environment.
Follow the instructions in the w261 repo for launching the docker container.

confirm jupyter is running on the remote system
`ps aux | grep jupyter`

#### Configuring our local machine
I'm assuming you're on a mac or a linux type machine or using a terminal of some sort.
Ok we're almost there.  We just need to configure our ssh tunnel.  
Note if you did the type less steps your life will much easier because all you need to do is modify your `~/.ssh/config` with your ssh tunnel directives.  But for now let's just do it the verbose way...
```
ssh -i ~/.ssh/<path to private ssh key> -N -f -L <local port>:localhost:<remote port> <user name>@<remote>
```
If your ssh key has a password you'll be prompted to enter it.

Confirm the tunnel is working correctly by typing 
`ps aux | grep ssh`.

You should see your ssh tunnel.  Ok almost there...

Open a broser and navigate to
`localhost:<port on your local machine>`
Enter the plain text password for the jupyter server.

If all went well you should be in your jupyter lab on your remote system!

How to close the tunnel...
Close your browser.  You can logout of jupyter if you so desire.
In a terminal session enter `ps aux | grep ssh` and take note of the pid, process id, for the tunnel process.
Enter `kill <pid>`.
If you're familiar with the flags for `kill` the ` -9` flag is not necessary.

Instructions for setting up ssh tunnel to jupyuter (this is where I started) http://www.blopig.com/blog/2018/03/running-jupyter-notebook-on-a-remote-server-via-ssh/

You can use this port forwarding method for other ui based tools such as the spark console.  
My configuration on my mac is as follows...

My /etc/hosts file...
127.0.0.1	localhost
192.168.1.1 w261-mine
192.168.1.2 w261-not-mine
255.255.255.255	broadcasthost
::1             localhost 
127.0.0.1 docker.261

My ~/.ssh/config file...
Host tunnel-w261-mine
	Hostname w261-mine
	IdentityFile ~/.ssh/w261/id_rsa
	LocalForward 10000 localhost:8889 
	LocalForward 10001 localhost:8088 
	LocalForward 10002 localhost:19888
	LocalForward 10003 localhost:50070
	LocalForward 10004 localhost:4040
	LocalForward 20000 localhost:9000 

Host tunnel-w261-not-mine
	Hostname not-mine
	IdentityFile ~/.ssh/w261/id_rsa
	LocalForward 30000 localhost:10000
	
Sometimes I want to use jupyter on my remote system but not in the w261 environment.
Test your knowledge... 
What is the command I need to run on the remote system to start the non-w261 jupyter server?
What is the command I need to run locally, yes the verbose command, to establish the ssh tunnel to the non-w261 jupyter server?

Congrats! You now have configured a remote server to do your bidding.
