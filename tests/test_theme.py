import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALETTE_PATH = ROOT / "palette" / "apollo.json"
ARTIFACT_PATH = ROOT / "apollo.json"
GENERATOR_PATH = ROOT / "scripts" / "generate.py"
NORMAL_NAMES = ("black", "red", "green", "yellow", "blue", "purple", "cyan", "white")
BRIGHT_NAMES = ("brightBlack", "brightRed", "brightGreen", "brightYellow", "brightBlue", "brightPurple", "brightCyan", "brightWhite")


def load_generator():
    spec = importlib.util.spec_from_file_location("generate", GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class WindowsTerminalThemeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.palette = json.loads(PALETTE_PATH.read_text(encoding="utf-8"))
        cls.scheme = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))

    def test_native_artifact_matches_terminal_palette(self):
        terminal = self.palette["terminal"]
        self.assertEqual(self.scheme["name"], "Apollo")
        self.assertEqual(self.scheme["background"], terminal["background"])
        self.assertEqual(self.scheme["foreground"], terminal["foreground"])
        self.assertEqual(self.scheme["cursorColor"], terminal["cursor"])
        self.assertEqual(self.scheme["selectionBackground"], terminal["selection"]["color"])
        self.assertEqual([self.scheme[name] for name in NORMAL_NAMES], terminal["ansi"])
        self.assertEqual([self.scheme[name] for name in BRIGHT_NAMES], terminal["bright"])

    def test_windows_terminal_uses_purple_field_names(self):
        self.assertIn("purple", self.scheme)
        self.assertIn("brightPurple", self.scheme)
        self.assertNotIn("magenta", self.scheme)
        self.assertNotIn("brightMagenta", self.scheme)

    def test_generator_is_deterministic(self):
        generator = load_generator()
        first = generator.render(generator.load_palette(PALETTE_PATH))
        second = generator.render(generator.load_palette(PALETTE_PATH))
        self.assertEqual(first, second)
        self.assertEqual(first, ARTIFACT_PATH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
