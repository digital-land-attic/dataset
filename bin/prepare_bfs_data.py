#!/usr/bin/env python3

import sys
import json
# add parent directory
sys.path.append(".")

from analyse_dataset import BrownfieldDatasetAnalyser
from organisation import fetch_organisations
from bin.points_to_features import convert_json_to_geojson


da = BrownfieldDatasetAnalyser("./brownfield-land-collection/index/dataset.csv")


def process_org(org):
    return {
        "id": org.get('organisation'),
        "statistical_geography": org.get("statistical-geography"),
        "name": org.get("name"),
        "count": len(da.get_data_for_organisation(org.get('organisation')))
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
orgs_with_bfs = da.organisations()
# need to remove any pesky None organisation values
orgs_with_bfs = [o for o in orgs_with_bfs if o is not None]
d = brownfield_map(orgs_with_bfs)

with open('data/org_boundaries.json', 'w') as file:
    file.write(json.dumps(d))


for o in orgs_with_bfs:
    curie_url = "/".join(organisations[o]["path-segments"])
    sites = da.get_data_for_organisation(o)
    gjson = convert_json_to_geojson(sites)
    with open(f'docs/brownfield-land/organisation/{curie_url}/sites.geojson', 'w') as file:
        file.write(json.dumps(gjson))


