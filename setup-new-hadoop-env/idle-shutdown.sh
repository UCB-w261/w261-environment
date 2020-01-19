#!/bin/bash

# This script is located in the /home folder in the VM.
# It will run during startup to make sure the docker containers
# is immediately avaliable.

# After the first 20 minutes, it will start checking the rolling
# 15 mintue average load on the VM. If this load is below 0.10,
# it will start the process to shutdown. Otherwise, it will check
# back in an hour all the time he VM is running.

threshold=0.1

sudo docker-compose -f /home/docker-compose.yml up &

sleep 1200

while true
  do

  load=$(uptime | sed -e 's/.*load average: //g' | awk '{ print $3 }') # 15-minute average load
  load="${load//,}" # remove trailing comma
  res=$(echo $load'<'$threshold | bc -l)

  if (( $res ))

    then
      sudo docker stop $(sudo docker ps -a -q)
      sleep 120
      sudo poweroff

    else
      sleep 3600

  fi

done
