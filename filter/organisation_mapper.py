import csv
import requests

# get data from organisation dataset
dataset = "https://raw.githubusercontent.com/digital-land/organisation-dataset/master/collection/organisation.csv"


class OrganisationMapper:
    def __init__(self, url):
        self.mapping = {}
        self.dataset_url = url
        self.raw = self.fetch_data()

        self.create_mapping()

    def fetch_data(self):
        response = requests.get(self.dataset_url)
        return response.text

    def create_mapping(self):
        cr = csv.DictReader(self.raw.splitlines())
        for row in cr:
            key = row['organisation']
            self.mapping[key] = row['name']

    def get_by_key(self, k):
        return self.mapping.get(k)

    def get_mapping(self):
        return self.mapping

    def replace_key(self, current, replacement):
        if current in self.mapping:
            self.mapping[replacement] = self.mapping[current]
            del self.mapping[current]


organisation_mapper = OrganisationMapper(dataset)
def map_organisation_id_filter(id):
    return organisation_mapper.get_by_key(id)
