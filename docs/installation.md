# Installation

## Requirements

- Joomla 5.4 or 6.x with PHP 8.3 or later, pending integration qualification.
- A Ramblers website using the Gantry 5 Hydrogen template (`g5_hydrogen`).
- A staging copy on which to review your site's content and interactive widgets.

Other templates need their own style review. The plugin skips them by default.

## Install and enable

1. Download `plg_system_ra_darktheme-0.1.0-beta2.zip` from the
   [beta release](https://github.com/buckwem/ra-dark-theme/releases/tag/v0.1.0-beta2),
   or build it with `make package`. GitHub's automatic source archives are not
   Joomla installation packages.
2. In Joomla, open **System → Install → Extensions** and upload
   `plg_system_ra_darktheme-0.1.0-beta2.zip` (in `dist/` if built locally).
3. Open **System → Manage → Plugins → System - RA Dark Theme**.
4. Choose the default theme and switch position, then enable the plugin.
5. Clear Joomla, Gantry and browser caches and check the pages used by your visitors.

Remove the earlier standalone `alton-dark.css` and `preview-toggle` assets before
enabling this plugin. Those prototype files use different identifiers and would
otherwise create a second switch. Festive Overlay can remain enabled.

The plugin installs files under `plugins/system/ra_darktheme/` and
`media/plg_system_ra_darktheme/`. It does not change the template or the database
schema. Joomla stores the plugin settings as normal extension parameters.

## Update or remove

Upload a newer ZIP to update the plugin. Its manifest uses Joomla's upgrade
method. There is no update server yet.

Disable the plugin to stop loading its assets on subsequent page loads. Remove
it through **System → Manage → Extensions** if it is no longer required.
Clear cached pages after either operation. Visitor preferences remain in their
browser storage but have no effect while the plugin is absent.
