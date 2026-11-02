#!/usr/bin/env python3
"""Cassette Futurism — Obsidian Theme Generator

Reads palette.toml and generates:
  - manifest.json
  - theme.css
"""

import json
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parent


def load_palette() -> dict:
    with open(ROOT / "palette.toml", "rb") as f:
        return tomllib.load(f)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def hex_to_rgb_str(value: str) -> str:
    r, g, b = hex_to_rgb(value)
    return f"{r}, {g}, {b}"


def mix_hex(base: str, overlay: str, ratio: float) -> str:
    """Blend overlay into base for readable semantic surfaces."""
    base_rgb, overlay_rgb = hex_to_rgb(base), hex_to_rgb(overlay)
    mixed = tuple(
        round(base_rgb[i] + (overlay_rgb[i] - base_rgb[i]) * ratio) for i in range(3)
    )
    return "#{:02x}{:02x}{:02x}".format(*mixed)


def gen_manifest(palette: dict) -> str:
    meta = palette["meta"]
    manifest = {
        "name": meta.get("name", "Cassette Futurism"),
        "version": "1.0.0",
        "minAppVersion": "1.0.0",
        "author": meta.get("author", "taotao7"),
        "authorUrl": "https://github.com/taotao7",
    }
    return json.dumps(manifest, indent=2) + "\n"


