-- ! Query the data
-- @block
SELECT
  stn,
  date,
  IF(
     temp=9999.9,
     NULL,
     temp) AS temperature,
  IF(
     wdsp="999.9",
     NULL,
     CAST(wdsp AS Float64)) AS wind_speed,
  IF(
     prcp=99.99,
     0,
     prcp) AS precipitation
FROM
  `bigquery-public-data.noaa_gsod.gsod2020`
WHERE
  stn="725030" -- La Guardia
  OR stn="744860" -- JFK
ORDER BY
  date DESC,
  stn ASC

-- ! Save a new table
-- * Save to MySql (Must create `nyc_weather` schema first)
-- @block
USE nyc_weather; -- Connect to MySQL database/schema

DROP TABLE IF EXISTS weather_data;
CREATE TABLE weather_data (
    stn VARCHAR(10),
    date DATE,
    temperature FLOAT,
    wind_speed FLOAT,
    precipitation FLOAT
);

-- * Insert data into the table
-- @block
INSERT INTO weather_data (stn, date, temperature, wind_speed, precipitation)
SELECT
 stn,
 date,
 IF(temp = 9999.9, NULL, temp) AS temperature,
 IF(wdsp = "999.9", NULL, CAST(wdsp AS FLOAT)) AS wind_speed,
 IF(prcp = 99.99, 0, prcp) AS precipitation
FROM
 `bigquery-public-data.noaa_gsod.gsod2020`
WHERE
 stn IN ("725030", "744860")
ORDER BY
 date DESC, stn ASC;





-- ! Query the new table
-- @block
SELECT
    AVG(temperature)
FROM
    `your_project_name.demos.nyc_weather`  
WHERE
    date BETWEEN '2020-06-01' AND '2020-06-30'