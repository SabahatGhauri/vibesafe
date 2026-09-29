#!/usr/bin/env python3
"""Render the VibeSafe social pack: static images + a vertical short.

Free toolchain only: headless Chromium (Playwright) draws each frame from the
HTML templates in this folder, ffmpeg encodes them into an H.264 MP4.

    pip install playwright imageio-ffmpeg kokoro-onnx soundfile numpy
    python3 social/generator/render.py [out_dir] [--stills] [--silent]

Uses ffmpeg from PATH, or `pip install imageio-ffmpeg` for a static build. Output defaults to social/2026-09-vibesafe-launch/.
"""
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
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


# One narration line per scene. Scene lengths stretch to fit them.
NARRATION = [
    "Built your app with AI? It works, and the demo looks great. But is it safe to ship?",
    "Your AI tool might have put your live Stripe key in the frontend, where anyone can use it.",
    "Three mistakes AI tools ship all the time: exposed API keys, Supabase tables anyone can read, and admin pages with no login.",
    "VibeSafe finds them in seconds, and explains every fix in plain English.",
    "Scan your app free, no signup, at vibesafe dot info.",
]
MIN_SCENE = [4.5, 5.5, 8.0, 5.0, 5.5]  # animations in short.html need at least this long
VO_LEAD, VO_TAIL = 0.25, 0.6            # silence before / after each line inside its scene

# Sound effects, as (kind, seconds into the scene) — matched to data-in cues in short.html
SFX = [
    [("pop", 0.9), ("pop", 1.1), ("pop", 1.3), ("pop", 1.5), ("pop", 1.7)],
    [("alert", 3.0)] + [("click", 1.0 + i / 22) for i in range(38)],
    [("whoosh", 2.6), ("whoosh", 4.5), ("whoosh", 6.6)],
    [("whoosh", 0.5), ("pop", 1.8), ("pop", 2.2)],
    [("chime", 0.1), ("pop", 1.3)],
]


def build_audio(path):
    """Write the soundtrack WAV and return scene lengths, or None if the TTS isn't installed."""
    try:
        import soundfile as sf
        import audio
    except ImportError as e:
        print(f"no soundtrack ({e}); pip install kokoro-onnx soundfile numpy")
        return None
    clips = audio.voiceover(NARRATION)
    lengths = [max(m, VO_LEAD + len(c) / audio.SR + VO_TAIL) for m, c in zip(MIN_SCENE, clips)]
    starts = [sum(lengths[:i]) for i in range(len(lengths))]
    events = [("whoosh", max(s - 0.2, 0)) for s in starts[1:]]
    events += [(k, starts[i] + at) for i, cues in enumerate(SFX) for k, at in cues]
    track = audio.mix(sum(lengths), clips, [s + VO_LEAD for s in starts], events)
    sf.write(str(path), track, audio.SR)
    for i, (c, l) in enumerate(zip(clips, lengths)):
        print(f"  scene {i + 1}: voice {len(c) / audio.SR:.1f}s, scene {l:.1f}s")
    return lengths


def render_short(browser):
    page = open_page(browser, "short.html", 1080, 1920)
    wav = OUT / "short-soundtrack.wav"
    lengths = None if "--silent" in sys.argv else build_audio(wav)
    if lengths:
        page.evaluate(f"setScenes({lengths})")
        audio_in = ["-i", str(wav)]
    else:  # silent stereo track: some apps reject video-only uploads
        audio_in = ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    duration = page.evaluate("window.DURATION")
    frames = int(duration * FPS)
    out = OUT / "short-1080x1920.mp4"
    ffmpeg = subprocess.Popen(
        [ffmpeg_exe(), "-y", "-loglevel", "error",
         "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
         *audio_in,
         "-shortest", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
         "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
         # -14 LUFS is what TikTok, Reels and Shorts normalise to
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2",
         "-c:a", "aac", "-b:a", "192k", str(out)],
        stdin=subprocess.PIPE,
    )
    for i in range(frames):
        t = i / FPS
        page.evaluate(f"render({t})")
        ffmpeg.stdin.write(page.screenshot(type="jpeg", quality=95))
        if i % (FPS * 3) == 0:
            print(f"  frame {i}/{frames}")
    ffmpeg.stdin.close()
    if ffmpeg.wait() != 0:
        sys.exit("ffmpeg failed")
    # cover frame for platforms that ask for a thumbnail: the call-to-action scene
    page.evaluate(f"render({duration - 2.5})")
    page.screenshot(path=str(OUT / "short-cover-1080x1920.png"))
    page.close()
    wav.unlink(missing_ok=True)
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
