import validators

from filter.organisation_mapper import map_organisation_id_filter

def is_valid_uri(uri):
    if validators.url(uri):
        return True
    return False

def float_to_int(v):
    if v:
        return int(float(v))
    return ""

def statistical_geography_code(v):
    if v:
        return v.replace("statistical-geography:", "")
    return v
