# Gantry template

RA Dark Theme **0.2.0-beta3** is a complete Joomla/Gantry template, with the
light/dark switch built in. Its Joomla folder is `ra_darktheme`; the installer
is `tpl_ra_darktheme-0.2.0-beta3.zip`. It appears separately from Hydrogen in
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
3. Upload **tpl_ra_darktheme-0.2.0-beta3.zip** through
   **System → Install → Extensions**. Installation should leave Hydrogen assigned.
4. Find **RA Dark Theme** in **Components → Gantry 5 → Themes**. Open its
   default outline, check the Ramblers layout and use **Save Styles** to compile
   its CSS if necessary.
5. In Gantry, select **Base Outline**, open **Page Settings**, and find the
   **RA Dark Theme** section. Set **Default theme** to **Dark**, **Light** or
   **Device preference**, then click **Save Page Settings**. You can also enable
   or hide the switch and enable weather colour matching here. New installations
   default to Dark. A specific outline can override inherited page settings;
   enable its override checkbox before saving an outline-specific choice.
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

## Instructions for webmasters

To change the default appearance:

1. Open **Components → Gantry 5 Themes → RA Dark Theme**.
2. Select **Base Outline** to set the default across the template.
3. Open **Page Settings** and locate **RA Dark Theme**.
4. Choose **Default theme → Dark**, **Light**, or **Device preference**.
5. Click **Save Page Settings** and refresh a page using this template.

The default applies when the visitor has not saved a choice. Test defaults in
an anonymous/private browser window, or use the switch to choose the appearance
for your current browser. Clearing Joomla's cache does not clear a visitor's
saved browser preference. Review outline overrides if only some pages change.

When upgrading from beta1 or beta2, upload the beta3 ZIP without uninstalling,
then use these Gantry controls. Earlier Joomla template-style default parameters
are superseded by the Gantry Page Settings controls.
