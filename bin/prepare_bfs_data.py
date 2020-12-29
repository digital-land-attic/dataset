#!/usr/bin/env python3

import os
import sys
import json

# add parent directory
sys.path.append(".")

from analyse_dataset import BrownfieldDatasetAnalyser
from organisation import fetch_organisations
from points_to_features import convert_json_to_geojson


brownfield_dataset = "./brownfield-land-collection/dataset/deduped.csv"


def process_org(org):
    sites = da.get_data_for_organisation(org.get("organisation"))
    return {
        "id": org.get("organisation"),
        "statistical_geography": org.get("statistical-geography"),
        "name": org.get("name"),
        "count": len(sites),
    }


def brownfield_map(orgs):
    orgs_data = []
    for o_id in orgs:
        if organisations.get(o_id) is not None:
            orgs_data.append(process_org(organisations.get(o_id)))
        else:
            print("no match for", o_id)
    return orgs_data


def create_site_geojson(organisation):
    curie_url = "/".join(organisation["path-segments"])
    sites = da.get_data_for_organisation(organisation["organisation"])
    gjson = convert_json_to_geojson(sites)
    with open(
        f"docs/brownfield-land/organisation/{curie_url}/sites.geojson", "w"
    ) as file:
        file.write(json.dumps(gjson))


if os.path.exists(brownfield_dataset):
    da = BrownfieldDatasetAnalyser(brownfield_dataset)

    organisations = fetch_organisations()
    orgs_with_bfs = da.organisations()
    # need to remove any pesky None organisation values
    orgs_with_bfs = [o for o in orgs_with_bfs if o is not None]
    d = brownfield_map(orgs_with_bfs)

    # save summary data needed by map
    with open("data/organisation_boundary_data.json", "w") as file:
        file.write(json.dumps(d))

    # create geojson of sites for each organisation
    for o in orgs_with_bfs:
        create_site_geojson(organisations[o])

else:
    print(f"Error: {brownfield_dataset} does not exist! Unable to prepare data.")
