CREATE USER 'zen-rofiqy'@'localhost'
identified BY 'Justaplebian0';

GRANT CREATE, ALTER, DROP
ON new_app.*
TO 'zen-rofiqy'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE
ON new_app.* TO 'zen-rofiqy'@'localhost';

GRANT ALL PRIVILEGES ON cars.* TO 'zen-rofiqy'@'localhost';
GRANT CREATE ON *.* TO 'zen-rofiqy'@'localhost';
GRANT ALL PRIVILEGES ON nyc_weather.* TO 'zen-rofiqy'@'localhost';

