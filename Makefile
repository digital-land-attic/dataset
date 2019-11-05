.PHONY: init all render clobber black clean prune
.SECONDARY:
.DELETE_ON_ERROR:

all:	render

render:	render.py $(DATASET_FILES)
	@-rm -rf ./docs/
	@-mkdir ./docs/
	python3 render.py
	touch ./docs/.nojekyll

black:
	black .

init::
	python3 -m pip install -r requirements.txt

clobber clean:
	rm -rf docs .cache
