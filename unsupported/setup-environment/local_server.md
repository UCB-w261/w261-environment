### Converting an old laptop into a home "cloud" compute server

It may be useful for you to dedicate an old laptop or machine to computing for this course. This allows you to keep your main machine free for work, study, and other tasks, while avoiding cloud computing costs. This can be used to run jobs while behind corporate firewalls at work, and general work on the go.It also preserves continuity of assignments when worked over several days.

1. Wipe the laptop and install a fresh Linux distribution, if possible. You can run it headless if you like (no GUI).

2. Install Docker (see instructions for Linux) and clone the class repo.

3. Install tmux

2. Follow the instructions here: https://dev.to/zduey/how-to-set-up-an-ssh-server-on-a-home-computer
    
    Summary:
    
    __a__) Install SSH on the compute machine
    
    __b__) Test the connection on the same network
    
    __c__) Set up your router to forward incoming traffic to your compute machine
    
    __d__) Set up security (ssh keys preferred).
    
3. From your client machine, connect over port 22 and set up ssh port forwarding either in terminal or with PuTTy (Windows). 4040 to 4040 and 8889 to 8889 (for the Spark job GUI and the Jupyter Notebook).

4. Helpful tips for PuttY (as far as I know, there are ways to do all of this in Unix as well):

   * Save a profile for when you are on the same network (this will have the private IP address) and another for when you are connecting from outside your home network (this will have your public IP address, which can change periodically). Then your setup each time is very quick.
   
   * Connection: Set a positive value like 30 to "Seconds between keepalives" so the session doesn't time out
   
   * Connection -> SSH -> Auth: Specify path to the private key file
   
   * Connection -> SSH -> Tunnels -> L4040 to Localhost:4040 and L8889 to Localhhost:8889 for running Jupyter Notebook on the client browser
   
5. Create a tmux session on the comute machine (via your SSH connection) and run docker-compose up

6. Connect on the client machine browser. For long compute jobs, you can use the cell magic "%%capture output" at the top of a cell and it will run in the background, even if you close the connection. When you return, add a cell below it with "output.show()" and you will be able to view the output of the job.   
