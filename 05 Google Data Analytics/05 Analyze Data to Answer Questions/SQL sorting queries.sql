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

-- * ASC
-- @block
SELECT
  *
FROM
  bigquery-public-data.sdoh_cdc_wonder_natality.county_natality
ORDER BY
  Births ASC --Place the ASC or DESC specifier directly after the column name separated by a space (no other punctuation)
LIMIT
  10

-- * DESC
-- @block
SELECT
  *
FROM
  bigquery-public-data.sdoh_cdc_wonder_natality.county_natality
ORDER BY
  Births DESC --Note that this is the only change you've made
LIMIT
  10

-- ! Q1
-- @block
-- * Check every country
SELECT DISTINCT County_of_Residence
FROM bigquery-public-data.sdoh_cdc_wonder_natality.county_natality;

-- * Check the condition & then sort
-- @block
WITH County_Data AS (
  SELECT
    County_of_Residence,
    EXTRACT(YEAR FROM DATE(Year)) AS Year,
    SUM(Births) AS Total_Births
  FROM
    bigquery-public-data.sdoh_cdc_wonder_natality.county_natality
  WHERE
    County_of_Residence LIKE '%Erie%' OR
    County_of_Residence LIKE '%Chautauqua%' OR
    County_of_Residence LIKE '%Niagara%'
    AND EXTRACT(YEAR FROM DATE(Year)) BETWEEN 2016 AND 2018
  GROUP BY
    County_of_Residence,
    EXTRACT(YEAR FROM DATE(Year))
)
SELECT
  County_of_Residence,
  Year,
  Total_Births
FROM
  County_Data
ORDER BY
  Total_Births DESC;





