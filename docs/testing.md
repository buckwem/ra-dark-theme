# Testing

## Completed local checks

The source palette was audited on 162 static Alton Ramblers pages at desktop
(1,400 pixels) and mobile (390 pixels) widths. The final audit reported no
flagged light CSS surfaces or low-contrast text in those inspected states.
It did not examine image pixels, hidden content or every interactive state.

The plugin has focused browser-runtime tests for saved/default/device choices,
unavailable storage, cross-tab changes, translated button labels, missing-header
fallback, duplicate loading and existing weather widget colours. PHP tests cover
public/administrator, HTML/non-HTML, component-only and template guards, settings
validation and subdirectory asset URLs. These use API test doubles.

Manifest validation, deterministic packaging, PHP syntax and a strict
Zensical/Prodockit documentation build are part of the local checks and CI.

The new shipped assets were also checked in Chrome on the local Home and
Contacts pages, including both themes, weather colour changes, saved choices
and a 390-pixel mobile viewport. All ten browser-runtime tests and the PHP
checks passed. PHP was checked with the existing PHP WebAssembly runner; this
does not load Joomla itself.

## Required Joomla staging checks

Before a production release, install, update and uninstall the ZIP on both
Joomla 5.4 and 6.x. Check that the actual site template and asset ordering work,
that settings persist, and that administrator/non-HTML pages are unchanged.
Test standard and subdirectory installations, keyboard navigation, both themes,
device preference, browser storage restrictions and printing.

Review your own articles, menus, contact forms, walk filters and calendar views,
gallery lightboxes and map pop-ups. Dynamic map tiles, external help and full-size
gallery images were incomplete in the source mirror. The preview cannot validate
form submission or live Joomla API behaviour. The local colour audit is not an
accessibility certification.
