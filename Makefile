PYTHON ?= python3.13
PHP_BIN ?= php
NODE ?= node
VENV ?= .venv

.PHONY: setup check lint-php test test-js test-php package docs docs-assets docs-serve preview
setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/python -m pip install -r requirements-docs.txt
check:
	$(PYTHON) scripts/build_package.py --check
lint-php:
	$(PHP_BIN) -r 'exit(PHP_VERSION_ID >= 80300 ? 0 : 1);'
	$(PHP_BIN) -l extension/services/provider.php
	$(PHP_BIN) -l extension/src/Extension/DarkTheme.php
	$(PHP_BIN) -l theme-source/includes/ra-theme.php
test: test-js test-php
test-js:
	$(NODE) --test tests/theme.test.cjs
test-php:
	$(PHP_BIN) tests/plugin.php
	$(PHP_BIN) tests/template.php
package:
	$(PYTHON) scripts/build_package.py
docs-assets:
	$(VENV)/bin/prodockit shared-files --apply
docs:
	$(VENV)/bin/prodockit shared-files --check
	$(VENV)/bin/zensical build --clean --strict
docs-serve:
	$(VENV)/bin/zensical serve --dev-addr 127.0.0.1:8000
preview:
	$(PYTHON) -m http.server 8768 --bind 127.0.0.1 --directory .local-site
