#!/usr/bin/env python3
"""Validate and package only the Joomla manifest's declared installation files."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "extension"
MANIFEST = SOURCE / "ra_darktheme.xml"


def package_inputs() -> tuple[str, list[Path]]:
    manifest = ET.parse(MANIFEST).getroot()
    if manifest.tag != "extension" or manifest.get("type") != "plugin" or manifest.get("group") != "system":
        raise ValueError("The manifest must declare a system plugin.")
    if manifest.find("files/folder[@plugin='ra_darktheme']") is None:
        raise ValueError("The plugin element must match ra_darktheme.xml.")

    version = manifest.findtext("version", "")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[A-Za-z0-9.]+)?", version):
        raise ValueError("The manifest needs a valid package version.")

    files = {MANIFEST}
    for section_name in ("files", "media", "languages"):
        section = manifest.find(section_name)
        if section is None:
            raise ValueError(f"Missing manifest section: {section_name}")
        base = SOURCE / section.get("folder", "")
        for entry in section:
            path = base / (entry.text or "").strip()
            if not path.resolve().is_relative_to(SOURCE.resolve()):
                raise ValueError(f"Manifest path escapes the extension: {path}")
            if entry.tag == "folder":
                if not path.is_dir():
                    raise ValueError(f"Missing folder: {path}")
                files.update(item for item in path.rglob("*") if item.is_file())
            else:
                if not path.is_file():
                    raise ValueError(f"Missing file: {path}")
                files.add(path)

    for path in files:
        if not path.resolve().is_relative_to(SOURCE.resolve()) or path.is_symlink():
            raise ValueError(f"Refusing linked package input: {path}")
        relative = path.relative_to(SOURCE)
        if any(part.startswith(".") or part in {"__pycache__", "node_modules", "vendor"} for part in relative.parts):
            raise ValueError(f"Unexpected development file in extension: {relative}")

    return version, sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate inputs without writing a ZIP.")
    args = parser.parse_args()

    try:
        version, files = package_inputs()
        if args.check:
            print(f"Validated RA Dark Theme {version}: {len(files)} package files.")
            return 0

        output = ROOT / "dist" / f"plg_system_ra_darktheme-{version}.zip"
        output.parent.mkdir(exist_ok=True)
        # Stable order, permissions and timestamps make identical sources reproducible.
        with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
            for path in files:
                info = ZipInfo(path.relative_to(SOURCE).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
        print(f"Built {output.relative_to(ROOT)} ({len(files)} files).")
        return 0
    except (OSError, ValueError, ET.ParseError) as error:
        print(f"Package error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
