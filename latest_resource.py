#!/usr/bin/env python3

import json
import requests
import pandas as pd
from io import StringIO

from data_analyser import DataAnalyser
from collection_index import CollectionIndex

from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache

d_index = CollectionIndex()

# cache files collected
session = CacheControl(requests.session(), cache=FileCache(".cache"))

# brownfield harmonised resources
def url_for_harmonised(resource_hash):
    return f'https://raw.githubusercontent.com/digital-land/brownfield-land-collection/master/var/harmonised/{resource_hash}.csv'


def get(url):
    r = session.get(url)
    r.raise_for_status()
    return r.text


def remote_or_cached(path):
    if session:
        csv_str = get(path)
        return pd.read_csv(StringIO(csv_str), sep=",")
    else:
        return pd.read_csv(path, sep=",")


def fetch_csv(url):
    print(f"...... collecting harmonised data from {url}")
    try:
        data = remote_or_cached(url)
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
    latest_resource = resource_list[-1]
    raw_data_url = url_for_harmonised(latest_resource['resource'])

    data = fetch_csv(raw_data_url)
    json_data = json.loads(data.to_json(orient='records'))

    analysed = DataAnalyser(json_data)
    latest_resource['summary'] = analysed.summary()
    latest_resource['url'] = raw_data_url

    return latest_resource