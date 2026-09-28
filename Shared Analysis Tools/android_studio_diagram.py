#!/usr/bin/env python3
"""
Generates a detailed mock-up of the Android Studio editor window, matched to
this user's own real Android Studio install (dark "Darcula"-family theme,
full toolbar chrome, syntax-highlighted code, status bar) -- built from the
exact real file tree and exact real source code of each challenge project,
drawn with PIL. Not a captured screenshot: every pixel is generated from the
real files on disk, not a pixel-for-pixel copy of an actual screen.

Icon note: many toolbar glyphs (gear, checkmark, bug, hammer, etc.) are not
present in Consolas/Courier/Arial, so they render as blank "tofu" boxes if
drawn as text. Every such icon here is instead hand-drawn with basic PIL
shapes (lines/circles/polygons) so nothing is ever a blank box.
"""

import os
import re
from PIL import Image, ImageDraw, ImageFont

W, H = 1360, 860

# Dark theme palette -- pixel-sampled directly from the user's own real
# Android Studio screenshot (2026 "new UI" dark theme).
BG_TITLEBAR = (44, 36, 46)       # purple-tinted title bar (project color accent)
BG_TOOLWINDOW = (25, 26, 28)     # project tree panel
BG_EDITOR = (25, 26, 28)         # code editor background (sampled: (25,26,28))
BG_TAB = (25, 26, 28)            # inactive tab strip
BG_TAB_ACTIVE = (37, 38, 41)     # active tab, slightly lighter
BG_GUTTER = (25, 26, 28)         # line-number gutter -- same as editor, no seam
BG_STATUSBAR = (43, 45, 48)
BG_RUNPANEL = (25, 26, 28)
BG_NOTIFBAR = (58, 48, 62)       # the purple "Gradle files have changed" banner
ACCENT = (53, 116, 240)          # #3574F0 - Android Studio blue accent
GREEN_OK = (89, 168, 105)
LINK_BLUE = (88, 157, 246)
FG_TEXT = (188, 190, 196)        # main editor text
FG_DIM = (140, 140, 140)         # toolbar icon color (sampled)
FG_TREE_FOLDER = (188, 190, 196)
FG_TREE_FILE = (169, 183, 198)
LINE = (50, 52, 55)
LINE_DARK = (70, 72, 76)

# Syntax-highlight colors -- pixel-sampled from the real screenshot.
SYN_KEYWORD = (204, 120, 50)     # orange (Java keywords -- not visible in the
                                  # XML sample, kept from the standard Darcula set)
SYN_STRING = (98, 165, 100)      # green -- sampled from "false"/"Hasher" values
SYN_COMMENT = (128, 128, 128)    # gray
SYN_ANNOTATION = (187, 181, 41)  # yellow
SYN_NUMBER = (104, 151, 187)     # light blue
SYN_TAG = (213, 183, 120)        # warm gold -- sampled from <application>/<activity>
SYN_ATTR = (189, 88, 78)         # salmon-red -- sampled from android:allowBackup

JAVA_KEYWORDS = set("""
public private protected static final void class interface extends implements
new return if else for while do try catch finally throw throws import package
this super int long short byte char boolean float double String true false null
break continue switch case default synchronized volatile transient abstract
enum instanceof
""".split())

# Glyphs confirmed (by rendering a test grid) to actually draw with
# Consolas/Courier/Arial -- everything NOT in this set is hand-drawn instead.
# Usable: \u25BE \u25B4 \u2261 \u2500 \u2192 \u2190 \u25CF \u25CB \u25A0 \u25A1
#         \u203A \u2039 \u00B7 \u2022 \u25AA \u00D7 + - \u25B2 \u25BC


