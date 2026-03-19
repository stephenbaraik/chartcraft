"""
Color utilities — 16 built-in palettes, HSV/RGB/HSL converters, ColorScale.
"""

from __future__ import annotations
import colorsys
import re
from typing import List, Optional


# ---------------------------------------------------------------------------
# 16 built-in palettes
# ---------------------------------------------------------------------------

PALETTES = {
    "aurora": ["#8B5CF6", "#EC4899", "#06B6D4", "#10B981", "#F59E0B", "#EF4444", "#A78BFA", "#F472B6"],
    "sunset": ["#F97316", "#EF4444", "#EC4899", "#F59E0B", "#FB923C", "#FCA5A5", "#FDE68A", "#FBBF24"],
    "ocean": ["#0284C7", "#0EA5E9", "#38BDF8", "#06B6D4", "#0891B2", "#67E8F9", "#BAE6FD", "#7DD3FC"],
    "forest": ["#10B981", "#059669", "#34D399", "#6EE7B7", "#065F46", "#A7F3D0", "#047857", "#D1FAE5"],
    "neon": ["#00FF88", "#00D4FF", "#FF00FF", "#FFD700", "#FF4444", "#AA00FF", "#00FFFF", "#FF8C00"],
    "pastel": ["#A5B4FC", "#FCA5A5", "#6EE7B7", "#FDE68A", "#BAE6FD", "#F9A8D4", "#C4B5FD", "#FDBA74"],
    "categorical": ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1", "#FF9DA7"],
    "diverging": ["#A50026", "#D73027", "#F46D43", "#FDAE61", "#FFFFBF", "#ABD9E9", "#74ADD1", "#4575B4"],
    "midnight": ["#6366F1", "#8B5CF6", "#A78BFA", "#C084FC", "#E879F9", "#F0ABFC", "#818CF8", "#93C5FD"],
    "corporate": ["#1E40AF", "#2563EB", "#3B82F6", "#60A5FA", "#93C5FD", "#BFDBFE", "#6D28D9", "#7C3AED"],
    "minimal": ["#111827", "#374151", "#6B7280", "#9CA3AF", "#D1D5DB", "#E5E7EB", "#F3F4F6", "#F9FAFB"],
    "earth": ["#92400E", "#B45309", "#D97706", "#F59E0B", "#FCD34D", "#A3A3A3", "#6B7280", "#374151"],
    "retro": ["#E9C46A", "#F4A261", "#E76F51", "#264653", "#2A9D8F", "#A8DADC", "#457B9D", "#1D3557"],
    "candy": ["#EC4899", "#F472B6", "#F9A8D4", "#8B5CF6", "#A78BFA", "#C084FC", "#06B6D4", "#67E8F9"],
    "sequential_blues": ["#EFF3FF", "#BDD7E7", "#6BAED6", "#3182BD", "#08519C", "#08306B", "#041F4A", "#020D20"],
    "scientific": ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1", "#FF9DA7"],
}


def get_palette(name: str) -> List[str]:
    if name not in PALETTES:
        raise ValueError(f"Unknown palette '{name}'. Available: {list(PALETTES.keys())}")
    return PALETTES[name].copy()


def list_palettes() -> List[str]:
    return list(PALETTES.keys())


# ---------------------------------------------------------------------------
# Color conversion
# ---------------------------------------------------------------------------

def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def hex_to_rgb(hex_color: str) -> tuple:
    """#RRGGBB or #RRGGBBAA → (r, g, b[, a]) integers."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) == 6:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    if len(h) == 8:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4, 6))
    raise ValueError(f"Invalid hex color: {hex_color}")


def rgb_to_hex(r: int, g: int, b: int, a: Optional[int] = None) -> str:
    if a is not None:
        return f"#{r:02X}{g:02X}{b:02X}{a:02X}"
    return f"#{r:02X}{g:02X}{b:02X}"


def hex_to_hsl(hex_color: str) -> tuple:
    """Returns (h 0-360, s 0-100, l 0-100)."""
    rgb = hex_to_rgb(hex_color)
    r, g, b = (v / 255 for v in rgb[:3])
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return round(h * 360, 1), round(s * 100, 1), round(l * 100, 1)


def hsl_to_hex(h: float, s: float, l: float) -> str:
    """h 0-360, s 0-100, l 0-100 → #RRGGBB."""
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return rgb_to_hex(round(r * 255), round(g * 255), round(b * 255))


