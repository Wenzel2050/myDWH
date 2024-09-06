## Images vorbereiten
Vor dem ersten Start muessen zwei Images manuell gebaut werden :
### gitsync Image
```
cd docker/gitsync
docker build --tag toda-gitsync .
```
### dbt Image
```
cd docker/dbt
docker build --tag toda-dbt .
``` 

## Prepare Volumes
Vor dem ersten Start muessen verschiedene Volumes ausserhalb von Docker Compose angelegt werden
Diese sind abhängig von der jeweiligen Umgebung.
Der Pfad in **--opt device** ist entsprechend anzupassen :

```
docker volume rm $(docker volume ls -q | grep toda )
docker volume create --driver local --opt type=none --opt device=/home/peterf/work/sources/toda/data/sources/hop --opt o=bind toda_sources_hop
docker volume create --driver local --opt type=none --opt device=/home/peterf/work/sources/toda/data/sources/dbt --opt o=bind toda_sources_dbt
docker volume create --driver local --opt type=none --opt device=/home/peterf/work/sources/toda/data/sources/dags --opt o=bind toda_sources_dags
docker volume create --driver local --opt type=none --opt device=/home/peterf/work/sources/toda/data/db_data --opt o=bind toda_db_data
docker volume create --driver local --opt type=none --opt device=/home/peterf/work/sources/toda/data/airflow --opt o=bind toda_airflow
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