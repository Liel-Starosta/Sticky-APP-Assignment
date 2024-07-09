CREATE DATABASE IF NOT EXISTS app_db;

USE app_db;

CREATE TABLE IF NOT EXISTS global_counter (
    id INT AUTO_INCREMENT PRIMARY KEY,
    counter_value INT NOT NULL
);

CREATE TABLE IF NOT EXISTS access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_time DATETIME NOT NULL,
    client_ip VARCHAR(45) NOT NULL,
    internal_ip VARCHAR(45) NOT NULL
);

INSERT INTO global_counter (counter_value) VALUES (0);

