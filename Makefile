HUGO := /opt/homebrew/bin/hugo

.PHONY: preview build clean sync

## preview: Start local dev server with live reload
preview:
	$(HUGO) server --buildDrafts --navigateToChanged

## build: Production build with minification
build:
	$(HUGO) --gc --minify

## clean: Remove generated files
clean:
	rm -rf public resources/_gen .hugo_build.lock

## sync: Sync rules to a target repo (usage: make sync TARGET=/path/to/repo)
sync:
	@if [ -z "$(TARGET)" ]; then echo "Usage: make sync TARGET=/path/to/repo"; exit 1; fi
	./scripts/sync-rules.sh $(TARGET)

## help: Show available targets
help:
	@grep '^## ' Makefile | sed 's/^## //' | column -t -s ':'
