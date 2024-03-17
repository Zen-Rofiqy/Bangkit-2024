
-- Inspect the fuel_typ column
-- @block
-- SELECT
--   DISTINCT fuel_type
-- FROM
--   your project name.cars.car_info
-- LIMIT 1000
SELECT DISTINCT fuel_type
FROM cars.car_info
LIMIT 1000;

-- Inspect the length column
-- @block
-- SELECT
--     MIN(length) AS min_length,
--     MAX(length) AS max_length
-- FROM
--     you project name.cars.car_info;
SELECT
    MIN(length) AS min_length,
    MAX(length) AS max_length
FROM
    cars.car_info;

-- Fill in missing data
-- @block
-- SELECT
--   *
-- FROM
--   your project name.cars.car_info 
-- WHERE 
--   num_of_doors IS NULL;
SELECT
  *
FROM
  cars.car_info 
WHERE
  num_of_doors IS NULL;

-- @block
UPDATE
  cars.car_info
SET
  num_of_doors = "four"
WHERE
  make = "dodge"
  AND fuel_type = "gas"
  AND body_style = "sedan";

-- @block
SELECT
  *
FROM
  cars.car_info
WHERE
  num_of_doors IS NULL;

-- @block
SELECT num_of_doors
FROM cars.car_info;