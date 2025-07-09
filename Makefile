SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command

.PHONY: all update-repo

all: update-repo

create-plots:
	python .\src\authors.py
	python .\src\works.py

update-repo:
	python .\src\authors.py
	python .\src\works.py
	git add .
	git commit -m "Make commit."
	git push