

# Docker Stack vorbereiten
## Annahmen
Der Stack kann in verschiedenen Umgebungen ausgeführt werden :
* Standalone Linux
* Windows mit Docker Desktop und WSL, Stack Sourcen im WSL Dateisystem
* Windows mit Docker Desktop, Stack Sourcen im Windows Dateisystem

## Auschecken

Die Git Einstellung zum Handling von Zeilenenden muss angepasst sein. Sonst werden auf Windows Clients die Zeilenenden der Linux Scripte, die in den Docker Containern verwendet werden sollen CRLF Zeilenenden generiert, die dann dazu führen, dass die Skripte nicht laufen.
```
git config --global core.autocrlf false
```

Das Repository verwendet submodules/subrepositories. Um diese beim Auschecken direkt mit abszuholen muss
```
git clone --recurse-submodules git@github.com:pfabrici/toda.git
```
anstelle eines "normalen" git clone verwendet werden.
## Images vorbereiten
Vor dem ersten Start muessen zwei Images manuell gebaut werden. Kommandos jeweils ausgehend vom Projekthomeverzeichnis.

**Linux/WSL**
```
( cd docker/gitsync && docker build --tag toda-gitsync . )
( cd docker/dbt && docker build --tag toda-dbt . )
```
**Windows**
Das kann z.B. in der Powershell ausgeführt werden.
```
cd docker\dbt 
docker build --tag toda-dbt . 
cd ..\gitsync
docker build --tag toda-gitsync . 
``` 

## Prepare Network
In Airflow wird der Docker Operator verwendet, um Apache Hop oder dbt auszuführen. D.h. dass diese als "Docker-in-Docker" ausgeführt werden. Damit die Hop und dbt Worker Container auch auf die Datenbank ( und evtl. andere Services ) im eigentlichen Stack zugreifen können, müssen alle im gleichen Netzwerksegment liegen.
Also wird ein externes Docker Network angelegt, welches aus docker-compose und den Docker Operatorn referenziert wird.

**Anlegen**
```
docker network create -d bridge --subnet=172.18.0.0/16 toda-network
```

## Prepare Volumes

Nach dem Auschecken muessen Verzeichnisse manuel angelegt werden. Verwendung von .gitkeep klappt leider nicht,
da Postgres dann meckert. 

**Linux/WSL**
```
cd data
mkdir -p db_data 
```
**Windows**
```
cd data
md db_data
```

Vor dem ersten Start muessen verschiedene Volumes ausserhalb von Docker Compose angelegt werden
Diese sind abhängig von der jeweiligen Umgebung.
Der Pfad in **--opt device** ist entsprechend anzupassen :

**Linux/WSL**
```
docker volume rm $(docker volume ls -q | grep toda )
docker volume create --driver local --opt type=none --opt device=/home/peterf/work/sources/toda/data/sources/hop --opt o=bind toda_sources_hop
docker volume create --driver local --opt type=none --opt device=/home/peterf/work/sources/toda/data/sources/dbt --opt o=bind toda_sources_dbt
docker volume create --driver local --opt type=none --opt device=/home/peterf/work/sources/toda/data/sources/dags --opt o=bind toda_sources_dags
docker volume create --driver local --opt type=none --opt device=/home/peterf/work/sources/toda/data/env/hop --opt o=bind toda_env_hop
docker volume create --driver local --opt type=none --opt device=/home/peterf/work/sources/toda/data/db_data --opt o=bind toda_db_data
docker volume create --driver local --opt type=none --opt device=/home/peterf/work/sources/toda/data/airflow --opt o=bind toda_airflow
```
**Windows**
```
docker volume rm $(docker volume ls -q | grep toda )
docker volume create --driver local --opt type=none --opt device=c:\work\sources\toda\data\sources\hop --opt o=bind toda_sources_hop
docker volume create --driver local --opt type=none --opt device=c:\work\sources\toda\data\sources\dbt --opt o=bind toda_sources_dbt
docker volume create --driver local --opt type=none --opt device=c:\work\sources\toda\data\sources\dags --opt o=bind toda_sources_dags
docker volume create --driver local --opt type=none --opt device=c:\work\sources\toda\data\env\hop --opt o=bind toda_env_hop
docker volume create --driver local --opt type=none --opt device=c:\work\sources\toda\data\db_data --opt o=bind toda_db_data
docker volume create --driver local --opt type=none --opt device=c:\work\sources\toda\data\airflow --opt o=bind toda_airflow
```


## Umgebung starten stoppen 
Jeweils im Hauptverzeichnis ausführen :

### Start der Umgebung
```
docker compose up -d 
```

### Stop der Umgebung
```
docker compose down
```

### Zuruecksetzen
Löscht die Datenbanken und alle Airflow Einstellungen + Logs. Zuerst die Umgebung stoppen, s.o.
Evtl. als Admin/root User aus dem Hauptverzeichnis ausführen. 
Linux Variante :
```
rm -rf data/db_data/* data/airflow/*
```

# Apache Hop Client vorbereiten

Download von [Apache Hop|https://hop.apache.org]

GUI Starten. Projekt anlegen ( toda )