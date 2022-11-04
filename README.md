# GCP-Minecraft-Server-Automation
GCP Minecraft server automation stuff. Includes: backups, shutdown, and update

### Minecraft server instance details:
```
Machine type:       n1-standard-1
Network tags:       [unique name to identify minecraft servers for firewall rules i.e. minecraft-server-fwr]
Network interfaces: [Static IP]
Boot disk:          10 GB; SSD persistent disk
local disks:        50 GB; SSD persistent disk
```
### VPC network details:
Firewall rule:
```
Direction:            Ingress
Action on match:      Allow
Targets:              [tag previously created in minecraft instance, i.e. minecraft-server-fwr]
IP ranges:            0.0.0.0/0
Protocols and Ports:  tcp:25565 #default minecraft port
```

### Ephemeral IP:
#### Google Domains:
1. [buy your domain name]
2. DNS / Show advanced settings / Manage dynamic DNS:
```
Host name: [subnet]
```
  - Save
3. [Carrot] / View credentials:
  - copy username & password
#### VM:
```
sudo apt-get ddclient
```
install GUI / window:
```
program/protocol: googledomains
username: [copied]
password: [copied]
method:
```
  - I can't remember what steps here, but you can either just choose web and modify later, or might be able to choose 'other'.
  - Regardless, we will go to the config file to directly set the method.
```
sudo cd /etc/ddclient.conf
```
Replace the line containing the method (probably says: use=web) with:
```
use=cmd, cmd='curl -s ifconfig.me'
```
The script will likely look like this:
```
protocol=googledomains \
use=cmd, cmd='curl -s ifconfig.me' \
login=[username] \
password='[password]' \
[subdomain.domain.topleveldomain]\
```
Then start the service:
```sudo ddclient```

### Discord bot instance details:
```
Machine type: e2-micro
Network interfaces: [Ephemeral IP]
Boot disk:    10 GB; Standard persistent disk
```
### Discord Bot:
Discord Developer Applications:
    Settings / Bot / Privileged Gateway Intents / Message content intent: On
    Settings / OAuth2 / URL Generator / Scopes: bot, (messeges.read?), (applications.commands?)
