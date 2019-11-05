#!/usr/bin/env python3

import os
import jinja2
import csv
import json
import requests
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache
from collections import OrderedDict

session = CacheControl(requests.session(), cache=FileCache('.cache'))

dataset_csv='https://raw.githubusercontent.com/digital-land/dataset-collection/master/dataset/dataset.csv'
organisation_csv='https://raw.githubusercontent.com/digital-land/organisation-collection/master/collection/organisation.csv'
organisation_tag_csv='https://raw.githubusercontent.com/digital-land/organisation-collection/master/data/tag.csv'

def get(url):
    r = session.get(url)
    r.raise_for_status()
    return r.text


loader = jinja2.FileSystemLoader(searchpath="./templates")
env = jinja2.Environment(loader=loader)


datasets_template = env.get_template("datasets.html")
dataset_template = env.get_template("dataset.html")
item_template = env.get_template("dataset-organisation.html")


organisations = OrderedDict()
for o in csv.DictReader(get(organisation_csv).splitlines()):
    organisations[o["organisation"]] = o


tags = OrderedDict()
for o in csv.DictReader(get(organisation_tag_csv).splitlines()):
    o["organisations"] = []
    tags[o["tag"]] = o


index = {}
datasets = OrderedDict()
for o in csv.DictReader(get(dataset_csv).splitlines()):
    index = json.loads(get(o['resource-url']))
    datasets[o["dataset"]] = o


for dataset in index['dataset']:
    for organisation in index['dataset'][dataset]:
        o = organisations[organisation]

        o["path-segments"] = list(filter(None, o["organisation"].split(":")))
        prefix = o["prefix"] = o["path-segments"][0]
        o["id"] = o["path-segments"][1]
        o.setdefault("tags", [])
        o["tags"].append(prefix)

        tags[prefix]["organisations"].append(o)

        for tag in tags:
            for o in tags[tag]["organisations"]:
                o["path"] = "./docs/" + "/".join(o["path-segments"])

                if o["path"] and not os.path.exists(o["path"]):
                    os.makedirs(o["path"])

                #with open('docs/' + o["path"] + "/" + "index.html", "w") as f:
                    #f.write(item_template.render(organisation=o, ))
print(datasets)
with open("docs/index.html", "w") as f:
    f.write(datasets_template.render(datasets=datasets, download_url=dataset_csv))
