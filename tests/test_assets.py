"""Check that the site's local media paths match files included in the upload."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AssetPathsTest(unittest.TestCase):
    def test_story_photos_exist(self):
        content = (ROOT / "content.js").read_text(encoding="utf-8")
        story = json.loads(content.removeprefix("const STORY = ").strip().removesuffix(";"))
        photos = [photo for page in story["pages"] for photo in page.get("photos", [])]
        self.assertTrue(photos, "No photos found in the story")
        for photo in photos:
            with self.subTest(photo=photo):
                self.assertFalse(Path(photo).is_absolute())
                self.assertTrue((ROOT / photo).is_file(), f"Missing photo: {photo}")

    def test_music_exists(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        match = re.search(r'<audio\b[^>]*\bsrc="([^"]+)"', html)
        self.assertIsNotNone(match, "Audio source not found")
        self.assertTrue((ROOT / match.group(1)).is_file())


if __name__ == "__main__":
    unittest.main()
