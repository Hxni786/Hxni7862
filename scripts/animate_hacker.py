#!/usr/bin/env python3
"""
HXNI // The Cipher Stack — Living 3D Hacker Workstation Animation Pipeline
Synthesizes seamless looping volumetric smoke, floating emerald cyber particles,
and holographic display glow sweeps over the cinematic 3D workstation render.
"""

import os
import math
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageEnhance, ImageDraw

BRAIN_DIR = r"C:\Users\Dell\.gemini\antigravity\brain\aad9b56d-40d3-4d27-b585-fa97e9632230"
WORKSPACE = r"d:\github readme"
BASE_IMG_PATH = os.path.join(BRAIN_DIR, "cipher_hacker_dark_1788604083381.jpg")

def generate_noise_field(w, h, seed, scale):
    np.random.seed(seed)
    # Generate coarse noise and upscale with gaussian filter
    cw, ch = int(w / scale), int(h / scale)
    coarse = np.random.randn(ch, cw)
    smooth = gaussian_filter(coarse, sigma=2.0)
    # Resize to full
    img = Image.fromarray(smooth).resize((w, h), Image.Resampling.BICUBIC)
    arr = np.array(img)
    return (arr - arr.mean()) / (arr.std() + 1e-5)

def create_animated_hacker():
    print("Loading base 3D hacker render...")
    base = Image.open(BASE_IMG_PATH).convert("RGB")
    # Scale to crisp web dimension: 1000x558 for optimal performance & fast load
    target_w, target_h = 1000, 558
    base = base.resize((target_w, target_h), Image.Resampling.LANCZOS)
    base_arr = np.array(base, dtype=np.float32)

    num_frames = 24
    frames = []

    # Pre-generate noise fields for seamless circular time modulation
    n1_a = generate_noise_field(target_w, target_h, seed=101, scale=35)
    n1_b = generate_noise_field(target_w, target_h, seed=202, scale=35)
    n2_a = generate_noise_field(target_w, target_h, seed=303, scale=70)
    n2_b = generate_noise_field(target_w, target_h, seed=404, scale=70)

    # Smoke mask: concentrated on left side, above chair, and ambient room air
    y_idx, x_idx = np.indices((target_h, target_w))
    # Ambient room mask (avoiding heavy occluding over keyboard/hands)
    smoke_mask = np.clip((target_w * 0.75 - x_idx) / (target_w * 0.45), 0, 1) * 0.8
    # Height falloff: rises into the upper atmosphere
    height_mask = np.clip(1.2 - (y_idx / target_h), 0.2, 1.0)
    combined_mask = smoke_mask * height_mask

    # Floating particles setup (50 particles)
    np.random.seed(786)
    num_particles = 55
    particles = []
    for _ in range(num_particles):
        px = np.random.uniform(50, target_w - 50)
        py = np.random.uniform(20, target_h - 40)
        speed = np.random.uniform(1.2, 3.2)
        radius = np.random.uniform(1.2, 2.8)
        drift = np.random.uniform(-0.8, 0.8)
        particles.append({"x": px, "y": py, "speed": speed, "radius": radius, "drift": drift})

    print(f"Synthesizing {num_frames} looping cinematic frames with volumetric smoke & particles...")

    for i in range(num_frames):
        theta = (i / num_frames) * 2 * math.pi
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        # 1. Seamless circular time combination of smoke noise
        smoke1 = cos_t * n1_a + sin_t * n1_b
        # Vertical upward drift component
        shift_y = int(sin_t * 12)
        smoke1 = np.roll(smoke1, shift_y, axis=0)

        smoke2 = sin_t * n2_a + cos_t * n2_b
        combined_smoke = (smoke1 * 0.6 + smoke2 * 0.4)
        # Normalize and clip
        smoke_intensity = np.clip((combined_smoke + 0.5) * 0.5, 0, 1) * combined_mask

        # Apply smoke lighting (emerald green tint: #00ff9c mixed with deep mist)
        frame_arr = base_arr.copy()
        # Additive atmospheric mist
        frame_arr[:, :, 0] += smoke_intensity * 12.0   # subtle red/dark ambient
        frame_arr[:, :, 1] += smoke_intensity * 45.0   # emerald glow
        frame_arr[:, :, 2] += smoke_intensity * 28.0   # subtle cyan tint

        # Screen light breathing pulse
        screen_pulse = 1.0 + 0.035 * math.sin(theta * 2)
        # Apply pulse specifically to bright green pixels (screens)
        green_mask = (frame_arr[:, :, 1] > 90) & (frame_arr[:, :, 1] > frame_arr[:, :, 0] * 1.3)
        frame_arr[green_mask, 1] *= screen_pulse
        frame_arr[green_mask, 2] *= screen_pulse

        # Clip frame
        frame_arr = np.clip(frame_arr, 0, 255).astype(np.uint8)
        frame_img = Image.fromarray(frame_arr)

        # 2. Draw floating luminous cyber particles & flares
        draw = ImageDraw.Draw(frame_img, "RGBA")
        for p in particles:
            # Seamless particle vertical loop
            curr_y = (p["y"] - (i / num_frames) * target_h * 0.25) % (target_h - 40) + 20
            curr_x = p["x"] + math.sin(theta + p["drift"]) * 14.0
            r = p["radius"]
            # Soft glowing halo
            draw.ellipse([curr_x - r * 2.5, curr_y - r * 2.5, curr_x + r * 2.5, curr_y + r * 2.5], fill=(0, 255, 156, 35))
            # Bright spark core
            draw.ellipse([curr_x - r, curr_y - r, curr_x + r, curr_y + r], fill=(200, 255, 230, 220))

        # 3. Holographic scanline drift across curved screen area
        scan_y = int((i / num_frames) * target_h * 0.7) + 50
        draw.line([(int(target_w * 0.28), scan_y), (int(target_w * 0.88), scan_y)], fill=(0, 255, 156, 45), width=2)

        frames.append(frame_img)

    # Save animated WebP
    out_webp = os.path.join(WORKSPACE, "assets", "hero", "hero-hacker.webp")
    frames[0].save(
        out_webp,
        format="WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
        quality=88,
        method=6
    )
    print(f"  -> Saved animated WebP: {out_webp} ({os.path.getsize(out_webp) / 1024:.1f} KB)")

    # Also save as hero-01.webp (for primary hero compatibility)
    out_hero01 = os.path.join(WORKSPACE, "assets", "hero", "hero-01.webp")
    frames[0].save(
        out_hero01,
        format="WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
        quality=88,
        method=6
    )
    print(f"  -> Saved {out_hero01} ({os.path.getsize(out_hero01) / 1024:.1f} KB)")

    # Save animated GIF fallback
    out_gif = os.path.join(WORKSPACE, "assets", "hero", "hero-hacker.gif")
    gif_frames = [f.resize((720, 402), Image.Resampling.LANCZOS).quantize(colors=128, method=Image.Quantize.MEDIANCUT) for f in frames]
    gif_frames[0].save(
        out_gif,
        save_all=True,
        append_images=gif_frames[1:],
        duration=80,
        loop=0,
        optimize=True
    )
    print(f"  -> Saved animated GIF: {out_gif} ({os.path.getsize(out_gif) / 1024:.1f} KB)")

    # Save mobile crop
    out_mob = os.path.join(WORKSPACE, "assets", "hero", "hero-01-mobile.webp")
    cw = int(target_h * 1.05)
    left = (target_w - cw) // 2
    mob_frames = [f.crop((left, 0, left + cw, target_h)).resize((600, 570), Image.Resampling.LANCZOS) for f in frames]
    mob_frames[0].save(
        out_mob,
        format="WEBP",
        save_all=True,
        append_images=mob_frames[1:],
        duration=80,
        loop=0,
        quality=86,
        method=6
    )
    print(f"  -> Saved mobile animated WebP: {out_mob} ({os.path.getsize(out_mob) / 1024:.1f} KB)")

if __name__ == "__main__":
    create_animated_hacker()
