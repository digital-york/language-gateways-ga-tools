
This repository contains tools to query Google Analytics GA4 data for Language gateways projects.


How access GA4 download stats for OASIS Summaries 
=================================================

Google Cloud Credentials
------------------------
Access to OASIS staging and production GA4 accounts is facilitated via dedicated _analytics-credentials.json_ file. The credentials file was generated via Google Cloud dashboard where a projet with required API priviliges has been set up. The files is store in our credential managment system. We manage installation of credential file on staging and prodcution serves with puppet. 

Installaiton - Python libraries
--------------------------------
Script requires access to Python 3. Create python virtualenv and install required libries.

```
virtualenv ga4-virtualenv
source ga4-virtualenv/bin/activate
pip install google-analytics-data
```

How to run script
-----------------
Script require google 
```
source ga4-virtualenv/bin/activate
python oasis-download-stats-ga4-client.py --help

usage: oasis-download-stats-ga4-client.py [-h] [--ga_credentials_path GA_CREDENTIALS_PATH] [--property_id PROPERTY_ID]
                                          [--ua_downloads_number UA_DOWNLOADS_NUMBER]
                                          [--downloads_json_path DOWNLOADS_JSON_PATH]

Query GA4 report to obtain OASIS total downlods stats

optional arguments:
  -h, --help            show this help message and exit
  --ga_credentials_path GA_CREDENTIALS_PATH
                        Path to the credentials JSON file.
  --property_id PROPERTY_ID
                        GA4 property ID.
  --ua_downloads_number UA_DOWNLOADS_NUMBER
                        Number of UA downloads as recorded on UA before switchihg to GA4
  --downloads_json_path DOWNLOADS_JSON_PATH
                        Path where to save oasis_download_stats.json file. Default "./"
```

