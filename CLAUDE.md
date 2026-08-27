# Windows Terminal Apollo Theme

## Architecture

`palette/apollo.json` is the exact canonical snapshot. `scripts/generate.py` maps it deterministically to the committed JSON scheme object `apollo.json`; `scripts/check.py` validates snapshot schema, lowercase colors, required Windows Terminal fields, exact mappings, and artifact drift. `tests/test_theme.py` covers ordered normal/bright colors, `purple` field naming, JSON generation, and determinism.

The artifact is one scheme object for insertion into a user's `schemes` array, never a replacement `settings.json`. Windows Terminal calls the magenta slots `purple` and `brightPurple`. Its scheme schema cannot represent canonical selection alpha or cursor-text color, so the generated selection color is opaque and `terminal.cursorText` is not emitted. Do not add profile or user settings.

Never edit the snapshot independently. Update it from the canonical Apollo palette, regenerate, and commit both changes. Scripts and tests must not read or write real Windows Terminal settings.

## Commands

```sh
# Build
python3 scripts/generate.py

# Generated-file gate
python3 scripts/generate.py --check

# Syntax lint
python3 -m compileall -q scripts tests

# JSON schema, colors, and drift
python3 scripts/check.py

# Full tests
python3 -m unittest discover -s tests -v

# Named single test
python3 -m unittest tests.test_theme.WindowsTerminalThemeTests.test_native_artifact_matches_terminal_palette -v
```

Windows Terminal has no documented non-GUI validation command for a standalone scheme object. Run the README visual check on Windows.
