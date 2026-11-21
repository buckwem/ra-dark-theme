# RA Dark Theme

Use natural British English. Preserve code identifiers and direct quotations.

- Keep Joomla plugin source in `extension/`, documentation in `docs/`, build
  utilities in `scripts/` and behaviour checks in `tests/`.
- The repository name is `ra-dark-theme`; Joomla's system-plugin element is
  `ra_darktheme`. Keep its manifest, namespace and provider consistent.
- Keep this extension independent of Festive Overlay. Do not bundle public-site
  snapshots, photographs, videos, administrator data or credentials.
- Target Joomla 5.4 and 6.x with PHP 8.3+. Describe support as provisional until
  installation, update and removal have been checked on real Joomla sites.
- Use service providers, event subscribers and Web Asset Manager APIs.
- Preserve keyboard operation, visitor preferences, original fonts and photos.
- Run `make check lint-php test package docs` when applicable.
- Prodockit owns `docs/stylesheets/pdk*.css` and `docs/javascripts/pdk.js`.
  Put custom documentation styles in `docs/stylesheets/extra.css`.
- Do not use Playwright.
