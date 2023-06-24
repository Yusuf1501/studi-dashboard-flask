
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