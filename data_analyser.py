#!/usr/bin/env python3

from numbers import Number


class DataAnalyser():

    def __init__(self, data):
        super().__init__()
        self.data = data

    def count_pip(self):
        permission_types = [x["PermissionType"] for x in self.data]
        return permission_types.count("permission in principle")

    def count_pip_active(self):
        permission_types = [x["PermissionType"] for x in self.data if x['EndDate'] is None]
        return permission_types.count("permission in principle")

    def countHasLatLng(self):
        return len([(row['GeoY'], row['GeoX']) for row in self.data if row['GeoX'] and row['GeoY']])

    def end_date_count(self):
        return len([x['EndDate'] for x in self.data if x['EndDate'] is not None])

    def row_count(self):
        return len(self.data)

    def org_uris(self):
        return [row['OrganisationURI'] for row in self.data]

    def sum_max_dwellings(self):
        return sum([x['NetDwellingsRangeTo'] for x in self.data if isinstance(x['NetDwellingsRangeTo'], Number)])

    def sum_max_dwellings_active(self):
        return sum([x['NetDwellingsRangeTo'] for x in self.data if isinstance(x['NetDwellingsRangeTo'], Number) and x['EndDate'] is None])

    def sum_min_dwellings(self):
        return sum([x['NetDwellingsRangeFrom'] for x in self.data if isinstance(x['NetDwellingsRangeFrom'], Number)])

    def sum_min_dwellings_active(self):
        return sum([x['NetDwellingsRangeFrom'] for x in self.data if isinstance(x['NetDwellingsRangeFrom'], Number) and x['EndDate'] is None])

    def total_hectares(self):
        return sum([x['Hectares'] for x in self.data if isinstance(x['Hectares'], Number)])

    def total_hectares_active(self):
        h = [x['Hectares'] for x in self.data if isinstance(x['Hectares'], Number) and x['EndDate'] is None]
        return sum(h)

    def summary(self):
        return {
            "total": self.row_count(),
            "end_dates": self.end_date_count(),
            "hasLatLng": self.countHasLatLng(),
            "hectares": self.total_hectares(),
            "hectares_active": self.total_hectares_active(),
            "max_dwellings": self.sum_max_dwellings(),
            "max_dwellings_active": self.sum_max_dwellings_active(),
            "min_dwellings": self.sum_min_dwellings(),
            "min_dwellings_active": self.sum_min_dwellings_active(),
            "permission_in_principle": self.count_pip(),
            "permission_in_principle_active": self.count_pip_active(),
            "unique_organisation_uris": len(set(self.org_uris()))
        }