def _font(size, bold=False):
    candidates = (
        ["consolab.ttf", "C:/Windows/Fonts/consolab.ttf"] if bold else ["consola.ttf", "C:/Windows/Fonts/consola.ttf"]
    ) + ["cour.ttf", "arial.ttf", "arialbd.ttf",
         "C:/Windows/Fonts/cour.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    return ImageFont.load_default()

F_UI = _font(14)
F_UI_BOLD = _font(14, bold=True)
F_TREE = _font(14)
F_CODE = _font(15)
F_LINENO = _font(13)
F_SMALL = _font(12)


# ============================================================================
# Hand-drawn vector icons (every toolbar icon that has no working font glyph)
# ============================================================================

def _dots_vertical(d, cx, cy, color, r=1.4, gap=5):
    for i in (-1, 0, 1):
        yy = cy + i * gap
        d.ellipse([cx - r, yy - r, cx + r, yy + r], fill=color)


def _dots_horizontal(d, cx, cy, color, r=1.4, gap=5):
    for i in (-1, 0, 1):
        xx = cx + i * gap
        d.ellipse([xx - r, cy - r, xx + r, cy + r], fill=color)


def _gear(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=1)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], outline=color, width=1)
    import math
    for i in range(8):
        a = i * math.pi / 4
        x1, y1 = cx + (r + 1) * math.cos(a), cy + (r + 1) * math.sin(a)
        x2, y2 = cx + (r + 4) * math.cos(a), cy + (r + 4) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=color, width=1)


def _check(d, x, y, color, size=10):
    d.line([x, y + size * 0.5, x + size * 0.35, y + size * 0.85], fill=color, width=2)
    d.line([x + size * 0.35, y + size * 0.85, x + size, y], fill=color, width=2)


def _target(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=1)
    d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill=color)


def _hammer(d, x, y, color):
    # diagonal handle
    d.line([x, y + 14, x + 10, y + 4], fill=color, width=2)
    # hammer head
    d.polygon([(x + 7, y + 1), (x + 15, y - 3), (x + 18, y + 1), (x + 11, y + 6)], outline=color)
    # small "sync" arrow beside it
    d.arc([x + 12, y + 6, x + 22, y + 16], 30, 300, fill=color, width=1)
    d.polygon([(x + 21, y + 6), (x + 24, y + 9), (x + 19, y + 10)], fill=color)


def _apply_changes(d, x, y, color, font):
    d.text((x, y - 2), "A", font=font, fill=color)
    d.arc([x + 10, y - 2, x + 24, y + 12], 200, 430, fill=color, width=1)
    d.polygon([(x + 22, y - 1), (x + 25, y + 2), (x + 20, y + 3)], fill=color)


def _lines_arrow(d, x, y, color):
    for i in range(3):
        yy = y + i * 4
        d.line([x, yy, x + 12 - i * 2, yy], fill=color, width=1)
    d.line([x + 16, y + 2, x + 22, y + 2], fill=color, width=1)
    d.polygon([(x + 16, y + 2), (x + 19, y - 1), (x + 19, y + 5)], fill=color)


def _bug(d, x, y, color):
    cx, cy = x + 8, y + 8
    d.ellipse([cx - 5, cy - 6, cx + 5, cy + 6], outline=color, width=1)
    for dy in (-4, 0, 4):
        d.line([cx - 5, cy + dy, cx - 9, cy + dy], fill=color, width=1)
        d.line([cx + 5, cy + dy, cx + 9, cy + dy], fill=color, width=1)
    d.line([cx - 2, cy - 8, cx - 4, cy - 11], fill=color, width=1)
    d.line([cx + 2, cy - 8, cx + 4, cy - 11], fill=color, width=1)


def _ribbon(d, x, y, color):
    d.arc([x, y + 2, x + 14, y + 12], 200, 20, fill=color, width=1)
    d.arc([x + 6, y, x + 20, y + 10], 20, 200, fill=color, width=1)
    d.polygon([(x + 18, y + 1), (x + 21, y + 3), (x + 17, y + 5)], fill=color)


def _folder_icon(d, x, y, w, h, color):
    d.polygon([(x, y + 2), (x + w * 0.4, y + 2), (x + w * 0.5, y), (x + w, y),
               (x + w, y + h), (x, y + h)], fill=color)


