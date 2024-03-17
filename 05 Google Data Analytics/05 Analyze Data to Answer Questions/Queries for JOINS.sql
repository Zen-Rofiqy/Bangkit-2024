-- ! Query the dataset and incorporate aliases
-- @block
SELECT `bigquery-public-data.world_bank_intl_education.international_education`.country_name,
    `bigquery-public-data.world_bank_intl_education.country_summary`.country_code,
    `bigquery-public-data.world_bank_intl_education.international_education`.value
FROM `bigquery-public-data.world_bank_intl_education.international_education`
INNER JOIN `bigquery-public-data.world_bank_intl_education.country_summary`
ON `bigquery-public-data.world_bank_intl_education.country_summary`.country_code = `bigquery-public-data.world_bank_intl_education.international_education`.country_code
-- damn loading this data took a whole day

-- * same but use alias
-- @block
SELECT
    edu.country_name,
    summary.country_code,
    edu.value
FROM
    `bigquery-public-data.world_bank_intl_education.international_education` AS edu
INNER JOIN
    `bigquery-public-data.world_bank_intl_education.country_summary` AS summary
ON edu.country_code = summary.country_code
-- same here.. whatever.. imma skip. but yea from here i know that we actually can run the program silmutaneously

-- ! Use a JOIN to answer a question
-- @block
SELECT
summary.region,
SUM(edu.value) secondary_edu_population
FROM
    `bigquery-public-data.world_bank_intl_education.international_education` AS edu
INNER JOIN
    `bigquery-public-data.world_bank_intl_education.country_summary` AS summary
ON edu.country_code = summary.country_code --country_code is our key
    WHERE summary.region IS NOT NULL
    AND edu.indicator_name = 'Population of the official age for secondary education, both sexes (number)'
    AND edu.year = 2015
GROUP BY summary.region
ORDER BY secondary_edu_population DESC
-- hey this one was quick

-- ! Decide when to use INNER JOINs vs OUTER JOINs
-- @block
SELECT
 seasons.market AS university,
 seasons.name AS team_name,
 mascots.mascot AS team_mascot,
 AVG(seasons.wins) AS avg_wins,
 AVG(seasons.losses) AS avg_losses,
 AVG(seasons.ties) AS avg_ties
FROM `bigquery-public-data.ncaa_basketball.mbb_historical_teams_seasons` AS seasons
LEFT JOIN `bigquery-public-data.ncaa_basketball.mascots` AS mascots
ON seasons.team_id = mascots.id
WHERE seasons.season BETWEEN 1990 AND 1999
 AND seasons.division = 1
 GROUP BY 1,2,3
ORDER BY avg_wins DESC, university

-- ! Q1
-- @block
SELECT
 seasons.market AS university,
 seasons.name AS team_name,
 mascots.mascot AS team_mascot,
 AVG(seasons.wins) AS avg_wins,
 AVG(seasons.losses) AS avg_losses,
 AVG(seasons.ties) AS avg_ties
FROM `bigquery-public-data.ncaa_basketball.mbb_historical_teams_seasons` AS seasons
INNER JOIN `bigquery-public-data.ncaa_basketball.mascots` AS mascots
ON seasons.team_id = mascots.id
WHERE seasons.season BETWEEN 1990 AND 1999
 AND seasons.division = 1
 GROUP BY 1,2,3
ORDER BY avg_wins DESC, university