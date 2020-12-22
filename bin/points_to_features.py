#!/usr/bin/env python3

import sys
import json

# add parent directory
sys.path.append(".")

from utils import get
from digital_land_frontend.render import wkt_to_json_geometry

sample_file = "docs/brownfield-land/organisation/local-authority-eng/HAG/sites.json"


def create_feature_collection(features):
    return {"type": "FeatureCollection", "features": features}


def create_feature(row):
    feature = {"type": "Feature"}
    feature["properties"] = row
    if row["point"] is not None:
        feature["geometry"] = wkt_to_json_geometry(row["point"])
    return feature


def convert_json_to_geojson(data):
    features = []
    for row in data:
        features.append(create_feature(row))

    return create_feature_collection(features)


def test_convert(fn):
    # if file local
    with open(fn) as file:
        data = json.load(file)

    gjson = convert_json_to_geojson(data)

    with open(
        f"docs/brownfield-land/organisation/local-authority-eng/HAG/sites.geojson", "w"
    ) as file:
        file.write(json.dumps(gjson))
