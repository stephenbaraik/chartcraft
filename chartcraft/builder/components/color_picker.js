/**
 * ChartCraft Color Picker — Phase 3
 * Self-contained HSV color picker with:
 *   - HSV wheel (canvas) with saturation/value square
 *   - Hex / RGB / HSL bidirectional inputs
 *   - EyeDropper API integration
 *   - 16-palette ChartCraft swatches
 *   - Gradient editor (multi-stop)
 *   - Color harmonies (complementary, triadic, analogous)
 *   - Recent colors (localStorage, last 8)
 *
 * Usage:
 *   const picker = new CCColorPicker(anchorEl, {
 *     value: '#8B5CF6',
 *     onChange: (hex) => { ... },
 *     showGradient: false,
 *   });
 *   picker.open();
 *   picker.destroy();
 */

'use strict';

// ─── Color math ──────────────────────────────────────────────────────────────

function hexToRgb(hex) {
  hex = hex.replace(/^#/, '');
  if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
  const n = parseInt(hex, 16);
  return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 };
}

function rgbToHex({ r, g, b }) {
  return '#' + [r, g, b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
}

function rgbToHsv({ r, g, b }) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  const d = max - min;
  let h = 0, s = max === 0 ? 0 : d / max, v = max;
  if (d !== 0) {
    if (max === r) h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
    else if (max === g) h = ((b - r) / d + 2) / 6;
    else h = ((r - g) / d + 4) / 6;
  }
  return { h: h * 360, s, v };
}

function hsvToRgb({ h, s, v }) {
  h = ((h % 360) + 360) % 360;
  const i = Math.floor(h / 60), f = h / 60 - i;
  const p = v * (1 - s), q = v * (1 - f * s), t = v * (1 - (1 - f) * s);
  const [r, g, b] = [
    [v, t, p, p, q, v],
    [q, v, v, t, p, p],
    [p, p, q, v, v, t],
  ].map(ch => ch[i % 6]);
  return { r: Math.round(r * 255), g: Math.round(g * 255), b: Math.round(b * 255) };
}

function rgbToHsl({ r, g, b }) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  const l = (max + min) / 2;
  if (max === min) return { h: 0, s: 0, l: Math.round(l * 100) };
  const d = max - min;
  const s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
  let h = 0;
  if (max === r) h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
  else if (max === g) h = ((b - r) / d + 2) / 6;
  else h = ((r - g) / d + 4) / 6;
  return { h: Math.round(h * 360), s: Math.round(s * 100), l: Math.round(l * 100) };
}

function hslToRgb({ h, s, l }) {
  s /= 100; l /= 100;
  const a = s * Math.min(l, 1 - l);
  const f = n => {
    const k = (n + h / 30) % 12;
    return l - a * Math.max(-1, Math.min(k - 3, 9 - k, 1));
  };
  return { r: Math.round(f(0) * 255), g: Math.round(f(8) * 255), b: Math.round(f(4) * 255) };
}

function harmonies(hex) {
  const rgb = hexToRgb(hex);
  const { h, s, v } = rgbToHsv(rgb);
  return {
    complementary: [hex, rgbToHex(hsvToRgb({ h: h + 180, s, v }))],
    triadic: [hex, rgbToHex(hsvToRgb({ h: h + 120, s, v })), rgbToHex(hsvToRgb({ h: h + 240, s, v }))],
    analogous: [
      rgbToHex(hsvToRgb({ h: h - 30, s, v })), hex,
      rgbToHex(hsvToRgb({ h: h + 30, s, v })),
    ],
    split: [
      hex,
      rgbToHex(hsvToRgb({ h: h + 150, s, v })),
      rgbToHex(hsvToRgb({ h: h + 210, s, v })),
    ],
    tetradic: [
      hex,
      rgbToHex(hsvToRgb({ h: h + 90, s, v })),
      rgbToHex(hsvToRgb({ h: h + 180, s, v })),
      rgbToHex(hsvToRgb({ h: h + 270, s, v })),
    ],
  };
}

// ─── ChartCraft palettes (16) ─────────────────────────────────────────────────

const CC_PALETTES = {
  aurora:      ['#8B5CF6','#6366F1','#3B82F6','#06B6D4','#10B981'],
  sunset:      ['#F59E0B','#EF4444','#EC4899','#8B5CF6','#6366F1'],
  ocean:       ['#06B6D4','#0EA5E9','#3B82F6','#6366F1','#8B5CF6'],
  forest:      ['#10B981','#34D399','#6EE7B7','#059669','#047857'],
  neon:        ['#F0FF00','#00FFF0','#FF00F0','#00FF7F','#FF7F00'],
  pastel:      ['#FCA5A5','#FCD34D','#86EFAC','#93C5FD','#D8B4FE'],
  corporate:   ['#1E3A5F','#2E86AB','#A8DADC','#457B9D','#1D3557'],
  warm:        ['#DC2626','#EA580C','#D97706','#CA8A04','#65A30D'],
  cool:        ['#0369A1','#0891B2','#0D9488','#059669','#16A34A'],
  monochrome:  ['#F9FAFB','#D1D5DB','#9CA3AF','#4B5563','#111827'],
  categorical: ['#3B82F6','#EF4444','#10B981','#F59E0B','#8B5CF6','#EC4899','#06B6D4','#84CC16'],
  diverging:   ['#DC2626','#EF4444','#FCA5A5','#E5E7EB','#93C5FD','#3B82F6','#1D4ED8'],
  sequential:  ['#EFF6FF','#BFDBFE','#93C5FD','#60A5FA','#3B82F6','#2563EB','#1E3A8A'],
  earth:       ['#92400E','#B45309','#D97706','#F59E0B','#78716C','#57534E'],
  candy:       ['#F472B6','#FB7185','#FCD34D','#34D399','#60A5FA','#A78BFA'],
  retro:       ['#FF6B6B','#FFE66D','#4ECDC4','#45B7D1','#96CEB4','#FFEAA7'],
};

