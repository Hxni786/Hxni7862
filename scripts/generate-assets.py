#!/usr/bin/env python3
"""
HXNI // THE CIPHER STACK — Asset Generation Pipeline
Generates, converts, and optimizes all visual assets for the GitHub Profile.
Target aesthetic:
- 85% Black (#030303 / #080808 / #0D0D0D)
- 10% White / Gray (#F2F2F2 / #737373)
- 5% Emerald & Cyan (#00FF9C / #00C8FF)
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BRAIN_DIR = r"C:\Users\Dell\.gemini\antigravity\brain\aad9b56d-40d3-4d27-b585-fa97e9632230"
WORKSPACE = r"d:\github readme"

# Base generated renders
HERO_RENDER = os.path.join(BRAIN_DIR, "hero_01_1788601488940.jpg")
CIPHER_RENDER = os.path.join(BRAIN_DIR, "cipher_core_1788601509566.jpg")
AVATAR_RENDER = os.path.join(BRAIN_DIR, "avatar_cipher_1788601531095.jpg")
NEXUS_RENDER = os.path.join(BRAIN_DIR, "the_3d_nexus_1788601555452.jpg")
TICKET_RENDER = os.path.join(BRAIN_DIR, "ticketverse_1788601584484.jpg")

def ensure_dirs():
    dirs = [
        os.path.join(WORKSPACE, "assets", "hero"),
        os.path.join(WORKSPACE, "assets", "identity"),
        os.path.join(WORKSPACE, "assets", "projects"),
        os.path.join(WORKSPACE, "assets", "experiments"),
        os.path.join(WORKSPACE, "assets", "activity"),
        os.path.join(WORKSPACE, "assets", "footer"),
        os.path.join(WORKSPACE, "scripts"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def process_hero():
    print("Processing Hero Assets...")
    out_dir = os.path.join(WORKSPACE, "assets", "hero")
    if os.path.exists(HERO_RENDER):
        img = Image.open(HERO_RENDER).convert("RGB")
        # 1. hero-01.png
        img.save(os.path.join(out_dir, "hero-01.png"), format="PNG", optimize=True)
        # 2. hero-01.webp
        img.save(os.path.join(out_dir, "hero-01.webp"), format="WEBP", quality=90, method=6)
        # 3. hero-static.webp
        enhancer = ImageEnhance.Contrast(img)
        static_img = enhancer.enhance(1.1)
        static_img.save(os.path.join(out_dir, "hero-static.webp"), format="WEBP", quality=88, method=6)
        # 4. hero-01-mobile.webp (cropped centered 800x720)
        w, h = img.size
        cw = min(w, int(h * 1.1))
        left = (w - cw) // 2
        mobile_img = img.crop((left, 0, left + cw, h)).resize((800, 720), Image.Resampling.LANCZOS)
        mobile_img.save(os.path.join(out_dir, "hero-01-mobile.webp"), format="WEBP", quality=88, method=6)
        print("  -> Hero assets generated successfully.")

def process_identity():
    print("Processing Identity Assets...")
    out_dir = os.path.join(WORKSPACE, "assets", "identity")
    if os.path.exists(CIPHER_RENDER):
        img = Image.open(CIPHER_RENDER).convert("RGB")
        img.save(os.path.join(out_dir, "cipher-core.webp"), format="WEBP", quality=90, method=6)
    
    if os.path.exists(AVATAR_RENDER):
        img = Image.open(AVATAR_RENDER).convert("RGB")
        img.save(os.path.join(out_dir, "avatar-cipher.webp"), format="WEBP", quality=90, method=6)
    
    generate_cipher_core_gif(out_dir)

def generate_cipher_core_gif(out_dir):
    print("Generating animated cipher-core.gif...")
    gif_path = os.path.join(out_dir, "cipher-core.gif")
    
    if os.path.exists(CIPHER_RENDER):
        base = Image.open(CIPHER_RENDER).convert("RGBA").resize((400, 400), Image.Resampling.LANCZOS)
    else:
        base = Image.new("RGBA", (400, 400), (3, 3, 3, 255))
    
    frames = []
    num_frames = 24
    
    for i in range(num_frames):
        angle = (i / num_frames) * 2 * math.pi
        frame = Image.new("RGBA", (400, 400), (3, 3, 3, 255))
        
        glow_factor = 0.94 + 0.06 * math.sin(angle)
        enhancer = ImageEnhance.Brightness(base)
        b_frame = enhancer.enhance(glow_factor)
        frame.paste(b_frame, (0, 0))
        
        overlay = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        cx, cy = 200, 200
        
        # Ring 1
        r1_x, r1_y = 150, 60
        a1 = angle
        p1_x = cx + r1_x * math.cos(a1)
        p1_y = cy + r1_y * math.sin(a1)
        draw.ellipse([p1_x - 3, p1_y - 3, p1_x + 3, p1_y + 3], fill=(0, 255, 156, 220))
        draw.ellipse([p1_x - 6, p1_y - 6, p1_x + 6, p1_y + 6], outline=(0, 255, 156, 100), width=1)
        
        # Ring 2
        r2_x, r2_y = 175, 75
        a2 = -angle * 1.2
        p2_x = cx + r2_x * math.cos(a2)
        p2_y = cy + r2_y * math.sin(a2)
        draw.ellipse([p2_x - 3, p2_y - 3, p2_x + 3, p2_y + 3], fill=(0, 200, 255, 200))
        
        # Ring 3
        r3_x, r3_y = 190, 85
        a3 = angle * 0.7 + 1.5
        p3_x = cx + r3_x * math.cos(a3)
        p3_y = cy + r3_y * math.sin(a3)
        draw.ellipse([p3_x - 2, p3_y - 2, p3_x + 2, p3_y + 2], fill=(0, 255, 156, 180))
        
        frame = Image.alpha_composite(frame, overlay).convert("RGB")
        frames.append(frame.quantize(colors=128, method=Image.Quantize.MEDIANCUT))
    
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=60,
        loop=0,
        optimize=True
    )
    print(f"  -> Generated {gif_path} ({os.path.getsize(gif_path)} bytes)")

def create_cinematic_backdrop(w=1280, h=720):
    arr = np.zeros((h, w, 3), dtype=np.float32)
    y_coords, x_coords = np.indices((h, w))
    cx, cy = w / 2.0, h / 2.0
    r = np.sqrt(((x_coords - cx) / (w * 0.6)) ** 2 + ((y_coords - cy) / (h * 0.6)) ** 2)
    center_glow = np.clip(1.0 - r, 0, 1) ** 2.2
    
    arr[:, :, 0] = 3.0 + center_glow * 6.0
    arr[:, :, 1] = 3.0 + center_glow * 10.0
    arr[:, :, 2] = 3.0 + center_glow * 8.0
    
    img = Image.fromarray(arr.astype(np.uint8))
    draw = ImageDraw.Draw(img)
    
    horizon = int(h * 0.62)
    for y in range(horizon, h, 20):
        alpha = int(18 + 45 * ((y - horizon) / (h - horizon)))
        draw.line([(0, y), (w, y)], fill=(12, 35, 24, alpha), width=1)
    
    for x in range(-w, 2 * w, 50):
        draw.line([(w // 2 + (x - w // 2) // 4, horizon), (x, h)], fill=(10, 30, 20, 25), width=1)
    
    np.random.seed(42)
    for _ in range(70):
        px = np.random.randint(0, w)
        py = np.random.randint(0, h)
        intensity = np.random.randint(40, 160)
        draw.point((px, py), fill=(0, intensity, int(intensity * 0.7)))
        
    return img

def render_hxnix(out_path):
    img = create_cinematic_backdrop()
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    cx, cy = w // 2, int(h * 0.46)
    
    np.random.seed(101)
    num_nodes = 22
    nodes = []
    for i in range(num_nodes):
        angle = np.random.uniform(0, 2 * math.pi)
        radius = np.random.uniform(40, 240)
        nx = int(cx + radius * math.cos(angle) * 1.3)
        ny = int(cy + radius * math.sin(angle) * 0.8)
        nodes.append((nx, ny))
    
    for i, (x1, y1) in enumerate(nodes):
        for j, (x2, y2) in enumerate(nodes):
            if i < j:
                dist = math.hypot(x2 - x1, y2 - y1)
                if dist < 170:
                    alpha = int(140 * (1.0 - dist / 170))
                    draw.line([(x1, y1), (x2, y2)], fill=(0, 255, 156, alpha), width=1)
    
    for i, (x, y) in enumerate(nodes):
        is_hub = (i % 4 == 0)
        r = 6 if is_hub else 3
        draw.ellipse([x - r * 2.5, y - r * 2.5, x + r * 2.5, y + r * 2.5], fill=(0, 255, 156, 35))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(220, 255, 240, 255))
    
    gw, gh = 420, 260
    gx, gy = cx - gw // 2, cy - gh // 2
    draw.rectangle([gx, gy, gx + gw, gy + gh], outline=(0, 255, 156, 120), width=1)
    draw.rectangle([gx + 1, gy + 1, gx + gw - 1, gy + gh - 1], fill=(10, 18, 14, 110))
    cl = 15
    for px, py in [(gx, gy), (gx + gw, gy), (gx, gy + gh), (gx + gw, gy + gh)]:
        sx = 1 if px == gx else -1
        sy = 1 if py == gy else -1
        draw.line([(px, py), (px + sx * cl, py)], fill=(0, 255, 156, 255), width=2)
        draw.line([(px, py), (px, py + sy * cl)], fill=(0, 255, 156, 255), width=2)
        
    draw.text((gx + 20, gy + 18), "SYS // PROTOCOL: HXNIX NEURAL MESH", fill=(0, 255, 156, 220))
    draw.text((gx + 20, gy + 38), "TOPOLOGY: DECENTRALIZED GRAPH // 22 NODES", fill=(115, 115, 115, 200))
    draw.text((gx + 20, gy + gh - 30), "LATENCY: 0.12ms  SYNC: 99.98%  STATUS: ENCRYPTED", fill=(0, 200, 255, 210))
    
    img.save(out_path, format="WEBP", quality=88, method=6)
    print(f"  -> Created {out_path}")

def render_hxni_express(out_path):
    img = create_cinematic_backdrop()
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    cx, cy = w // 2, int(h * 0.48)
    
    for rad in [80, 160, 240, 320]:
        draw.ellipse([cx - rad * 1.4, cy - rad * 0.7, cx + rad * 1.4, cy + rad * 0.7], outline=(0, 255, 156, 30), width=1)
    
    route_points = [
        (cx - 280, cy + 90), (cx - 160, cy + 30), (cx - 60, cy + 70),
        (cx + 40, cy - 20), (cx + 180, cy + 40), (cx + 290, cy - 50)
    ]
    for i in range(len(route_points) - 1):
        p1, p2 = route_points[i], route_points[i + 1]
        draw.line([p1, p2], fill=(0, 255, 156, 180), width=2)
        draw.ellipse([p1[0] - 4, p1[1] - 4, p1[0] + 4, p1[1] + 4], fill=(0, 200, 255, 220))
    draw.ellipse([route_points[-1][0] - 5, route_points[-1][-1] - 5, route_points[-1][0] + 5, route_points[-1][-1] + 5], fill=(0, 255, 156, 255))
    
    pw, ph = 280, 160
    px, py = cx - pw // 2, cy - ph // 2 - 30
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=16, fill=(12, 14, 16, 235), outline=(0, 255, 156, 180), width=2)
    draw.rectangle([px + 20, py + 40, px + pw - 20, py + 42], fill=(0, 200, 255, 220))
    draw.text((px + 24, py + 16), "HXNI EXPRESS // LOGISTICS ENGINE", fill=(242, 242, 242, 240))
    draw.text((px + 24, py + 55), "CARRIER POD: HYPER-ISOLATED 0x786", fill=(115, 115, 115, 220))
    draw.text((px + 24, py + 78), "ROUTE OPTIMIZATION: REAL-TIME GRAPH", fill=(115, 115, 115, 220))
    draw.text((px + 24, py + 105), "STATUS: DISPATCHED  ETA: 4 MIN", fill=(0, 255, 156, 240))
    
    img.save(out_path, format="WEBP", quality=88, method=6)
    print(f"  -> Created {out_path}")

def render_hxni_finance(out_path):
    img = create_cinematic_backdrop()
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    cx, cy = w // 2, int(h * 0.48)
    
    for off_x, off_y, col in [(cx - 180, cy + 20, (180, 200, 205)), (cx + 190, cy + 40, (0, 255, 156)), (cx, cy + 90, (0, 200, 255))]:
        draw.ellipse([off_x - 35, off_y - 12, off_x + 35, off_y + 12], fill=(col[0], col[1], col[2], 80), outline=(col[0], col[1], col[2], 200), width=2)
    
    gw, gh = 520, 280
    gx, gy = cx - gw // 2, cy - gh // 2 - 20
    draw.rounded_rectangle([gx, gy, gx + gw, gy + gh], radius=12, fill=(8, 12, 11, 230), outline=(0, 255, 156, 140), width=1)
    
    for line_y in range(gy + 50, gy + gh - 40, 40):
        draw.line([(gx + 30, line_y), (gx + gw - 30, line_y)], fill=(30, 45, 38, 160), width=1)
    
    points = [
        (gx + 35, gy + 190), (gx + 110, gy + 160), (gx + 180, gy + 175),
        (gx + 260, gy + 110), (gx + 340, gy + 130), (gx + 420, gy + 80),
        (gx + 485, gy + 65)
    ]
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=(0, 255, 156, 240), width=3)
        draw.ellipse([points[i][0] - 3, points[i][1] - 3, points[i][0] + 3, points[i][1] + 3], fill=(0, 200, 255, 255))
    draw.ellipse([points[-1][0] - 4, points[-1][1] - 4, points[-1][0] + 4, points[-1][1] + 4], fill=(0, 255, 156, 255))
    
    draw.text((gx + 25, gy + 20), "HXNI FINANCE // TELEMETRY & LEDGER", fill=(242, 242, 242, 240))
    draw.text((gx + gw - 170, gy + 20), "+34.82%  [OPTIMAL]", fill=(0, 255, 156, 240))
    draw.text((gx + 25, gy + gh - 32), "CURRENCY: CIPHER-X  VOLUME: 1.48M  SECURITY: ISOLATED", fill=(115, 115, 115, 220))
    
    img.save(out_path, format="WEBP", quality=88, method=6)
    print(f"  -> Created {out_path}")

def render_bespoke_estore(out_path):
    img = create_cinematic_backdrop()
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    cx, cy = w // 2, int(h * 0.46)
    
    mw, mh = 240, 300
    mx, my = cx - mw // 2, cy - mh // 2
    
    draw.rectangle([mx - 40, my - 20, mx + mw + 40, my + mh + 20], outline=(0, 200, 255, 50), width=1)
    draw.rectangle([mx, my, mx + mw, my + mh], fill=(14, 15, 18, 250), outline=(0, 255, 156, 200), width=2)
    draw.line([(mx, my), (mx + 20, my - 20), (mx + mw + 20, my - 20), (mx + mw, my)], fill=(0, 255, 156, 120), width=1)
    draw.line([(mx + mw, my), (mx + mw + 20, my - 20), (mx + mw + 20, my + mh - 20), (mx + mw, my + mh)], fill=(0, 255, 156, 90), width=1)
    
    draw.text((mx + 45, my + 60), "HXNI // BESPOKE", fill=(242, 242, 242, 240))
    draw.text((mx + 40, my + 85), "AUTONOMOUS LUXURY", fill=(0, 255, 156, 220))
    draw.rectangle([mx + 30, my + 130, mx + mw - 30, my + 131], fill=(115, 115, 115, 160))
    draw.text((mx + 35, my + 150), "SKU: CX-984-LTD", fill=(115, 115, 115, 200))
    draw.text((mx + 35, my + 175), "MATERIAL: CARBON TITANIUM", fill=(115, 115, 115, 200))
    draw.text((mx + 35, my + 210), "EDITION: 01 // 10", fill=(0, 200, 255, 220))
    
    img.save(out_path, format="WEBP", quality=88, method=6)
    print(f"  -> Created {out_path}")

def render_secret_vault(out_path):
    img = create_cinematic_backdrop()
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    cx, cy = w // 2, int(h * 0.48)
    
    for r in [220, 190, 160, 130, 90, 50]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 35, 34, 255), width=3)
    
    draw.ellipse([cx - 162, cy - 162, cx + 162, cy + 162], outline=(0, 255, 156, 190), width=2)
    draw.ellipse([cx - 92, cy - 92, cx + 92, cy + 92], outline=(0, 255, 156, 240), width=2)
    
    for i in range(12):
        rad = (i / 12) * 2 * math.pi
        bx1 = cx + 130 * math.cos(rad)
        by1 = cy + 130 * math.sin(rad)
        bx2 = cx + 190 * math.cos(rad)
        by2 = cy + 190 * math.sin(rad)
        draw.line([(bx1, by1), (bx2, by2)], fill=(0, 255, 156, 200), width=4)
        draw.ellipse([bx2 - 5, by2 - 5, bx2 + 5, by2 + 5], fill=(220, 255, 240, 255))
        
    draw.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], fill=(10, 14, 12, 250), outline=(0, 255, 156, 255), width=2)
    draw.text((cx - 24, cy - 8), "LOCKED", fill=(0, 255, 156, 255))
    
    draw.text((cx - 160, cy + 240), "CLASSIFIED ENCLAVE // LEVEL 5 ACCESS REQUIRED", fill=(255, 59, 48, 220))
    draw.text((cx - 130, cy + 265), "ZERO-KNOWLEDGE AUTHENTICATION ACTIVE", fill=(115, 115, 115, 200))
    
    img.save(out_path, format="WEBP", quality=88, method=6)
    print(f"  -> Created {out_path}")

def render_spice_with_hassan(out_path):
    img = create_cinematic_backdrop()
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    cx, cy = w // 2, int(h * 0.48)
    
    pw, ph = 480, 180
    px, py = cx - pw // 2, cy - ph // 2 + 40
    draw.ellipse([px, py, px + pw, py + ph], fill=(18, 19, 21, 240), outline=(0, 255, 156, 120), width=2)
    draw.ellipse([px + 30, py + 15, px + pw - 30, py + ph - 15], outline=(35, 40, 38, 200), width=1)
    
    dw, dh = 200, 130
    dx, dy = cx - dw // 2, cy - dh // 2 - 20
    draw.chord([dx, dy, dx + dw, dy + dh * 2], 180, 360, fill=(22, 25, 28, 250), outline=(0, 255, 156, 180), width=2)
    draw.ellipse([cx - 15, dy - 15, cx + 15, dy + 15], fill=(0, 255, 156, 190))
    
    draw.ellipse([cx - 90, cy + 20, cx + 90, cy + 60], fill=(255, 180, 100, 25))
    
    draw.text((cx - 190, cy - 140), "RESTAURANT PROTOCOL // SPICE WITH HASSAN", fill=(242, 242, 242, 240))
    draw.text((cx - 190, cy - 118), "CUISINE: CONTEMPORARY FUSION // GASTRONOMY ENGINE", fill=(115, 115, 115, 200))
    draw.text((cx - 190, cy + 150), "SEAT TELEMETRY: TABLE 07 // RESERVATION SYNCED", fill=(0, 255, 156, 220))
    
    img.save(out_path, format="WEBP", quality=88, method=6)
    print(f"  -> Created {out_path}")

def render_experiments():
    print("Processing Experiment Lab Assets...")
    out_dir = os.path.join(WORKSPACE, "assets", "experiments")
    
    img_void = create_cinematic_backdrop(800, 600)
    d = ImageDraw.Draw(img_void, "RGBA")
    cx, cy = 400, 300
    for r in range(180, 40, -10):
        alpha = int(220 * (1 - r / 180))
        d.ellipse([cx - r * 1.5, cy - r * 0.6, cx + r * 1.5, cy + r * 0.6], outline=(0, 255, 156, alpha), width=2)
    d.ellipse([cx - 60, cy - 60, cx + 60, cy + 60], fill=(0, 0, 0, 255), outline=(0, 200, 255, 180), width=2)
    d.text((cx - 65, cy + 180), "EXPERIMENT 01 // THE VOID", fill=(242, 242, 242, 240))
    d.text((cx - 80, cy + 205), "GRAVITATIONAL EVENT HORIZON 3D", fill=(0, 255, 156, 200))
    img_void.save(os.path.join(out_dir, "void.webp"), format="WEBP", quality=88, method=6)
    
    img_sig = create_cinematic_backdrop(800, 600)
    d = ImageDraw.Draw(img_sig, "RGBA")
    for wave_i, amp in enumerate([40, 70, 30, 90]):
        pts = []
        for x in range(60, 740, 8):
            y = int(300 + amp * math.sin((x + wave_i * 80) * 0.025) * math.cos(x * 0.008))
            pts.append((x, y))
        col = (0, 255, 156, 220) if wave_i % 2 == 0 else (0, 200, 255, 190)
        for p_idx in range(len(pts) - 1):
            d.line([pts[p_idx], pts[p_idx + 1]], fill=col, width=2)
    d.text((cx - 70, cy + 180), "EXPERIMENT 02 // THE SIGNAL", fill=(242, 242, 242, 240))
    d.text((cx - 85, cy + 205), "AUDIO-REACTIVE SHADER WAVEFORM", fill=(0, 255, 156, 200))
    img_sig.save(os.path.join(out_dir, "signal.webp"), format="WEBP", quality=88, method=6)
    
    img_vlt = create_cinematic_backdrop(800, 600)
    d = ImageDraw.Draw(img_vlt, "RGBA")
    for step in range(3):
        off = step * 35
        d.polygon([(cx, cy - 90 + off), (cx + 100, cy - 35 + off), (cx, cy + 20 + off), (cx - 100, cy - 35 + off)], outline=(0, 255, 156, 220), fill=(10, 18, 14, 120))
    d.text((cx - 70, cy + 180), "EXPERIMENT 03 // THE VAULT", fill=(242, 242, 242, 240))
    d.text((cx - 95, cy + 205), "ZERO-KNOWLEDGE AUTH PROTOCOL", fill=(0, 255, 156, 200))
    img_vlt.save(os.path.join(out_dir, "vault.webp"), format="WEBP", quality=88, method=6)

def render_footer_assets():
    print("Processing Footer Assets...")
    out_dir = os.path.join(WORKSPACE, "assets", "footer")
    
    if os.path.exists(CIPHER_RENDER):
        img = Image.open(CIPHER_RENDER).convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)
        dark = ImageEnhance.Brightness(img).enhance(0.35)
        contrast = ImageEnhance.Contrast(dark).enhance(1.4)
        contrast.save(os.path.join(out_dir, "transmission.webp"), format="WEBP", quality=88, method=6)
    else:
        img = create_cinematic_backdrop(1280, 720)
        img.save(os.path.join(out_dir, "transmission.webp"), format="WEBP", quality=88, method=6)

def render_activity_assets():
    print("Processing Activity Assets...")
    out_dir = os.path.join(WORKSPACE, "assets", "activity")
    
    city = create_cinematic_backdrop(1280, 720)
    d = ImageDraw.Draw(city, "RGBA")
    cx, cy = 640, 420
    np.random.seed(786)
    for row in range(-6, 7):
        for col in range(-12, 13):
            ix = cx + (col - row) * 28
            iy = cy + (col + row) * 14
            h_val = int(np.random.choice([10, 25, 45, 80, 140], p=[0.4, 0.25, 0.2, 0.1, 0.05]))
            
            if h_val > 100:
                top_col = (0, 255, 156, 240)
                side_col = (12, 45, 30, 220)
            elif h_val > 40:
                top_col = (0, 200, 255, 200)
                side_col = (10, 35, 38, 200)
            else:
                top_col = (45, 55, 50, 180)
                side_col = (15, 20, 18, 180)
                
            top_y = iy - h_val
            d.polygon([
                (ix, top_y - 8),
                (ix + 16, top_y),
                (ix, top_y + 8),
                (ix - 16, top_y)
            ], fill=top_col, outline=(0, 255, 156, 120))
            d.polygon([
                (ix - 16, top_y),
                (ix, top_y + 8),
                (ix, iy + 8),
                (ix - 16, iy)
            ], fill=side_col)
            d.polygon([
                (ix, top_y + 8),
                (ix + 16, top_y),
                (ix + 16, iy),
                (ix, iy + 8)
            ], fill=side_col)
            
    city.save(os.path.join(out_dir, "contribution-city.webp"), format="WEBP", quality=88, method=6)
    print(f"  -> Created {out_dir}/contribution-city.webp")

def process_projects():
    print("Processing Project Assets...")
    out_dir = os.path.join(WORKSPACE, "assets", "projects")
    
    if os.path.exists(NEXUS_RENDER):
        img = Image.open(NEXUS_RENDER).convert("RGB")
        img.save(os.path.join(out_dir, "the-3d-nexus.webp"), format="WEBP", quality=90, method=6)
        print("  -> Saved the-3d-nexus.webp")
        
    if os.path.exists(TICKET_RENDER):
        img = Image.open(TICKET_RENDER).convert("RGB")
        img.save(os.path.join(out_dir, "ticketverse.webp"), format="WEBP", quality=90, method=6)
        print("  -> Saved ticketverse.webp")
        
    render_hxnix(os.path.join(out_dir, "hxnix.webp"))
    render_hxni_express(os.path.join(out_dir, "hxni-express.webp"))
    render_hxni_finance(os.path.join(out_dir, "hxni-finance.webp"))
    render_bespoke_estore(os.path.join(out_dir, "bespoke-estore.webp"))
    render_secret_vault(os.path.join(out_dir, "secret-vault.webp"))
    render_spice_with_hassan(os.path.join(out_dir, "spice-with-hassan.webp"))

def main():
    ensure_dirs()
    process_hero()
    process_identity()
    process_projects()
    render_experiments()
    render_activity_assets()
    render_footer_assets()
    print("\nAll raster visual assets successfully synthesized!")

if __name__ == "__main__":
    main()
