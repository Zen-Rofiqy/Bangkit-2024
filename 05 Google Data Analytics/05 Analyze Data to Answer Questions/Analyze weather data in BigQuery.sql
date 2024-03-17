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
-- @block
CREATE OR REPLACE TABLE `my-first-project-417404.demos.nyc_weather`
AS
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
  stn ASC;





-- ! Query the new table
-- @block
SELECT
    AVG(temperature)
FROM
    `your_project_name.demos.nyc_weather`  
WHERE
    date BETWEEN '2020-06-01' AND '2020-06-30'