// ─── Recent colors ────────────────────────────────────────────────────────────

const RECENT_KEY = 'cc_recent_colors';
function getRecent() {
  try { return JSON.parse(localStorage.getItem(RECENT_KEY) || '[]'); } catch { return []; }
}
function addRecent(hex) {
  let recent = getRecent().filter(c => c !== hex);
  recent.unshift(hex);
  if (recent.length > 8) recent = recent.slice(0, 8);
  try { localStorage.setItem(RECENT_KEY, JSON.stringify(recent)); } catch {}
}

// ─── CSS ──────────────────────────────────────────────────────────────────────

const PICKER_CSS = `
.cc-picker-overlay {
  position: fixed; inset: 0; z-index: 99998;
  background: transparent;
}
.cc-picker {
  position: fixed;
  z-index: 99999;
  width: 300px;
  background: #1C1C27;
  border: 1px solid #2D2D3F;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.6);
  font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
  font-size: 12px;
  color: #E4E4F0;
  overflow: hidden;
  user-select: none;
}
.cc-picker-tabs {
  display: flex;
  border-bottom: 1px solid #2D2D3F;
}
.cc-picker-tab {
  flex: 1;
  padding: 8px 4px;
  text-align: center;
  cursor: pointer;
  color: #9999BB;
  font-size: 11px;
  font-weight: 500;
  transition: color 0.15s, background 0.15s;
  border-bottom: 2px solid transparent;
}
.cc-picker-tab:hover { color: #E4E4F0; background: #23233A; }
.cc-picker-tab.active { color: #8B5CF6; border-bottom-color: #8B5CF6; }
.cc-picker-panel { display: none; padding: 12px; }
.cc-picker-panel.active { display: block; }

/* HSV Wheel */
.cc-wheel-wrap {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto 12px;
}
.cc-wheel-wrap canvas { position: absolute; top: 0; left: 0; cursor: crosshair; }
.cc-wheel-cursor {
  position: absolute;
  width: 14px; height: 14px;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.6);
  transform: translate(-50%,-50%);
  pointer-events: none;
  z-index: 2;
}

/* SV Square */
.cc-sv-wrap {
  position: relative;
  width: 160px;
  height: 100px;
  margin: 0 auto 10px;
  border-radius: 6px;
  overflow: hidden;
  cursor: crosshair;
}
.cc-sv-cursor {
  position: absolute;
  width: 12px; height: 12px;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.5);
  transform: translate(-50%,-50%);
  pointer-events: none;
}

/* Hue + Alpha sliders */
.cc-slider-row { margin-bottom: 8px; }
.cc-slider-label { font-size: 10px; color: #9999BB; margin-bottom: 2px; }
.cc-hue-track, .cc-alpha-track {
  width: 100%;
  height: 14px;
  border-radius: 7px;
  position: relative;
  cursor: pointer;
}
.cc-hue-track {
  background: linear-gradient(to right,
    hsl(0,100%,50%),hsl(30,100%,50%),hsl(60,100%,50%),
    hsl(90,100%,50%),hsl(120,100%,50%),hsl(150,100%,50%),
    hsl(180,100%,50%),hsl(210,100%,50%),hsl(240,100%,50%),
    hsl(270,100%,50%),hsl(300,100%,50%),hsl(330,100%,50%),hsl(360,100%,50%));
}
.cc-slider-thumb {
  position: absolute;
  top: 50%; transform: translate(-50%,-50%);
  width: 18px; height: 18px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.5), 0 0 0 1.5px rgba(255,255,255,0.4);
  cursor: grab;
}
.cc-slider-thumb:active { cursor: grabbing; }

/* Hex/RGB/HSL inputs */
.cc-input-row { display: flex; gap: 4px; margin-bottom: 8px; }
.cc-input-group { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 2px; }
.cc-input-group input {
  width: 100%; box-sizing: border-box;
  background: #0F0F1A; border: 1px solid #2D2D3F; border-radius: 4px;
  color: #E4E4F0; font-size: 11px; font-family: monospace;
  padding: 3px 4px; text-align: center;
  outline: none; transition: border-color 0.15s;
}
.cc-input-group input:focus { border-color: #8B5CF6; }
.cc-input-group label { font-size: 10px; color: #9999BB; }
.cc-hex-input { width: 80px; }

/* Color preview */
.cc-preview-row {
  display: flex; gap: 8px; align-items: center; margin-bottom: 12px;
}
.cc-preview-swatch {
  width: 40px; height: 40px;
  border-radius: 6px;
  border: 1px solid #2D2D3F;
  background-image: linear-gradient(45deg,#555 25%,transparent 25%),
    linear-gradient(-45deg,#555 25%,transparent 25%),
    linear-gradient(45deg,transparent 75%,#555 75%),
    linear-gradient(-45deg,transparent 75%,#555 75%);
  background-size: 10px 10px;
  background-position: 0 0, 0 5px, 5px -5px, -5px 0;
  position: relative;
  flex-shrink: 0;
}
.cc-preview-fill {
  position: absolute; inset: 0; border-radius: 6px;
}
.cc-preview-hex {
  flex: 1; font-size: 14px; font-weight: 600;
  color: #E4E4F0; font-family: monospace;
  background: #0F0F1A; border: 1px solid #2D2D3F; border-radius: 6px;
  padding: 6px 8px; outline: none;
}
.cc-preview-hex:focus { border-color: #8B5CF6; }
.cc-eyedropper-btn {
  background: #23233A; border: 1px solid #2D2D3F; border-radius: 6px;
  color: #9999BB; cursor: pointer; padding: 6px 8px;
  font-size: 16px; line-height: 1; transition: color 0.15s, background 0.15s;
}
.cc-eyedropper-btn:hover { color: #E4E4F0; background: #2D2D3F; }

/* Swatches */
.cc-swatch-grid {
  display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 8px;
}
.cc-swatch {
  width: 22px; height: 22px; border-radius: 4px; cursor: pointer;
  border: 1px solid rgba(255,255,255,0.08);
  transition: transform 0.1s, box-shadow 0.1s;
}
.cc-swatch:hover { transform: scale(1.2); box-shadow: 0 2px 8px rgba(0,0,0,0.4); }
.cc-palette-select {
  width: 100%; background: #0F0F1A; border: 1px solid #2D2D3F;
  border-radius: 4px; color: #E4E4F0; font-size: 11px; padding: 4px 6px;
  outline: none; margin-bottom: 8px; cursor: pointer;
}
.cc-section-label {
  font-size: 10px; font-weight: 600; color: #9999BB;
  text-transform: uppercase; letter-spacing: 0.05em;
  margin: 10px 0 6px;
}

/* Harmonies */
.cc-harmony-row { display: flex; gap: 4px; margin-bottom: 4px; align-items: center; }
.cc-harmony-label { font-size: 10px; color: #9999BB; width: 90px; flex-shrink: 0; }
.cc-harmony-swatch {
  width: 18px; height: 18px; border-radius: 3px; cursor: pointer;
  border: 1px solid rgba(255,255,255,0.1);
  transition: transform 0.1s;
}
.cc-harmony-swatch:hover { transform: scale(1.2); }

/* Gradient editor */
.cc-gradient-track {
  width: 100%; height: 20px; border-radius: 6px;
  position: relative; cursor: crosshair;
  border: 1px solid #2D2D3F;
  margin-bottom: 8px;
}
.cc-gradient-stop {
  position: absolute; top: 50%;
  transform: translate(-50%,-50%);
  width: 16px; height: 24px;
  background: #1C1C27; border: 1px solid #9999BB;
  border-radius: 3px; cursor: pointer;
}
.cc-gradient-stop.active { border-color: #8B5CF6; }
.cc-gradient-stop-color {
  position: absolute; inset: 2px; border-radius: 2px;
}
.cc-gradient-add-btn, .cc-gradient-del-btn {
  background: #23233A; border: 1px solid #2D2D3F; border-radius: 4px;
  color: #9999BB; cursor: pointer; padding: 3px 8px; font-size: 11px;
  margin-right: 4px; transition: color 0.15s;
}
.cc-gradient-add-btn:hover, .cc-gradient-del-btn:hover { color: #E4E4F0; }
.cc-gradient-actions { display: flex; gap: 4px; margin-bottom: 8px; }
.cc-gradient-type {
  flex: 1; background: #0F0F1A; border: 1px solid #2D2D3F;
  border-radius: 4px; color: #E4E4F0; font-size: 11px; padding: 3px 6px;
  outline: none; cursor: pointer;
}

/* Apply / Cancel */
.cc-picker-actions {
  display: flex; gap: 8px; padding: 10px 12px;
  border-top: 1px solid #2D2D3F;
}
.cc-btn {
  flex: 1; padding: 7px; border-radius: 6px;
  font-size: 12px; font-weight: 600; cursor: pointer;
  border: none; transition: opacity 0.15s;
}
.cc-btn:hover { opacity: 0.85; }
.cc-btn-apply { background: #8B5CF6; color: #fff; }
.cc-btn-cancel { background: #23233A; color: #9999BB; border: 1px solid #2D2D3F; }
`;

