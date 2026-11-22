# Development

The complete installable Gantry source is in `template/`. The manifest
`template/templateDetails.xml` owns the package version. Keep both Gantry theme
metadata files consistent and preserve upstream notices.

```sh
make setup
make check lint-php test package docs
```

The deterministic package builder validates the manifest and builds the template
ZIP without an external archive. GitHub Actions checks PHP 8.3/8.4, JavaScript,
packaging and the strict Zensical/Prodockit documentation build.

The template boots Gantry and loads `includes/ra-theme.php` before rendering.
This reads the active outline's `page.ra-theme` settings and registers assets
through Joomla's Web Asset Manager with absolute URLs. An early bootstrap sets
the palette; the deferred runtime reads `tpl_ra_darktheme` script options.

Run `make docs-serve` to preview the documentation. Prodockit owns the managed
pdk styles and JavaScript; custom styles belong in `docs/stylesheets/extra.css`.
Use `make docs-assets` to refresh the managed assets.

For a static preview, run `scripts/prepare_preview.py --source PATH` with a
separate local page mirror, then `make preview`. It does not execute Joomla.
Test installation, updates, removal, menu assignment and dynamic widgets on a
Joomla staging copy. Keep website mirrors, credentials and compiled caches out
of Git.
