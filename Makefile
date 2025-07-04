SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command

.PHONY: all create-plots

all: create-plots

create-plots:
	python .\src\authors.py
	python .\src\works.py
	git add .
	git commit -m "Make commit."
	git push