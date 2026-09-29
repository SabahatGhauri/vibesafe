#!/usr/bin/env python3
"""Render the VibeSafe social pack: static images + a vertical short.

Free toolchain only: headless Chromium (Playwright) draws each frame from the
HTML templates in this folder, ffmpeg encodes them into an H.264 MP4.

    pip install playwright && python3 social/generator/render.py [out_dir]

Uses ffmpeg from PATH, or `pip install imageio-ffmpeg` for a static build. Output defaults to social/2026-09-vibesafe-launch/.
"""
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = Path(ARGS[0]) if ARGS else HERE.parent / "2026-09-vibesafe-launch"
FPS = 30


def ffmpeg_exe():
    """ffmpeg on PATH, else the static build from `pip install imageio-ffmpeg`."""
    found = shutil.which("ffmpeg")
    if found:
        return found
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

STILLS = [
    ("square.html", 1200, 1200, "facebook-1200x1200.png"),
    ("devto-cover.html", 1000, 420, "devto-cover-1000x420.png"),
]


def launch(p):
    kwargs = {}
    exe = "/opt/pw-browsers/chromium"
    if Path(exe).is_file():
        kwargs["executable_path"] = exe
    return p.chromium.launch(**kwargs)


def open_page(browser, name, w, h):
    page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
    page.goto((HERE / name).as_uri())
    page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready")
    return page


def render_stills(browser):
    for name, w, h, out in STILLS:
        page = open_page(browser, name, w, h)
        page.screenshot(path=str(OUT / out))
        page.close()
        print("wrote", out)


def render_short(browser):
    page = open_page(browser, "short.html", 1080, 1920)
    duration = page.evaluate("window.DURATION")
    frames = int(duration * FPS)
    out = OUT / "short-1080x1920.mp4"
    ffmpeg = subprocess.Popen(
        [ffmpeg_exe(), "-y", "-loglevel", "error",
         "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
         # silent stereo track: some apps reject video-only uploads
         "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
         "-shortest", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
         "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
         "-c:a", "aac", "-b:a", "128k", str(out)],
        stdin=subprocess.PIPE,
    )
    for i in range(frames):
        t = i / FPS
        page.evaluate(f"render({t})")
        ffmpeg.stdin.write(page.screenshot(type="jpeg", quality=95))
        if i == int(1.2 * FPS):  # cover frame for platforms that ask for a thumbnail
            page.evaluate("render(24.5)")
            page.screenshot(path=str(OUT / "short-cover-1080x1920.png"))
        if i % (FPS * 3) == 0:
            print(f"  frame {i}/{frames}")
    ffmpeg.stdin.close()
    if ffmpeg.wait() != 0:
        sys.exit("ffmpeg failed")
    page.close()
    print("wrote", out.name)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = launch(p)
        render_stills(browser)
        if "--stills" not in sys.argv:
            render_short(browser)
        browser.close()


if __name__ == "__main__":
    main()
