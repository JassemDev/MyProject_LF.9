## MyProject_LF.9

## Einrichtung des Linux-Servers
---

# Netzwerkkonfiguration
Öffnen Sie die Datei `/etc/dhcpcd.conf` mit einem Texteditor wie nano:

```
sudo nano /etc/dhcpcd.conf
```

Fügen Sie folgende Zeilen am Ende der Datei hinzu, um eine statische IP-Adresse zu konfigurieren:

```
interface eth0
```
```
static ip_address=192.168.24.132
```
```
static routers=192.168.1.1
```
```
static domain_name_servers=5000
```

---

# Benutzer erstellen
 Erstellen Sie den Benutzer "willi" ohne Administratorrechte:

```
sudo adduser willi
```

Erstellen Sie den Benutzer "fernzugriff" mit sudo-Rechten:

```
sudo adduser fernzugriff
```
```
sudo usermod -aG sudo fernzugriff
```

---

# SSH-Dienst einrichten
Installieren Sie den SSH-Server:

```
sudo apt-get update
```
```
sudo apt-get install openssh-server
```

Konfigurieren Sie den SSH-Dienst, um nur den Benutzer "fernzugriff" zuzulassen:

```
sudo nano /etc/ssh/sshd_config
```

Ändern Sie die Zeile `PermitRootLogin` zu `PermitRootLogin no` und füge `AllowUsers fernzugriff` hinzu.

Starten Sie den SSH-Dienst neu:

```
sudo systemctl restart sshd
```

---

# Docker installieren
Installieren Sie Docker und Docker Compose:

```
sudo apt-get update
```
```
sudo apt-get install docker.io docker-compose
```

---

# Web-App deployen
Klonen Sie das Git-Repository mit der Web-App:

```
git clone https://github.com/JassemDev/MyProject_LF.9.git
```

Navigieren Sie in das Verzeichnis:

```
cd MyProject_LF.9
```

Starten Sie die Web-App mit Docker Compose:

```
sudo docker-compose up -d
```

Die Web-App ist nun unter http://192.168.24.132:5000 erreichbar.

---

# Git-Befehle
Klonen des Repositories:

```
git clone https://github.com/JassemDev/MyProject_LF.9.git
```

Pullen der neuesten Änderungen:

```
git pull
```

Committen von Änderungen:

```
git add .
```
```
git commit -m "Commit-Nachricht"
```

Pushen von Änderungen:

```
git push
```

---
