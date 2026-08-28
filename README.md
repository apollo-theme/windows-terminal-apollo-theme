<h1 align="center">Windows Terminal Apollo Theme</h1>

<p align="center">Apollo brings a near-black canvas, warm contrast, and vivid terminal colors to Windows Terminal.</p>

<p align="center">
  <a href="https://apollo-theme.github.io/#app-windows-terminal"><img alt="Preview" src="https://img.shields.io/badge/preview-explore-fabd2f?style=for-the-badge&amp;labelColor=141617"></a>
  <a href="https://github.com/apollo-theme/windows-terminal-apollo-theme/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/apollo-theme/windows-terminal-apollo-theme/ci.yml?branch=main&amp;style=for-the-badge&amp;label=CI&amp;labelColor=141617&amp;color=b8bb26"></a>
  <a href="https://github.com/apollo-theme/windows-terminal-apollo-theme/releases/latest"><img alt="Latest GitHub release" src="https://img.shields.io/github/v/release/apollo-theme/windows-terminal-apollo-theme?display_name=tag&amp;sort=semver&amp;style=for-the-badge&amp;label=release&amp;labelColor=141617&amp;color=d3869b"></a>
  <a href="https://github.com/apollo-theme/windows-terminal-apollo-theme/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-83a598?style=for-the-badge&amp;labelColor=141617"></a>
  <a href="https://github.com/microsoft/terminal"><img alt="Target: Windows Terminal on Windows" src="https://img.shields.io/badge/target-Windows%20Terminal%20%C2%B7%20Windows-fb4934?style=for-the-badge&amp;labelColor=141617"></a>
  <a href="https://github.com/apollo-theme/apollo-theme/blob/main/palette/apollo.json"><img alt="Canonical Apollo palette" src="https://img.shields.io/badge/palette-canonical-8ec07c?style=for-the-badge&amp;labelColor=141617"></a>
</p>

<p align="center">
  <a href="https://apollo-theme.github.io/#app-windows-terminal"><img src="https://raw.githubusercontent.com/apollo-theme/apollo-theme.github.io/main/previews/windows-terminal.svg" alt="Simulated Apollo preview for Windows Terminal"></a>
</p>
<p align="center"><sub><strong>Simulated preview.</strong> Rendered output may vary by font and platform.</sub></p>

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

The committed `apollo.json` is generated from the pinned palette snapshot at `palette/apollo.json`.

```sh
python3 scripts/generate.py --check
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

## License

[MIT](LICENSE)
