
Konfiguriere MySQL Datenbank mit folgenden Befehlen:

```sql
CREATE DATABASE ba_version_1;

CREATE USER 'user_version_1'@'localhost' IDENTIFIED BY 'pw_version_1';

GRANT ALL PRIVILEGES ON ba_version_1.* TO 'user_version_1'@'localhost';

FLUSH PRIVILEGES;
```

Erstelle Tabellen:

```sql
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE theses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    student_id INT,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
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