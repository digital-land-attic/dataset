#!/usr/bin/env python3

import os
import jinja2
import csv
import json
import requests
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache
from collections import OrderedDict

session = CacheControl(requests.session(), cache=FileCache(".cache"))

dataset_csv = "https://raw.githubusercontent.com/digital-land/dataset-collection/master/dataset/dataset.csv"
organisation_csv = "https://raw.githubusercontent.com/digital-land/organisation-collection/master/collection/organisation.csv"
organisation_tag_csv = "https://raw.githubusercontent.com/digital-land/organisation-collection/master/data/tag.csv"


def get(url):
    r = session.get(url)
    r.raise_for_status()
    return r.text


loader = jinja2.FileSystemLoader(searchpath="./templates")
env = jinja2.Environment(loader=loader)


datasets_template = env.get_template("datasets.html")
dataset_template = env.get_template("dataset.html")
dataset_organisations_template = env.get_template("dataset-organisations.html")
dataset_organisation_template = env.get_template("dataset-organisation.html")


tags = OrderedDict()
for o in csv.DictReader(get(organisation_tag_csv).splitlines()):
    o["organisations"] = []
    tags[o["tag"]] = o


organisations = OrderedDict()
for o in csv.DictReader(get(organisation_csv).splitlines()):
    o["path-segments"] = list(filter(None, o["organisation"].split(":")))
    prefix = o["prefix"] = o["path-segments"][0]
    o["id"] = o["path-segments"][1]
    o.setdefault("tags", [])
    o["tags"].append(prefix)
    organisations[o["organisation"]] = o


datasets = OrderedDict()
for d in csv.DictReader(get(dataset_csv).splitlines()):
    dataset = d["dataset"]

    index_url = os.environ.get(dataset.replace("-", "_") + "_index", d["resource-url"])

    d["index"] = json.loads(get(index_url))
    d["organisation"] = {}

    # expand index
    for key in d["index"]:
        dates = list(d["index"][key]["log"].keys())
        if dates:
            date = list(d["index"][key]["log"].keys())[-1]
            d["index"][key]["date"] = date
            d["index"][key]["status"] = d["index"][key]["log"][date].get("status", d["index"][key]["log"][date].get("exception", "*"))
            d["index"][key]["colour"] = "green" if d["index"][key]["status"] in ["200", "*"] else "red"

        for organisation in d["index"][key]["organisation"]:
            d["organisation"].setdefault(organisation, {"key": []})
            d["organisation"][organisation]["key"].append(key)

    for organisation in d["organisation"]:
        d["organisation"][organisation]["key"] = sorted(d["organisation"][organisation]["key"], key=lambda key: d["index"][key].get("date", ""))

    datasets[dataset] = d

    # organisation page
    for organisation in d["organisation"]:
        o = organisations[organisation]

        o["path"] = "/".join(o["path-segments"])
        p = "docs/" + dataset + "/organisation/" + o["path"]
        if p and not os.path.exists(p):
            os.makedirs(p)

        with open(p + "/" + "index.html", "w") as f:
            f.write(
                dataset_organisation_template.render(
                    organisations=organisations, organisation=o, dataset=d
                )
            )

    # indexes
    with open("docs/" + dataset + "/organisation/index.html", "w") as f:
        f.write(
            dataset_organisations_template.render(
                organisations=organisations, tags=tags, dataset=d
            )
        )

    with open("docs/" + dataset + "/index.html", "w") as f:
        f.write(
            dataset_template.render(organisations=organisations, tags=tags, dataset=d)
        )

with open("docs/index.html", "w") as f:
    f.write(datasets_template.render(datasets=datasets, download_url=dataset_csv))
