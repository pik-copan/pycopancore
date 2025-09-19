#!/usr/bin/env python3
"""
Update CITATION.cff with current package version and release date.
"""

import sys
import subprocess
from datetime import datetime
from pathlib import Path


def get_package_version():
    """Get the current package version."""
    try:
        # Try to import the package and get version
        import pycopancore
        return pycopancore.__version__
    except ImportError:
        # Fallback: try to get version from Git tag
        try:
            result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], 
                                  capture_output=True, text=True, check=True)
            git_tag = result.stdout.strip()
            # Remove 'v' prefix if present
            if git_tag.startswith('v'):
                return git_tag[1:]
            return git_tag
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Fallback: try to get version from _version.py file
        try:
            version_file = Path("pycopancore/_version.py")
            if version_file.exists():
                content = version_file.read_text()
                # Extract version from __version__ = "x.y.z"
                import re
                match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1)
        except Exception:
            pass
        
        # Final fallback: try to get version from pyproject.toml
        try:
            with open("pyproject.toml", "r") as f:
                content = f.read()
            # Extract fallback_version from pyproject.toml
            import re
            match = re.search(r'fallback_version = "([^"]+)"', content)
            if match:
                return match.group(1)
        except (FileNotFoundError, Exception):
            pass
        
        print("Error: Could not determine package version")
        sys.exit(1)


def update_citation_file(version, date=None):
    """Update CITATION.cff with new version and date."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    citation_file = Path("CITATION.cff")
    if not citation_file.exists():
        print("Error: CITATION.cff not found")
        sys.exit(1)
    
    # Read current content
    with open(citation_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update version
    lines = content.split('\n')
    updated = False
    
    for i, line in enumerate(lines):
        if line.startswith('version:'):
            old_version = line.split(':', 1)[1].strip()
            lines[i] = f'version: {version}'
            if old_version != version:
                print(f"Updated version: {old_version} -> {version}")
                updated = True
        elif line.startswith('date-released:'):
            old_date = line.split(':', 1)[1].strip().strip("'\"")
            lines[i] = f"date-released: '{date}'"
            if old_date != date:
                print(f"Updated date: {old_date} -> {date}")
                updated = True
    
    if updated:
        # Write back to file
        with open(citation_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"Successfully updated CITATION.cff")
        return True
    else:
        print("No updates needed for CITATION.cff")
        return False


def main():
    """Main function."""
    if len(sys.argv) > 1:
        version = sys.argv[1]
    else:
        version = get_package_version()
    
    if len(sys.argv) > 2:
        date = sys.argv[2]
    else:
        date = None
    
    print(f"Updating CITATION.cff to version {version}")
    updated = update_citation_file(version, date)
    
    if updated:
        print("CITATION.cff has been updated!")
        sys.exit(0)
    else:
        print("No changes were made.")
        sys.exit(0)


if __name__ == "__main__":
    main()