def gen_mode_css(palette: dict, mode: str) -> str:
    p = palette[mode]
    b, t, a, d = p["base"], p["text"], p["accent"], p["diagnostic"]

    primary_accent = a["orange"]
    secondary_accent = a["purple"]
    link_color = a["cyan"]
    link_hover = a["orange"]
    link_ext = a["blue"]
    inline_code = a["yellow"]
    syntax_keyword = a["orange"]
    syntax_function = a["orange"]
    syntax_value = a["cyan"]
    syntax_operator = a["pink"]
    graph_tag = a["cyan"]

    color_scheme = "dark" if mode == "dark" else "light"
    box_shadow = "rgba(0, 0, 0, 0.3)" if mode == "dark" else "rgba(0, 0, 0, 0.08)"
    cover_bg = "rgba(0, 0, 0, 0.6)" if mode == "dark" else "rgba(0, 0, 0, 0.3)"
    text_on_accent = b["bg"] if mode == "dark" else "#ffffff"

    return f""".theme-{mode},
body.theme-{mode} {{
  color-scheme: {color_scheme};

  /* Grayscale / base ramp */
  --color-base-00: {b['bg']};
  --color-base-05: {b['bg_dim']};
  --color-base-10: {b['bg1']};
  --color-base-20: {b['bg2']};
  --color-base-25: {b['bg3']};
  --color-base-30: {b['bg4']};
  --color-base-35: {b['border']};
  --color-base-40: {t['comment']};
  --color-base-50: {t['fg_dim']};
  --color-base-60: {t['fg_dim']};
  --color-base-70: {t['fg']};
  --color-base-100: {t['fg']};

  /* Palette accents */
  --color-red: {a['red']};
  --color-red-rgb: {hex_to_rgb_str(a['red'])};
  --color-orange: {a['orange']};
  --color-orange-rgb: {hex_to_rgb_str(a['orange'])};
  --color-yellow: {a['yellow']};
  --color-yellow-rgb: {hex_to_rgb_str(a['yellow'])};
  --color-green: {a['green']};
  --color-green-rgb: {hex_to_rgb_str(a['green'])};
  --color-cyan: {a['cyan']};
  --color-cyan-rgb: {hex_to_rgb_str(a['cyan'])};
  --color-blue: {a['blue']};
  --color-blue-rgb: {hex_to_rgb_str(a['blue'])};
  --color-purple: {a['purple']};
  --color-purple-rgb: {hex_to_rgb_str(a['purple'])};
  --color-pink: {a['pink']};
  --color-pink-rgb: {hex_to_rgb_str(a['pink'])};

  /* Core surfaces */
  --background-primary: {b['bg']};
  --background-primary-alt: {b['bg_dim']};
  --background-secondary: {b['bg1']};
  --background-secondary-alt: {b['bg2']};
  --background-modifier-border: {b['border']};
  --background-modifier-border-hover: {b['bg4']};
  --background-modifier-border-focus: {primary_accent};
  --background-modifier-form-field: {b['bg1']};
  --background-modifier-form-field-hover: {b['bg2']};
  --background-modifier-box-shadow: {box_shadow};
  --background-modifier-success: {d['hint']};
  --background-modifier-error: {d['error']};
  --background-modifier-error-hover: {mix_hex(d['error'], t['fg'], 0.15)};
  --background-modifier-error-rgb: {hex_to_rgb_str(d['error'])};
  --background-modifier-cover: {cover_bg};

  /* Text & typography */
  --text-normal: {t['fg']};
  --text-muted: {t['fg_dim']};
  --text-faint: {t['comment']};
  --text-error: {d['error']};
  --text-warning: {d['warn']};
  --text-success: {d['hint']};
  --text-accent: {primary_accent};
  --text-accent-hover: {mix_hex(primary_accent, t['fg'], 0.15)};
  --text-on-accent: {text_on_accent};
  --text-on-accent-inverted: {t['fg']};
  --text-selection: {b['bg3']};
  --text-highlight-bg: {mix_hex(b['bg'], a['yellow'], 0.35)};
  --text-highlight-bg-active: {mix_hex(b['bg'], primary_accent, 0.45)};
  --caret-color: {primary_accent};

  /* Interactive elements */
  --interactive-normal: {b['bg1']};
  --interactive-hover: {b['bg2']};
  --interactive-accent: {primary_accent};
  --interactive-accent-hover: {mix_hex(primary_accent, t['fg'], 0.15)};
  --interactive-accent-rgb: {hex_to_rgb_str(primary_accent)};
  --interactive-success: {d['hint']};

  /* Links */
  --link-color: {link_color};
  --link-color-hover: {link_hover};
  --link-external-color: {link_ext};
  --link-external-color-hover: {link_hover};
  --link-unresolved-color: {t['comment']};
  --link-unresolved-opacity: 0.75;

  /* Headings */
  --h1-color: {a['orange']};
  --h2-color: {a['purple']};
  --h3-color: {a['cyan']};
  --h4-color: {a['yellow']};
  --h5-color: {a['green']};
  --h6-color: {a['pink']};
  --heading-formatting: {t['comment']};

  /* Code & Syntax */
  --code-normal: {t['fg']};
  --code-background: {b['bg1']};
  --code-block-background: {b['bg1']};
  --code-border-color: {b['border']};
  --inline-code-color: {inline_code};
  --inline-code-background: {b['bg2']};
  --code-comment: {t['comment']};
  --code-keyword: {syntax_keyword};
  --code-function: {syntax_function};
  --code-string: {a['green']};
  --code-value: {syntax_value};
  --code-operator: {syntax_operator};
  --code-property: {a['cyan']};
  --code-tag: {a['pink']};
  --code-punctuation: {t['fg_dim']};
  --code-important: {d['warn']};

  /* Tables */
  --table-border-color: {b['border']};
  --table-border-width: 1px;
  --table-header-background: {b['bg1']};
  --table-header-background-hover: {b['bg2']};
  --table-header-color: {t['fg']};
  --table-row-background-hover: {b['bg2']};
  --table-row-alt-background: {mix_hex(b['bg'], b['bg1'], 0.5)};

  /* Graph view */
  --graph-line: {b['border']};
  --graph-node: {t['fg_dim']};
  --graph-node-unresolved: {t['comment']};
  --graph-node-focused: {primary_accent};
  --graph-node-tag: {graph_tag};
  --graph-node-attachment: {a['green']};
  --graph-text: {t['fg']};

  /* Titlebar & Status bar */
  --titlebar-background: {b['bg1']};
  --titlebar-background-focused: {b['bg1']};
  --titlebar-border-color: {b['border']};
  --titlebar-text-color: {t['fg_dim']};
  --titlebar-text-color-focused: {t['fg']};
  --status-bar-background: {b['bg1']};
  --status-bar-border-color: {b['border']};
  --status-bar-text-color: {t['fg_dim']};

  /* Navigation & File Explorer */
  --nav-item-color: {t['fg_dim']};
  --nav-item-color-hover: {t['fg']};
  --nav-item-color-active: {t['fg']};
  --nav-item-background-hover: {b['bg2']};
  --nav-item-background-active: {b['bg3']};

  /* Tabs */
  --tab-background-active: {b['bg']};
  --tab-text-color: {t['fg_dim']};
  --tab-text-color-focused: {t['fg']};
  --tab-text-color-active: {t['fg']};
  --tab-outline-color: {b['border']};
  --tab-divider-color: {b['border']};
  --divider-color: {b['border']};

  /* Ribbons & Modals */
  --ribbon-background: {b['bg1']};
  --ribbon-background-collapsed: {b['bg1']};
  --modal-background: {b['bg2']};
  --modal-border-color: {b['border']};
  --prompt-border-color: {b['border']};

  /* Blockquotes & Dividers */
  --blockquote-border-color: {primary_accent};
  --blockquote-border-thickness: 2px;
  --blockquote-color: {t['fg_dim']};
  --blockquote-background-color: {mix_hex(b['bg'], b['bg1'], 0.4)};
  --hr-color: {b['border']};
  --hr-thickness: 1px;

  /* Checkboxes */
  --checkbox-color: {primary_accent};
  --checkbox-color-hover: {mix_hex(primary_accent, t['fg'], 0.2)};
  --checkbox-border-color: {b['border']};
  --checkbox-border-color-hover: {primary_accent};
  --checklist-done-color: {t['comment']};

  /* Tags */
  --tag-color: {primary_accent};
  --tag-color-hover: {secondary_accent};
  --tag-background: {b['bg2']};
  --tag-background-hover: {b['bg3']};
  --tag-border-color: {b['border']};
  --tag-border-color-hover: {primary_accent};
  --tag-border-width: 1px;

  /* Search results & Canvas */
  --search-result-background: {b['bg4']};
  --search-result-active-background: {mix_hex(b['bg'], primary_accent, 0.45)};
  --canvas-background: {b['bg']};
  --canvas-card-background: {b['bg1']};
  --canvas-card-border-color: {b['border']};
}}"""