def _android_head(d, cx, cy, color):
    r = 5
    d.pieslice([cx - r, cy - r, cx + r, cy + r + 2], 180, 360, fill=color)
    d.line([cx - 3, cy - r - 2, cx - 1, cy - r], fill=color, width=1)
    d.line([cx + 3, cy - r - 2, cx + 1, cy - r], fill=color, width=1)
    d.ellipse([cx - 5, cy - 1, cx - 3, cy + 1], fill=BG_TITLEBAR)
    d.ellipse([cx + 3, cy - 1, cx + 5, cy + 1], fill=BG_TITLEBAR)


def _profile_avatar(d, x0, y0, x1, y1, color):
    d.ellipse([x0, y0, x1, y1], outline=color, width=1)
    cx = (x0 + x1) / 2
    r = (x1 - x0) / 2
    d.ellipse([cx - r * 0.32, y0 + r * 0.4, cx + r * 0.32, y0 + r * 1.05], outline=color, width=1)
    d.arc([x0 + r * 0.15, y0 + r * 0.9, x1 - r * 0.15, y1 + r * 0.6], 200, 340, fill=color, width=1)


def _window_controls(d, x, y, color):
    d.line([x, y + 6, x + 12, y + 6], fill=color, width=1)
    d.rectangle([x + 32, y, x + 44, y + 12], outline=color, width=1)
    d.line([x + 64, y, x + 76, y + 12], fill=color, width=1)
    d.line([x + 76, y, x + 64, y + 12], fill=color, width=1)


# ---- left vertical tool-window icon strip (Project/Structure/Run/Build/
# Gradle/Problems/Terminal/Git -- matches the real IDE's edge strip) ----

def _icon_structure(d, cx, cy, color):
    d.ellipse([cx - 5, cy - 7, cx + 1, cy - 1], outline=color, width=1)
    d.rectangle([cx - 6, cy + 1, cx, cy + 7], outline=color, width=1)
    d.polygon([(cx + 5, cy + 7), (cx + 1, cy + 1), (cx + 9, cy + 1)], outline=color)


def _icon_play_box(d, cx, cy, color):
    d.rounded_rectangle([cx - 11, cy - 9, cx + 11, cy + 9], radius=2, fill=(60, 62, 66))
    d.polygon([(cx - 3, cy - 5), (cx - 3, cy + 5), (cx + 5, cy)], fill=color)


def _icon_ribbon_up(d, cx, cy, color):
    d.arc([cx - 8, cy - 2, cx + 2, cy + 6], 200, 20, fill=color, width=1)
    d.arc([cx - 2, cy - 6, cx + 8, cy + 2], 20, 200, fill=color, width=1)
    d.line([cx + 6, cy - 8, cx + 6, cy - 2], fill=color, width=1)
    d.polygon([(cx + 3, cy - 6), (cx + 6, cy - 10), (cx + 9, cy - 6)], fill=color)


def _icon_build_t(d, cx, cy, color):
    d.line([cx - 7, cy - 7, cx + 7, cy - 7], fill=color, width=2)
    d.line([cx, cy - 7, cx, cy + 7], fill=color, width=2)
    d.line([cx - 5, cy + 7, cx + 5, cy + 7], fill=color, width=1)


def _icon_diamond(d, cx, cy, r, color):
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], outline=color, width=1)


def _icon_paw(d, cx, cy, color):
    d.ellipse([cx - 6, cy - 3, cx + 6, cy + 7], outline=color, width=1)
    for dx in (-6, -2, 2, 6):
        d.ellipse([cx + dx - 2, cy - 8, cx + dx + 2, cy - 4], outline=color, width=1)


def _icon_alert_circle(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=1)
    d.line([cx, cy - r * 0.5, cx, cy + r * 0.15], fill=color, width=1)
    d.ellipse([cx - 1, cy + r * 0.45, cx + 1, cy + r * 0.55], fill=color)


