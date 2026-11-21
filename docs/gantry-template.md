# Gantry template

RA Dark Theme **0.2.0-beta2** is a complete Joomla/Gantry template, with the
light/dark switch built in. Its Joomla folder is `ra_darktheme`; the installer
is `tpl_ra_darktheme-0.2.0-beta2.zip`. It appears separately from Hydrogen in
**Components → Gantry 5 → Themes**.

This local build is based on Alton Ramblers' administrator-supplied Hydrogen
5.6.7 template. It retains its Ramblers layout, module positions, Assistant font
settings, custom menu rendering and SCSS. The source site's active outline 12
becomes a portable base outline; Joomla/Gantry allocates a new template style ID.
Existing modules, articles and media stay in Joomla. The installer does not
import a database or create sample menus.

## Template requirements

Joomla 5.4 and Gantry 5.6.7 are the versions reported in the supplied export.
PHP 8.3 or later is the project baseline. Actual installation and Gantry SCSS
compilation still require verification on a Joomla staging site. This is a beta,
not a qualified production replacement.

## Install and preview

1. Back up the website and retain Hydrogen for rollback.
2. Disable **System - RA Dark Theme**. The template provides its own controls.
3. Upload **tpl_ra_darktheme-0.2.0-beta2.zip** through
   **System → Install → Extensions**. Installation should leave Hydrogen assigned.
4. Find **RA Dark Theme** in **Components → Gantry 5 → Themes**. Open its
   default outline, check the Ramblers layout and use **Save Styles** to compile
   its CSS if necessary.
5. In **System → Site Template Styles**, open the new RA Dark Theme style.
   In its **RA Dark Theme** settings, choose **Device preference**, **Light** or
   **Dark** as the default theme, and whether to show the switch and recolour the
   weather widget. Saved visitor choices override the default.
6. Preview it before making it the default. Check Home, Contacts, Current Walks
   including its calendar, galleries, menus and the mobile layout. Check Festive
   Overlay separately when its effects are enabled.
7. When satisfied, make the RA Dark Theme style the site default. Existing
   menu-specific assignments to Hydrogen can still override the default; review
   those assignments if some pages retain the old template.
8. Clear Joomla/Gantry/browser caches and check both themes again.

To roll back, restore the original Hydrogen template style as the default and
restore any menu assignments changed during testing. Keep Hydrogen installed.

## Build locally

The builder requires the complete template-folder archive, not a Gantry content
export. It generates a new package without modifying the original archive:

```sh
.venv/bin/python scripts/build_gantry_theme.py \
  --source /path/to/g5_hydrogen.zip \
  --output dist/gantry-build
```

Choose a fresh output directory each time. Generated template files, original
archives and site-specific assets remain local and are excluded from Git.
The builder removes compiled CSS, backup files, old numeric style IDs and the
Hydrogen update feed. Future updates must be prepared for this fork explicitly;
do not install Hydrogen updates over the replacement template.

## Verification limits

Package identity, manifest contents, portable outline configuration, asset URL
construction and PHP syntax can be checked locally. The browser runtime reuses
the plugin's tested light/dark code. A static website mirror cannot prove Joomla
installation, Gantry outline creation, CSS compilation or template assignment.
These require the staging checks above.
