/*  1. connect with SQLTools
    2. search BigQuery, (install the extention first)
    3. In Authenticator*, select GCloud CLI
    4. In Project ID*, get your BigQuery sandbox ID (https://cloud.google.com/bigquery/docs/sandbox)
        if you haven't create any Project, then create new project
        the Project will appear in Welcome page (https://console.cloud.google.com/)
*/
-- @block
SELECT
  language,
  title,
  SUM(views) AS views
FROM
  `bigquery-samples.wikipedia_benchmark.Wiki10B`
WHERE
  title LIKE '%Google%'
GROUP BY
  language,
  title
ORDER BY
  views DESC;

-- @block

