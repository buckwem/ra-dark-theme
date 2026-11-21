# Configuration

Open **System → Manage → Plugins → System - RA Dark Theme**.

| Setting | Default | Effect |
| --- | --- | --- |
| Joomla status | Disabled after a fresh installation | Enable to load the plugin on matching public pages. |
| Default theme | Device preference | Follow the operating system, or start in light/dark mode. A saved visitor choice takes precedence. |
| Show light/dark switch | Yes | Show the compact icon button. Hiding it retains any existing visitor preference. |
| Switch position | Beside site title | Use `#ramblerstitle`; fall back to bottom right if missing. Fixed bottom-left/right positions are also available. |
| Match weather widget colours | Yes | Theme an existing WeatherWidget.io forecast; do not create or download one. |
| Template folder | `g5_hydrogen` | Limit the plugin to the reviewed template. Blank allows other templates after their styles have been adapted and tested. |

## Visitor choices

The switch saves `light` or `dark` under `ra-dark-theme:preference` in local
storage. Device changes are followed until the visitor saves a choice. Storage
failures are tolerated, and theme changes are synchronised between open tabs.
No theme preference is sent to the server.

Clearing site storage restores the configured default. For development, the
console API also supports `RADarkTheme.resetPreference()` and
`RADarkTheme.setPreference('system')`.

## Appearance and compatibility

The colours activate through `data-ra-theme="dark"` on the HTML element.
An external bootstrap script applies the saved choice before the body renders.
The main script adds the switch after the document is ready.

Dark CSS is restricted to screen media, so printing uses the site's original
print styling. Photos, logos, map tiles and embedded documents keep their
original colours. White image backgrounds are not recoloured.

The Walking Environment column correction also applies in light mode while
the plugin is active. Long URLs wrap and wide article images stay within their
columns.

Weather matching restores the widget's original colour attributes in light
mode and uses the dark palette in dark mode. The widget still needs its normal
external connection. No arbitrary iframe or embedded document is modified.

Festive Overlay keeps its own control colours and detects the page background.
The dark stylesheet excludes those controls from its general button styling.
