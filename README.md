# RA Dark Theme

A separate Joomla system plugin providing light and dark themes for Ramblers
websites using the Gantry 5 Hydrogen template. It includes the colours reviewed
on Alton Ramblers and the compact sun/moon icons used by Prodockit.

**Version 0.1.0-beta1.** Intended for Joomla 5.4 and 6.x with PHP 8.3+. The browser
behaviour and package are checked locally; installation, update and removal on
real Joomla installations remain required before a production release.

## Names

| Purpose | Name |
| --- | --- |
| Repository | `ra-dark-theme` |
| Joomla plugin | `System - RA Dark Theme` |
| Joomla element / group | `ra_darktheme` / `system` |
| Installable ZIP | `plg_system_ra_darktheme-0.1.0-beta1.zip` |
| Media directory | `media/plg_system_ra_darktheme/` |

The repository prefix follows projects such as
[ramblerswebs/ra-tools](https://github.com/ramblerswebs/ra-tools).
This is an independent extension, not an official Ramblers release.

## Features

- Device preference, light or dark default, with saved visitor choices.
- Small 18-pixel sun/moon icons, 32-pixel visible button and a 44-pixel pointer
  target beside the title; optional fixed corner positions.
- Dark article, contact-table, walks-list, calendar, mobile-menu, gallery-frame
  and map-control colours. Original font families and image colours are retained.
- Optional colour matching for an existing WeatherWidget.io forecast.
- Original print colours; no dark styling on administrator, component-only,
  non-HTML or non-matching template pages.

It has no Festive Overlay dependency. The existing festive runtime can detect
the new page background when both plugins are installed.

## Build and preview

```sh
make setup
make check lint-php test package docs
make docs-serve
```

The installer is generated in `dist/`; documentation is generated in `site/`.
The pinned documentation tools are Zensical and Prodockit. To test the browser
assets on a local copy without installing Joomla:

```sh
.venv/bin/python scripts/prepare_preview.py --source ../alton-dark-mode-prototype/.local-site
make preview
```

Open <http://127.0.0.1:8768/>. This uses the plugin's shipped browser files and
sample Joomla script options. It is a static preview, not a Joomla installation.

## Install on a staging site

1. Upload the generated ZIP through **System → Install → Extensions**.
2. Open **System → Manage → Plugins → System - RA Dark Theme** and enable it.
3. Check the default theme, switch position and template folder. The template
   defaults to `g5_hydrogen`.
4. Remove the earlier prototype CSS and switch before enabling this plugin,
   clear Joomla/template/browser caches, and review the pages on your site.

See `docs/installation.md`, `docs/configuration.md` and `docs/testing.md` for
scope, settings and the remaining integration checks.

## GitHub setup

The local Git repository starts on `main` and connects over SSH to
[the public repository](https://github.com/buckwem/ra-dark-theme).
For a fresh clone:

```sh
git clone git@github.com:buckwem/ra-dark-theme.git
cd ra-dark-theme
make setup
```

GitHub Actions is prepared to check PHP, JavaScript, packaging and documentation.
No release, update server or public website deployment is configured yet. Add
the documentation site URL to `zensical.toml` once that destination exists.

## Licence

GPL-2.0-or-later. Lucide/Feather icon notices are included in
`extension/THIRD_PARTY_NOTICES.txt`. Site photographs, logos, videos and copied
page content are excluded from the source repository and installer.
