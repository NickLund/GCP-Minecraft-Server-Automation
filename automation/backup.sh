#!/bin/bash
# Unique Server Variables
SCREEN_SOCKNAME = mcs
CLOUD_BACKUP_DIR = 'gs://[...]/'
WORLD_DIR = '/home/minecraft/world'

screen -r $SCREEN_SOCKNAME -X stuff '/save-all\n/save-off\n'
/usr/bin/gsutil -m cp -R $WORLD_DIR $CLOUD_BACKUP_DIR$(date "+%Y%m%d-%H%M%S")-world
screen -r $SCREEN_SOCKNAME -X stuff '/save-on\n'
