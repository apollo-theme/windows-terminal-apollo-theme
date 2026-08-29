import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "generate.py"
NORMAL_NAMES = ("black", "red", "green", "yellow", "blue", "purple", "cyan", "white")
BRIGHT_NAMES = ("brightBlack", "brightRed", "brightGreen", "brightYellow", "brightBlue", "brightPurple", "brightCyan", "brightWhite")
LIGHT_SHA256 = "b0dbdeb719ed1931c424e9590562689325ecac1609e2fed6406ec5c4d3dc5763"
EXPECTED_TOP_LEVEL = {"schemaVersion", "id", "name", "description", "appearance", "colorSpace", "provenance", "colors", "roles", "terminal", "constraints"}
VARIANTS = (
    ("apollo", "Apollo", "dark", ROOT / "palette" / "apollo.json", ROOT / "apollo.json"),
    ("apollo-light", "Apollo Light", "light", ROOT / "palette" / "apollo-light.json", ROOT / "apollo-light.json"),
)


def load_generator():
    spec = importlib.util.spec_from_file_location("generate", GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class WindowsTerminalThemeTests(unittest.TestCase):
    def test_light_palette_snapshot_is_canonical(self):
        path = ROOT / "palette" / "apollo-light.json"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), LIGHT_SHA256)

    def test_palette_variant_schema_and_semantics(self):
        for palette_id, name, appearance, palette_path, _ in VARIANTS:
            with self.subTest(variant=palette_id):
                palette = json.loads(palette_path.read_text(encoding="utf-8"))
                self.assertEqual(set(palette), EXPECTED_TOP_LEVEL)
                self.assertEqual(palette["schemaVersion"], 1)
                self.assertEqual((palette["id"], palette["name"], palette["appearance"]), (palette_id, name, appearance))
                self.assertEqual(palette["colorSpace"], "srgb")
                terminal = palette["terminal"]
                colors = palette["colors"]
                self.assertEqual(terminal["foreground"], colors["foreground"])
                self.assertEqual(terminal["background"], colors["background"])
                self.assertEqual(terminal["cursor"], colors["accent"])
                self.assertEqual(terminal["cursorText"], colors["background"])
                self.assertEqual(set(terminal["selection"]), {"color", "alpha", "foregroundMode"})
                self.assertEqual(terminal["selection"]["color"], colors["selection"])
                self.assertEqual(terminal["selection"]["alpha"], 0.5 if appearance == "dark" else 1.0)
                self.assertEqual(terminal["selection"]["foregroundMode"], "preserve")
                self.assertEqual(len(terminal["ansi"]), 8)
                self.assertEqual(len(terminal["bright"]), 8)

    def test_native_artifact_matches_terminal_palette(self):
        expected_keys = {"name", "background", "foreground", "cursorColor", "selectionBackground", *NORMAL_NAMES, *BRIGHT_NAMES}
        for palette_id, name, _, palette_path, artifact_path in VARIANTS:
            with self.subTest(variant=palette_id):
                palette = json.loads(palette_path.read_text(encoding="utf-8"))
                scheme = json.loads(artifact_path.read_text(encoding="utf-8"))
                terminal = palette["terminal"]
                self.assertEqual(set(scheme), expected_keys)
                self.assertEqual(scheme["name"], name)
                self.assertEqual(scheme["background"], terminal["background"])
                self.assertEqual(scheme["foreground"], terminal["foreground"])
                self.assertEqual(scheme["cursorColor"], terminal["cursor"])
                self.assertEqual(scheme["selectionBackground"], terminal["selection"]["color"])
                self.assertEqual([scheme[slot] for slot in NORMAL_NAMES], terminal["ansi"])
                self.assertEqual([scheme[slot] for slot in BRIGHT_NAMES], terminal["bright"])
                self.assertNotIn("magenta", scheme)
                self.assertNotIn("brightMagenta", scheme)

    def test_generator_is_deterministic(self):
        generator = load_generator()
        expected = [(artifact, palette) for _, _, _, palette, artifact in VARIANTS]
        self.assertEqual(list(generator.OUTPUTS.items()), expected)
        first = generator.render_outputs()
        self.assertEqual(first, generator.render_outputs())
        for artifact_path, rendered in first.items():
            self.assertEqual(rendered, artifact_path.read_text(encoding="utf-8"))

    def test_generator_finds_unexpected_native_outputs(self):
        generator = load_generator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("apollo.json", "apollo-light.json", "apollo-copy.json"):
                (root / name).touch()
            self.assertEqual(generator.find_unexpected_outputs(root), [root / "apollo-copy.json"])


if __name__ == "__main__":
    unittest.main()
