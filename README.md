# RA Dark Theme

A Joomla/Gantry template for Ramblers websites, with a built-in light/dark
switch and the compact sun/moon icons used by [Prodockit](https://prodockit.org/).

The **0.2.0-beta4 Gantry template** was built from Alton Ramblers' Hydrogen
5.6.7 template and retains its Ramblers layout, module positions, custom styling
and Assistant font settings. It appears separately as **RA Dark Theme** in
Gantry's Available Themes screen.

This is an independent project, not an official Ramblers release.

## Requirements and beta status

The supplied site export reports Joomla 5.4.10 and Gantry 5.6.7. The project
baseline is PHP 8.3 or later. Joomla 6.x remains a development target requiring
integration testing. Back up the website and test the template on a staging copy.

The template has been installed and previewed on Alton Ramblers. The default
appearance, switch and menu-assignment workflow have been checked there.
Local checks cover PHP syntax, configuration, browser behaviour, packaging and
documentation. Update, removal and wider compatibility checks remain necessary
before a production release.

## Obtain the installer

Download **[tpl_ra_darktheme-0.2.0-beta4.zip](https://github.com/buckwem/ra-dark-theme/releases/download/v0.2.0-beta4/tpl_ra_darktheme-0.2.0-beta4.zip)**
from the [Gantry beta release](https://github.com/buckwem/ra-dark-theme/releases/tag/v0.2.0-beta4).
The release also includes this README. This build contains Alton Ramblers'
Hydrogen customisations; other sites should review and adapt the layout before use.

GitHub's automatic source archives contain the development project and cannot
be installed as a Joomla template.

## Install the Gantry template

1. Back up the site and keep Hydrogen installed for rollback.
2. Open **System → Install → Extensions → Upload Package File** and upload
   `tpl_ra_darktheme-0.2.0-beta4.zip`. Use Joomla's installer, rather than Gantry's
   Import control. For an upgrade, upload the newer ZIP without uninstalling.
3. Open **Components → Gantry 5 Themes → Available Themes → RA Dark Theme**.
   Confirm that its version is **0.2.0-beta4** or later.
4. Review the Ramblers layout and preview the template. Previewing alone does
   not change the template used by the normal public URLs.

## Set the default appearance

1. In RA Dark Theme, choose **Base Outline** from the outline dropdown.
2. Open **Page Settings** and locate **RA Dark Theme**.
3. Set **Default theme** to **Light**, **Dark** or **Device preference**.
4. Click **Save Page Settings**.

Light is a suitable choice when you want the usual light appearance initially;
visitors can use the switch to select dark mode. The template's initial fallback
is Dark until configured. Saved visitor choices override the default. Test a
changed default in a fresh private window. Clearing Joomla's cache does not
clear browser preferences.

An individual outline can override the Base Outline. To make such a change,
select that outline and enable the field's override checkbox before saving.

## Activate the template on the public site

1. Open **System → Templates → Site Template Styles**.
2. Find **RA Dark Theme – Default** and make it the site default using its star
   or the **Default** toolbar button.
3. Under **Menus → Main Menu**, open existing menu items that explicitly select
   Hydrogen. In **Details → Template Style**, select **Use Default**, then
   **Save & Close**.
4. Repeat for all affected menu items, including Home, News, Gallery, Contacts
   and the walks pages. Check other menus if the site has them.
5. Refresh the normal public URLs and check the layout and switch on desktop
   and mobile, including the calendar and weather widget.

A menu item's explicit template assignment overrides the site default. On
Alton Ramblers, Home and Gallery changed successfully after their menu items
were set to **Use Default**. Changing Home does not change the other menu items.
Use this verified menu-item route when migrating existing assignments; clearing
or selecting all items in Gantry Assignments was not a reliable migration route
in the site checks.

If using Gantry's default-template dropdown, **All Languages** means the general
site default. A language-specific selection such as **English (UK)** is a
different assignment; it should not replace the general default inadvertently.

## Roll back

Keep Hydrogen installed. Restore **Hydrogen – Default** as the site default
and restore any explicit menu assignments needed by the original configuration.
Menu items set to **Use Default** will follow the restored default. Retain the
backup until the replacement has been fully checked.

## Festive Overlay

[Festive Overlay](https://github.com/buckwem/festive-extension) can be installed
separately. It works with light or dark appearance; RA Dark Theme is a recommended
companion, not a required dependency. Check the seasonal effects in both modes.

## Build and documentation

```sh
make setup
make check lint-php test package docs
make docs-serve
```

The complete installable source is in `template/`. `make package` builds
`dist/tpl_ra_darktheme-0.2.0-beta4.zip` directly from the declared files in
`template/templateDetails.xml`. No external archive is needed. Compiled caches,
website mirrors and build output stay out of Git.

See the [Gantry template guide](docs/installation.md) for installation details.
Documentation uses Zensical and Prodockit styles. Run `make docs-serve` for a local
preview at <http://127.0.0.1:8000>. No public documentation website is deployed.

## Licence

Authored project code and documentation are GPL-2.0-or-later. Hydrogen and its
customisations retain their original notices. Lucide/Feather icon notices are
included in `template/THIRD_PARTY_NOTICES.txt`. Supplied template customisations
and assets are included in the source and release. Database exports, website
snapshots and credentials are excluded.