// ─── Inject CSS once ──────────────────────────────────────────────────────────

let _cssInjected = false;
function injectCSS() {
  if (_cssInjected) return;
  const s = document.createElement('style');
  s.textContent = PICKER_CSS;
  document.head.appendChild(s);
  _cssInjected = true;
}

// ─── CCColorPicker class ──────────────────────────────────────────────────────

class CCColorPicker {
  /**
   * @param {HTMLElement} anchor - element to position the picker near
   * @param {Object} opts
   * @param {string}   opts.value       - initial hex color
   * @param {Function} opts.onChange    - called with hex string on change
   * @param {Function} opts.onApply     - called with hex string when Apply is clicked
   * @param {boolean}  opts.showGradient - show gradient editor tab
   * @param {boolean}  opts.showHarmonies - show harmonies tab
   */
  constructor(anchor, opts = {}) {
    injectCSS();
    this.anchor = anchor;
    this.opts = { showGradient: true, showHarmonies: true, ...opts };
    this.hsv = { h: 0, s: 1, v: 1 };
    this.alpha = 1;
    this.hex = '#FF0000';
    this.gradientStops = [
      { pos: 0, color: '#8B5CF6' },
      { pos: 1, color: '#EC4899' },
    ];
    this.activeStop = 0;
    this._el = null;
    this._overlay = null;
    this._rafId = null;
    this._activeTab = 'wheel';
    this._openPickerTab = null;

    if (opts.value) this._setHex(opts.value, false);
  }

