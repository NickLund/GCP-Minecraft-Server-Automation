# GCP-Minecraft-Server-Automation
GCP Minecraft server automation stuff. Includes: backups, shutdown, and update

Minecraft server instance details:
  Machine type:       n1-standard-1
  Network tags:       [minecraft server instance]
  Network interfaces: [Static IP]
  Boot disk:          10 GB; SSD persistent disk
  local disks:        50 GB; SSD persistent disk

Discord bot instance details:
  Machine type: e2-micro
  Network interfaces: [Ephemeral IP]
  Boot disk:    10 GB; Standard persistent disk
  
VPC network details:
  Firewall rule:
    Direction:            Ingress
    Action on match:      Allow
    Targets:              [minecraft server instance]
    IP ranges:            0.0.0.0/0
    Protocols and Ports:  tcp:25565 #default minecraft port

Discord Bot:
  Discord Developer Applications:
    Settings / Bot / Privileged Gateway Intents / Message content intent: On
    Settings / OAuth2 / URL Generator / Scopes: bot, (messeges.read?), (applications.commands?)
    
Ephemeral IP:
  Google Domains:
    [get your own domain]
    DNS / Show advanced settings / Manage dynamic DNS:
      Host name: [subnet]
      Save
    Carrot / View credentials:
      copy username & password
 VM:
  sudo apt-get ddclient
  (during install) program/protocol: googledomains
  username: [copied]
  password: [copied]
  method? doen't matter, we'll change later
  sudo cd /etc/ddclient.conf
    remove the method
    use=cmd, cmd='curl -s ifconfig.me'
