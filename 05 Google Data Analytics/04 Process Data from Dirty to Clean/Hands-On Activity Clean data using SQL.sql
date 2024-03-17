-- ! Inspect the fuel_typ column
-- @block
-- SELECT
--   DISTINCT fuel_type
-- FROM
--   your project name.cars.car_info
-- LIMIT 1000

SELECT DISTINCT fuel_type
FROM cars.car_info
LIMIT 1000;
-- so yea, just delete the "your project name."

-- ! Inspect the length column
-- @block
SELECT
    MIN(length) AS min_length,
    MAX(length) AS max_length
FROM
    cars.car_info;

-- ! Fill in missing data
-- @block
SELECT
  *
FROM
  cars.car_info 
WHERE
  num_of_doors IS NULL;
-- yea weird no missing value here

-- @block
SELECT *
FROM cars.car_info
WHERE TRIM(num_of_doors) = '';
-- gotcha! see? the cell wasn't identified as NULL, but an empty string
-- so if you call where is null again, it still won't show up

-- @block
SELECT
  *
FROM
  cars.car_info
WHERE
  num_of_doors IS NULL;

-- * update the data
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
SELECT *
FROM cars.car_info
WHERE TRIM(num_of_doors) = '';
-- see? we only update 1 row, and keep the other as missing value

-- ! Identify potential errors
-- @block
SELECT
  DISTINCT num_of_cylinders
FROM
  cars.car_info;

-- * correct the misspelling
-- @block
UPDATE
  cars.car_info
SET
  num_of_cylinders = "two"
WHERE
  num_of_cylinders = "tow";

-- @block
SELECT
  DISTINCT num_of_cylinders
FROM
  cars.car_info;

-- * check the compression_ratio
-- @block
SELECT
  MIN(compression_ratio) AS min_compression_ratio,
  MAX(compression_ratio) AS max_compression_ratio
FROM
  cars.car_info;
-- the maximum value in this column should be 23, not 70

-- @block
SELECT
  MIN(compression_ratio) AS min_compression_ratio,
  MAX(compression_ratio) AS max_compression_ratio
FROM
  cars.car_info
WHERE
  compression_ratio <> 70;

-- * check how much the value = 70
-- @block
SELECT
   COUNT(*) AS num_of_rows_to_delete
FROM
   cars.car_info
WHERE
   compression_ratio = 70;

-- * delete the value = 70
-- @block
DELETE FROM cars.car_info -- yea I added 'FROM'
WHERE compression_ratio = 70;

-- ! Ensure consistency
-- * check drive_wheels
-- @block
SELECT
  DISTINCT drive_wheels
FROM
  cars.car_info;