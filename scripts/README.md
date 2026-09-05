# HXNI // The Cipher Stack — Generator Scripts

This directory contains the automation scripts for building and maintaining the asset system and dynamic statistics for the GitHub Profile README.

---

## 🛠️ Scripts Overview

### 1. `generate-assets.py`
Synthesizes, processes, and optimizes the visual system for the entire repository:
- Converts base renders into optimized `.webp` (<400KB per project, <1.5MB for hero).
- Generates mobile and static fallback variants (`hero-01-mobile.webp`, `hero-static.webp`).
- Compiles the looping animated 3D `cipher-core.gif`.
- Synthesizes procedural 3D project visuals and experiment lab graphics.

**Usage**:
```bash
python scripts/generate-assets.py
```

---

### 2. `generate-contributions.py`
Queries the GitHub REST / GraphQL API for user `Hxni786` and compiles:
- `assets/activity/contribution-city.svg`: 3D isometric cyber city based on contribution intensity.
- `assets/activity/activity.svg`: Real-time HUD telemetry dashboard tracking public repositories, network nodes, and language breakdown.

Includes automatic fallback telemetry when executed offline or without an API token.

**Usage**:
```bash
python scripts/generate-contributions.py
# Or with GitHub Token:
GITHUB_TOKEN=your_token python scripts/generate-contributions.py
```

---

## ⚙️ CI / CD Automation
These scripts are automatically triggered daily at midnight UTC via `.github/workflows/update-profile.yml` to keep metrics and assets fresh.