def gen_css(palette: dict) -> str:
    """Generate complete Obsidian stylesheet with dark, light, and syntax blocks."""
    dark_css = gen_mode_css(palette, "dark")
    light_css = gen_mode_css(palette, "light")

    return f"""/* ===================================================================
 * Cassette Futurism — Obsidian Theme
 * Generated from palette.toml
 * =================================================================== */

{dark_css}

{light_css}

/* Text selection */
.theme-dark ::selection,
.theme-light ::selection {{
  background-color: var(--text-selection);
}}

/* Inline code and code blocks */
.theme-dark code,
.theme-light code {{
  color: var(--inline-code-color);
  background-color: var(--inline-code-background);
}}

.theme-dark pre > code,
.theme-light pre > code {{
  color: var(--code-normal);
  background-color: transparent;
}}

/* CodeMirror syntax highlighting (Live Preview / Editor) */
.theme-dark .cm-keyword,
.theme-light .cm-keyword {{
  color: var(--code-keyword);
}}
.theme-dark .cm-operator,
.theme-light .cm-operator {{
  color: var(--code-operator);
}}
.theme-dark .cm-variable,
.theme-light .cm-variable {{
  color: var(--text-normal);
}}
.theme-dark .cm-variable-2,
.theme-light .cm-variable-2 {{
  color: var(--code-property);
}}
.theme-dark .cm-def,
.theme-light .cm-def {{
  color: var(--code-function);
}}
.theme-dark .cm-property,
.theme-light .cm-property {{
  color: var(--code-property);
}}
.theme-dark .cm-string,
.theme-dark .cm-string-2,
.theme-light .cm-string,
.theme-light .cm-string-2 {{
  color: var(--code-string);
}}
.theme-dark .cm-number,
.theme-dark .cm-atom,
.theme-light .cm-number,
.theme-light .cm-atom {{
  color: var(--code-value);
}}
.theme-dark .cm-comment,
.theme-light .cm-comment {{
  color: var(--code-comment);
  font-style: italic;
}}
.theme-dark .cm-tag,
.theme-light .cm-tag {{
  color: var(--code-tag);
}}
.theme-dark .cm-attribute,
.theme-light .cm-attribute {{
  color: var(--code-property);
}}
.theme-dark .cm-link,
.theme-light .cm-link {{
  color: var(--link-color);
}}

/* Prism syntax highlighting (Reading View) */
.theme-dark .token.comment,
.theme-dark .token.prolog,
.theme-dark .token.doctype,
.theme-dark .token.cdata,
.theme-light .token.comment,
.theme-light .token.prolog,
.theme-light .token.doctype,
.theme-light .token.cdata {{
  color: var(--code-comment);
  font-style: italic;
}}
.theme-dark .token.punctuation,
.theme-light .token.punctuation {{
  color: var(--code-punctuation);
}}
.theme-dark .token.property,
.theme-dark .token.tag,
.theme-dark .token.boolean,
.theme-dark .token.number,
.theme-dark .token.constant,
.theme-dark .token.symbol,
.theme-light .token.property,
.theme-light .token.tag,
.theme-light .token.boolean,
.theme-light .token.number,
.theme-light .token.constant,
.theme-light .token.symbol {{
  color: var(--code-value);
}}
.theme-dark .token.selector,
.theme-dark .token.attr-name,
.theme-dark .token.string,
.theme-dark .token.char,
.theme-dark .token.builtin,
.theme-light .token.selector,
.theme-light .token.attr-name,
.theme-light .token.string,
.theme-light .token.char,
.theme-light .token.builtin {{
  color: var(--code-string);
}}
.theme-dark .token.operator,
.theme-dark .token.entity,
.theme-dark .token.url,
.theme-light .token.operator,
.theme-light .token.entity,
.theme-light .token.url {{
  color: var(--code-operator);
}}
.theme-dark .token.atrule,
.theme-dark .token.attr-value,
.theme-dark .token.keyword,
.theme-light .token.atrule,
.theme-light .token.attr-value,
.theme-light .token.keyword {{
  color: var(--code-keyword);
}}
.theme-dark .token.function,
.theme-dark .token.class-name,
.theme-light .token.function,
.theme-light .token.class-name {{
  color: var(--code-function);
}}
.theme-dark .token.regex,
.theme-dark .token.important,
.theme-dark .token.variable,
.theme-light .token.regex,
.theme-light .token.important,
.theme-light .token.variable {{
  color: var(--code-property);
}}
"""


def main():
    palette = load_palette()

    manifest_content = gen_manifest(palette)
    theme_css_content = gen_css(palette)

    (ROOT / "manifest.json").write_text(manifest_content, encoding="utf-8")
    (ROOT / "theme.css").write_text(theme_css_content, encoding="utf-8")

    print("Generated manifest.json")
    print("Generated theme.css")


if __name__ == "__main__":
    main()
