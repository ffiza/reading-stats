SHELL := /bin/bash
.SHELLFLAGS := -c

.PHONY: all update-repo create-plots

all: update-repo

create-plots:
	python ./src/authors.py
	python ./src/works.py

update-repo:
	python ./src/authors.py
	python ./src/works.py
	git add .
	git commit -m "Automated commit."
	git push