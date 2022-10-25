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
