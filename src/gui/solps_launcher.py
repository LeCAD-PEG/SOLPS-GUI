#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thin launcher for the SOLPS-GUI application.

Place this file as ``src/gui/solps_launcher.py`` (or ensure it is on the
import path as ``gui.solps_launcher``) so that the console-script entry
points defined in pyproject.toml / setup.py can start the GUI.

The original ``solps.py`` only executes under ``if __name__ == "__main__":``.
This launcher imports and runs that block in a controlled way.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    """Entry point used by the ``solps`` / ``solps-gui`` console scripts."""
    if argv is not None:
        sys.argv = [sys.argv[0], *argv]

    # Locate solps.py next to this launcher (src/gui/solps.py)
    gui_dir = Path(__file__).resolve().parent
    solps_script = gui_dir / "solps.py"

    if not solps_script.is_file():
        # Fallback: try to import the module and execute its __main__ block
        try:
            runpy.run_module("gui.solps", run_name="__main__", alter_sys=True)
            return 0
        except Exception as exc:  # pragma: no cover
            print(f"Failed to launch SOLPS-GUI: {exc}", file=sys.stderr)
            return 1

    # Execute solps.py as a script (honours its if __name__ == "__main__" block)
    runpy.run_path(str(solps_script), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
