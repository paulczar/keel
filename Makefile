HUGO := /opt/homebrew/bin/hugo

.PHONY: preview build clean rules test sync

## preview: Start local dev server with live reload
preview:
	$(HUGO) server --buildDrafts --navigateToChanged

## build: Production build with minification
build:
	$(HUGO) --gc --minify

## clean: Remove generated files
clean:
	rm -rf public resources/_gen .hugo_build.lock

# Rules to symlink into .cursor/rules/keel/ (add/remove as needed)
CURSOR_RULES := base yaml hugo markdown mdc

## rules: Create .cursor/rules/keel/ symlinks for local development
rules:
	@mkdir -p .cursor/rules/keel
	@for rule in $(CURSOR_RULES); do \
		ln -sf ../../../content/rules/$$rule.md .cursor/rules/keel/$$rule.mdc; \
	done
	@echo "Symlinked $(words $(CURSOR_RULES)) rules to .cursor/rules/keel/"

## sync: Dry-run keel-sync.py against this repo's rules
sync:
	python3 scripts/keel-sync.py --path content/rules --dry-run

## test: Run tests
test:
	@bash tests/test-install.sh
	@python3 -m pytest tests/test_keel_sync.py -v

## help: Show available targets
help:
	@grep '^## ' Makefile | sed 's/^## //' | column -t -s ':'
