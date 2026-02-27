HUGO := /opt/homebrew/bin/hugo

.PHONY: preview build clean rules

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

## help: Show available targets
help:
	@grep '^## ' Makefile | sed 's/^## //' | column -t -s ':'
