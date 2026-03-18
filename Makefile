SHELL := /bin/bash
.SHELLFLAGS := -c

.PHONY: all update

all: full-update

update:
	@echo "Updating reports..."
	@python -m reading_stats.reports.authors_scatter
	@python -m reading_stats.reports.genres_scatter
	@python -m reading_stats.reports.works_scatter
	@python -m reading_stats.reports.next_reads
	@python -m reading_stats.reports.author_bibliography --author "Stephen King" --table
	@echo "Reports updated."

full-update:
	@echo "Updating reading stats and reports..."
	@$(MAKE) update
	@echo "Pushing to GitHub..."
	@git add .
	@git commit -m "Automated update."
	@git push origin main
	@echo "Update complete."
