# src/gui/__init__.py
Ctrl+J

create pyproject.toml and setup.py for https://github.com/LeCAD-PEG/SOLPS-GUI.git

Created packaging files for SOLPS-GUI based on the repo structure, dependencies, and license.
Files in /home/workdir/artifacts/
File	Purpose
pyproject.toml	Modern PEP 621 metadata (primary)
setup.py	Compatibility + explicit package discovery
solps_launcher.py	Console-script entry point (place under src/gui/)
Highlights

Dependencies

    PySide6>=6.2.0
    matplotlib>=3.5.0
    numpy
    Optional: docs / dev extras (Sphinx, sphinx-rtd-theme)

Metadata

    Name: solps-gui
    License: LGPL-3.0-or-later
    Author: Leon Kos
    Python: >=3.8
    Homepage: https://github.com/LeCAD-PEG/SOLPS-GUI

Layout

    Packages discovered under src/ (gui, widgets, actors, utils, plugins, …)
    UI/resource files (*.ui, *.png, *.svg) included via package-data

Entry points

solps
solps-gui

Both call gui.solps_launcher:main, which runs solps.py (it only has an if __name__ == "__main__" block, no main()).
How to use

    Copy the three files into the repo root (and put solps_launcher.py in src/gui/):

cp pyproject.toml setup.py /path/to/SOLPS-GUI/
cp solps_launcher.py /path/to/SOLPS-GUI/src/gui/

Install:

pip install -e .          # editable
# or
pip install .

Run:

    solps
    # or
    solps-gui

Notes

    The project uses bare imports (from addmenu import …). For that to work after install, either:
        keep running from the source tree with PYTHONPATH=src:src/widgets:…, or
        later refactor imports to package-relative form (from widgets.addmenu import …).
    Full cluster builds (Qt, gnuplot-widget, IMAS, etc.) still use the existing Makefile / package/ scripts; these packaging files only cover the Python GUI layer.
    Version is set to 0.1.0; change it in both files when you tag a release.

25 sources

Create a tar.gz archive

Created archive:

 (3.1 KB)

Contents:

    pyproject.toml
    setup.py
    solps_launcher.py

where to put **init**.py and what content should be in so that packages are discovered?

For setuptools package discovery (find_packages / packages.find in your pyproject.toml), each directory that should be a Python package needs an __init__.py.
Where to put them

Under src/, add empty (or minimal) __init__.py in every top-level package you want installed:

src/
├── gui/
│   ├── __init__.py          ← add
│   ├── solps.py
│   ├── solps_launcher.py
│   └── ...
├── widgets/
│   ├── __init__.py          ← add
│   ├── addmenu.py
│   ├── QtGnuplot/
│   │   └── __init__.py      ← already exists
│   └── ...
├── actors/
│   ├── __init__.py          ← add
│   ├── ids/
│   │   └── __init__.py      ← already exists
│   └── ...
├── utils/
│   ├── __init__.py          ← add
│   └── ...
├── plugins/
│   ├── __init__.py          ← add
│   └── ...
├── generator/
│   ├── __init__.py          ← add
│   └── ...
└── examples/
    ├── __init__.py          ← optional (only if you package examples)
    └── ...

Do not put an __init__.py in src/ itself unless you intentionally want a top-level package named after the folder layout differently; with package-dir = {"" = "src"}, packages are the subdirs of src/.

Already present in the repo (no need to recreate):

    src/actors/QtGnuplot/__init__.py
    src/actors/ids/__init__.py
    src/widgets/QtGnuplot/__init__.py

What content to put in them

For discovery and install, empty files are enough:

# src/gui/__init__.py

# src/widgets/__init__.py

# src/actors/__init__.py

# src/utils/__init__.py

# src/plugins/__init__.py

# src/generator/__init__.py

Optional but useful for the main app package:

# src/gui/__init__.py
"""SOLPS-ITER Graphical User Interface."""

__version__ = "0.1.0"

You do not need to re-export modules unless you want a nicer public API, e.g.:

# optional, only if you want: from gui import solps
from . import solps  # noqa: F401

Why this is required

Your pyproject.toml has:

[tool.setuptools.packages.find]
where = ["src"]
include = ["gui*", "widgets*", "actors*", ...]
namespaces = false

With namespaces = false (default), setuptools only treats a directory as a package if it contains __init__.py. Without those files, find_packages finds nothing (or almost nothing), and install/entry points fail.
Quick create (from repo root)

for d in gui widgets actors utils plugins generator; do
  touch "src/$d/__init__.py"
done
# optional:
# touch src/examples/__init__.py

Bare imports caveat

Code like from addmenu import AddMenu (in solps.py) expects addmenu on sys.path, not as widgets.addmenu. After packaging:

    Either run with PYTHONPATH including src/widgets (and similar), or
    Prefer package imports later: from widgets.addmenu import AddMenu.

__init__.py only makes package discovery work; it does not by itself fix those bare imports.

What should be in the main **init**.py

For this project, the main package is gui (src/gui/), because that’s where the app entry point lives (solps.py / solps_launcher.py).
Recommended: src/gui/__init__.py

"""SOLPS-ITER Graphical User Interface.

Framework for preparing, controlling, and analysing SOLPS-ITER runs.
"""

from __future__ import annotations

__version__ = "1.6.1"
__author__ = "Leon Kos"
__license__ = "LGPL-3.0-or-later"

# Keep this file light: heavy Qt imports belong in solps.py / widgets.
# Optional convenience re-exports can be added later, e.g.:
# from .solps_launcher import main  # noqa: F401

__all__ = [
    "__version__",
    "__author__",
    "__license__",
]


