-- ! Query the data
-- Connect to BigQuery server in SQLTools
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
/* 1. to save it, just right click on the outputn, then save result as csv
   2. if you want to create the database, just create it in MySQL.
      Here, I'm gonna create `nyc_weather` schema
   3. Don't forget to add the table by import
*/

-- ! Query the new table
-- * Disconnect from BigQuery and Connect to MySQL server in SQL tools to show the saved data
-- Make sure you already have connection to nyc_weather
-- @block
SELECT * FROM weather_data;