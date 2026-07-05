# Reading Folders — CKEditor-style Toolbar Redesign

**Date:** 2026-07-05
**Status:** Approved, ready to implement
**Scope:** Visual redesign of the on-screen toolbar in `gen_html.py` (screen-only; print output unchanged). One functional change: folder filter moves into a dropdown popover.

## Goal
Replace the current MS-Word-ribbon toolbar with a **CKEditor-classic style** flat toolbar: one flat row of monochrome line-icon buttons, groups separated by thin vertical dividers, dropdowns with a caret. Remove the row of folder checkboxes.

## Changes

### Structure
- **Remove:** the tab strip (`.ribbon-tabs`, brand "Reading Folders", tab "Bố cục & In"), the collapse-on-tab-click behavior, and the folder checkbox row (`.folders-filter` in the bar).
- **Result:** a single flat toolbar (`.toolbar`) = one wrapping row of controls, grouped by vertical separators.

### Layout (left → right), separators `│` between groups
```
[view: both/words/graphemes] │ [orientation L/P] [grid cols×rows] │ [font ▾] [size ▾] [B] [I] │ [color red/bw] │ [Thư mục ▾] │ [Print] [Import] [Export] [Reset]
```

### Visual style (CKEditor)
- Flat icon buttons: no border by default; hover = light grey bg; active/on = light blue bg + darker icon.
- Monochrome **line SVG icons ~18–20px**, redrawn CKEditor-like for: view (2-col / single-card / list), orientation (landscape/portrait rects), grid (3×3), color (filled dot / half dot), print (printer), import (down-to-tray), export (up/save), reset (circular arrow), folder (folder + caret).
- **B / I** as bold/italic glyph buttons.
- Font & Size: native `<select>` restyled flat with caret (keep native for reliability/accessibility).
- Toolbar bg light (`#f7f7f9`-ish), thin bottom border; buttons share one consistent height.

### Folder dropdown (replaces checkbox row)
- A button **"📁 Thư mục ▾"**. Click toggles a **popover** anchored under it containing:
  - one toggle row per non-empty folder (checkbox + label), reflecting current selection,
  - **Chọn tất / Bỏ tất** buttons.
- Click-outside or Esc closes it. Changing toggles re-renders the sheets (same behavior as the old checkboxes).
- The existing `folderFilter` element becomes the popover body; `buildFolderFilter()` still populates it; `selectedFolders()` unchanged.

## Preserve (no behavior change)
- All controls keep function: view, orientation, grid (cols×rows), font, size, Bold, Italic, color, folder selection, Print, Import/Export/Reset (JSON), auto-mark rendering, auto-fit, preview zoom.
- Current defaults kept: **normal weight**, **80px** size, cursive-standard font, landscape, 3×3, red.
- URL params still work (`?font,fontsize,cols,rows,orientation,weight,italic,view,color`).
- Print CSS unchanged (`.toolbar` still `display:none` in print).

## Non-goals
- No change to card rendering, data model, or print output.
- No new features beyond the folder popover.

## Verification
- Rebuild `gen_html.py`; headless screenshots (desktop + mobile) confirm: flat CKEditor bar, new icons, folder popover opens/selects, defaults (normal, 80px), controls aligned.
- Spot-check a toggle in the folder popover re-filters the printed sheets.
