
-- @block
ATTACH DATABASE 'C:/Users/Fathan/Documents/Obsidian Vault/2. Kuliah/Smt 6/@ Bangkit 2024/05 Google Data Analytics/04 Process Data from Dirty to Clean/cars.db' AS cars;

CREATE TABLE cars.car_info AS
SELECT *
FROM csv.`C:/Users/Fathan/Documents/Obsidian Vault/2. Kuliah/Smt 6/@ Bangkit 2024/05 Google Data Analytics/04 Process Data from Dirty to Clean/automobile_data.csv`;
