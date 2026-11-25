# Testing

JavaScript checks cover default, device and saved appearance, storage failure,
cross-tab updates, duplicate loading, switch placement and weather colours.
PHP test doubles check Gantry settings, root/subdirectory asset URLs, print
isolation and dependencies. All shipped PHP files receive syntax checks.
Packaging validates the complete manifest; CI also builds the documentation.

The template was installed and previewed on Alton Ramblers. Appearance controls
were observed, and Home and Gallery followed the default after their explicit
Hydrogen menu assignments were changed to Use Default. Bulk assignment changes
caused a homepage failure during trials; follow the documented menu-item route
and keep a rollback path.

A local mirror was checked with Festive Overlay for snow, sleigh, fireworks,
pause/resume, on/off and palette changes. Static checks do not qualify PHP
execution, Gantry compilation or all dynamic states. Some gallery images are
missing from the mirror. Wider installation, update, removal, mobile, keyboard,
print, calendar, form, gallery and map checks remain necessary on staging.

Beta5 corrects walk-details dialogs appended outside the main
page container. A local browser check confirmed dark text panels, and a focused
check using the map library's stylesheet confirmed that map information boxes
retain their light background and dark text. Weather colour matching was also
observed working in Safari after enabling it in the local preview. Some map
tiles and marker images are missing from the static mirror; map imagery needs
verification on the installed site.

The site maintainer subsequently confirmed the beta5 installer working on the
target site. Wider Joomla/Gantry compatibility and update/removal checks remain
necessary before a production release.
