#!/usr/bin/env python3
"""Validate the Apollo snapshot and generated Windows Terminal scheme."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PALETTE_PATH = ROOT / "palette" / "apollo.json"
ARTIFACT_PATH = ROOT / "apollo.json"
HEX_COLOR = re.compile(r"^#[0-9a-f]{6}$")
NORMAL_NAMES = ("black", "red", "green", "yellow", "blue", "purple", "cyan", "white")
BRIGHT_NAMES = ("brightBlack", "brightRed", "brightGreen", "brightYellow", "brightBlue", "brightPurple", "brightCyan", "brightWhite")
EXPECTED_TOP_LEVEL = {"schemaVersion", "id", "name", "description", "appearance", "colorSpace", "provenance", "colors", "roles", "terminal", "constraints"}
REQUIRED_SCHEME_KEYS = {"name", "foreground", "background", *NORMAL_NAMES, *BRIGHT_NAMES}
OPTIONAL_SCHEME_KEYS = {"cursorColor", "selectionBackground"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"{path.name} root must be an object")
    return value


def validate_hex(value: Any, label: str) -> None:
    require(isinstance(value, str) and HEX_COLOR.fullmatch(value) is not None, f"{label} must be lowercase #rrggbb")


def validate_palette(palette: dict[str, Any]) -> None:
    require(set(palette) == EXPECTED_TOP_LEVEL, "palette top-level schema does not match schemaVersion 1")
    require(palette["schemaVersion"] == 1, "unsupported schemaVersion")
    require(palette["id"] == "apollo" and palette["name"] == "Apollo", "unexpected palette identity")
    require(palette["appearance"] == "dark" and palette["colorSpace"] == "srgb", "unexpected palette appearance or color space")
    colors = palette["colors"]
    require(isinstance(colors, dict) and colors, "colors must be a non-empty object")
    for name, value in colors.items():
        validate_hex(value, f"colors.{name}")

    terminal = palette["terminal"]
    require(set(terminal) == {"foreground", "background", "cursor", "cursorText", "selection", "ansi", "bright"}, "terminal schema is invalid")
    for name in ("foreground", "background", "cursor", "cursorText"):
        validate_hex(terminal[name], f"terminal.{name}")
    require(set(terminal["selection"]) == {"color", "alpha", "foregroundMode"}, "selection schema is invalid")
    validate_hex(terminal["selection"]["color"], "terminal.selection.color")
    require(terminal["selection"]["alpha"] == 0.5 and terminal["selection"]["foregroundMode"] == "preserve", "selection semantics changed")
    for group in ("ansi", "bright"):
        require(isinstance(terminal[group], list) and len(terminal[group]) == 8, f"terminal.{group} must contain eight colors")
        for index, value in enumerate(terminal[group]):
            validate_hex(value, f"terminal.{group}[{index}]")
    require(terminal["foreground"] == colors["foreground"], "foreground role drift")
    require(terminal["background"] == colors["background"], "background role drift")
    require(terminal["cursor"] == colors["accent"], "cursor role drift")
    require(terminal["cursorText"] == colors["background"], "cursor text role drift")
    require(terminal["selection"]["color"] == colors["selection"], "selection role drift")


def validate_scheme(scheme: dict[str, Any], palette: dict[str, Any]) -> None:
    require(REQUIRED_SCHEME_KEYS <= set(scheme), "Windows Terminal scheme is missing required fields")
    require(set(scheme) == REQUIRED_SCHEME_KEYS | OPTIONAL_SCHEME_KEYS, "Windows Terminal scheme has unknown fields")
    require("magenta" not in scheme and "brightMagenta" not in scheme, "Windows Terminal uses purple field names")
    terminal = palette["terminal"]
    expected = {
        "name": "Apollo",
        "background": terminal["background"],
        "foreground": terminal["foreground"],
        "cursorColor": terminal["cursor"],
        "selectionBackground": terminal["selection"]["color"],
        **dict(zip(NORMAL_NAMES, terminal["ansi"], strict=True)),
        **dict(zip(BRIGHT_NAMES, terminal["bright"], strict=True)),
    }
    require(scheme == expected, "Windows Terminal scheme drift")
    for name, value in scheme.items():
        if name != "name":
            validate_hex(value, name)


def main() -> int:
    try:
        palette = load_json(PALETTE_PATH)
        validate_palette(palette)
        scheme = load_json(ARTIFACT_PATH)
        validate_scheme(scheme, palette)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "generate.py"), "--check"], check=True)
    except (OSError, json.JSONDecodeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"check failed: {error}", file=sys.stderr)
        return 1
    print("Windows Terminal Apollo theme checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
