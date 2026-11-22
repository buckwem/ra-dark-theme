# RA Dark Theme

Use natural British English. Preserve code identifiers and direct quotations.

- This repository contains a complete Joomla/Gantry site template, `ra_darktheme`.
- Keep installable source in `template/`, documentation in `docs/`, build tools in `scripts/` and checks in `tests/`.
- The version in `template/templateDetails.xml` owns the package version. Keep both Gantry theme metadata files consistent.
- `make package` must build only `tpl_ra_darktheme-VERSION.zip` from the declared template files.
- Preserve the supplied Ramblers layout, font settings and module positions. Retain upstream copyright notices.
- Keep Festive Overlay separate. Do not include website snapshots, database exports, credentials, videos or compiled caches.
- Template source and its supplied custom assets are authorised for this repository; the original administrator archive stays local.
- Run `make check lint-php test package docs` when applicable.
- Prodockit owns `docs/stylesheets/pdk*.css` and `docs/javascripts/pdk.js`. Put custom styles in `docs/stylesheets/extra.css`.
- Do not use Playwright.
