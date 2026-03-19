# Themes & Colors

ChartCraft includes a comprehensive color system: 11 built-in themes, 16 color palettes, a professional HSV color picker, and full programmatic color control.

---

## Themes

Set the theme when creating your app:

```python
app = cc.App("Dashboard", theme="midnight")
```

Or switch themes in the browser using the ◆ Theme button in the nav bar.

### Built-in Themes

| Theme | Style | Background | Accent |
|-------|-------|------------|--------|
| `default` | Modern dark | `#09090B` | Indigo `#6366F1` |
| `midnight` | Deep purple | `#070318` | Purple `#8B5CF6` |
| `obsidian` | Pitch black | `#0A0A0A` | Cyan `#06B6D4` |
| `frost` | Clean light | `#F0F4F8` | Blue `#0284C7` |
| `ember` | Warm dark | `#1A0A00` | Orange `#F97316` |
| `jade` | Green dark | `#021A0E` | Green `#10B981` |
| `slate` | Professional light | `#FFFFFF` | Navy `#1E40AF` |
| `candy` | Pink dark | `#1A0015` | Pink `#EC4899` |
| `arctic` | Ice blue dark | `#0B1120` | Sky `#38BDF8` |
| `retro` | Vintage teal | `#1D3557` | Gold `#E9C46A` |
| `scientific` | Academic light | `#FAFAFA` | Slate `#4E79A7` |

```python
import chartcraft as cc

cc.list_themes()
# → ['default', 'midnight', 'obsidian', 'frost', 'ember', 'jade',
#    'slate', 'candy', 'arctic', 'retro', 'scientific']
```

---

## Custom Themes

Create a custom theme using `cc.Theme`:

```python
my_theme = cc.Theme(
    name="brand",
    # Backgrounds
    bg="#0A0A0A",
    bg_card="#1A1A1A",
    bg_elevated="#2A2A2A",
    # Text
    text="#FFFFFF",
    text_secondary="#A0A0A0",
    text_muted="#606060",
    # Accents
    accent="#FF6B00",
    accent_secondary="#FFB347",
    # Semantic
    success="#10B981",
    danger="#EF4444",
    warning="#F59E0B",
    # Structure
    border="#333333",
    grid="#1F1F1F",
    shadow="rgba(0,0,0,0.5)",
    # Typography
    font_display="Outfit",
    font_body="Inter",
    font_mono="JetBrains Mono",
    # Shape
    radius="12px",
    radius_sm="6px",
    # Default palette for charts
    palette="aurora",
    # Enable animations
    animate=True,
)

cc.register_theme("brand", my_theme)

app = cc.App("Dashboard", theme="brand")
```

### Theme Tokens Reference

| Token | Category | Description |
|-------|----------|-------------|
| `bg` | Background | Page background |
| `bg_card` | Background | Card/chart surface |
| `bg_elevated` | Background | Elevated surfaces, dropdowns |
| `text` | Typography | Primary text |
| `text_secondary` | Typography | Labels, secondary info |
| `text_muted` | Typography | Disabled, placeholders |
| `accent` | Accent | Primary brand color |
| `accent_secondary` | Accent | Companion accent |
| `success` | Semantic | Positive changes, "up" arrows |
| `danger` | Semantic | Negative changes, "down" arrows |
| `warning` | Semantic | Caution states |
| `border` | Structure | Card borders, dividers |
| `grid` | Structure | Chart grid lines |
| `shadow` | Structure | Box shadows |
| `font_display` | Typography | Heading font family |
| `font_body` | Typography | Body font family |
| `font_mono` | Typography | Code / data font |
| `radius` | Shape | Default border radius |
| `radius_sm` | Shape | Small border radius (badges, tags) |
| `glass` | Effects | Glassmorphism filter string |
| `animate` | Motion | Enable/disable animations globally |
| `palette` | Colors | Default chart color palette name |

---

## Color Palettes

Palettes are used as the default series colors for all chart types.

```python
import chartcraft as cc

# Use a named palette on any chart
cc.Bar(data, palette="sunset")
cc.Line(data, palette="ocean")

# Get palette colors
colors = cc.get_palette("aurora")
# → ['#6D28D9', '#8B5CF6', '#EC4899', '#06B6D4', ...]

# List all palette names
cc.list_palettes()
```

### Built-in Palettes

