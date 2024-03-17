
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