def _icon_terminal(d, cx, cy, color):
    d.rectangle([cx - 9, cy - 7, cx + 9, cy + 7], outline=color, width=1)
    d.line([cx - 6, cy - 2, cx - 2, cy + 1, cx - 6, cy + 4], fill=color, width=1)
    d.line([cx, cy + 4, cx + 6, cy + 4], fill=color, width=1)


def _icon_git_branch(d, cx, cy, color):
    d.ellipse([cx - 6, cy - 7, cx - 2, cy - 3], outline=color, width=1)
    d.ellipse([cx - 6, cy + 3, cx - 2, cy + 7], outline=color, width=1)
    d.ellipse([cx + 3, cy - 1, cx + 7, cy + 3], outline=color, width=1)
    d.line([cx - 4, cy - 3, cx - 4, cy + 3], fill=color, width=1)
    d.arc([cx - 4, cy - 2, cx + 5, cy + 3], 270, 360, fill=color, width=1)


def draw_left_strip(d, x0, top, bottom, width, tree_active_color):
    """The thin vertical strip of tool-window icons on the far left edge --
    Project (active/highlighted), Structure, more; a gap; then Run, Push,
    Build, Gradle, plugin, Problems, Terminal, Git near the bottom.

    Vertical gaps below are measured directly off a real Android Studio
    screenshot (icon-cluster detection by scanning for non-background
    pixels down the strip column): the top cluster uses ~35-40px gaps, the
    bottom cluster is a very consistent ~40px between icon centers, with
    the Run icon's button taking a little extra height.
    """
    d.rectangle([x0, top, x0 + width, bottom], fill=BG_TITLEBAR)
    cx = x0 + width // 2

    # ---- top cluster: Project (active), Structure, more (...) ----
    d.rectangle([x0, top, x0 + width, top + width], fill=ACCENT)
    _folder_icon(d, x0 + width * 0.22, top + width * 0.28, width * 0.56, width * 0.44, (255, 255, 255))
    y = top + width // 2  # folder icon center
    y += 35
    _icon_structure(d, cx, y, FG_DIM)
    y += 40
    _dots_horizontal(d, cx, y, FG_DIM, r=1.3, gap=4)

    # ---- bottom cluster: Run, Push, Build, Gradle, plugin, Problems, Terminal, Git ----
    gap = 40
    y2 = bottom - 32  # Git branch icon (closest to the bottom edge)
    _icon_git_branch(d, cx, y2, FG_DIM); y2 -= gap
    _icon_terminal(d, cx, y2, FG_DIM); y2 -= gap
    _icon_alert_circle(d, cx, y2, 8, FG_DIM); y2 -= gap
    _icon_paw(d, cx, y2, FG_DIM); y2 -= gap
    _icon_diamond(d, cx, y2, 8, FG_DIM); y2 -= gap
    _icon_build_t(d, cx, y2, FG_DIM); y2 -= gap
    _icon_ribbon_up(d, cx, y2, FG_DIM); y2 -= gap
    _icon_play_box(d, cx, y2, FG_DIM)


def _tok_java(line, state):
    """Yields (text, color) tokens for one line of Java source.

    `state` is a single-element list [in_block_comment: bool], mutated in
    place so the caller can carry /** ... */ block-comment state across
    successive lines (a Javadoc header would otherwise have its quoted
    example strings wrongly colored as real code strings, since a per-line
    tokenizer has no memory of an unclosed /* from a previous line).

    The string-literal alternative is tried BEFORE the line-comment
    alternative, so a "//" that appears inside a quoted string (very common
    in URLs, e.g. "http://...") is consumed as part of the string and never
    misdetected as the start of a comment.
    """
    out = []

    if state[0]:
        end = line.find('*/')
        if end == -1:
            out.append((line, SYN_COMMENT))
            return out
        out.append((line[:end + 2], SYN_COMMENT))
        line = line[end + 2:]
        state[0] = False

    token_re = re.compile(r'"(?:[^"\\]|\\.)*"|/\*.*?\*/|/\*.*$|//.*$|\b\d+\b|@\w+|\b\w+\b|\s+|.')
    for m in token_re.finditer(line):
        t = m.group(0)
        if t.startswith('"'):
            out.append((t, SYN_STRING))
        elif t.startswith('/*'):
            out.append((t, SYN_COMMENT))
            if not t.endswith('*/'):
                state[0] = True
        elif t.startswith('//'):
            out.append((t, SYN_COMMENT))
        elif t.startswith('@'):
            out.append((t, SYN_ANNOTATION))
        elif t.isdigit():
            out.append((t, SYN_NUMBER))
        elif t in JAVA_KEYWORDS:
            out.append((t, SYN_KEYWORD))
        else:
            out.append((t, FG_TEXT))
    return out


