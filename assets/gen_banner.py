"""Banner for the ldom1 profile README.

A fragment of GitHub's contribution grid in which the darkest cells
spell the word set in TEXT. Colours are GitHub's own, so the banner sits
natively above the real contribution graph further down the page.
"""
import random

W, H = 1200, 260
CELL, GAP = 20, 5
STEP = CELL + GAP
ROWS = 7
TEXT = "ARKHE"

GLYPHS = {  # 5 rows high, drawn on grid rows 1 to 5
    "D": ["110", "101", "101", "101", "110"],
    "A": ["010", "101", "111", "101", "101"],
    "T": ["111", "010", "010", "010", "010"],
    "H": ["101", "101", "111", "101", "101"],
    "P": ["110", "101", "110", "100", "100"],
    "C": ["011", "100", "100", "100", "011"],
    "R": ["110", "101", "110", "101", "101"],
    "K": ["101", "101", "110", "101", "101"],
    "E": ["111", "100", "110", "100", "111"],
    "&": ["0110", "1001", "0110", "1010", "0101"],
}

THEMES = {
    "light": {
        "levels": ["#EFF2F5", "#ACEEBB", "#4AC26B", "#2DA44E", "#116329"],
        "ink": "#1F2328", "muted": "#59636E",
    },
    "dark": {
        "levels": ["#151B23", "#033A16", "#196C2E", "#2EA043", "#56D364"],
        "ink": "#F0F6FC", "muted": "#9198A1",
    },
}

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', "
        "Helvetica, Arial, sans-serif")


def text_cells():
    """Set of (col, row) lit by the pixel text, starting at column 1."""
    lit, col = set(), 1
    for ch in TEXT:
        if ch == " ":
            col += 2
            continue
        g = GLYPHS[ch]
        for r, line in enumerate(g):
            for c, bit in enumerate(line):
                if bit == "1":
                    lit.add((col + c, r + 1))
        col += len(g[0]) + 1
    return lit, col  # col = total width incl. one-cell right margin


LIT, COLS = text_cells()
GRID_W = COLS * STEP - GAP
GRID_H = ROWS * STEP - GAP
GX = W - 48 - GRID_W
GY = 120 - GRID_H // 2


def levels_map():
    rng = random.Random(1793)
    grid = {}
    for c in range(COLS):
        for r in range(ROWS):
            if (c, r) in LIT:
                grid[c, r] = 4
            else:
                # quiet background activity, never as dark as the letters
                edge = r in (0, ROWS - 1)
                grid[c, r] = 1 if rng.random() < (0.3 if edge else 0.04) else 0
    return grid


def banner(theme):
    t = THEMES[theme]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="Ldom. Engineer who likes building things.">',
        f'<g font-family="{FONT}">',
        f'<text x="48" y="128" font-size="76" font-weight="600" '
        f'letter-spacing="-1.5" fill="{t["ink"]}">Ldom</text>',
        f'<text x="50" y="172" font-size="21" fill="{t["muted"]}">'
        f'Engineer who likes building things.</text>',
        '</g>',
    ]
    for (c, r), lvl in sorted(levels_map().items()):
        x, y = GX + c * STEP, GY + r * STEP
        out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                   f'rx="4" fill="{t["levels"][lvl]}"/>')
    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    import pathlib
    import cairosvg
    root = pathlib.Path("out/assets")
    root.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        svg = banner(theme)
        (root / f"banner-{theme}.svg").write_text(svg)
        bg = "#FFFFFF" if theme == "light" else "#0D1117"
        cairosvg.svg2png(bytestring=svg.encode(), write_to=f"preview-{theme}.png",
                         background_color=bg, output_width=1200)
    print("ok", COLS, GX)
