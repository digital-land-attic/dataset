#!/usr/bin/env python3

import json
import pandas as pd

from data_analyser import DataAnalyser
from collection_index import CollectionIndex


d_index = CollectionIndex()


# brownfield harmonised resources
def url_for_harmonised(resource_hash):
    return f'https://raw.githubusercontent.com/digital-land/brownfield-land-collection/master/var/harmonised/{resource_hash}.csv'


def fetch_csv(url):
    print(f"...... collecting harmonised data from {url}")
    try:
        data = pd.read_csv(url, sep=",")
        # strip spaces introduced to values
        data_frame_trimmed = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        # strip spaces introduced to column headers
        data_frame_trimmed = data_frame_trimmed.rename(columns=lambda x: x.strip())
        return data_frame_trimmed
    except Exception as e:
        print(f'FAILED: {e}')
        return pd.DataFrame()


def get_brownfield_resource_list(organisation):
    return d_index.get_resources_for_org(organisation, ordered=True)


def get_latest_brownfield_resource(resource_list):
    resource_hash = resource_list[-1]['resource']
    data = fetch_csv(url_for_harmonised(resource_hash))
    json_data = json.loads(data.to_json(orient='records'))
    analysed = DataAnalyser(json_data)
    return {
        "resource": resource_hash,
        "summary": analysed.summary()
    }
