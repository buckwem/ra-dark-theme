#!/usr/bin/env python3
"""Use shipped template assets on an existing local public-page mirror."""
import argparse
import json
from pathlib import Path
import shutil
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', required=True, type=Path)
args = parser.parse_args()
source = args.source.resolve()
target = ROOT / '.local-site'
if not (source / 'index.html').is_file() or source == target.resolve():
    parser.error('Use a separate local mirror containing index.html.')
shutil.copytree(source, target, dirs_exist_ok=True)
shutil.copytree(ROOT / 'template/ra-assets', target / 'templates/ra_darktheme/ra-assets', dirs_exist_ok=True)
count = 0
for path in target.rglob('*.html'):
    soup = BeautifulSoup(path.read_text(), 'html.parser')
    if not soup.head or not soup.html:
        continue
    for element in soup.select('link[href],script[src]'):
        url = element.get('href', element.get('src', ''))
        if any(name in url for name in ['alton-dark.css', 'preview-toggle.', '/ra-assets/']):
            element.decompose()
    soup.html.attrs.pop('data-alton-theme', None)
    soup.html.attrs.pop('data-ra-theme', None)
    options = soup.select_one('script.joomla-script-options')
    if not options:
        options = soup.new_tag('script', attrs={'class':'joomla-script-options new', 'type':'application/json'})
        soup.head.insert(0, options)
    data = json.loads(options.string or '{}')
    data['tpl_ra_darktheme'] = {'enabled':True, 'defaultTheme':'dark',
        'showToggle':True, 'position':'header', 'weather':True}
    options.string = json.dumps(data)
    for filename in ['theme.css', 'toggle.css']:
        soup.head.append(soup.new_tag('link', rel='stylesheet', media='screen',
            href='/templates/ra_darktheme/ra-assets/css/' + filename))
    soup.head.append(soup.new_tag('script', src='/templates/ra_darktheme/ra-assets/js/bootstrap.js',
        attrs={'data-ra-default':'dark'}))
    soup.head.append(soup.new_tag('script', src='/templates/ra_darktheme/ra-assets/js/theme.js', defer=True))
    path.write_text(str(soup))
    count += 1
print(f'Prepared {count} local pages with the shipped RA Dark Theme assets in {target}.')