def _tok_xml(line):
    """Yields (text, color) tokens for one line of XML/manifest source."""
    out = []
    token_re = re.compile(r'</?[\w:.]+|/?>|"[^"]*"|[\w:.-]+=|[\w:.-]+|\s+|.')
    for m in token_re.finditer(line):
        t = m.group(0)
        if t.startswith('<') or t in ('>', '/>'):
            out.append((t, SYN_TAG))
        elif t.startswith('"'):
            out.append((t, SYN_STRING))
        elif t.endswith('='):
            out.append((t[:-1], SYN_ATTR))
            out.append(('=', FG_TEXT))
        elif t.startswith('<!--') or t.startswith('-->'):
            out.append((t, SYN_COMMENT))
        else:
            out.append((t, FG_TEXT))
    return out


def _draw_tokens(d, x, y, tokens, font):
    cx = x
    for text, color in tokens:
        d.text((cx, y), text, font=font, fill=color)
        cx += d.textlength(text, font=font)


def compute_comment_state_before(lines, upto):
    """Scans lines[0:upto] purely to determine whether an unclosed /* ... */
    block comment is still open at the start of line `upto` -- needed when
    a diagram's visible slice starts mid-file (mid-comment), not at line 1."""
    state = [False]
    for l in lines[:upto]:
        _tok_java(l, state)
    return state[0]


def _highlight_line(d, x, y, line, font, filename, comment_state=None):
    if filename.endswith('.xml'):
        tokens = _tok_xml(line)
    elif filename.endswith('.java'):
        tokens = _tok_java(line, comment_state if comment_state is not None else [False])
    else:
        tokens = [(line, FG_TEXT)]
    _draw_tokens(d, x, y, tokens, font)


