SHELL := /bin/bash
.SHELLFLAGS := -c

.PHONY: all update

all: update

update:
	python ./src/read_history.py
	python ./src/authors.py
	python ./src/works.py
	python ./src/to_read_next.py
	python ./src/stephen_king.py
