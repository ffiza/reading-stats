SHELL := /bin/bash
.SHELLFLAGS := -c

.PHONY: all update

all: automatic-update

update:
	python ./reading_stats/export/read_history.py
	python ./reading_stats/export/authors.py
	python ./reading_stats/export/works.py
	python ./reading_stats/export/genres.py
	python ./reading_stats/export/next_reads.py
	python ./reading_stats/export/export_author_bibliography.py --author "Stephen King"
	python ./reading_stats/export/export_author_bibliography.py --author "H. P. Lovecraft"
	python ./reports/authors_scatter.py
	python ./reports/genres_scatter.py
	python ./reports/works_scatter.py

full-update:
	@echo "Updating reading stats and reports..."
	@$(MAKE) update
	@echo "Pushing to GitHub..."
	@git add .
	@git commit -m "Automated update."
	@git push origin main
	@echo "Update complete."
