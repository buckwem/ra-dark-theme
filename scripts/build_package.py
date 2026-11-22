#!/usr/bin/env python3
"""Validate and package the complete Joomla/Gantry template."""
import argparse
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'template'
MANIFEST = SOURCE / 'templateDetails.xml'

def package_inputs():
    manifest = ET.parse(MANIFEST).getroot()
    if manifest.get('type') != 'template' or manifest.get('client') != 'site' or manifest.findtext('name') != 'ra_darktheme':
        raise ValueError('Expected the RA Dark Theme site-template manifest')
    version = manifest.findtext('version', '')
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[A-Za-z0-9.]+)?', version):
        raise ValueError('Invalid template version')
    files = {MANIFEST}
    for section in [manifest.find('files')]:
        if section is None:
            raise ValueError('Missing files declaration')
        for entry in section:
            path = SOURCE / (entry.text or '').strip()
            if not path.resolve().is_relative_to(SOURCE.resolve()) or not path.exists():
                raise ValueError(f'Invalid manifest path: {entry.text}')
            files.update(p for p in path.rglob('*') if p.is_file()) if path.is_dir() else files.add(path)
    script = SOURCE / manifest.findtext('scriptfile', '')
    if not script.is_file():
        raise ValueError('Missing installer script')
    files.add(script)
    for path in files:
        rel = path.relative_to(SOURCE)
        if path.is_symlink() or any(part.startswith('.') or part in {'css-compiled','node_modules','vendor','__pycache__'} for part in rel.parts) or path.suffix in {'.backup','.sql'}:
            raise ValueError(f'Unexpected package file: {rel}')
    if files != {p for p in SOURCE.rglob('*') if p.is_file()}:
        raise ValueError('Template contains undeclared files')
    return version, sorted(files)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    version, files = package_inputs()
    if args.check:
        print(f'Validated RA Dark Theme {version}: {len(files)} template files')
        return
    output = ROOT / 'dist' / f'tpl_ra_darktheme-{version}.zip'
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, 'w', compression=ZIP_DEFLATED) as archive:
        for p in files:
            info = ZipInfo(p.relative_to(SOURCE).as_posix(), (2026,11,22,0,0,0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, p.read_bytes())
    print(f'Built {output.relative_to(ROOT)}')

if __name__ == '__main__':
    main()
