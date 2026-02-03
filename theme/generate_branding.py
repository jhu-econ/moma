#!/usr/bin/env python
"""Generate MoMa logo and favicon.

This script creates the branding assets for the MoMa course website:
- logo.svg and logo.png: Full "[MoMa]" logo with transparent background
- favicon.png: Square "[M]" icon with cream background

Colors:
- JHU Heritage Blue: #002D72
- Accent Orange: #E87722
- Favicon Background: #FDF8F0 (cream)

Font: Fira Sans Regular (install via: https://github.com/mozilla/Fira)

Usage:
    uv run python theme/generate_branding.py
"""

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

# Colors
JHU_BLUE = "#002D72"
ACCENT_ORANGE = "#E87722"
CREAM = "#FDF8F0"

# Output directory (same as script location)
OUTPUT_DIR = Path(__file__).parent


def get_fira_sans():
    """Load Fira Sans Regular font, with fallback to DejaVu Sans."""
    fira_paths = [
        Path.home() / ".local/share/fonts/FiraSans-Regular.ttf",
        Path("/usr/share/fonts/truetype/fira/FiraSans-Regular.ttf"),
    ]
    for path in fira_paths:
        if path.exists():
            fm.fontManager.addfont(str(path))
            return fm.FontProperties(fname=str(path))
    print("Warning: Fira Sans not found, using DejaVu Sans")
    return fm.FontProperties(family="DejaVu Sans")


def generate_logo(font_props):
    """Generate the full [MoMa] logo."""
    fig, ax = plt.subplots(figsize=(3.5, 1.2), facecolor="none")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    ax.text(
        1.2, 2, "[",
        fontsize=52,
        color=ACCENT_ORANGE,
        fontproperties=font_props,
        va="center",
        ha="center",
    )
    ax.text(
        5, 2, "MoMa",
        fontsize=44,
        color=JHU_BLUE,
        fontproperties=font_props,
        va="center",
        ha="center",
    )
    ax.text(
        8.8, 2, "]",
        fontsize=52,
        color=ACCENT_ORANGE,
        fontproperties=font_props,
        va="center",
        ha="center",
    )

    plt.savefig(
        OUTPUT_DIR / "logo.png",
        dpi=200,
        bbox_inches="tight",
        pad_inches=0.1,
        transparent=True,
    )
    plt.savefig(
        OUTPUT_DIR / "logo.svg",
        bbox_inches="tight",
        pad_inches=0.1,
        transparent=True,
    )
    plt.close()
    print(f"Created: {OUTPUT_DIR / 'logo.png'}")
    print(f"Created: {OUTPUT_DIR / 'logo.svg'}")


def generate_favicon(font_props):
    """Generate the [M] favicon with cream background."""
    fig, ax = plt.subplots(figsize=(1.5, 1.5), facecolor=CREAM)
    ax.set_facecolor(CREAM)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")

    lw = 7  # bracket line width

    # Left bracket [
    ax.plot([15, 28], [82, 82], color=ACCENT_ORANGE, linewidth=lw, solid_capstyle="butt")
    ax.plot([15, 15], [82, 18], color=ACCENT_ORANGE, linewidth=lw, solid_capstyle="butt")
    ax.plot([15, 28], [18, 18], color=ACCENT_ORANGE, linewidth=lw, solid_capstyle="butt")

    # Right bracket ]
    ax.plot([72, 85], [82, 82], color=ACCENT_ORANGE, linewidth=lw, solid_capstyle="butt")
    ax.plot([85, 85], [82, 18], color=ACCENT_ORANGE, linewidth=lw, solid_capstyle="butt")
    ax.plot([72, 85], [18, 18], color=ACCENT_ORANGE, linewidth=lw, solid_capstyle="butt")

    # M in center
    ax.text(
        50, 50, "M",
        fontsize=52,
        color=JHU_BLUE,
        fontproperties=font_props,
        va="center",
        ha="center",
    )

    plt.savefig(
        OUTPUT_DIR / "favicon.png",
        dpi=64,
        facecolor=CREAM,
        bbox_inches="tight",
        pad_inches=0.02,
    )
    plt.close()
    print(f"Created: {OUTPUT_DIR / 'favicon.png'}")


def main():
    """Generate all branding assets."""
    print("Generating MoMa branding assets...")
    font_props = get_fira_sans()
    generate_logo(font_props)
    generate_favicon(font_props)
    print("Done!")


if __name__ == "__main__":
    main()