def make_diagram(out_path, project_name, tree_lines, tree_highlight_index,
                  code_filename, code_lines, code_highlight_index, comment_text,
                  start_line_no=1, tool_name="Android Studio", module_name="app",
                  avd_name="upos avd", vcs_branch="main", initial_comment_state=False):
    """
    tree_lines: list of (depth, label, is_file) describing the project tree.
    code_lines: list of code text lines (already truncated to fit).
    Unused params (tree_highlight_index [tree row], code_highlight_index,
    comment_text) are kept for call-signature compatibility with older callers.
    """
    img = Image.new("RGB", (W, H), BG_EDITOR)
    d = ImageDraw.Draw(img)

    # ======================================================================
    # Row 1: ONE combined toolbar -- android icon, hamburger, project badge
    # +name, VCS on the left; device/module/run/debug/more, then the full
    # icon cluster (hammer, apply-changes, lines+arrow, bug, ribbon, search,
    # gear, profile), then Windows min/max/close on the right.
    # ======================================================================
    d.rectangle([0, 0, W - 1, 32], fill=BG_TITLEBAR)
    _android_head(d, 14, 16, GREEN_OK)
    d.text((26, 8), "\u2261", font=F_UI_BOLD, fill=FG_TEXT)
    badge_x = 48
    d.rectangle([badge_x, 6, badge_x + 20, 26], fill=(150, 60, 150))
    d.text((badge_x + 5, 8), project_name[0].upper(), font=F_UI_BOLD, fill=(255, 255, 255))
    name_x = badge_x + 28
    d.text((name_x, 8), f"{project_name} \u25BE", font=F_UI_BOLD, fill=FG_TEXT)
    vcs_x = name_x + d.textlength(f"{project_name} \u25BE", font=F_UI_BOLD) + 26
    d.text((vcs_x, 8), "Version Control \u25BE", font=F_UI, fill=FG_DIM)

    # right-aligned cluster, laid out right-to-left so it always fits
    rx = W - 18
    _window_controls_w = 96
    rx -= _window_controls_w
    _window_controls(d, rx, 10, FG_DIM)
    rx -= 28
    _profile_avatar(d, rx - 18, 7, rx, 25, FG_DIM)
    rx -= 30
    _gear(d, rx, 16, 7, FG_DIM)
    rx -= 26
    d.ellipse([rx - 12, 9, rx - 2, 19], outline=FG_DIM, width=1)
    d.line([rx - 4, 17, rx + 1, 22], fill=FG_DIM, width=1)
    rx -= 30
    _ribbon(d, rx - 20, 6, FG_DIM)
    rx -= 26
    _bug(d, rx - 16, 8, FG_DIM)
    rx -= 26
    _lines_arrow(d, rx - 24, 11, FG_DIM)
    rx -= 30
    _apply_changes(d, rx - 24, 12, FG_DIM, F_SMALL)
    rx -= 30
    _hammer(d, rx - 24, 14, FG_DIM)

    # device / module / run / debug / more, ending before the icon cluster.
    # Starts well clear of the left title block regardless of project-name length.
    tx = vcs_x + d.textlength("Version Control ▾", font=F_UI) + 70
    ty = 9
    dev_label = f"{avd_name} \u25BE"
    d.rectangle([tx, ty + 1, tx + 12, ty + 13], outline=FG_TEXT, width=1)  # device glyph
    tx += 18
    d.text((tx, ty), dev_label, font=F_UI, fill=FG_TEXT)
    tx += d.textlength(dev_label, font=F_UI) + 20
    mod_label = f"{module_name} \u25BE"
    _android_head(d, tx + 5, ty + 6, (100, 150, 200))
    tx += 16
    d.text((tx, ty), mod_label, font=F_UI, fill=FG_TEXT)
    tx += d.textlength(mod_label, font=F_UI) + 16
    d.polygon([(tx, ty + 1), (tx, ty + 13), (tx + 11, ty + 7)], fill=(140, 142, 146))
    tx += 22
    _bug(d, tx - 4, ty - 1, (140, 142, 146))
    tx += 20
    _dots_vertical(d, tx + 4, ty + 7, FG_DIM)

    STRIP_W = 32
    TREE_W = 300
    top = 32

    # ---- far-left vertical tool-window icon strip ----
    draw_left_strip(d, 0, top, H - 22, STRIP_W, ACCENT)

    # ======================================================================
    # Row 2: project-pane header (folder icon + "Android v" + its own small
    # icon toolbar) on the left; editor tab strip on the right.
    # ======================================================================
    tree_x0 = STRIP_W
    d.rectangle([tree_x0, top, tree_x0 + TREE_W, H - 22], fill=BG_TOOLWINDOW)
    _folder_icon(d, tree_x0 + 10, top + 9, 14, 12, (100, 150, 220))
    d.text((tree_x0 + 30, top + 8), "Android \u25BE", font=F_UI_BOLD, fill=FG_TEXT)
    ix = tree_x0 + TREE_W - 145
    d.text((ix, top + 6), "+", font=F_UI, fill=FG_DIM); ix += 20
    _target(d, ix + 6, top + 15, 6, FG_DIM); ix += 22
    d.text((ix, top + 3), "\u25B4", font=F_SMALL, fill=FG_DIM)
    d.text((ix, top + 12), "\u25BE", font=F_SMALL, fill=FG_DIM); ix += 18
    d.text((ix, top + 6), "\u00D7", font=F_UI, fill=FG_DIM); ix += 20
    _dots_vertical(d, ix + 3, top + 15, FG_DIM); ix += 18
    d.line([ix, top + 15, ix + 10, top + 15], fill=FG_DIM, width=1)
    d.line([tree_x0, top + 30, tree_x0 + TREE_W, top + 30], fill=LINE)

    y = top + 40
    row_h = 22
    for i, (depth, label, is_file) in enumerate(tree_lines):
        x = tree_x0 + 14 + depth * 16
        if i == tree_highlight_index:
            d.rectangle([tree_x0, y - 2, tree_x0 + TREE_W, y + row_h - 4], fill=(58, 48, 62))
        icon = "\u25A2" if not is_file else "\u2022"
        d.text((x, y), f"{icon} {label}", font=F_TREE,
                fill=FG_TREE_FOLDER if not is_file else FG_TREE_FILE)
        y += row_h
        if y > H - 60:
            break

    # ---- editor tab strip (file-type icon, filename, close x, tab-options) ----
    tab_x0 = tree_x0 + TREE_W
    d.rectangle([tab_x0, top, W, top + 30], fill=BG_TAB)
    tab_w = min(int(d.textlength(code_filename, font=F_UI)) + 62, W - tab_x0 - 10)
    d.rectangle([tab_x0, top, tab_x0 + tab_w, top + 30], fill=BG_TAB_ACTIVE)
    d.rectangle([tab_x0, top + 27, tab_x0 + tab_w, top + 30], fill=ACCENT)
    file_icon_color = SYN_TAG if code_filename.endswith(".xml") else (100, 150, 200)
    d.rectangle([tab_x0 + 10, top + 9, tab_x0 + 20, top + 19], fill=file_icon_color)
    d.text((tab_x0 + 26, top + 6), code_filename, font=F_UI, fill=FG_TEXT)
    close_x = tab_x0 + 26 + d.textlength(code_filename, font=F_UI) + 10
    d.text((close_x, top + 6), "\u00D7", font=F_UI, fill=FG_DIM)
    _dots_vertical(d, W - 20, top + 15, FG_DIM)
    d.line([tab_x0, top + 30, W, top + 30], fill=LINE_DARK)

    editor_top = top + 30

    # ---- "Gradle files have changed" notification banner (Android Studio
    # project files only -- authentic detail from the user's own screenshot) ----
    notif_h = 0
    if tool_name == "Android Studio":
        notif_h = 34
        d.rectangle([tab_x0, editor_top, W, editor_top + notif_h], fill=BG_NOTIFBAR)
        msg = "Gradle files have changed since last project sync. A project sync may be necessar..."
        d.text((tab_x0 + 12, editor_top + 10), msg, font=F_SMALL, fill=FG_TEXT)
        mx = tab_x0 + 12 + d.textlength(msg, font=F_SMALL) + 16
        d.text((mx, editor_top + 10), "Sync Now", font=F_SMALL, fill=LINK_BLUE)
        mx += d.textlength("Sync Now", font=F_SMALL) + 16
        d.text((mx, editor_top + 10), "Ignore these changes", font=F_SMALL, fill=LINK_BLUE)
    editor_top += notif_h

    # ---- editor gutter + syntax-highlighted code ----
    gutter_w = 50
    footer_h = 26  # for "Text | Merged Manifest"-style bottom editor tabs
    d.rectangle([tab_x0, editor_top, tab_x0 + gutter_w, H - 22 - footer_h], fill=BG_GUTTER)

    line_h = 22
    code_x = tab_x0 + gutter_w + 12
    y = editor_top + 8
    CODE_BOTTOM_LIMIT = H - 22 - footer_h - 20
    comment_state = [initial_comment_state]  # tracks an unclosed /* ... */ across lines in this visible slice
    for i, line in enumerate(code_lines):
        if y > CODE_BOTTOM_LIMIT:
            d.text((code_x, y), "  ...", font=F_CODE, fill=FG_DIM)
            break
        lineno = start_line_no + i
        d.text((tab_x0 + 10, y), str(lineno), font=F_LINENO, fill=FG_DIM)
        safe_line = line if len(line) <= 100 else line[:97] + "..."
        _highlight_line(d, code_x, y, safe_line, F_CODE, code_filename, comment_state)
        y += line_h

    # ---- bottom editor sub-tabs (Text / Merged Manifest, only for XML) ----
    subtab_y = H - 22 - footer_h
    d.rectangle([tab_x0, subtab_y, W, subtab_y + footer_h], fill=BG_TITLEBAR)
    if code_filename.endswith(".xml"):
        d.rectangle([tab_x0 + 8, subtab_y + 4, tab_x0 + 60, subtab_y + footer_h - 4], outline=LINE_DARK)
        d.text((tab_x0 + 16, subtab_y + 6), "Text", font=F_SMALL, fill=FG_TEXT)
        d.text((tab_x0 + 76, subtab_y + 6), "Merged Manifest", font=F_SMALL, fill=FG_DIM)

    # ---- bottom status bar ----
    sb_y = H - 22
    d.rectangle([0, sb_y, W, H], fill=BG_STATUSBAR)
    breadcrumb = f"{project_name}  \u203A  {module_name}  \u203A  src  \u203A  main  \u203A  {code_filename}"
    d.text((10, sb_y + 4), breadcrumb, font=F_SMALL, fill=FG_DIM)
    right_status = f"{len(code_lines) + start_line_no - 1}:1     CRLF     UTF-8     4 spaces"
    rw = d.textlength(right_status, font=F_SMALL)
    d.text((W - rw - 12, sb_y + 4), right_status, font=F_SMALL, fill=FG_DIM)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    return out_path


