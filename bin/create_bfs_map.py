#!/usr/bin/env python3

import os
import sys
import json

# add parent directory
sys.path.append(".")

from digital_land_frontend.jinja import setup_jinja

# from digital_land_frontend.render import render


def render(path, template, docs="docs", **kwargs):
    path = os.path.join(docs, path)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "w") as f:
        print(f"creating {path}")
        f.write(template.render(**kwargs))


def read_in_json(path):
    file = open(path, mode="r")
    s = file.read()
    return json.loads(s)


env = setup_jinja()
env.globals["includeAutocomplete"] = True
map_template = env.get_template("brownfield-land-map.html")

data = read_in_json("data/org_boundaries.json")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--local":
        env.globals["staticPath"] = "/static"
        env.globals["urlPath"] = ""

    render("brownfield-land/map/index.html", map_template, data=data)
