#!/usr/bin/env python3

import sys
import json
import csv

import pandas as pd


class DatasetAnalyser():

    def __init__(self, path):
        super().__init__()
        self.dataset_path = path
        self.pd_data = self.panda_read()
        self.json_data = json.loads(self.pd_data.to_json(orient='records'))

    def panda_read(self):
        # read local file
        data = pd.read_csv(self.dataset_path, sep=",")
        return data

    def number_of_fields(self):
        return len(self.json_data[0].keys())

    def number_of_records(self):
        return len(self.json_data)

    def active_records(self):
        return [x for x in self.json_data if x['end-date'] is None]

    def historical_records(self):
        return [x for x in self.json_data if x['end-date'] is not None]

    def sample(self, count=5, start_from=0):
        if len(self.json_data) >= count:
            return self.json_data[start_from:(start_from+count)]


# Keep Brownfield specific code separate 
class BrownfieldDatasetAnalyser(DatasetAnalyser):
    def __init__(self, path):
        self.type = "brownfield-land"
        DatasetAnalyser.__init__(self, path)

    # should this be moved to parent class
    def organisations(self):
        orgs = [x['organisation'] for x in self.json_data]
        return set(orgs)
    
    def no_organisation(self):
        sites = [x for x in self.json_data if x['organisation'] is None]
        return sites

    # dwelling analysis
    # currently uses min dwelling figure
    def largest_dwelling_count(self):
        return self.pd_data['minimum-net-dwellings'].max()

    def total_dwellings(self):
        min_dwellings = [x['minimum-net-dwellings']
                         for x in self.json_data if x['minimum-net-dwellings'] is not None]
        return sum(min_dwellings)

    # hectare analysis
    def largest_hectare_value(self):
        return self.pd_data['hectare'].max()

    def total_hectares(self):
        hectares = [x['hectares']
                    for x in self.json_data if x['hectares'] is not None]
        return "{0:.2f}".format(sum(hectares))

    def summary(self):
        return {
            'records': self.number_of_records(),
            'active_records': len(self.active_records()),
            'hectares': self.total_hectares(),
            'dwellings': int(self.total_dwellings()),
            'organisations': len(self.organisations()),
            'historical_records': int(self.number_of_records() - len(self.active_records())),
            'fields': self.number_of_fields()
        }


if __name__ == '__main__':
    da = BrownfieldDatasetAnalyser("https://raw.githubusercontent.com/digital-land/brownfield-land-collection/master/index/dataset.csv")
    da = BrownfieldDatasetAnalyser("https://raw.githubusercontent.com/digital-land/brownfield-land-collection/master/index/entries.csv")
    sites = [2,234,2333,23333,123,12234,24829,888,998,4672,776,7877,10232,12134]
    for s in sites:
        print(s, ": ", da.json_data[s]['end-date'])
    print(da.summary())