"""Free soundtrack for the short: Kokoro voiceover + generated music + sound effects.

Everything is made locally, so there is nothing to license:
- voiceover: Kokoro TTS (Apache 2.0 model), `pip install kokoro-onnx soundfile`
  plus the two model files (see MODEL_URLS), downloaded once into ./models/
- music: a lo-fi beat synthesised with numpy, original to this project
- effects: key clicks, pops, whooshes and an alert tone, also synthesised
"""
from pathlib import Path
import urllib.request

import numpy as np

SR = 24000  # Kokoro's native sample rate; the whole mix runs at it
HERE = Path(__file__).resolve().parent
MODELS = HERE / "models"
MODEL_URLS = {
    "kokoro-v1.0.onnx": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx",
    "voices-v1.0.bin": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin",
}
VOICE = "af_heart"
rng = np.random.default_rng(7)


# ── voiceover ──────────────────────────────────────────────────────────────

def voiceover(lines, speed=1.1):
    """Return one float32 clip per line of narration."""
    from kokoro_onnx import Kokoro

    MODELS.mkdir(exist_ok=True)
    for name, url in MODEL_URLS.items():
        if not (MODELS / name).exists():
            print("downloading", name)
            urllib.request.urlretrieve(url, MODELS / name)
    tts = Kokoro(str(MODELS / "kokoro-v1.0.onnx"), str(MODELS / "voices-v1.0.bin"))
    clips = []
    for line in lines:
        samples, sr = tts.create(line, voice=VOICE, speed=speed, lang="en-us")
        assert sr == SR, sr
        clips.append(trim(np.asarray(samples, dtype=np.float32)))
    return clips


def trim(x, thresh=0.01):
    """Cut leading/trailing silence so clips start exactly on their cue."""
    idx = np.flatnonzero(np.abs(x) > thresh)
    if not len(idx):
        return x
    return x[max(idx[0] - 240, 0): idx[-1] + 2400]


# ── synth helpers ──────────────────────────────────────────────────────────

def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def env(n, attack=0.005, release=0.1):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1) if attack else np.ones(n)
    return a * np.exp(-t / release)


def lowpass(x, cutoff):
    """One-pole low-pass: cheap, smooth, good enough for pads and noise."""
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def place(buf, clip, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(clip))
    buf[i:j] += clip[: j - i] * gain


# ── drums and music ────────────────────────────────────────────────────────

def kick():
    t = t_axis(0.35)
    f = 50 + 90 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.001, 0.12)


def snare():
    t = t_axis(0.25)
    noise = lowpass(rng.standard_normal(len(t)), 5000) * env(len(t), 0.001, 0.06)
    body = np.sin(2 * np.pi * 190 * t) * env(len(t), 0.001, 0.05)
    return 0.6 * noise + 0.4 * body


def hat():
    n = rng.standard_normal(int(0.06 * SR))
    n = n - lowpass(n, 7000)  # keep only the fizz
    return n * env(len(n), 0.0005, 0.018)


def pad(freqs, dur):
    t = t_axis(dur)
    x = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t + 0.4) for f in freqs)
    x *= 0.5 + 0.5 * np.sin(2 * np.pi * 0.25 * t)  # slow swell
    fade = np.minimum(1, np.minimum(t / 0.25, (dur - t) / 0.4))
    return lowpass(x * fade, 1400) / len(freqs)


def note(hz):
    return 440 * 2 ** ((hz - 69) / 12)


def music(total, bpm=96):
    """Four-chord lo-fi loop (Am–F–C–G) with kick, snare and hats."""
    buf = np.zeros(int(total * SR) + SR, dtype=np.float32)
    beat = 60 / bpm
    bar = 4 * beat
    chords = [(57, 60, 64), (53, 57, 60), (48, 55, 60), (55, 59, 62)]
    k, s, h = kick(), snare(), hat()
    b = 0
    while b * bar < total:
        start = b * bar
        place(buf, pad([note(m) for m in chords[b % 4]], bar + 0.3), start, 0.55)
        root = note(chords[b % 4][0] - 12)
        bass = np.sin(2 * np.pi * root * t_axis(bar)) * env(int(bar * SR), 0.01, 0.9)
        place(buf, bass, start, 0.35)
        for i in range(4):
            place(buf, k, start + i * beat, 0.9 if i in (0, 2) else 0.0)
            if i in (1, 3):
                place(buf, s, start + i * beat, 0.45)
        for i in range(8):
            swing = 0.03 if i % 2 else 0
            place(buf, h, start + i * beat / 2 + swing, 0.22 if i % 2 else 0.3)
        b += 1
    fade = np.minimum(1, (total - np.arange(len(buf)) / SR) / 1.5).clip(0, 1)
    return buf * fade


# ── sound effects ──────────────────────────────────────────────────────────

def click():
    n = rng.standard_normal(int(0.018 * SR))
    return lowpass(n, 3500) * env(len(n), 0.0003, 0.004)


def pop():
    t = t_axis(0.12)
    f = 500 + 900 * np.exp(-t * 40)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.001, 0.035)


def whoosh(dur=0.45):
    n = rng.standard_normal(int(dur * SR))
    t = np.arange(len(n)) / len(n)
    shaped = lowpass(n, 2500) * np.sin(np.pi * t) ** 2
    return shaped * 0.9


def alert():
    t = t_axis(0.5)
    tone = np.sign(np.sin(2 * np.pi * 220 * t)) * 0.4 + np.sin(2 * np.pi * 330 * t) * 0.6
    gate = (np.sin(2 * np.pi * 8 * t) > 0).astype(float)
    return lowpass(tone * gate, 2200) * env(len(t), 0.002, 0.3)


def chime():
    t = t_axis(1.2)
    x = sum(np.sin(2 * np.pi * note(m) * t) / (i + 1) for i, m in enumerate((76, 83, 88)))
    return x * env(len(t), 0.002, 0.45) * 0.6


# ── mixdown ────────────────────────────────────────────────────────────────

def normalise(x, peak=0.95):
    m = np.max(np.abs(x)) or 1.0
    return x * (peak / m)


def mix(total, vo_clips, vo_starts, sfx_events):
    """Music ducked under the voice, effects on top. Returns float32 mono."""
    n = int(total * SR)
    voice = np.zeros(n + SR, dtype=np.float32)
    for clip, at in zip(vo_clips, vo_starts):
        place(voice, normalise(clip, 0.9), at)

    fx = np.zeros_like(voice)
    makers = {"click": click, "pop": pop, "whoosh": whoosh, "alert": alert, "chime": chime}
    gains = {"click": 0.35, "pop": 0.35, "whoosh": 0.25, "alert": 0.35, "chime": 0.25}
    for kind, at in sfx_events:
        place(fx, makers[kind](), at, gains[kind])

    bed = music(total)[: len(voice)]
    # side-chain duck: follow the voice envelope, pull the music down ~9 dB under speech
    follow = lowpass(np.abs(voice), 6)
    duck = 1 - 0.65 * np.clip(follow / (follow.max() or 1) * 3, 0, 1)
    out = voice + fx + bed * 0.22 * duck
    # soft-clip stray peaks so loudness normalisation can lift the whole mix evenly
    out = np.tanh(2.2 * normalise(out[:n], 1.0)) / np.tanh(2.2)
    return normalise(out, 0.97).astype(np.float32)
