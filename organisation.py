#!/usr/bin/env python3

import csv
from collections import OrderedDict

from utils import get


def fetch_organisations(organisation_csv="https://raw.githubusercontent.com/digital-land/organisation-dataset/master/collection/organisation.csv"):
    organisations = OrderedDict()
    for o in csv.DictReader(get(organisation_csv).splitlines()):
        o["path-segments"] = list(filter(None, o["organisation"].split(":")))
        prefix = o["prefix"] = o["path-segments"][0]
        o["id"] = o["path-segments"][1]
        o.setdefault("tags", [])
        o["tags"].append(prefix)
        organisations[o["organisation"]] = o
    return organisations


def get_organisation_boundary(organisations, _id):
    if organisations.get(_id) and not organisations.get(_id)['boundary'] == "":
        return organisations[_id]['boundary']
    return None
    #return [org for org in organisations if org['organisation'] == _id and org['boundary'] is not None]


def get_boundaries(organisations, ids):
    boundaries = []
    for _id in ids:
        if get_organisation_boundary(organisations, _id) is not None:
            boundaries.append(get_organisation_boundary(organisations, _id))
    return boundaries
