#!/usr/bin/env python3

import sys
import json

# add parent directory
sys.path.append(".")

from utils import get

sample_file = "docs/brownfield-land/organisation/local-authority-eng/HAG/sites.json"


def create_feature_collection(features):
    return {"type": "FeatureCollection", "features": features}


def create_feature_from_point(lng, lat, _properties):
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": _properties,
    }


def convert_json_to_geojson(data):
    features = []
    for row in data:
        if "point" in row.keys():
            features.append(row["point"])
        else:
            features.append(
                create_feature_from_point(row["longitude"], row["latitude"], row)
            )

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
