/*  How to SQLTools : "https://youtu.be/9ADd-_mM5Dw?si=XvYxrq-iWub91kof"
    1. connect with SQLTools
    2. search BigQuery, (install the extention first)
    3. In Authenticator*, select GCloud CLI
    4. In Project ID*, get your BigQuery sandbox ID (https://cloud.google.com/bigquery/docs/sandbox)
        if you haven't create any Project, then create new project
        the Project will appear in Welcome page (https://console.cloud.google.com/)
    5. Test the connection

    If you get this error : Error opening connection Failed to connect to BigQuery: Could not load the default credentials. Browse to https://cloud.google.com/docs/authentication/getting-started for more information.
    1. Then got to "https://cloud.google.com/sdk/docs/install", search SDK. Click "Download the Google Cloud CLI installer.", download then install
    2. After installment complete, the cmd will appear, try to connect your account by follow the instruction in cmd (Just tipe Y and enter)
    3. Then close vscode, and open it again to restart the vscode
        This time you should be able to run `gcloud auth application-default login` in your vscode cmd
        try ctrl + ` then run `gcloud auth application-default login` in yor vscode cmd
    make sure you login with your account that already enable BigQuery sandbox

    After successfully logged in do this : 
    1. Creating New Credentials:
       * Open the Google Cloud Platform console (https://console.cloud.google.com/).
       * Select the project that corresponds to the BigQuery project you want to access.
       * Go to "IAM & admin" > "Service accounts" menu.
       * Select or create a service account that suits your needs.
       * After that, select "Add Key" > "Create new key".
       * Select the JSON file format and click "Create". This will download the credentials.json file to your computer.
    2. Locate your downloaded JSON file, then run this in your vscode cmd :
        set GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Fathan\Documents\Obsidian Vault\2. Kuliah\Smt 6\@ Bangkit 2024\05 Google Data Analytics\04 Process Data from Dirty to Clean\ILT ML 02\my-first-project-417404-5e004b0cd9d6.json"
        Note: Change the path with your own path
        to see if this was run successfully you can try to run this in you vscode cmd :
        `echo %GOOGLE_APPLICATION_CREDENTIALS%`
    
    Welldone! now try again the test connection in SQLTools, it should successfully connect.
*/
-- Run a large query
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

-- Run a larger query
-- @block
SELECT
  language,
  title,
  SUM(views) AS views
FROM
  `bigquery-samples.wikipedia_benchmark.Wiki100B`
WHERE
  title LIKE '%Google%'
GROUP BY
  language,
  title
ORDER BY
  views DESC;

--