  // ── Public ──────────────────────────────────────────────────────────────────

  open() {
    if (this._el) return;
    this._render();
    this._position();
    this._bindEvents();
    this._drawWheel();
    this._drawSV();
    this._updateAllUI();
  }

  close() {
    if (!this._el) return;
    this._overlay?.remove();
    this._el?.remove();
    this._overlay = null;
    this._el = null;
  }

  destroy() { this.close(); }

  getValue() { return this.hex; }

  setValue(hex) {
    this._setHex(hex, false);
    if (this._el) this._updateAllUI();
  }

  // ── Internal: state ─────────────────────────────────────────────────────────

  _setHex(hex, notify = true) {
    if (!/^#[0-9A-Fa-f]{3,8}$/.test(hex)) return;
    if (hex.length === 4) hex = '#' + hex.slice(1).split('').map(c => c + c).join('');
    this.hex = hex.slice(0, 7).toLowerCase();
    const rgb = hexToRgb(this.hex);
    this.hsv = rgbToHsv(rgb);
    if (notify && this.opts.onChange) this.opts.onChange(this.hex);
  }

  _setHSV(h, s, v, notify = true) {
    this.hsv = {
      h: ((h % 360) + 360) % 360,
      s: Math.max(0, Math.min(1, s)),
      v: Math.max(0, Math.min(1, v)),
    };
    this.hex = rgbToHex(hsvToRgb(this.hsv));
    if (notify && this.opts.onChange) this.opts.onChange(this.hex);
  }

  // ── Internal: render ────────────────────────────────────────────────────────

  _render() {
    const overlay = document.createElement('div');
    overlay.className = 'cc-picker-overlay';
    document.body.appendChild(overlay);
    this._overlay = overlay;

    const el = document.createElement('div');
    el.className = 'cc-picker';
    el.innerHTML = this._html();
    document.body.appendChild(el);
    this._el = el;
  }

  _html() {
    const tabs = [
      { id: 'wheel', label: 'Wheel' },
      { id: 'sliders', label: 'Sliders' },
      { id: 'palettes', label: 'Palettes' },
      ...(this.opts.showHarmonies ? [{ id: 'harmonies', label: 'Harmonies' }] : []),
      ...(this.opts.showGradient  ? [{ id: 'gradient',  label: 'Gradient'  }] : []),
    ];
    return `
      <div class="cc-picker-tabs">
        ${tabs.map(t => `<div class="cc-picker-tab${t.id === this._activeTab ? ' active' : ''}" data-tab="${t.id}">${t.label}</div>`).join('')}
      </div>

      <!-- Wheel tab -->
      <div class="cc-picker-panel${this._activeTab === 'wheel' ? ' active' : ''}" id="cc-panel-wheel">
        <div class="cc-wheel-wrap">
          <canvas id="cc-hue-wheel" width="200" height="200"></canvas>
          <div class="cc-wheel-cursor" id="cc-wheel-cursor"></div>
        </div>
        <div class="cc-sv-wrap" id="cc-sv-wrap">
          <canvas id="cc-sv-canvas" width="160" height="100"></canvas>
          <div class="cc-sv-cursor" id="cc-sv-cursor"></div>
        </div>
        ${this._previewHTML()}
        ${this._inputRowHTML()}
      </div>

      <!-- Sliders tab -->
      <div class="cc-picker-panel${this._activeTab === 'sliders' ? ' active' : ''}" id="cc-panel-sliders">
        <div class="cc-slider-row">
          <div class="cc-slider-label">Hue</div>
          <div class="cc-hue-track" id="cc-hue-track"><div class="cc-slider-thumb" id="cc-hue-thumb"></div></div>
        </div>
        <div class="cc-slider-row">
          <div class="cc-slider-label">Saturation</div>
          <div class="cc-hue-track" id="cc-sat-track" style="background:linear-gradient(to right,#fff,hsl(${this.hsv.h},100%,50%))">
            <div class="cc-slider-thumb" id="cc-sat-thumb"></div>
          </div>
        </div>
        <div class="cc-slider-row">
          <div class="cc-slider-label">Value / Brightness</div>
          <div class="cc-hue-track" id="cc-val-track" style="background:linear-gradient(to right,#000,hsl(${this.hsv.h},100%,50%))">
            <div class="cc-slider-thumb" id="cc-val-thumb"></div>
          </div>
        </div>
        <div class="cc-slider-row">
          <div class="cc-slider-label">Alpha</div>
          <div class="cc-alpha-track" id="cc-alpha-track"
            style="background:linear-gradient(to right,transparent,${this.hex});background-color:#fff">
            <div class="cc-slider-thumb" id="cc-alpha-thumb"></div>
          </div>
        </div>
        ${this._previewHTML()}
        ${this._inputRowHTML()}
      </div>

      <!-- Palettes tab -->
      <div class="cc-picker-panel${this._activeTab === 'palettes' ? ' active' : ''}" id="cc-panel-palettes">
        <select class="cc-palette-select" id="cc-palette-select">
          ${Object.keys(CC_PALETTES).map(k => `<option value="${k}">${k.charAt(0).toUpperCase() + k.slice(1)}</option>`).join('')}
        </select>
        <div class="cc-swatch-grid" id="cc-palette-swatches"></div>
        <div class="cc-section-label">Recent</div>
        <div class="cc-swatch-grid" id="cc-recent-swatches"></div>
        ${this._previewHTML()}
        ${this._inputRowHTML()}
      </div>

      <!-- Harmonies tab -->
      ${this.opts.showHarmonies ? `
      <div class="cc-picker-panel${this._activeTab === 'harmonies' ? ' active' : ''}" id="cc-panel-harmonies">
        <div id="cc-harmony-rows"></div>
        ${this._previewHTML()}
        ${this._inputRowHTML()}
      </div>` : ''}

      <!-- Gradient tab -->
      ${this.opts.showGradient ? `
      <div class="cc-picker-panel${this._activeTab === 'gradient' ? ' active' : ''}" id="cc-panel-gradient">
        <div class="cc-section-label">Gradient Preview</div>
        <div class="cc-gradient-track" id="cc-gradient-track">
          <div id="cc-gradient-fill" style="position:absolute;inset:0;border-radius:5px;"></div>
        </div>
        <div class="cc-gradient-actions">
          <select class="cc-gradient-type" id="cc-gradient-type">
            <option value="linear">Linear</option>
            <option value="radial">Radial</option>
          </select>
          <button class="cc-gradient-add-btn" id="cc-gradient-add">+ Stop</button>
          <button class="cc-gradient-del-btn" id="cc-gradient-del">Del</button>
        </div>
        <div id="cc-gradient-stops-list" style="font-size:11px;color:#9999BB;margin-bottom:8px;">
          Select a stop then pick its color below.
        </div>
        ${this._previewHTML()}
        ${this._inputRowHTML()}
      </div>` : ''}

      <div class="cc-picker-actions">
        <button class="cc-btn cc-btn-cancel" id="cc-btn-cancel">Cancel</button>
        <button class="cc-btn cc-btn-apply" id="cc-btn-apply">Apply</button>
      </div>
    `;
  }

  _previewHTML() {
    return `
      <div class="cc-preview-row">
        <div class="cc-preview-swatch">
          <div class="cc-preview-fill" id="cc-preview-fill" style="background:${this.hex}"></div>
        </div>
        <input class="cc-preview-hex" id="cc-preview-hex" value="${this.hex}" maxlength="7" spellcheck="false"/>
        ${window.EyeDropper ? `<button class="cc-eyedropper-btn" id="cc-eyedropper" title="Pick from screen">&#x1F4A7;</button>` : ''}
      </div>
    `;
  }

  _inputRowHTML() {
    const rgb = hexToRgb(this.hex);
    const hsl = rgbToHsl(rgb);
    return `
      <div class="cc-input-row">
        <div class="cc-input-group">
          <input id="cc-inp-r" type="number" min="0" max="255" value="${rgb.r}">
          <label>R</label>
        </div>
        <div class="cc-input-group">
          <input id="cc-inp-g" type="number" min="0" max="255" value="${rgb.g}">
          <label>G</label>
        </div>
        <div class="cc-input-group">
          <input id="cc-inp-b" type="number" min="0" max="255" value="${rgb.b}">
          <label>B</label>
        </div>
        <div class="cc-input-group">
          <input id="cc-inp-h" type="number" min="0" max="359" value="${hsl.h}">
          <label>H</label>
        </div>
        <div class="cc-input-group">
          <input id="cc-inp-s" type="number" min="0" max="100" value="${hsl.s}">
          <label>S%</label>
        </div>
        <div class="cc-input-group">
          <input id="cc-inp-l" type="number" min="0" max="100" value="${hsl.l}">
          <label>L%</label>
        </div>
      </div>
    `;
  }

  // ── Internal: drawing ───────────────────────────────────────────────────────

  _drawWheel() {
    const canvas = this._el.querySelector('#cc-hue-wheel');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const cx = 100, cy = 100, outerR = 96, innerR = 72;
    ctx.clearRect(0, 0, 200, 200);
    for (let angle = 0; angle < 360; angle++) {
      const start = (angle - 1) * Math.PI / 180;
      const end   = (angle + 1) * Math.PI / 180;
      const grad = ctx.createLinearGradient(
        cx + outerR * Math.cos(start), cy + outerR * Math.sin(start),
        cx + outerR * Math.cos(end),   cy + outerR * Math.sin(end)
      );
      grad.addColorStop(0, `hsl(${angle},100%,50%)`);
      grad.addColorStop(1, `hsl(${angle+1},100%,50%)`);
      ctx.beginPath();
      ctx.moveTo(cx + innerR * Math.cos(start), cy + innerR * Math.sin(start));
      ctx.arc(cx, cy, outerR, start, end);
      ctx.arc(cx, cy, innerR, end, start, true);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();
    }
  }

  _drawSV() {
    const canvas = this._el.querySelector('#cc-sv-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = 160, H = 100;
    const hueColor = `hsl(${this.hsv.h},100%,50%)`;
    // White → Hue
    const gradH = ctx.createLinearGradient(0, 0, W, 0);
    gradH.addColorStop(0, '#fff');
    gradH.addColorStop(1, hueColor);
    ctx.fillStyle = gradH;
    ctx.fillRect(0, 0, W, H);
    // Transparent → Black
    const gradV = ctx.createLinearGradient(0, 0, 0, H);
    gradV.addColorStop(0, 'rgba(0,0,0,0)');
    gradV.addColorStop(1, '#000');
    ctx.fillStyle = gradV;
    ctx.fillRect(0, 0, W, H);
  }

  // ── Internal: UI update ─────────────────────────────────────────────────────

  _updateAllUI() {
    if (!this._el) return;
    const el = this._el;
    const hex = this.hex;
    const rgb = hexToRgb(hex);
    const hsl = rgbToHsl(rgb);

    // Preview swatches & hex inputs (multiple per panel)
    el.querySelectorAll('.cc-preview-fill').forEach(e => e.style.background = hex);
    el.querySelectorAll('.cc-preview-hex').forEach(e => { if (document.activeElement !== e) e.value = hex; });
    el.querySelectorAll('#cc-inp-r').forEach(e => { if (document.activeElement !== e) e.value = rgb.r; });
    el.querySelectorAll('#cc-inp-g').forEach(e => { if (document.activeElement !== e) e.value = rgb.g; });
    el.querySelectorAll('#cc-inp-b').forEach(e => { if (document.activeElement !== e) e.value = rgb.b; });
    el.querySelectorAll('#cc-inp-h').forEach(e => { if (document.activeElement !== e) e.value = hsl.h; });
    el.querySelectorAll('#cc-inp-s').forEach(e => { if (document.activeElement !== e) e.value = hsl.s; });
    el.querySelectorAll('#cc-inp-l').forEach(e => { if (document.activeElement !== e) e.value = hsl.l; });

    // Wheel cursor
    const wheelCursor = el.querySelector('#cc-wheel-cursor');
    if (wheelCursor) {
      const cx = 100, cy = 100, r = 84;
      const angle = this.hsv.h * Math.PI / 180;
      wheelCursor.style.left = (cx + r * Math.cos(angle - Math.PI/2)) + 'px';
      wheelCursor.style.top  = (cy + r * Math.sin(angle - Math.PI/2)) + 'px';
      wheelCursor.style.background = `hsl(${this.hsv.h},100%,50%)`;
    }

    // SV square cursor
    this._drawSV();
    const svCursor = el.querySelector('#cc-sv-cursor');
    if (svCursor) {
      svCursor.style.left = (this.hsv.s * 160) + 'px';
      svCursor.style.top  = ((1 - this.hsv.v) * 100) + 'px';
      svCursor.style.background = hex;
    }

    // Hue/Sat/Val thumbs
    const hueThumb = el.querySelector('#cc-hue-thumb');
    if (hueThumb) hueThumb.style.left = (this.hsv.h / 360 * 100) + '%';
    const satThumb = el.querySelector('#cc-sat-thumb');
    if (satThumb) satThumb.style.left = (this.hsv.s * 100) + '%';
    const valThumb = el.querySelector('#cc-val-thumb');
    if (valThumb) valThumb.style.left = (this.hsv.v * 100) + '%';
    const alphaThumb = el.querySelector('#cc-alpha-thumb');
    if (alphaThumb) alphaThumb.style.left = (this.alpha * 100) + '%';

    // Slider track colors
    const satTrack = el.querySelector('#cc-sat-track');
    if (satTrack) satTrack.style.background = `linear-gradient(to right,#fff,hsl(${this.hsv.h},100%,50%))`;
    const valTrack = el.querySelector('#cc-val-track');
    if (valTrack) valTrack.style.background = `linear-gradient(to right,#000,hsl(${this.hsv.h},100%,50%))`;
    const alphaTrack = el.querySelector('#cc-alpha-track');
    if (alphaTrack) alphaTrack.style.background = `linear-gradient(to right,transparent,${hex})`;

    // Palette swatches
    this._renderPaletteSwatches();

    // Recent swatches
    this._renderRecentSwatches();

    // Harmonies
    this._renderHarmonies();

    // Gradient
    this._renderGradient();
  }

  _renderPaletteSwatches() {
    const el = this._el;
    const sel = el.querySelector('#cc-palette-select');
    const grid = el.querySelector('#cc-palette-swatches');
    if (!grid || !sel) return;
    const palName = sel.value || Object.keys(CC_PALETTES)[0];
    const colors = CC_PALETTES[palName] || [];
    grid.innerHTML = colors.map(c =>
      `<div class="cc-swatch" style="background:${c}" data-color="${c}" title="${c}"></div>`
    ).join('');
    grid.querySelectorAll('.cc-swatch').forEach(s =>
      s.addEventListener('click', () => { this._setHex(s.dataset.color); this._updateAllUI(); })
    );
  }

  _renderRecentSwatches() {
    const el = this._el;
    const grid = el.querySelector('#cc-recent-swatches');
    if (!grid) return;
    const recent = getRecent();
    grid.innerHTML = recent.length
      ? recent.map(c => `<div class="cc-swatch" style="background:${c}" data-color="${c}" title="${c}"></div>`).join('')
      : '<span style="color:#555;font-size:10px">No recent colors</span>';
    grid.querySelectorAll('.cc-swatch').forEach(s =>
      s.addEventListener('click', () => { this._setHex(s.dataset.color); this._updateAllUI(); })
    );
  }

  _renderHarmonies() {
    const el = this._el;
    const container = el.querySelector('#cc-harmony-rows');
    if (!container) return;
    const H = harmonies(this.hex);
    container.innerHTML = Object.entries(H).map(([name, colors]) => `
      <div class="cc-harmony-row">
        <div class="cc-harmony-label">${name.charAt(0).toUpperCase() + name.slice(1)}</div>
        ${colors.map(c => `<div class="cc-harmony-swatch" style="background:${c}" data-color="${c}" title="${c}"></div>`).join('')}
      </div>
    `).join('');
    container.querySelectorAll('.cc-harmony-swatch').forEach(s =>
      s.addEventListener('click', () => { this._setHex(s.dataset.color); this._updateAllUI(); })
    );
  }

  _renderGradient() {
    const el = this._el;
    const fill = el.querySelector('#cc-gradient-fill');
    if (!fill) return;
    const stops = [...this.gradientStops].sort((a, b) => a.pos - b.pos);
    const stopsCSS = stops.map(s => `${s.color} ${Math.round(s.pos * 100)}%`).join(', ');
    fill.style.background = `linear-gradient(to right, ${stopsCSS})`;

    // Re-render stop markers
    const track = el.querySelector('#cc-gradient-track');
    if (track) {
      track.querySelectorAll('.cc-gradient-stop').forEach(e => e.remove());
      this.gradientStops.forEach((stop, i) => {
        const marker = document.createElement('div');
        marker.className = 'cc-gradient-stop' + (i === this.activeStop ? ' active' : '');
        marker.style.left = (stop.pos * 100) + '%';
        marker.innerHTML = `<div class="cc-gradient-stop-color" style="background:${stop.color}"></div>`;
        marker.addEventListener('click', (e) => {
          e.stopPropagation();
          this.activeStop = i;
          this._setHex(stop.color);
          this._updateAllUI();
        });
        // Drag stop position
        marker.addEventListener('pointerdown', (e) => {
          e.stopPropagation();
          this.activeStop = i;
          marker.setPointerCapture(e.pointerId);
          const rect = track.getBoundingClientRect();
          marker.onpointermove = (ev) => {
            const pos = Math.max(0, Math.min(1, (ev.clientX - rect.left) / rect.width));
            this.gradientStops[i].pos = pos;
            this._renderGradient();
          };
          marker.onpointerup = () => {
            marker.onpointermove = null;
            marker.onpointerup = null;
          };
        });
        track.appendChild(marker);
      });
    }

    // Update active stop info
    const list = el.querySelector('#cc-gradient-stops-list');
    if (list) {
      const s = this.gradientStops[this.activeStop];
      list.textContent = s ? `Stop ${this.activeStop + 1}: ${s.color} @ ${Math.round(s.pos * 100)}%` : '';
    }
  }

  getGradientCSS(type) {
    const stops = [...this.gradientStops].sort((a, b) => a.pos - b.pos);
    const stopsCSS = stops.map(s => `${s.color} ${Math.round(s.pos * 100)}%`).join(', ');
    if (type === 'radial') return `radial-gradient(circle, ${stopsCSS})`;
    return `linear-gradient(to right, ${stopsCSS})`;
  }

  // ── Internal: events ────────────────────────────────────────────────────────

  _bindEvents() {
    const el = this._el;
    const overlay = this._overlay;

    // Overlay click = close
    overlay.addEventListener('click', () => this.close());

    // Stop propagation on picker itself
    el.addEventListener('click', e => e.stopPropagation());

    // Tabs
    el.querySelectorAll('.cc-picker-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        this._activeTab = tab.dataset.tab;
        el.querySelectorAll('.cc-picker-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === this._activeTab));
        el.querySelectorAll('.cc-picker-panel').forEach(p => p.classList.toggle('active', p.id === `cc-panel-${this._activeTab}`));
        if (this._activeTab === 'wheel') { this._drawWheel(); this._drawSV(); }
        this._updateAllUI();
      });
    });

    // HSV Wheel interaction
    const wheelCanvas = el.querySelector('#cc-hue-wheel');
    if (wheelCanvas) {
      const onWheelPick = (e) => {
        const rect = wheelCanvas.getBoundingClientRect();
        const cx = rect.width / 2, cy = rect.height / 2;
        const dx = (e.clientX - rect.left) - cx;
        const dy = (e.clientY - rect.top) - cy;
        const dist = Math.sqrt(dx*dx + dy*dy);
        const innerR = 72 * (rect.width / 200);
        const outerR = 96 * (rect.width / 200);
        if (dist >= innerR && dist <= outerR) {
          const angle = ((Math.atan2(dy, dx) * 180 / Math.PI) + 90 + 360) % 360;
          this._setHSV(angle, this.hsv.s, this.hsv.v);
          this._updateAllUI();
        }
      };
      wheelCanvas.addEventListener('pointerdown', (e) => {
        wheelCanvas.setPointerCapture(e.pointerId);
        onWheelPick(e);
        wheelCanvas.onpointermove = onWheelPick;
        wheelCanvas.onpointerup = () => { wheelCanvas.onpointermove = null; wheelCanvas.onpointerup = null; };
      });
    }

    // SV Square interaction
    const svWrap = el.querySelector('#cc-sv-wrap');
    if (svWrap) {
      const onSVPick = (e) => {
        const rect = svWrap.getBoundingClientRect();
        const s = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
        const v = Math.max(0, Math.min(1, 1 - (e.clientY - rect.top) / rect.height));
        this._setHSV(this.hsv.h, s, v);
        this._updateAllUI();
      };
      const svCanvas = svWrap.querySelector('#cc-sv-canvas');
      if (svCanvas) {
        svCanvas.addEventListener('pointerdown', (e) => {
          svCanvas.setPointerCapture(e.pointerId);
          onSVPick(e);
          svCanvas.onpointermove = onSVPick;
          svCanvas.onpointerup = () => { svCanvas.onpointermove = null; svCanvas.onpointerup = null; };
        });
      }
    }

    // Hue slider
    this._bindSlider('#cc-hue-track', '#cc-hue-thumb', (t) => {
      this._setHSV(t * 360, this.hsv.s, this.hsv.v);
      this._updateAllUI();
    });
    // Sat slider
    this._bindSlider('#cc-sat-track', '#cc-sat-thumb', (t) => {
      this._setHSV(this.hsv.h, t, this.hsv.v);
      this._updateAllUI();
    });
    // Val slider
    this._bindSlider('#cc-val-track', '#cc-val-thumb', (t) => {
      this._setHSV(this.hsv.h, this.hsv.s, t);
      this._updateAllUI();
    });
    // Alpha slider
    this._bindSlider('#cc-alpha-track', '#cc-alpha-thumb', (t) => {
      this.alpha = t;
      this._updateAllUI();
    });

    // Hex inputs (multiple per panel)
    el.querySelectorAll('.cc-preview-hex').forEach(inp => {
      inp.addEventListener('input', () => {
        const val = inp.value.trim();
        if (/^#[0-9A-Fa-f]{6}$/.test(val)) { this._setHex(val); this._updateAllUI(); }
      });
    });

    // RGB/HSL inputs
    const numInputs = ['r','g','b','h','s','l'];
    numInputs.forEach(ch => {
      el.querySelectorAll(`#cc-inp-${ch}`).forEach(inp => {
        inp.addEventListener('change', () => {
          const v = parseInt(inp.value);
          const rgb = hexToRgb(this.hex);
          const hsl = rgbToHsl(rgb);
          if (ch === 'r') rgb.r = v;
          else if (ch === 'g') rgb.g = v;
          else if (ch === 'b') rgb.b = v;
          else if (ch === 'h') hsl.h = v;
          else if (ch === 's') hsl.s = v;
          else if (ch === 'l') hsl.l = v;
          const newRgb = (ch === 'r' || ch === 'g' || ch === 'b') ? rgb : hslToRgb(hsl);
          this._setHex(rgbToHex(newRgb));
          this._updateAllUI();
        });
      });
    });

    // EyeDropper
    el.querySelectorAll('#cc-eyedropper').forEach(btn => {
      btn.addEventListener('click', async () => {
        try {
          const dropper = new EyeDropper();
          const { sRGBHex } = await dropper.open();
          this._setHex(sRGBHex);
          this._updateAllUI();
        } catch {}
      });
    });

    // Palette select
    el.querySelectorAll('#cc-palette-select').forEach(sel => {
      sel.addEventListener('change', () => this._renderPaletteSwatches());
    });

    // Gradient add/del
    const addBtn = el.querySelector('#cc-gradient-add');
    if (addBtn) addBtn.addEventListener('click', () => {
      const pos = this.gradientStops.length > 0
        ? Math.min(1, this.gradientStops[this.gradientStops.length-1].pos + 0.2)
        : 0.5;
      this.gradientStops.push({ pos, color: this.hex });
      this.activeStop = this.gradientStops.length - 1;
      this._renderGradient();
    });
    const delBtn = el.querySelector('#cc-gradient-del');
    if (delBtn) delBtn.addEventListener('click', () => {
      if (this.gradientStops.length > 2) {
        this.gradientStops.splice(this.activeStop, 1);
        this.activeStop = Math.max(0, this.activeStop - 1);
        this._renderGradient();
      }
    });

    // When gradient tab is active and color changes, update active stop
    const origSetHex = this._setHex.bind(this);
    this._setHex = (hex, notify = true) => {
      origSetHex(hex, notify);
      if (this._activeTab === 'gradient' && this.gradientStops[this.activeStop]) {
        this.gradientStops[this.activeStop].color = this.hex;
      }
    };

    // Apply / Cancel
    el.querySelector('#cc-btn-apply')?.addEventListener('click', () => {
      addRecent(this.hex);
      if (this.opts.onApply) this.opts.onApply(this.hex);
      else if (this.opts.onChange) this.opts.onChange(this.hex);
      this.close();
    });
    el.querySelector('#cc-btn-cancel')?.addEventListener('click', () => this.close());
  }

  _bindSlider(trackSel, thumbSel, onValue) {
    const el = this._el;
    const track = el.querySelector(trackSel);
    const thumb = el.querySelector(thumbSel);
    if (!track || !thumb) return;
    const pick = (e) => {
      const rect = track.getBoundingClientRect();
      const t = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      onValue(t);
    };
    track.addEventListener('pointerdown', (e) => {
      track.setPointerCapture(e.pointerId);
      pick(e);
      track.onpointermove = pick;
      track.onpointerup = () => { track.onpointermove = null; track.onpointerup = null; };
    });
    thumb.addEventListener('pointerdown', (e) => {
      e.stopPropagation();
      thumb.setPointerCapture(e.pointerId);
      pick(e);
      thumb.onpointermove = pick;
      thumb.onpointerup = () => { thumb.onpointermove = null; thumb.onpointerup = null; };
    });
  }

  // ── Internal: positioning ───────────────────────────────────────────────────

  _position() {
    const el = this._el;
    const rect = this.anchor.getBoundingClientRect();
    const W = 300, H = 500;
    let top = rect.bottom + 8;
    let left = rect.left;
    if (top + H > window.innerHeight) top = rect.top - H - 8;
    if (left + W > window.innerWidth) left = window.innerWidth - W - 8;
    if (left < 8) left = 8;
    if (top < 8) top = 8;
    el.style.top  = top  + 'px';
    el.style.left = left + 'px';
  }
}

// ─── Export ───────────────────────────────────────────────────────────────────

window.CCColorPicker = CCColorPicker;
window.ccColorUtils = { hexToRgb, rgbToHex, rgbToHsv, hsvToRgb, rgbToHsl, hslToRgb, harmonies, CC_PALETTES };