def make_terminal_diagram(out_path, title, log_lines, max_lines=40):
    """
    A dark terminal/logcat mock-up showing real captured output text
    (verbatim platform analysis log, or a real script run), styled to match
    Android Studio's own "Run" panel (green checkmark + monospace output).
    """
    line_h = 20
    body_h = max(120, min(len(log_lines), max_lines) * line_h + 70)
    h = 66 + body_h
    img = Image.new("RGB", (W, h), BG_RUNPANEL)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W - 1, 32], fill=BG_TITLEBAR)
    _android_head(d, 14, 16, GREEN_OK)
    d.text((26, 8), "\u2261", font=F_UI_BOLD, fill=FG_TEXT)
    d.text((48, 8), title, font=F_UI_BOLD, fill=FG_TEXT)
    _window_controls(d, W - 114, 10, FG_DIM)

    d.rectangle([0, 32, W - 1, 62], fill=BG_EDITOR)
    d.polygon([(12, 38), (12, 52), (23, 45)], fill=GREEN_OK)
    d.text((30, 39), "Run", font=F_UI_BOLD, fill=FG_TEXT)
    d.line([0, 62, W, 62], fill=LINE_DARK)

    y = 74
    for i, line in enumerate(log_lines[:max_lines]):
        safe_line = line if len(line) <= 150 else line[:147] + "..."
        d.text((16, y), safe_line, font=F_CODE, fill=(163, 219, 138))
        y += line_h
    if len(log_lines) > max_lines:
        d.text((16, y), f"  ... [{len(log_lines) - max_lines} more lines omitted]", font=F_CODE, fill=FG_DIM)
        y += line_h

    d.rectangle([0, h - 24, W, h], fill=BG_STATUSBAR)
    _check(d, 10, h - 18, GREEN_OK, size=9)
    d.text((24, h - 20), "Process finished", font=F_SMALL, fill=GREEN_OK)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    return out_path


def _wrap_text(draw, text, x, y, max_w, font, fill):
    words = text.split(" ")
    line = ""
    cy = y
    for w in words:
        test = (line + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_w and line:
            draw.text((x, cy), line, font=font, fill=fill)
            cy += 18
            line = w
        else:
            line = test
    if line:
        draw.text((x, cy), line, font=font, fill=fill)
