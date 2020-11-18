#!/usr/bin/env python3

import sys
import json
# add parent directory
sys.path.append(".")

from analyse_dataset import BrownfieldDatasetAnalyser
from organisation import fetch_organisations

def process_org(org):
    return {
        "id": org.get('organisation'),
        "statistical_geography": org.get("statistical-geography"),
        "name": org.get("name")
    }


def brownfield_map(orgs):
    orgs_data = []
    for o_id in orgs:
        if organisations.get(o_id) is not None:
            orgs_data.append( process_org(organisations.get(o_id)))
        else:
            print("no match for", o_id)
    return orgs_data


organisations = fetch_organisations()
da = BrownfieldDatasetAnalyser("./brownfield-land-collection/index/dataset.csv")
d = brownfield_map(da.organisations())

with open('data/org_boundaries.json', 'w') as file:
    file.write(json.dumps(d))
