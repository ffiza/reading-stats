SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command

.PHONY: all create-environment create-plots

all: create-environment create-plots

create-environment:
	if (Test-Path ".venv") { Remove-Item -Recurse -Force ".venv" }
	python -m venv .venv
	.venv\Scripts\python.exe -m pip install -r requirements.txt

create-plots:
	python .\src\authors.py