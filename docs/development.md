# Development

## Set up and check

Install Python 3.13, Node.js 22 or later, and PHP 8.3 or later:

```sh
make setup
make check lint-php test package docs
```

The build uses the version in `extension/ra_darktheme.xml` and includes only its
declared files. Archive order, permissions and timestamps are deterministic.
`dist/`, `site/`, local previews and test output are ignored by Git.

## Joomla integration

The service provider registers `DarkTheme` as a system plugin. Its event
subscriber handles `onBeforeCompileHead`, checks the application, document and
template, then registers assets through Web Asset Manager. Styles use a higher
weight than normal template CSS. Asset URLs support subdirectory installations.

The small bootstrap script is synchronous and independent of Joomla's core
JavaScript. Its validated default is passed as an HTML data attribute. The
deferred main script depends on Joomla core and reads normal script options.
The plugin uses no inline executable script or runtime CDN dependency.

The namespace is `RADarkTheme\Plugin\System\RaDarktheme`, and the element is
`ra_darktheme`. Keep the namespace, provider and manifest consistent.

## Documentation

Zensical and Prodockit are pinned in `requirements-docs.txt`. Managed styles and
scripts are checked before a strict documentation build. Put local styling in
`docs/stylesheets/extra.css`; run `make docs-assets` after deliberately changing
the Prodockit pin. `make docs-serve` serves the guide on localhost port 8000.

GitHub Actions is prepared for PHP syntax/behaviour checks and browser-runtime,
package and documentation checks. The repository URL is configured; add the site URL to `zensical.toml` when
documentation is published.

## Local public-site preview

```sh
.venv/bin/python scripts/prepare_preview.py --source ../alton-dark-mode-prototype/.local-site
make preview
```

The helper copies an existing static mirror into ignored `.local-site/`, removes
the prototype theme assets and installs the shipped plugin assets with sample
Joomla options. It defaults to dark mode for review. Existing source content
security rules remain in place. It performs no network mirroring and copies no
Joomla database or administrator credentials.

## Sources

- [Joomla plugin tutorial](https://manual.joomla.org/docs/building-extensions/plugins/basic-content-plugin/)
- [Joomla Web Asset Manager](https://manual.joomla.org/docs/general-concepts/web-asset-manager/)
- [Ramblers naming example](https://github.com/ramblerswebs/ra-tools)
- [Prodockit icon reference](https://prodockit.org/)
