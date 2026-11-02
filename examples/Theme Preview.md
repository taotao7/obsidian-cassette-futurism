---
tags:
  - design
  - notes
status: In progress
---
# Cassette Futurism

A warm, colorful writing space for your everyday notes. Available in **dark** and **light**.

## Capture an idea

A note begins with a sentence. Connect it to [[Reading notes]], mark a ==useful thought==, and keep writing.

> [!tip] Keep the important things close
> Links, headings, code, and callouts share the same palette.

### A small plan

- [x] Choose a palette
- [x] Follow the light
- [ ] Make room for the next idea

| Element | Dark | Light |
| --- | --- | --- |
| Background | Deep charcoal | Warm paper |
| Accent | Soft amber | Burnt orange |
| Links | Cool cyan | Muted teal |

```python
from pathlib import Path


def collect_notes(folder: Path) -> list[Path]:
    """Find the ideas worth returning to."""
    return sorted(folder.glob("*.md"))
```

Use `collect_notes()` to find a place to start. Read more in [Obsidian Help](https://help.obsidian.md).
