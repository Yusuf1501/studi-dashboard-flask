
Konfiguriere MySQL Datenbank mit folgenden Befehlen, falls nötig:

```sql
CREATE DATABASE ba_version_1;

CREATE USER 'user_version_1'@'localhost' IDENTIFIED BY 'pw_version_1';

GRANT ALL PRIVILEGES ON ba_version_1.* TO 'user_version_1'@'localhost';

FLUSH PRIVILEGES;
```

Falls Änderungen an den SQLAlchemy modellen vorgenommen werden, muss man neue Migrierungen erstellen, um die Tabellen auf dem letzten Stand halten zu können.
Damit SQLAlchemy ordentlich funktioniert muss bei der allerersten installierung folgender Befehl ausgeführt werden:

```bash
flask db init
```

Anschließen muss man bei jeder Änderung folgende Befehle ausführen:
```bash
# erstellen der Migrierungsdateien
flask db migrate

# übernehmen der Änderungen in der Datenbank
flask db upgrade
```

# Run dev server

```bash 
python app.py
```
