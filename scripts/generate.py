#!/usr/bin/env python3
"""Generate the Windows Terminal Apollo scheme from the palette snapshot."""

from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PALETTE_PATH = ROOT / "palette" / "apollo.json"
OUTPUT_PATH = ROOT / "apollo.json"
NORMAL_NAMES = ("black", "red", "green", "yellow", "blue", "purple", "cyan", "white")
BRIGHT_NAMES = ("brightBlack", "brightRed", "brightGreen", "brightYellow", "brightBlue", "brightPurple", "brightCyan", "brightWhite")


def load_palette(path: Path = PALETTE_PATH) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build_scheme(palette: dict[str, Any]) -> OrderedDict[str, str]:
    terminal = palette["terminal"]
    scheme: OrderedDict[str, str] = OrderedDict(
        (
            ("name", palette["name"]),
            ("background", terminal["background"]),
            ("foreground", terminal["foreground"]),
            ("cursorColor", terminal["cursor"]),
            ("selectionBackground", terminal["selection"]["color"]),
        )
    )
    scheme.update(zip(NORMAL_NAMES, terminal["ansi"], strict=True))
    scheme.update(zip(BRIGHT_NAMES, terminal["bright"], strict=True))
    return scheme


def render(palette: dict[str, Any]) -> str:
    return json.dumps(build_scheme(palette), indent=2, ensure_ascii=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if apollo.json is stale")
    args = parser.parse_args()
    rendered = render(load_palette())

    if args.check:
        try:
            current = OUTPUT_PATH.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"missing generated artifact: {OUTPUT_PATH.name}", file=sys.stderr)
            return 1
        if current != rendered:
            print(f"generated artifact is stale: {OUTPUT_PATH.name}", file=sys.stderr)
            return 1
        print(f"up to date: {OUTPUT_PATH.name}")
        return 0

    OUTPUT_PATH.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"wrote {OUTPUT_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