def hex_to_hsv(hex_color: str) -> tuple:
    """Returns (h 0-360, s 0-100, v 0-100)."""
    rgb = hex_to_rgb(hex_color)
    r, g, b = (v / 255 for v in rgb[:3])
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return round(h * 360, 1), round(s * 100, 1), round(v * 100, 1)


def hsv_to_hex(h: float, s: float, v: float) -> str:
    """h 0-360, s 0-100, v 0-100 → #RRGGBB."""
    r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
    return rgb_to_hex(round(r * 255), round(g * 255), round(b * 255))


# ---------------------------------------------------------------------------
# Color manipulation utilities
# ---------------------------------------------------------------------------

def lighten(hex_color: str, amount: float = 0.2) -> str:
    """Lighten a hex color by mixing with white."""
    r, g, b = hex_to_rgb(hex_color)[:3]
    r = round(r + (255 - r) * amount)
    g = round(g + (255 - g) * amount)
    b = round(b + (255 - b) * amount)
    return rgb_to_hex(r, g, b)


def darken(hex_color: str, amount: float = 0.2) -> str:
    """Darken a hex color by mixing with black."""
    r, g, b = hex_to_rgb(hex_color)[:3]
    r = round(r * (1 - amount))
    g = round(g * (1 - amount))
    b = round(b * (1 - amount))
    return rgb_to_hex(r, g, b)


def opacity(hex_color: str, alpha: float = 0.5) -> str:
    """Return rgba(...) string."""
    r, g, b = hex_to_rgb(hex_color)[:3]
    return f"rgba({r},{g},{b},{alpha})"


def auto_colors(n: int, palette: str = "aurora") -> List[str]:
    """Return n colors from the named palette (cycles if n > palette length)."""
    pal = get_palette(palette)
    if n <= len(pal):
        return pal[:n]
    # cycle
    return [pal[i % len(pal)] for i in range(n)]


# ---------------------------------------------------------------------------
# Color harmonies
# ---------------------------------------------------------------------------

def complementary(hex_color: str) -> List[str]:
    h, s, v = hex_to_hsv(hex_color)
    return [hex_color, hsv_to_hex((h + 180) % 360, s, v)]


def triadic(hex_color: str) -> List[str]:
    h, s, v = hex_to_hsv(hex_color)
    return [hsv_to_hex((h + i * 120) % 360, s, v) for i in range(3)]


def analogous(hex_color: str, steps: int = 3, angle: float = 30) -> List[str]:
    h, s, v = hex_to_hsv(hex_color)
    start = h - angle * (steps // 2)
    return [hsv_to_hex((start + i * angle) % 360, s, v) for i in range(steps)]


def split_complementary(hex_color: str) -> List[str]:
    h, s, v = hex_to_hsv(hex_color)
    return [
        hex_color,
        hsv_to_hex((h + 150) % 360, s, v),
        hsv_to_hex((h + 210) % 360, s, v),
    ]


# ---------------------------------------------------------------------------
# ColorScale — interpolates between stops
# ---------------------------------------------------------------------------

class ColorScale:
    """Multi-stop color scale with linear interpolation."""

    def __init__(self, stops: List[str]):
        if len(stops) < 2:
            raise ValueError("ColorScale requires at least 2 stops.")
        self.stops = stops

    def _lerp(self, a: int, b: int, t: float) -> int:
        return round(a + (b - a) * t)

    def at(self, t: float) -> str:
        """Return interpolated color at position t (0.0 – 1.0)."""
        t = _clamp(t)
        n = len(self.stops) - 1
        scaled = t * n
        lo = int(scaled)
        hi = min(lo + 1, n)
        frac = scaled - lo
        r1, g1, b1 = hex_to_rgb(self.stops[lo])[:3]
        r2, g2, b2 = hex_to_rgb(self.stops[hi])[:3]
        return rgb_to_hex(
            self._lerp(r1, r2, frac),
            self._lerp(g1, g2, frac),
            self._lerp(b1, b2, frac),
        )

    def generate(self, n: int) -> List[str]:
        """Return n evenly-spaced colors from the scale."""
        if n == 1:
            return [self.at(0.5)]
        return [self.at(i / (n - 1)) for i in range(n)]
