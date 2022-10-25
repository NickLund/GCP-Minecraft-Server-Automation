#!/bin/bash
# Your server's unique variables
MINECRAFT_SERVER_PATH = /home/minecraft/
MINECRAFT_SERVER_AUTOMATION_PATH = /home/minecraft/automation/
SCREEN_SOCKNAME = mcs
CLOUD_BACKUP_DIR = 'gs://[...]/'

# Checks if any established connections on minecraft port (25565); assigns to variable connectedVar; counts num of tokens & assigns to var count
cd $MINECRAFT_SERVER_AUTOMATION_PATH
connectedVar=$(lsof -iTCP:25565 -sTCP:ESTABLISHED)
count=$(wc -m < timer.txt)

# if variable is not empty (someone is connected)
if [ ! -z "$connectedVar" ]
then
        # resets 'tokens' to timer file
        echo -n "" > timer.txt
# if < 144 tokens (12 five minute intervals over 12 hours)
elif [[ $count -lt 144 ]]
then
        # adds a 'token' to the timer file;
        echo -n "1" >> timer.txt
else
        # resets 'tokens' to timer file; stops minecraft server; waits till process is terminated; shuts down VM
        echo -n "" > timer.txt
        cd $MINECRAFT_SERVER_PATH
        screen -r $SCREEN_SOCKNAME -X stuff '/stop\n'
        x=1
        while [ ! -z "$x" ]
        do
                x=$(pidof java)
        done
        /usr/bin/gsutil -m cp -R $MINECRAFT_SERVER_PATHworld $CLOUD_BACKUP_DIR$(date "+%Y%m%d-%H%M%S")-world
        /sbin/shutdown -h now
fi
