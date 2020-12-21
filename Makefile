.PHONY: init all render clobber black clean prune
.SECONDARY:
.DELETE_ON_ERROR:

TEMPLATE_FILES=\
	templates/dataset.html\
	templates/dataset-organisation.html\
	templates/dataset-organisations.html\
	templates/dataset-resources.html\
	templates/datasets.html

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


map:
	python3 bin/create_bfs_map.py


map/local:
	python3 bin/create_bfs_map.py --local

