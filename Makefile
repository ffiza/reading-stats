.PHONY: all create-environment create-plots

all: create-environment create-plots

create-environment:
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r requirements.txt

create-plots:
	python .\src\authors.py