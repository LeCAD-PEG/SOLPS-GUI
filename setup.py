#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for SOLPS-GUI.

Modern packaging metadata lives in pyproject.toml (PEP 621).
This setup.py is kept for compatibility with older tools and for
any custom build logic that cannot yet be expressed in pyproject.toml.

Usage:
    pip install .
    pip install -e .          # editable / development install
    python -m build           # build sdist + wheel
"""

from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).parent.resolve()

# ---------------------------------------------------------------------------
# Minimal fallback metadata (primary source is pyproject.toml)
# ---------------------------------------------------------------------------
NAME = "solps-gui"
VERSION = "1.6.1"
DESCRIPTION = "Graphical User Interface for SOLPS-ITER"
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding="utf-8") if (HERE / "README.md").exists() else DESCRIPTION
AUTHOR = "Leon Kos"
AUTHOR_EMAIL = "leon.kos@lecad.fs.uni-lj.si"
URL = "https://github.com/LeCAD-PEG/SOLPS-GUI"
LICENSE = "LGPL-3.0-or-later"

# Runtime dependencies (keep in sync with pyproject.toml)
INSTALL_REQUIRES = [
    "PySide6>=6.2.0",
    "matplotlib>=3.5.0",
    "numpy",
]

EXTRAS_REQUIRE = {
    "docs": [
        "Sphinx>=3.5.0",
        "sphinx-rtd-theme",
    ],
    "dev": [
        "Sphinx>=3.5.0",
        "sphinx-rtd-theme",
    ],
}

# ---------------------------------------------------------------------------
# Package discovery
# ---------------------------------------------------------------------------
# Python sources live under src/ with a flat-ish layout:
#   src/gui/          – main application (solps.py)
#   src/widgets/      – reusable pyQt5 widgets (addmenu, b2, eirene, …)
#   src/actors/       – actor components for PySide6
#   src/utils/        – utilities
#   src/plugins/      – plugins for pyQt5 and PySide6 designer, ParaView
#   src/generator/    – Actor generators
#   src/examples/     – examples
#
# Because many modules are imported by bare name (e.g. `from addmenu import …`)
# when running from the source tree, we expose the relevant packages and
# also add the top-level src directories to the package search path.

PACKAGES = find_packages(
    where="src",
    include=[
        "gui*",
        "actors*",
        "plugins*",
        "generator*",
    ],
)

PACKAGE_DIR = {"": "src"}

PACKAGE_DATA = {
    "": ["*.ui", "*.png", "*.svg", "*.qrc", "*.qm", "*.ts"],
    "gui": ["*.ui", "*.png", "*.svg"],
    "widgets": ["*.ui", "*.png", "*.svg"],
}

# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------
# solps.py currently runs under `if __name__ == "__main__":` and does not
# expose a main() function.  We therefore register a thin wrapper that
# executes the module as a script.

ENTRY_POINTS = {
    "console_scripts": [
        "solps = gui.solps_launcher:main",
        "solps-gui = gui.solps_launcher:main",
    ],
}

# ---------------------------------------------------------------------------
# setup()
# ---------------------------------------------------------------------------
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    project_urls={
        "Homepage": URL,
        "Repository": URL + ".git",
        "Issues": URL + "/issues",
    },
    license=LICENSE,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.8",
    package_dir=PACKAGE_DIR,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points=ENTRY_POINTS,
    zip_safe=False,
)
