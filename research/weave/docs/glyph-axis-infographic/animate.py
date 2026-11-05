# === MODULE_BUILD ===
# id: weave_glyph_axis_animation
#   module_kind: documentation-renderer
#   summary: animate the existing glyph address and eight-axis construction figure
#   owner: The-Interdependency/stack
#   public_surface: CLI --ucns-source PATH --output PATH
#   storage_boundary: GIF and animation-evidence.json in the selected output directory
#   network_boundary: none
#   tests: native fixture, 512 cube addresses, all three slice families, GIF decode
#   rollout: companion to the existing static infographic
#   rollback: remove animation exports, renderer and README links
#   unresolved: glyph matching and deletion; higher-axis native closure
# === END MODULE_BUILD ===
"""Make a looping, source-verified illustration; retain the static alternative.

Usage: python animate.py --ucns-source /checkout/ucns/src/ucns/ordinal_affixiation.py
Requires the existing render.py, Python 3.12+, Pillow and Matplotlib. No network.
The 4–8 axis frames are grouped schematics with exact counts, not spatial models.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import PIL
from PIL import Image, ImageDraw, ImageFont
from matplotlib.font_manager import FontProperties, findfont

import render as source

W, H, SCALE = 720, 1040, 2
COLORS = dict(bg='#F5F3EE', ink='#162C42', muted='#536578', line='#CBD3D9',
              white='#FFFFFF', teal='#006B61', pale='#E0F0EB', violet='#65449C',
              lavender='#EEE8F7', blue='#D9E5EC')
FONT = Path(findfont(FontProperties(family='DejaVu Sans')))
BOLD = Path(findfont(FontProperties(family='DejaVu Sans', weight='bold')))
FONTS = {}


def rgb(c):
    c = COLORS.get(c, c)
    return tuple(int(c[i:i+2], 16) for i in (1, 3, 5))


def font(n, bold=False):
    key = (n, bold)
    if key not in FONTS:
        FONTS[key] = ImageFont.truetype(str(BOLD if bold else FONT), round(n*SCALE))
    return FONTS[key]


class Canvas:
    def __init__(self, step, title, subtitle):
        self.image = Image.new('RGB', (W*SCALE, H*SCALE), rgb('bg'))
        self.draw = ImageDraw.Draw(self.image)
        self.text(36, 31, 'WHOLE GLYPHS · NEW AXES', 17, 'teal', True)
        self.text(36, 72, title, 34, bold=True)
        self.text(36, 126, subtitle, 21, 'muted')
        self.line([(36, 952), (684, 952)], 'line', 1)
        labels = ('Turn', 'Stack', 'Slice', 'Extend')
        for i, label in enumerate(labels):
            x = 36 + i*166
            self.rect(x, 969, 144, 5, 'teal' if i == step else 'line', radius=2)
            self.text(x, 984, label, 16, 'teal' if i == step else 'muted', i == step)
        self.text(36, 1016, 'GPT generated; context, prompt Erin Spencer.', 12, 'muted')

    def text(self, x, y, s, n=24, color='ink', bold=False, anchor='la'):
        self.draw.text((round(x*SCALE), round(y*SCALE)), str(s), font=font(n, bold),
                       fill=rgb(color), anchor=anchor)

    def rect(self, x, y, w, h, fill='white', edge=None, radius=0, width=1):
        box = tuple(round(v*SCALE) for v in (x, y, x+w, y+h))
        self.draw.rounded_rectangle(box, radius=round(radius*SCALE), fill=rgb(fill),
                                   outline=rgb(edge) if edge else None, width=round(width*SCALE))

    def line(self, points, color='line', width=1):
        self.draw.line([(round(x*SCALE), round(y*SCALE)) for x, y in points],
                       fill=rgb(color), width=round(width*SCALE))

    def polygon(self, points, fill='white', edge='line', width=1):
        p = [(round(x*SCALE), round(y*SCALE)) for x, y in points]
        self.draw.polygon(p, fill=rgb(fill))
        self.draw.line(p+[p[0]], fill=rgb(edge), width=round(width*SCALE))

    def finish(self):
        return self.image.resize((W, H), Image.Resampling.LANCZOS)


def ease(t):
    t = min(1., max(0., t))
    return t*t*(3-2*t)


def turn(angle):
    c = Canvas(0, 'A row becomes a column', '64 whole glyph occurrences · clockwise address turn')
    cx, cy, unit = 360, 475, 45
    a = math.radians(angle)
    co, si = math.cos(a), math.sin(a)
    def point(x, y):
        return (cx+co*x-si*y, cy+si*x+co*y)
    for r in range(8):
        for col in range(8):
            x, y = (col-3.5)*unit, (r-3.5)*unit
            chosen, selected = r == 0, (r == 0 and col == 2)
            corners = [point(x+u, y+v) for u, v in [(-21,-21),(21,-21),(21,21),(-21,21)]]
            c.polygon(corners, 'lavender' if selected else 'pale' if chosen else 'white',
                      'violet' if selected else 'teal' if chosen else 'line', 2 if chosen else 1)
            px, py = point(x, y)
            c.text(px, py-5, source.GLYPHS[col], 26, 'violet' if selected else 'ink', selected, 'mm')
            c.text(px, py+15, 8*r+col, 10, 'muted', anchor='mm')
    c.text(360, 181, f'{round(angle):d}° clockwise', 25, 'teal', True, 'ma')
    c.rect(36, 755, 648, 160, radius=18)
    c.text(60, 776, 'Ω #2 keeps its identity.', 27, 'violet', True)
    if abs(angle-90) < .01:
        detail = 'Row 0, column 2  →  row 2, column 7'
    elif abs(angle-360) < .01:
        detail = 'Four turns: all 64 return to their original addresses.'
    else:
        detail = 'The numbered occurrence moves with the whole glyph.'
    c.text(60, 822, detail, 20)
    c.text(60, 864, 'Letters stay upright as reading labels.', 20, 'muted')
    return c.finish()


def stack(t):
    c = Canvas(1, 'Eight squares form a cube', '8 × 8 × 8 = 512 addressed glyph occurrences')
    for z in reversed(range(8)):
        reveal = ease(t*9-z)
        if reveal <= 0:
            continue
        ox, oy = 103+z*23, 365-z*20 - (1-reveal)*110
        c.rect(ox, oy, 322, 322, 'white', 'teal', radius=3, width=2)
        for y in range(8):
            for x in range(8):
                c.rect(ox+x*40+2, oy+y*40+2, 38, 38, 'pale' if x == 2 else 'white', 'line')
                c.text(ox+x*40+21, oy+y*40+21, source.GLYPHS[x], 21, anchor='mm')
        c.rect(ox+327, oy+2, 58, 31, 'bg', radius=5)
        c.text(ox+356, oy+5, f'z={z}', 19, 'teal', True, 'ma')
    c.rect(36, 755, 648, 160, radius=18)
    c.text(60, 776, 'Every extra coordinate locates an occurrence.', 23, bold=True)
    c.text(60, 821, 'Next, follow Ω #234 at (x=2, y=5, z=3).', 23, 'violet', True)
    c.text(60, 865, 'Equal glyph labels can have different addresses.', 20, 'muted')
    return c.finish()


def slice_view(view, u):
    # xy: row y, col x; xz: row z, col x; yz: row z, col y.
    axes = [('x–y', 'z=3', 'y', 'x', 5, 2),
            ('x–z', 'y=5', 'z', 'x', 3, 2),
            ('y–z', 'x=2', 'z', 'y', 3, 5)]
    name, fixed, rows, cols, rp, cp = axes[view]
    c = Canvas(2, 'One object, three slice views', 'P = Ω #234 · (x=2, y=5, z=3) stays fixed')
    c.rect(36, 180, 648, 126, radius=18)
    c.text(60, 199, f'{name} slice  ·  fix {fixed}', 29, 'teal', True)
    c.text(60, 251, f'Rows: {rows}     Columns: {cols}     P: row {rp}, column {cp}', 21)
    left, top, cell = 148, 380, 53
    c.text(360, 331, f'column coordinate {cols}', 21, 'muted', anchor='ma')
    for i in range(8):
        c.text(left+(i+.5)*cell, top-21, i, 18, 'muted', anchor='mm')
        c.text(left-27, top+(i+.5)*cell, i, 18, 'muted', anchor='mm')
    for r in range(8):
        for col in range(8):
            x,y,z = (col,r,3) if view == 0 else (col,5,r) if view == 1 else (2,col,r)
            selected = (r,col) == (rp,cp)
            c.rect(left+col*cell, top+r*cell, cell-2, cell-2,
                   'lavender' if selected else 'pale' if col == cp else 'white',
                   'violet' if selected else 'teal' if col == cp else 'line', radius=4,
                   width=2 if col == cp else 1)
            c.text(left+(col+.5)*cell, top+(r+.5)*cell-5, source.GLYPHS[x], 27,
                   'violet' if selected else 'ink', selected, 'mm')
            c.text(left+(col+.5)*cell, top+(r+.5)*cell+16, 64*z+8*y+x, 11,
                   'violet' if selected else 'muted', anchor='mm')
    # A traveling margin marker draws attention to the entire selected column.
    yy = top+ease(u)*7*cell+cell/2
    c.line([(left+cp*cell-7, yy-7), (left+cp*cell-2, yy), (left+cp*cell-7, yy+7)], 'teal', 3)
    c.text(36, 840, f'Highlighted column: vary {rows}, keep the other coordinates.', 21, 'teal', True)
    text = ('8 occurrences on a y-directed line.' if view == 0 else
            'This is the z-directed line through P.' if view == 1 else
            'Same z-line as the previous view: count it once.')
    c.text(36, 882, text, 22)
    return c.finish()


def extend(d, t):
    c = Canvas(3, f'{d} axes · eight groups', 'Each group contains the complete preceding arrangement.')
    c.text(36, 185, f'New coordinate a{d}: choose one of eight slots', 23, 'teal', True)
    active = min(8, max(1, int(t*8)+1))
    for k in range(8):
        x, y = 36+(k%4)*166, 263+(k//4)*186
        on = k < active
        c.rect(x, y, 148, 161, 'white' if on else 'bg', 'teal' if on else 'line', radius=12, width=2)
        c.text(x+74, y+14, f'slot {k}', 19, 'teal' if on else 'muted', True, 'ma')
        if on:
            for j in range(8):
                c.rect(x+28+(j%4)*25, y+53+(j//4)*25, 17, 17, 'pale', 'teal', radius=3)
            c.text(x+74, y+114, f'{d-1} axes', 21, 'ink', True, 'ma')
    c.text(360, 646, f'8 × {8**(d-1):,} = {8**d:,} occurrences', 27, bold=True, anchor='ma')
    c.rect(36, 707, 648, 134, radius=18)
    c.text(60, 726, 'Axis-aligned 8-cell lines', 21, 'muted')
    c.text(660, 724, f'{d*8**(d-1):,}', 26, 'teal', True, 'ra')
    c.text(60, 785, '8 × 8 square slices', 21, 'muted')
    c.text(660, 783, f'{math.comb(d,2)*8**(d-2):,}', 26, 'teal', True, 'ra')
    c.text(36, 867, 'Grouping schematic · counts describe all eight slots.', 21, 'muted')
    c.text(36, 907, 'hmmm: whole-glyph matching and deletion remain open.', 19)
    return c.finish()


def verify_cube():
    module = sys.modules['_verified_ucns_ordinal_for_figure']
    carrier = module.Carrier(source.GLYPHS, 'weave:glyph-axis-figure:illustrative-order-v1')
    atoms = tuple(module.Participant.atom(carrier, g) for g in source.GLYPHS)
    cube = tuple(tuple(tuple((64*z+8*y+x, atoms[x]) for x in range(8))
                       for y in range(8)) for z in range(8))
    cells = [cube[z][y][x] for z in range(8) for y in range(8) for x in range(8)]
    assert len({a[0] for a in cells}) == 512
    xy = [tuple(tuple(cube[z][y][x] for x in range(8)) for y in range(8)) for z in range(8)]
    xz = [tuple(tuple(cube[z][y][x] for x in range(8)) for z in range(8)) for y in range(8)]
    yz = [tuple(tuple(cube[z][y][x] for y in range(8)) for z in range(8)) for x in range(8)]
    for z in range(8):
        for y in range(8):
            for x in range(8):
                assert xy[z][y][x] is xz[y][z][x] is yz[x][z][y] is cube[z][y][x]
                assert cube[z][y][x][1] is atoms[x]
    assert all(xz[5][z][2] is yz[2][z][5] for z in range(8))
    assert cube[3][5][2][0] == 234
    return dict(native_occurrences=512, native_object_references_retained=True,
                all_three_slice_families_checked=True, slice_memberships_checked=1536,
                selected_occurrence=234, selected_xyz=[2,5,3],
                xz_yz_highlighted_columns_same_physical_line=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ucns-source', type=Path, required=True)
    p.add_argument('--output', type=Path, default=Path(__file__).parent)
    a = p.parse_args()
    evidence = source.checked_example(a.ucns_source)
    cube_evidence = verify_cube()
    a.output.mkdir(parents=True, exist_ok=True)
    frames, durations = [], []
    # Fixed palette prevents color changes between frames; no dithering or flashes.
    palette = []
    for base in ('ink','muted','teal','violet','line','pale','lavender','blue'):
        fg, bg = rgb(base), rgb('bg')
        for i in range(30):
            palette.extend(round(bg[j]+(fg[j]-bg[j])*i/29) for j in range(3))
    for key in COLORS:
        palette.extend(rgb(key))
    palette = (palette+[255]*768)[:768]
    pal = Image.new('P',(1,1)); pal.putpalette(palette)
    def add(image, ms=80):
        frames.append(image.quantize(palette=pal, dither=Image.Dither.NONE))
        durations.append(ms)
    add(turn(0), 1600)
    for i in range(1,31): add(turn(90*ease(i/30)))
    add(turn(90), 2000)
    for i in range(1,46): add(turn(90+270*ease(i/45)))
    add(turn(360), 1500)
    for i in range(41): add(stack(i/40))
    add(stack(1), 1600)
    for v in range(3):
        for i in range(26): add(slice_view(v,i/25))
        add(slice_view(v,1), 1800)
    for d in range(4,9):
        for k in range(8): add(extend(d,k/8), 160)
        add(extend(d,1), 1200 if d < 8 else 2800)
    gif = a.output/'glyph-axis-animation.gif'
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, disposal=1, optimize=True)
    with Image.open(gif) as decoded:
        total_ms = 0
        for n in range(decoded.n_frames):
            decoded.seek(n); decoded.load()
            assert decoded.size == (W,H)
            total_ms += decoded.info['duration']
        assert total_ms == sum(durations)
        frame_count = decoded.n_frames
        assert decoded.info['loop'] == 0
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    receipt = dict(schema='weave.glyph-axis-animation-evidence.v1',
        classification='ANIMATED_ADDRESS_ILLUSTRATION_WITH_EXACT_CHECKS',
        stack_base='dceea8fd9996363e192c255d790f92312773cb1f',
        static_fixture=evidence, cube_fixture=cube_evidence,
        output=dict(file=gif.name, sha256=digest(gif), bytes=gif.stat().st_size,
                    width=W,height=H,decoded_frames=frame_count,duration_ms=total_ms,
                    loop='infinite',all_frames_decoded=True),
        sources=dict(renderer_sha256=digest(Path(__file__)),
                     static_renderer_sha256=digest(Path(source.__file__)),
                     font_sha256=digest(FONT),bold_font_sha256=digest(BOLD)),
        environment=dict(python=sys.version.split()[0],pillow=PIL.__version__),
        hmmm=['4–8 axes are grouping schematics, not native higher-axis closure.',
              'Glyph matching, retained-interior predicates and deletion remain open.'])
    (a.output/'animation-evidence.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt['output'],indent=2))


if __name__ == '__main__':
    main()
