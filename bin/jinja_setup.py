#!/usr/bin/env python3

import jinja2
import digital_land_frontend.filters as dlfilters
from filters import statistical_geography_code, map_organisation_id_filter

multi_loader = jinja2.ChoiceLoader([
    jinja2.FileSystemLoader(searchpath="./templates"),
    jinja2.PrefixLoader({
        'govuk-jinja-components': jinja2.PackageLoader('govuk_jinja_components'),
        'digital-land-frontend': jinja2.PackageLoader('digital_land_frontend')
    })
])
env = jinja2.Environment(loader=multi_loader)

# set variables to make available to all templates
env.globals["staticPath"] = "https://digital-land.github.io"

# register common filters
env.filters['commanum'] = dlfilters.commanum
env.filters['is_valid_uri'] = dlfilters.is_valid_uri
env.filters['float_to_int'] = dlfilters.float_to_int

# register repo specific filters
env.filters['statistical_geography_code'] = statistical_geography_code
env.filters['map_organisation_by_id'] = map_organisation_id_filter
