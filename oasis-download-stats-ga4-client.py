#!/usr/bin/env python

# Copyright 2021 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Analytics Data API sample quickstart application.

This application demonstrates the usage of the Analytics Data API using
service account credentials from a JSON file downloaded from
the Google Cloud Console.

Usage:
  pip3 install --upgrade google-analytics-data
  python3 oasis-download-stats-ga4-client.py --path ../../google-analytics-ruby-client/oasis-analytics-sp1487-dev-a258b80e0667.json --property_id 259985601 --ud_downloads 53948 

  credentials.json file for your service account downloaded from the Cloud Console.
"""
# [START analyticsdata_json_credentials_quickstart]
import json
import argparse

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    Filter,
    FilterExpression
)


def downloads_report(credentials_json_path, property_id, number_of_downloads_ua, downloads_json_path):
    """Runs a simple report on a Google Analytics 4 property."""

    # Explicitly use service account credentials by specifying
    # the private key file.
    client = BetaAnalyticsDataClient.from_service_account_json(
        credentials_json_path)
    # [END analyticsdata_json_credentials_initialize]

    # [START analyticsdata_json_credentials_run_report]
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="eventName")],
        metrics=[Metric(name="eventCount")],
        date_ranges=[DateRange(start_date="2020-05-01", end_date="today")],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="eventName",
                string_filter=Filter.StringFilter(value="Downloaded"),
            )
        ),
    )
    response = client.run_report(request)

    """   
    print(response)
        dimension_headers {
            name: "eventName"
        }
        metric_headers {
            name: "eventCount"
        type_: TYPE_INTEGER
        }
        rows {
        dimension_values {
            value: "Downloaded"
        }
        metric_values {
            value: "14"
        }
        }
        row_count: 1
        metadata {
            currency_code: "GBP"
            time_zone: "Etc/GMT"
        }
        kind: "analyticsData#runReport"
    """

    print("Report result:")
    # for row in response.rows:
    # print(row.dimension_values[0].value, row.metric_values[0])

    number_of_downloads_ga4 = int(response.rows[0].metric_values[0].value)
    total_downloads = number_of_downloads_ua + number_of_downloads_ga4
    print("OASIS total number of downloads: ", total_downloads)
    # [END analyticsdata_json_credentials_run_report]

    # Create the JSON structure
    data = {
        "total_downloads": total_downloads
    }

    # Write the JSON to a file
    with open(downloads_json_path + '/' + 'oasis_download_stats.json', 'w') as f:
        json.dump(data, f)

# [END analyticsdata_json_credentials_quickstart]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Query GA4 report to obtain OASIS total downlods stats')
    parser.add_argument('--ga_credentials_path', type=str,
                        help='Path to the credentials JSON file.')
    parser.add_argument('--property_id', type=str, help='GA4 property ID.')
    parser.add_argument('--ua_downloads_number', type=str, help='Number of UA downloads as recorded on UA before switchihg to GA4')
    parser.add_argument('--downloads_json_path', type=str, help='Path where to save oasis_download_stats.json file. Default "./"')
    args = parser.parse_args()

    if not args.ga_credentials_path:
        raise ValueError(
            'Please provide the path to the credentials.json file using the --ga_credentials_path argument')

    if not args.property_id:
        raise ValueError(
            'Please provide the GA4 property ID using the --property_id argument')
        
    credentials_json_path = args.ga_credentials_path
    ga4_property_id = args.property_id
    downloads_json_path = args.downloads_json_path
    
    if not args.ua_downloads_number:
        # Number of downloads from OASIS UA on 22nd Jun 2023
        number_of_downloads_ua = 53948
    else:
        number_of_downloads_ua = int(args.ua_downloads_number)
        
    if not args.downloads_json_path:
        downloads_json_path = '.'

    downloads_report(credentials_json_path, ga4_property_id, number_of_downloads_ua, downloads_json_path)
