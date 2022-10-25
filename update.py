import os
import time
import hashlib
import logging
import requests
import subprocess
import threading

# CONFIGURATION
UPDATE_TO_SNAPSHOT = False
CLOUD_BACKUP_DIR = 'gs://[...]/'
WORLD_DIR = '/home/minecraft/world/'
LOG_FILENAME = 'auto_updater.log'
RAM_INITIAL = '2725M'
RAM_MAX = '2725M'
MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
SCREEN_SOCKNAME = 'mcs'

# Multithread Global Variables
CUR_VER = ''

logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Server shutdown message & timer
def timer():
        logging.info('Logged in user. Shutting down server in 30 seconds.')
        for i in range(30, 10, -10):
                os.system('screen -r ' + str(SCREEN_SOCKNAME) + ' -X stuff \'say ATTENTION: Server will shutdown temporarily to update in ' + str(i) + ' seconds.^M\'')
                time.sleep(10)
        for i in range(10, 0, -1):
                os.system('screen -r ' + str(SCREEN_SOCKNAME) + ' -X stuff \'say Shutdown in ' + str(i) + ' seconds^M\'')
                time.sleep(1)
        return

# Download latest server version
def downloadLatest(jar_data):
        link = jar_data['downloads']['server']['url']
        response = requests.get(link)
        with open('minecraft_serverUpdated.jar', 'wb') as jar_file:
                jar_file.write(response.content)
        logging.info('Download success.')
        return

# Backup server
def backup():
        commandFirst = '/usr/bin/gsutil -m cp -R '
        commandSecond = '$(date "+%Y%m%d-%H%M%S")'
        os.system(str(commandFirst) + str(WORLD_DIR) + " " + str(CLOUD_BACKUP_DIR) + str(commandSecond) + "-world")
        logging.info('Backup success.')
        return

# Updating server .jar file
def updateJar():
        if os.path.exists('../minecraft_server.jar'):
                os.remove('../minecraft_server.jar')
        os.rename('minecraft_serverUpdated.jar', '../minecraft_server.jar')
        return

# retrieve wanted version:
def getCurrentVersion(data):
        if UPDATE_TO_SNAPSHOT:
                return data['latest']['snapshot']
        return data['latest']['release']

# Get checksum of running server
def serverChecksum():
        global CUR_VER
        if os.path.exists('../minecraft_server.jar'):
                sha = hashlib.sha1()
                f = open("../minecraft_server.jar", 'rb')
                sha.update(f.read())
                CUR_VER = sha.hexdigest()
        return

# Stop Minecraft Server, but don't continue until after the process is actually done
def stopServer(javaPID):
        os.system('screen -r ' + str(SCREEN_SOCKNAME) + ' -X stuff \'stop^M\'')
        while javaPID:
                javaPID = os.popen('pidof java').read()
        logging.info('Stopped server success.')
        return

def main():
        versionThread = threading.Thread(target=serverChecksum)
        versionThread.start()
        data = requests.get(MANIFEST_URL).json()
        minecraft_ver = getCurrentVersion(data)
        for version in data['versions']:
                if version['id'] == minecraft_ver:
                        jar_data = requests.get(version['url']).json()
                        jar_sha = jar_data['downloads']['server']['sha1']
                        versionThread.join()
                        if CUR_VER != jar_sha:
                                logging.info('Latest version is ' + str(minecraft_ver) + '. Updating server now.')
                                downloadThread = threading.Thread(target=downloadLatest,args=(jar_data,))
                                downloadThread.start()

                                logged_in = os.popen('lsof -iTCP:25565 -sTCP:ESTABLISHED').read()
                                if logged_in:
                                        timer()
                                stopServer(1)
                                backup()
                                downloadThread.join()
                                updateJar()

                                logging.info('Starting server...')
                                os.chdir("..")
                                os.system('screen -d -m -S ' + str(SCREEN_SOCKNAME) + ' java -Xms' + RAM_INITIAL + ' -Xmx' + RAM_MAX + ' -jar minecraft_server.jar nogui')

                        else:
                                logging.info('Server is already up to date.')

                        break

if __name__ == "__main__":
        main()
