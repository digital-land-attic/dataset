import json
import pandas as pd
import requests

from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache

session = CacheControl(requests.session(), cache=FileCache(".cache"))

def get(url):
    r = session.get(url)
    r.raise_for_status()
    return r.text


def get_csv_as_json(path_to_csv, cache=False):
    if cache:
        csv_str = get(path_to_csv)
        csv_pd = pd.read_csv(StringIO(csv_str), sep=",")
    else:
        csv_pd = pd.read_csv(path_to_csv, sep=",")
    return json.loads(csv_pd.to_json(orient="records"))


def make_index(data, key):
    idx = {}
    idx['with_key_missing'] = []
    for row in data:
        if key in row:
            idx.setdefault(row[key], [])
            idx[row[key]].append(row)
        else:
            idx['with_key_missing'].append(row)
    return idx
