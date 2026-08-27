# Apollo for Windows Terminal

Apollo is SonicTerm's high-contrast Gruvbox Dark Hard variant, with its near-black canvas and bright Base16 terminal colors. This repository is standalone; `palette/apollo.json` is the pinned source snapshot and `apollo.json` is generated from it.

Repository: https://github.com/apollo-theme/windows-terminal-apollo-theme

## Install and activate

Open Windows Terminal **Settings**, choose **Open JSON file**, and paste the object from `apollo.json` into the top-level `schemes` array. Do not replace the entire settings file. Activate it for a profile (or profile defaults) with:

```json
"colorScheme": "Apollo"
```

Save the settings file; Windows Terminal reloads it.

## Uninstall

Select another `colorScheme`, then remove the object whose `name` is `Apollo` from the `schemes` array.

## Visual check

Print ANSI colors 0–15, move the cursor over text, and select text. Confirm the `#141617` canvas, warm foreground, yellow cursor, and exact normal/bright colors in `palette/apollo.json`. Windows Terminal schemes cannot express Apollo's selection alpha or cursor-text color, so selection uses opaque `#3c3836`. This repository was generated and JSON-validated off Windows; rendered pixels require a Windows Terminal check.

## Development

```sh
python3 scripts/generate.py --check
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```
