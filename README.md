## MyProject_LF.9

###Einrichtung des Linux-Servers
---

# Netzwerkkonfiguration
Öffnen Sie die Datei `/etc/dhcpcd.conf` mit einem Texteditor wie nano:

```bash
sudo nano /etc/dhcpcd.conf
```

Fügen Sie folgende Zeilen am Ende der Datei hinzu, um eine statische IP-Adresse zu konfigurieren:

```
interface eth0
static ip_address=192.168.24.132
static routers=192.168.1.1
static domain_name_servers=5000
```

---

# Benutzer erstellen
Erstellen Sie den Benutzer "willi" ohne Administratorrechte:

```bash
sudo adduser willi
```

Erstellen Sie den Benutzer "fernzugriff" mit sudo-Rechten:

```bash
sudo adduser fernzugriff
sudo usermod -aG sudo fernzugriff
```

---

# SSH-Dienst einrichten
Installiere den SSH-Server:

```bash
sudo apt-get update
sudo apt-get install openssh-server
```

Konfigurieren Sie den SSH-Dienst, um nur den Benutzer "fernzugriff" zuzulassen:

```bash
sudo nano /etc/ssh/sshd_config
```

Ändern Sie die Zeile `PermitRootLogin` zu `PermitRootLogin no` und füge `AllowUsers fernzugriff` hinzu.

Starten Sie den SSH-Dienst neu:

```bash
sudo systemctl restart sshd
```

---

# Docker installieren
Installieren Sie Docker und Docker Compose:

```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
```

---

# Web-App deployen
Klonen Sie das Git-Repository mit der Web-App:

```bash
git clone <Repository-URL>
```

Navigieren Sie in das Verzeichnis:

```bash
cd ToDoList_ifa22
```

Starten Sie die Web-App mit Docker Compose:

```bash
sudo docker-compose up -d
```

Die Web-App ist nun unter http://192.168.24.132:5000 erreichbar.

---

# Git-Befehle
Klonen des Repositories:

```bash
git clone https://github.com/JassemDev/MyProject_LF.9.git
```

Pullen der neuesten Änderungen:

```bash
git pull
```

Committen von Änderungen:

```bash
git add .
git commit -m "Commit-Nachricht"
```

Pushen von Änderungen:

```bash
git push
```

---
