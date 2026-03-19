"""
Theme system — 11 built-in themes, custom theme support, CSS variable export.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, Optional


@dataclass
class Theme:
    name: str = "default"

    # Backgrounds
    bg: str = "#09090B"
    bg_card: str = "#18181B"
    bg_elevated: str = "#27272A"

    # Typography
    text: str = "#FAFAFA"
    text_secondary: str = "#A1A1AA"
    text_muted: str = "#71717A"

    # Accents
    accent: str = "#6366F1"
    accent_secondary: str = "#8B5CF6"

    # Semantic
    success: str = "#10B981"
    danger: str = "#EF4444"
    warning: str = "#F59E0B"

    # Structure
    border: str = "#3F3F46"
    grid: str = "#27272A"
    shadow: str = "rgba(0,0,0,0.4)"

    # Fonts
    font_display: str = "'Inter', 'Segoe UI', sans-serif"
    font_body: str = "'Inter', 'Segoe UI', sans-serif"
    font_mono: str = "'JetBrains Mono', 'Fira Code', monospace"

    # Shape / Effects
    radius: str = "10px"
    radius_sm: str = "6px"
    glass: str = "rgba(255,255,255,0.04)"
    animate: bool = True

    # Default palette name
    palette: str = "aurora"

    def to_css_vars(self) -> str:
        """Return a :root { ... } CSS block with all design tokens."""
        lines = [":root {"]
        mapping = {
            "--cc-bg": self.bg,
            "--cc-bg-card": self.bg_card,
            "--cc-bg-elevated": self.bg_elevated,
            "--cc-text": self.text,
            "--cc-text-secondary": self.text_secondary,
            "--cc-text-muted": self.text_muted,
            "--cc-accent": self.accent,
            "--cc-accent-secondary": self.accent_secondary,
            "--cc-success": self.success,
            "--cc-danger": self.danger,
            "--cc-warning": self.warning,
            "--cc-border": self.border,
            "--cc-grid": self.grid,
            "--cc-shadow": self.shadow,
            "--cc-font-display": self.font_display,
            "--cc-font-body": self.font_body,
            "--cc-font-mono": self.font_mono,
            "--cc-radius": self.radius,
            "--cc-radius-sm": self.radius_sm,
            "--cc-glass": self.glass,
        }
        for var, val in mapping.items():
            lines.append(f"  {var}: {val};")
        lines.append("}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items()}

    def to_echarts_theme(self) -> dict:
        """Return an ECharts theme object derived from this theme."""
        from chartcraft.core.colors import PALETTES
        colors = PALETTES.get(self.palette, PALETTES["aurora"])
        return {
            "color": colors,
            "backgroundColor": "transparent",
            "textStyle": {"color": self.text, "fontFamily": self.font_body},
            "title": {"textStyle": {"color": self.text, "fontFamily": self.font_display}},
            "legend": {"textStyle": {"color": self.text_secondary}},
            "tooltip": {
                "backgroundColor": self.bg_elevated,
                "borderColor": self.border,
                "textStyle": {"color": self.text},
            },
            "axisPointer": {"lineStyle": {"color": self.border}},
            "categoryAxis": {
                "axisLine": {"lineStyle": {"color": self.border}},
                "axisTick": {"lineStyle": {"color": self.border}},
                "axisLabel": {"color": self.text_muted},
                "splitLine": {"lineStyle": {"color": self.grid}},
            },
            "valueAxis": {
                "axisLine": {"lineStyle": {"color": self.border}},
                "axisLabel": {"color": self.text_muted},
                "splitLine": {"lineStyle": {"color": self.grid}},
            },
        }


# ---------------------------------------------------------------------------
# 11 built-in themes
# ---------------------------------------------------------------------------

THEMES: Dict[str, Theme] = {
    "default": Theme(
        name="default",
        bg="#09090B", bg_card="#18181B", bg_elevated="#27272A",
        text="#FAFAFA", text_secondary="#A1A1AA", text_muted="#71717A",
        accent="#6366F1", accent_secondary="#8B5CF6",
        border="#3F3F46", grid="#27272A",
        palette="aurora",
    ),
    "midnight": Theme(
        name="midnight",
        bg="#070318", bg_card="#0F0A2E", bg_elevated="#1A1040",
        text="#F0EEFF", text_secondary="#A89ECF", text_muted="#6B5FA0",
        accent="#8B5CF6", accent_secondary="#C084FC",
        border="#2D1F5E", grid="#1A1040",
        shadow="rgba(0,0,0,0.6)",
        palette="aurora",
    ),
    "obsidian": Theme(
        name="obsidian",
        bg="#0A0A0A", bg_card="#111111", bg_elevated="#1A1A1A",
        text="#F4F4F5", text_secondary="#A1A1AA", text_muted="#52525B",
        accent="#06B6D4", accent_secondary="#0EA5E9",
        border="#262626", grid="#1A1A1A",
        palette="ocean",
    ),
    "frost": Theme(
        name="frost",
        bg="#F0F4F8", bg_card="#FFFFFF", bg_elevated="#E8EFF7",
        text="#0F172A", text_secondary="#475569", text_muted="#94A3B8",
        accent="#0284C7", accent_secondary="#0369A1",
        success="#059669", danger="#DC2626", warning="#D97706",
        border="#CBD5E1", grid="#E2E8F0", shadow="rgba(0,0,0,0.08)",
        glass="rgba(255,255,255,0.6)",
        palette="ocean",
    ),
    "ember": Theme(
        name="ember",
        bg="#1A0A00", bg_card="#2A1200", bg_elevated="#3D1C00",
        text="#FFF7ED", text_secondary="#FED7AA", text_muted="#C2410C",
        accent="#F97316", accent_secondary="#FB923C",
        border="#7C2D12", grid="#3D1C00",
        palette="sunset",
    ),
    "jade": Theme(
        name="jade",
        bg="#021A0E", bg_card="#042D18", bg_elevated="#065F30",
        text="#ECFDF5", text_secondary="#A7F3D0", text_muted="#34D399",
        accent="#10B981", accent_secondary="#34D399",
        border="#065F30", grid="#042D18",
        palette="forest",
    ),
    "slate": Theme(
        name="slate",
        bg="#FFFFFF", bg_card="#F8FAFC", bg_elevated="#F1F5F9",
        text="#0F172A", text_secondary="#334155", text_muted="#64748B",
        accent="#1E40AF", accent_secondary="#3B82F6",
        success="#16A34A", danger="#DC2626", warning="#CA8A04",
        border="#E2E8F0", grid="#F1F5F9", shadow="rgba(0,0,0,0.06)",
        glass="rgba(255,255,255,0.8)",
        palette="categorical",
    ),
    "candy": Theme(
        name="candy",
        bg="#1A0015", bg_card="#2D0026", bg_elevated="#450038",
        text="#FFF0F6", text_secondary="#FBBDDA", text_muted="#F472B6",
        accent="#EC4899", accent_secondary="#F9A8D4",
        border="#831843", grid="#450038",
        palette="candy",
    ),
    "arctic": Theme(
        name="arctic",
        bg="#0B1120", bg_card="#0F172A", bg_elevated="#1E293B",
        text="#F0F9FF", text_secondary="#BAE6FD", text_muted="#7DD3FC",
        accent="#38BDF8", accent_secondary="#0EA5E9",
        border="#1E3A5F", grid="#1E293B",
        palette="ocean",
    ),
    "retro": Theme(
        name="retro",
        bg="#1D3557", bg_card="#264573", bg_elevated="#1A4A6B",
        text="#F1FAEE", text_secondary="#A8DADC", text_muted="#457B9D",
        accent="#E9C46A", accent_secondary="#F4A261",
        border="#457B9D", grid="#264573",
        palette="retro",
    ),
    "scientific": Theme(
        name="scientific",
        bg="#FAFAFA", bg_card="#FFFFFF", bg_elevated="#F5F5F5",
        text="#111827", text_secondary="#374151", text_muted="#6B7280",
        accent="#4E79A7", accent_secondary="#A0CBE8",
        success="#59A14F", danger="#E15759", warning="#F28E2B",
        border="#D1D5DB", grid="#E5E7EB", shadow="rgba(0,0,0,0.06)",
        glass="rgba(255,255,255,0.9)",
        palette="scientific",
        font_display="'Georgia', 'Times New Roman', serif",
    ),
}


def get_theme(name: str) -> Theme:
    if name not in THEMES:
        raise ValueError(f"Unknown theme '{name}'. Available: {list(THEMES.keys())}")
    return THEMES[name]


def register_theme(name: str, theme: Theme) -> None:
    """Register a custom theme."""
    theme.name = name
    THEMES[name] = theme


def list_themes() -> list:
    return list(THEMES.keys())
