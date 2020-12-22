import json

from utils import get, read_csv
from data_analyser import DataAnalyser

brownfield_dataset_path = "./brownfield-land-collection/dataset/brownfield-land.csv"
brownfield_deduped_dataset_path = "./brownfield-land-collection/dataset/deduped.csv"

# brownfield harmonised resources
def url_for_harmonised(resource_hash):
    return f"https://raw.githubusercontent.com/digital-land/brownfield-land-collection/main/harmonised/brownfield-land/{resource_hash}.csv"


# brownfield transformed resources
def url_for_transformed(resource_hash):
    return f"https://raw.githubusercontent.com/digital-land/brownfield-land-collection/main/transformed/brownfield-land/{resource_hash}.csv"


def index_by_org(resources):
    idx = {}
    for resource in resources:
        orgs = resource["organisations"].split(";")
        for org in orgs:
            idx.setdefault(org, {"resource": []})
            idx[org]["resource"].append(resource)
    return idx


def index_with_sort_resources(resources):
    idx = index_by_org(resources)
    for org in idx.keys():
        idx[org]["resource"].sort(key=lambda x: x["start-date"])
    return idx


def resources_by_org():
    all_resources = read_csv("data/brownfield/resource.csv")
    return index_with_sort_resources(all_resources)


def get_brownfield_resource_list(idx, organisation):
    return idx.get(organisation)["resource"]


def get_brownfield_resource(hash):
    url = url_for_transformed(hash)
    return read_csv(url, True)


def get_latest_brownfield_resource(resource_list, data_preview=False):
    latest_resource = resource_list[-1]
    raw_data_url = url_for_transformed(latest_resource["resource"])

    json_data = get_brownfield_resource(latest_resource["resource"])

    analysed = DataAnalyser(json_data, transformed=True)
    latest_resource["summary"] = analysed.summary()
    latest_resource["url"] = raw_data_url
    if data_preview:
        latest_resource["data_preview"] = json_data[:10]

    return latest_resource