| Palette | Description |
|---------|-------------|
| `aurora` | Vibrant purples and pinks — the default |
| `sunset` | Warm reds, oranges, and yellows |
| `ocean` | Cool blues and cyan |
| `forest` | Natural greens |
| `neon` | Electric neon colors |
| `pastel` | Soft, muted pastels |
| `categorical` | 8 distinct colors for categorical data |
| `diverging` | Red → neutral → blue (for diverging scales) |
| `midnight` | Deep purple and violet scale |
| `corporate` | Professional blues and grays |
| `minimal` | Grayscale |
| `earth` | Browns, tans, warm neutrals |
| `retro` | Vintage 1970s palette |
| `candy` | Pink, purple, magenta |
| `sequential_blues` | Light to dark blue scale |
| `scientific` | Publication-ready colors (Tableau-inspired) |

---

## Per-Chart Colors

Override the theme palette with custom colors on any individual chart:

```python
# Custom hex colors
cc.Bar(data, colors=["#6366F1", "#EC4899", "#22D3EE"])

# Named palette
cc.Line(data, palette="sunset")

# Colors map to series in order
cc.Line(
    data,
    y=["revenue", "cost", "profit"],
    colors=["#10B981", "#EF4444", "#6366F1"],  # green, red, blue
)
```

---

## Color Utilities

### Lighten & Darken

```python
cc.lighten("#6366F1", 0.3)       # → lighter shade by 30%
cc.darken("#6366F1", 0.3)        # → darker shade by 30%
```

### Opacity

```python
cc.opacity("#6366F1", 0.5)       # → "rgba(99,102,241,0.5)"
cc.opacity("#6366F1", 0.0)       # → fully transparent
```

### Color Harmonies

Generate harmonious color combinations from any starting color:

```python
cc.complementary("#6366F1")
# → ["#6366F1", "#91631B"]            # 2 opposite colors

cc.triadic("#6366F1")
# → ["#6366F1", "#F163BB", "#63F163"] # 3 evenly spaced

cc.analogous("#6366F1", steps=4)
# → 4 colors within 30° of each other

cc.split_complementary("#6366F1")
# → 3 colors: original + two near-complements
```

### Auto Colors

Generate N colors automatically cycled from a palette:

```python
cc.auto_colors(5)                       # 5 from default palette
cc.auto_colors(5, palette="sunset")     # 5 from sunset palette
# → ["#F97316", "#FB923C", "#FBBF24", "#EF4444", "#DC2626"]
```

### ColorScale

Interpolate between color stops for continuous scales:

```python
scale = cc.ColorScale(["#0F0F23", "#4F46E5", "#818CF8"])

scale.at(0.0)      # → "#0F0F23" (start)
scale.at(0.5)      # → "#4F46E5" (midpoint)
scale.at(1.0)      # → "#818CF8" (end)

scale.generate(10)  # → 10 evenly-spaced interpolated colors
```

Use with Heatmaps:

```python
cc.Heatmap(
    data,
    color_scale=cc.ColorScale(["#0F172A", "#6366F1", "#F9FAFB"]).generate(5),
)
```

---

## Color Picker (Visual Builder)

When using the visual builder at `/builder`, every color property opens a professional HSV color picker with:

- **Hue wheel** — circular ring for selecting hue (0–360°)
- **SV square** — saturation and brightness picker
- **Alpha slider** — transparency control
- **Hex input** — type any `#RRGGBB` or `#RRGGBBAA` value
- **RGB/HSL sliders** — bidirectionally synced with the wheel
- **EyeDropper** — sample any color on screen (Chromium only)
- **Palettes tab** — one-click access to all 16 ChartCraft palettes
- **Harmonies tab** — auto-generate complementary/triadic/analogous/split sets
- **Gradient editor** — create multi-stop gradients for area fills

Colors selected in the builder are written to the generated Python code:

```python
cc.Bar(data, colors=["#6366F1", "#EC4899", "#22D3EE"])
```

---

## CSS Variables

ChartCraft renders all theme tokens as CSS custom properties. You can reference them in custom HTML or TextBlock content:

```css
color: var(--cc-accent);
background: var(--cc-bg-card);
border-color: var(--cc-border);
```

| CSS Variable | Theme Token |
|-------------|-------------|
| `--cc-bg` | `bg` |
| `--cc-bg-card` | `bg_card` |
| `--cc-bg-elevated` | `bg_elevated` |
| `--cc-text` | `text` |
| `--cc-text-secondary` | `text_secondary` |
| `--cc-text-muted` | `text_muted` |
| `--cc-accent` | `accent` |
| `--cc-accent-secondary` | `accent_secondary` |
| `--cc-success` | `success` |
| `--cc-danger` | `danger` |
| `--cc-warning` | `warning` |
| `--cc-border` | `border` |
