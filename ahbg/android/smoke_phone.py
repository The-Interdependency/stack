"""Install verification runs against the signed alpha on an Android device or emulator."""
import re
import subprocess
import time
import xml.etree.ElementTree as ET

PACKAGE = "org.interdependency.ahbg.alpha"
ACTIVITY = PACKAGE + "/org.interdependency.ahbg.MainActivity"


def adb(*args):
    return subprocess.check_output(["adb", *args], text=True, timeout=30)


def screen():
    adb("shell", "uiautomator", "dump", "/sdcard/ahbg-smoke.xml")
    return ET.fromstring(adb("shell", "cat", "/sdcard/ahbg-smoke.xml"))


def target(text, *, tap=False, scroll=False, timeout=100):
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
        for node, name in zip(nodes, last):
            if name != text:
                continue
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
    raise RuntimeError(f"Android did not expose {text!r}; last visible labels: {[s for s in last if s][:45]}")


adb("shell", "am", "start", "-n", ACTIVITY)
target("Start a plane", tap=True)
target("Move to Ring 5", tap=True, scroll=True)
target("Explorer", tap=True, scroll=True)
target("Move to Center", tap=True, scroll=True)
target("Commit plan", tap=True, scroll=True)
target("Turn 2 / 16", scroll=True, timeout=150)
adb("shell", "am", "force-stop", PACKAGE)
adb("shell", "am", "start", "-n", ACTIVITY)
target("Turn 2 / 16", scroll=True)
target("Commit plan", scroll=True)
print("Release APK recovered the plane after application process termination.", flush=True)
