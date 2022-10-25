import os
import hashlib
import requests
import threading

# CONFIGURATION & Global Variables
UPDATE_TO_SNAPSHOT = False
MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
CUR_VER = ''

# Download latest server version
def downloadLatest(jar_data):
        link = jar_data['downloads']['server']['url']
        response = requests.get(link)
        with open('minecraft_serverUpdated.jar', 'wb') as jar_file:
                jar_file.write(response.content)
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
                                downloadLatest(jar_data)
                                updateJar()
                        break

if __name__ == "__main__":
        main()
