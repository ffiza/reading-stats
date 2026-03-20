SHELL := /bin/bash
.SHELLFLAGS := -c

.PHONY: all update

all: full-update

update:
	@echo "Updating reports..."
	@reading-stats all
	@echo "Reports updated."

full-update:
	@echo "Updating reading stats and reports..."
	@$(MAKE) update
	@echo "Pushing to GitHub..."
	@git add .
	@git commit -m "Automated update."
	@git push origin main
	@echo "Update complete."
