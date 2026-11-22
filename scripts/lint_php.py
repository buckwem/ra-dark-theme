#!/usr/bin/env python3
"""Syntax-check the shipped template's PHP files."""
import argparse
from pathlib import Path
import subprocess
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--php', default='php')
args = parser.parse_args()
subprocess.run([args.php, '-r', 'exit(PHP_VERSION_ID >= 80300 ? 0 : 1);'],check=True)
for path in sorted((Path(__file__).resolve().parents[1] / 'template').rglob('*.php')):
    subprocess.run([args.php, '-l', str(path)],check=True)
