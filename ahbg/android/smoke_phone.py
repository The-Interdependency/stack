"""Install verification runs against the signed alpha on an Android device or emulator."""
import re
from pathlib import Path
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

PACKAGE = "org.interdependency.ahbg.alpha"
ACTIVITY = PACKAGE + "/org.interdependency.ahbg.MainActivity"


def adb(*args):
    return subprocess.check_output(["adb", *args], text=True, timeout=30)


def screen():
    adb("shell", "uiautomator", "dump", "/sdcard/ahbg-smoke.xml")
    return ET.fromstring(adb("shell", "cat", "/sdcard/ahbg-smoke.xml"))


def select_controls(nodes, label, html_id):
    """Android exposes either the HTML select or an anonymous view after its label."""
    for node in nodes:
        if node.get("resource-id", "").split("/")[-1] == html_id:
            yield node
    for caption, field in zip(nodes, nodes[1:]):
        if label in (caption.get("text"), caption.get("content-desc")):
            if field.get("class") in ("android.widget.Spinner", "android.view.View"):
                yield field


def target(text, *, tap=False, scroll=False, timeout=100, contains=False, select_id=None):
    until = time.monotonic() + timeout
    attempt = 0
    last = []
    while time.monotonic() < until:
        try:
            nodes = list(screen().iter("node"))
        except (ET.ParseError, subprocess.SubprocessError):
            time.sleep(1)
            continue
        last = [n.get("text") or n.get("content-desc", "") for n in nodes]
        if any("Launcher isn" in label for label in last):
            dialog = next((n for n in nodes if n.get("text") == "Close app"), None)
            if dialog is not None:
                x1,y1,x2,y2=map(int,re.findall(r"-?\d+",dialog.get("bounds","")))
                adb("shell","input","tap",str((x1+x2)//2),str((y1+y2)//2))
                adb("shell","am","start","-n",ACTIVITY)
                continue
        if text.startswith("Turn ") and "reconnect" in [label.casefold() for label in last]:
            retry = next(n for n in nodes if n.get("text", "").casefold() == "reconnect")
            x1,y1,x2,y2=map(int,re.findall(r"-?\d+",retry.get("bounds","")))
            adb("shell","input","tap",str((x1+x2)//2),str((y1+y2)//2))
            time.sleep(2)
            continue
        if select_id:
            candidates = select_controls(nodes, text, select_id)
        elif contains:
            candidates = (n for n, name in zip(nodes, last) if text.casefold() in name.casefold())
        else:
            candidates = (n for n, name in zip(nodes, last) if text.casefold() == name.casefold())
        for node in candidates:
            x1, y1, x2, y2 = map(int, re.findall(r"-?\d+", node.get("bounds", "")))
            if x2 <= x1 or y2 <= y1:
                continue
            if tap:
                adb("shell", "input", "tap", str((x1+x2)//2), str((y1+y2)//2))
            print(("tapped " if tap else "observed ") + text, flush=True)
            return
        if scroll:
            size = adb("shell", "wm", "size")
            width, height = map(int, re.findall(r"(\d+)x(\d+)", size)[-1])
            top, bottom = int(height*.32), int(height*.8)
            if attempt % 8 >= 4:
                top, bottom = bottom, top
            adb("shell", "input", "swipe", str(width//2), str(bottom), str(width//2), str(top), "400")
        attempt += 1
        time.sleep(1)
    Path("/tmp/ahbg-android-screen.png").write_bytes(subprocess.check_output(["adb","exec-out","screencap","-p"]))
    print(adb("shell","dumpsys","activity","activities").split("topResumedActivity")[-1][:350],flush=True)
    print(adb("logcat","-d","-s","chromium:E","AndroidRuntime:E")[-2300:],flush=True)
    raise RuntimeError(f"Android did not expose {text!r}; last visible labels: {[s for s in last if s][:45]}")


adb("shell", "input", "keyevent", "KEYCODE_WAKEUP")
adb("shell", "wm", "dismiss-keyguard")
adb("shell", "am", "start", "-W", "-n", ACTIVITY)
target("Start a plane", tap=True)
target("Move to Ring 5", tap=True, scroll=True)
target("Explorer", tap=True, scroll=True)
target("Move to Center", tap=True, scroll=True)
target("Commit plan", tap=True, scroll=True)
target("Turn 2 / 16", scroll=True, timeout=150)
def visible_plane():
    tree = screen()
    labels = " ".join(n.get("text", "") + " " + n.get("content-desc", "") for n in tree.iter("node"))
    found = re.search(r"amber seat\s*·\s*([0-9a-f]{6})", labels, re.IGNORECASE)
    if not found:
        raise RuntimeError("Android must show the private plane identifier")
    return found[1].lower()


plane_id = visible_plane()
adb("shell", "am", "force-stop", PACKAGE)
adb("shell", "cmd", "connectivity", "airplane-mode", "enable")
try:
    adb("shell", "am", "start", "-W", "-n", ACTIVITY)
    target("Reconnect")
finally:
    adb("shell", "cmd", "connectivity", "airplane-mode", "disable")
target("Turn 2 / 16", scroll=True, timeout=150)
assert visible_plane() == plane_id
target("Commit plan", scroll=True)
target("Builder moved to Ring 5 / Explorer moved to Center", scroll=True, contains=True)
print("Release APK recovered the identical plane after process termination and a network interruption.", flush=True)

# Deployment acceptance runs after the server publishes the new WebView UI.
if "--scouting" in sys.argv[1:]:
    target("Explorer", tap=True, scroll=True)
    target("Report a sighting to the Builder", tap=True, scroll=True, select_id="report-tile")
    target("Center", tap=True)
    target("Explorer report · Center to Builder", scroll=True, contains=True)
    target("Commit plan", tap=True, scroll=True)
    target("Turn 3 / 16", scroll=True, timeout=150)
    target("Builder", tap=True, scroll=True)
    target("Turn 2 · Center · Explorer · Constructed", scroll=True, contains=True)
