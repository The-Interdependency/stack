"""Exercise the production renderer in Chromium, including private map overlays."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

CHROME = os.environ.get("AHBG_CHROME") or shutil.which("google-chrome") or shutil.which("chromium")


@unittest.skipUnless(CHROME, "Chromium is required for the live SVG selection test")
class SelectionTests(unittest.TestCase):
    def test_selection_preserves_fog_and_build_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copy(Path(__file__).resolve().parents[1] / "board.js", root)
            (root / "test.html").write_text('''<!doctype html><body data-live>
<svg id="board"></svg><ol id="feed-list"></ol><p id="inspect"></p><output id="result"></output>
<script src="board.js"></script><script>
render(validateSnapshot(EMBEDDED_SNAPSHOT));
const points = document.querySelectorAll(".tile-point");
const hit = document.querySelectorAll(".tile-hit");
points[0].classList.add("built");
points[1].classList.add("fog");
hit[1].dispatchEvent(new MouseEvent("click"));
const afterTap = points[1].classList.contains("selected");
hit[0].dispatchEvent(new KeyboardEvent("keydown", {key:"Enter"}));
if (afterTap && points[0].classList.contains("selected") && !points[1].classList.contains("selected")
    && points[0].classList.contains("built") && points[1].classList.contains("fog")) {
  document.querySelector("output").textContent="PASS";
}
</script>''')
            result = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                                     "--user-data-dir="+str(root/"profile"), "--dump-dom",
                                     (root/"test.html").as_uri()], capture_output=True, text=True,
                                    check=True, timeout=45)
            self.assertIn('<output id="result">PASS</output>', result.stdout)
