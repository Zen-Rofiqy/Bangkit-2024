-- ! Query the data to explore its sturcture
-- @block
SELECT
  * 
FROM
  bigquery-public-data.sdoh_cdc_wonder_natality.county_natality 
LIMIT
  1000 

-- ! USe ORDER BY to sort relevant data
-- @block
SELECT
  *
FROM
  bigquery-public-data.sdoh_cdc_wonder_natality.county_natality
ORDER BY --This is a SQL sort order function
  Births --Applies the sorting to the Births column
LIMIT
  10