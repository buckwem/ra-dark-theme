#!/usr/bin/env python3
"""Build a local Gantry theme from an administrator-supplied Hydrogen archive.

The input archive and generated theme contain site customisations and must not
be committed to the public repository. No database export is consumed.
"""
import argparse
from pathlib import Path, PurePosixPath
import shutil
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

VERSION = '0.2.0-beta1'
NAME = 'ra_darktheme'
ROOT = Path(__file__).resolve().parents[1]


def build(archive, output):
    target = output / NAME
    if target.exists():
        raise ValueError('Choose a fresh output directory; refusing to overwrite an existing theme.')
    target.mkdir(parents=True)
    with ZipFile(archive) as source:
        if source.testzip():
            raise ValueError('Invalid source archive')
        for item in source.infolist():
            path = PurePosixPath(item.filename)
            if path.is_absolute() or '..' in path.parts or (item.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError('Unsafe archive path')
            prefix = ('templates', 'g5_hydrogen')
            if path.parts[:2] != prefix:
                raise ValueError('Expected templates/g5_hydrogen in archive')
            rel = Path(*path.parts[2:])
            if not rel.parts or item.is_dir():
                continue
            if 'css-compiled' in rel.parts or rel.suffix == '.backup' or rel.name == 'MD5SUMS':
                continue
            dst = target / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(source.read(item))

    # Rename template-specific identifiers and absolute paths, keeping Hydrogen's
    # SCSS filenames and upstream copyright notices intact.
    for p in list(target.rglob('*')):
        if p.is_file() and p.suffix in {'.php', '.yaml', '.ini', '.scss', '.twig', '.xml'}:
            text = p.read_text().replace('g5_hydrogen', NAME).replace('G5_HYDROGEN', 'RA_DARKTHEME').replace('G5_Hydrogen', 'Ra_darktheme')
            p.write_text(text)
            if 'g5_hydrogen' in p.name:
                p.rename(p.with_name(p.name.replace('g5_hydrogen', NAME)))

    # The original numeric directories are Joomla database style IDs. Supply
    # their content as a portable base outline; Gantry allocates new style IDs.
    original = target / 'custom/config'
    base = original / 'default'
    for filename in ['layout.yaml', 'styles.yaml']:
        shutil.copyfile(original / '12' / filename, base / filename)
    base_index = original / '12/index.yaml'
    (base / 'index.yaml').write_text(base_index.read_text().replace('name: 12\n', 'name: default\n', 1))
    for p in original.iterdir():
        if p.is_dir() and p.name.isdecimal():
            shutil.rmtree(p)
    # Put configurations in install/outlines so Gantry can create them without
    # relying on source-site style IDs or overwriting later local edits.
    for p in list(original.iterdir()):
        if p.is_dir():
            shutil.copytree(p, target / 'install/outlines' / p.name)
    shutil.rmtree(original)
    (target / 'install/outlines.yaml').write_text('default:\n  title: Default\n  preset: Ramblers\n')
    (target / 'install/menus.yaml').write_text('{}\n')

    # Gantry theme discovery uses its own metadata in addition to Joomla XML.
    for p in [target / 'gantry/theme.yaml', target / 'custom/gantry/theme.yaml']:
        text = p.read_text().replace('name: Hydrogen', 'name: RA Dark Theme')
        import re
        text = re.sub(r"version: '[^']+'", f"version: '{VERSION}'", text, count=1)
        text = re.sub(r'  updates:\n(?:    .*\n|\n)*', '', text)
        text = text.replace('description: Hydrogen Theme', 'description: Ramblers light and dark Gantry theme')
        p.write_text(text)

    manifest = ET.parse(target / 'templateDetails.xml')
    xml = manifest.getroot()
    xml.find('version').text = VERSION
    xml.find('description').text = 'RA Dark Theme: Ramblers layouts with built-in light and dark mode.'
    for node in list(xml.findall('updateservers')):
        xml.remove(node)
    files = xml.find('files')
    files.clear()
    for p in sorted(target.iterdir()):
        if p.name in {'templateDetails.xml', 'install.php'}:
            continue
        ET.SubElement(files, 'folder' if p.is_dir() else 'filename').text = p.name
    fieldset = xml.find('config/fields/fieldset')
    fieldset.set('label', 'RA Dark Theme')
    field = ET.SubElement(fieldset, 'field', name='ra_default_theme', type='list', default='system', filter='cmd', label='Default theme', description='Saved visitor choices override this default.')
    for value, label in [('system', 'Device preference'), ('light', 'Light'), ('dark', 'Dark')]:
        ET.SubElement(field, 'option', value=value).text = label
    for name, label in [('ra_show_toggle', 'Show light/dark switch'), ('ra_weather', 'Match weather widget colours')]:
        field = ET.SubElement(fieldset, 'field', name=name, type='radio', default='1', filter='integer', label=label, layout='joomla.form.field.radio.switcher')
        ET.SubElement(field, 'option', value='0').text = 'JNO'
        ET.SubElement(field, 'option', value='1').text = 'JYES'
    ET.indent(manifest, space='    ')
    manifest.write(target / 'templateDetails.xml', encoding='utf-8', xml_declaration=True)

    # Include runtime assets directly in the template, without a system plugin.
    assets = target / 'ra-assets'
    shutil.copytree(ROOT / 'extension/media', assets)
    for filename in ['LICENSE.txt', 'THIRD_PARTY_NOTICES.txt']:
        shutil.copyfile(ROOT / 'extension' / filename, target / filename)
    helper = ROOT / 'theme-source/includes/ra-theme.php'
    shutil.copyfile(helper, target / 'includes/ra-theme.php')
    p = target / 'index.php'
    text = p.read_text().replace('// Render the page.', "// Register the built-in palette before Gantry compiles the document head.\nrequire __DIR__ . '/includes/ra-theme.php';\n\n// Render the page.")
    p.write_text(text)
    # New files added after the initial manifest enumeration.
    for name in ['ra-assets', 'LICENSE.txt', 'THIRD_PARTY_NOTICES.txt']:
        ET.SubElement(files, 'folder' if (target / name).is_dir() else 'filename').text = name
    ET.indent(manifest, space='    ')
    manifest.write(target / 'templateDetails.xml', encoding='utf-8', xml_declaration=True)
    # Do not advertise Hydrogen updates or install promotional sample data.
    for p in (target / 'install/templates').glob('*.twig'):
        p.write_text('<h2>RA Dark Theme</h2><p>Installed as a separate Gantry template. Preview before assigning it to your site. Configure light/dark defaults in Joomla Site Template Styles. Disable the separate RA Dark Theme plugin when using this template.</p>\n')
    p = target / 'language/en-GB/en-GB.tpl_ra_darktheme.sys.ini'
    with p.open('a') as f:
        f.write('\nRA_DARKTHEME="RA Dark Theme"\nTPL_RA_DARKTHEME="RA Dark Theme"\n')

    package = output / f'tpl_{NAME}-{VERSION}.zip'
    with ZipFile(package, 'w', compression=ZIP_DEFLATED) as z:
        for p in sorted(target.rglob('*')):
            if p.is_file():
                info = ZipInfo(p.relative_to(target).as_posix(), (2026, 11, 21, 0, 0, 0))
                info.external_attr = 0o100644 << 16
                info.compress_type = ZIP_DEFLATED
                z.writestr(info, p.read_bytes())
    print(package)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build(args.source, args.output)
