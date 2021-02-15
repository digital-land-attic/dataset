.PHONY: init all render clobber black clean prune
.SECONDARY:
.DELETE_ON_ERROR:

TEMPLATE_FILES=\
	templates/dataset.html\
	templates/dataset-organisation.html\
	templates/dataset-organisations.html\
	templates/dataset-resources.html\
	templates/datasets.html

# current git branch
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

all:	render

render:	render.py $(DATASET_FILES) $(TEMPLATE_FILES)
	@-rm -rf ./docs/
	@-mkdir ./docs/
	python3 render.py
	@touch ./docs/.nojekyll
	cd brownfield-resources && make collect && python3 resource_generator/check_per_org.py --all # this is done in a subshell
	rsync -a ./dataset/docs/ ./docs/
	rm -rf dataset
	python3 bin/prepare_bfs_data.py

black:
	black .

init::
	git submodule update --init --recursive --remote
	python3 -m pip install -r requirements.txt
	cd brownfield-resources && python3 -m pip install -r requirements.txt # this is done in a subshell

clobber clean:
	rm -rf docs .cache


collect::
	mkdir -p data/brownfield 
	curl -qsL 'https://raw.githubusercontent.com/digital-land/brownfield-land-collection/main/collection/resource.csv' > data/brownfield/resource.csv


map:
	python3 bin/create_bfs_map.py


map/local:
	python3 bin/create_bfs_map.py --local


commit-docs::
	git add docs
	git diff --quiet && git diff --staged --quiet || (git commit -m "Rebuilt design system $(shell date +%F)"; git push origin $(BRANCH))
