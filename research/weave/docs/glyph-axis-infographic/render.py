# === MODULE_BUILD ===
# id: weave_glyph_axis_infographic
#   module_kind: documentation-renderer
#   summary: draw the declared glyph-cell arrangement and exact lattice counts
#   owner: The-Interdependency/stack
#   public_surface: CLI --ucns-source PATH --output PATH
#   auth_boundary: none
#   storage_boundary: writes figure exports and evidence to the selected directory
#   network_boundary: none
#   user_data_boundary: fixed illustrative glyphs only
#   tests: exact producer identity, all 64 address moves, four-turn recovery, count formulae
#   rollout: documentation only; no cipher or UCNS producer changes
#   rollback: remove this documentation bundle and its README link
#   requires: Python 3.12+, matplotlib, Pillow; exact UCNS ordinal_affixiation.py
#   unresolved: glyph matching and deletion rules; higher-axis native closure
# === END MODULE_BUILD ===
"""Render a source-bound explanatory figure, not a cipher or glyph census.

Usage: python render.py --ucns-source /checkout/ucns/src/ucns/ordinal_affixiation.py
The exact source blob below is required; the renderer does not fetch or replace it.
Outputs: glyph-axis-infographic.svg, .png, .pdf and evidence.json.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch

UCNS_COMMIT = '3f97f5292b0bd2dab911540062ccf79dea2be1bf'
UCNS_BLOB = '9fa84ef20f19fe0c04df680f49b50ea307e6d624'
STACK_BASE = '37e493d194651ca45c7bc3fbd6327f653df6879e'
GLYPHS = ('A', 'é', 'Ω', 'Ж', 'λ', 'π', 'ß', '→')
W, H = 1100, 2550
C = dict(paper='#F5F3EE', white='#FFFFFF', ink='#162C42', muted='#536578',
         line='#CBD3D9', teal='#006B61', pale='#E0F0EB', violet='#65449C',
         lavender='#EEE8F7', soft='#F1F3F5')


def checked_example(path: Path) -> dict:
    raw = path.read_bytes()
    sha = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
    if sha != UCNS_BLOB:
        raise ValueError(f'UCNS producer drift: {sha} != {UCNS_BLOB}')
    name = '_verified_ucns_ordinal_for_figure'
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    carrier = module.Carrier(GLYPHS, 'weave:glyph-axis-figure:illustrative-order-v1')
    objects = tuple(module.Participant.atom(carrier, g) for g in GLYPHS)
    # The tuple is an occurrence wrapper, not a replacement UCNS object.
    square = tuple(tuple((8*r+c, objects[c]) for c in range(8)) for r in range(8))
    def rotate(a):
        return tuple(tuple(a[7-c][r] for c in range(8)) for r in range(8))
    moved = rotate(square)
    for r in range(8):
        for c in range(8):
            if moved[c][7-r] is not square[r][c]:
                raise AssertionError('native occurrence was replaced or moved incorrectly')
    restored = square
    for _ in range(4):
        restored = rotate(restored)
    if not all(restored[r][c] is square[r][c] for r in range(8) for c in range(8)):
        raise AssertionError('four rotations failed to recover object references')
    counts = [dict(axes=d, occurrences=8**d, lines=d*8**(d-1),
                   square_slices=comb(d, 2)*8**(d-2)) for d in range(2, 9)]
    return dict(schema='weave.glyph-axis-figure-evidence.v1',
        classification='ILLUSTRATION_WITH_EXACT_COUNTS_AND_64_OCCURRENCE_CHECK',
        ucns_commit=UCNS_COMMIT, ucns_blob=sha, producer_sha256=hashlib.sha256(raw).hexdigest(),
        stack_base=STACK_BASE, glyphs=list(GLYPHS), carrier_receipt=carrier.receipt,
        carrier_scope='Explicit eight-identity example; not the Public Gonol arrangement',
        rotation='(row,column) -> (column,7-row)', moved_occurrences=64,
        original_native_objects_retained=True, four_turn_identity=True,
        dimensions=counts,
        distinction='Occurrence address rotation is not internal UCNS orientation transport.',
        hmmm=['Matching/deletion predicates for glyph interiors and whole objects remain distinct.',
              'Higher-axis native UCNS closure and Unicode-wide frequencies were not tested.'])


def contrast(a, b):
    def lum(h):
        vals = [int(h[i:i+2], 16)/255 for i in (1, 3, 5)]
        vals = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in vals]
        return sum(v*w for v, w in zip(vals, (.2126, .7152, .0722)))
    x, y = sorted((lum(a), lum(b)))
    return (y+.05)/(x+.05)


def render(out: Path, evidence: dict):
    plt.rcParams.update({'font.family':'DejaVu Sans', 'svg.fonttype':'path',
                         'svg.hashsalt':'weave-glyph-axis-v1', 'pdf.fonttype':42})
    fig = plt.figure(figsize=(11, 25.5), dpi=140, facecolor=C['paper'])
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
    def text(x, y, s, size=23, color='ink', weight='normal', ha='left', va='top', **kw):
        return ax.text(x, y, s, fontsize=size*.72, color=C.get(color, color),
                       weight=weight, ha=ha, va=va, **kw)
    def box(x, y, w, h, face='white', edge=None, radius=20, lw=1.5):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={radius}',
            facecolor=C.get(face, face), edgecolor=C.get(edge,edge) if edge else 'none', linewidth=lw))
    def small_label(x, y, s, color='muted'):
        text(x, y, s, 16, color, 'bold')
    def grid(x, y, after=False):
        cell=42
        for r in range(8):
            for c in range(8):
                sr, sc = (7-c, r) if after else (r, c)
                highlight = sr == 0
                ax.add_patch(Rectangle((x+c*cell,y+r*cell),cell,cell,
                    facecolor=C['pale'] if highlight else C['white'],
                    edgecolor=C['teal'] if highlight else C['line'], linewidth=1.4 if highlight else .65))
                text(x+(c+.5)*cell,y+r*cell+6,GLYPHS[sc],23,'ink',ha='center')
                # Ordinals redundantly identify each repeated glyph occurrence.
                text(x+(c+.5)*cell,y+r*cell+30,str(8*sr+sc),9,'muted',ha='center')
        for i in range(8):
            text(x+(i+.5)*cell,y-21,str(i),13,'muted',ha='center')
            text(x-17,y+(i+.5)*cell,str(i),13,'muted',ha='center',va='center')
        rr, cc = (2,7) if after else (0,2)
        ax.add_patch(Rectangle((x+cc*cell+1.5,y+rr*cell+1.5),cell-3,cell-3,
                              fill=False,edgecolor=C['violet'],linewidth=3))
    def slice_grid(x, y, row, col, row_axis, col_axis, title):
        text(x+112,y-48,title,20,'ink','bold',ha='center')
        cell=28
        for r in range(8):
            for c in range(8):
                ax.add_patch(Rectangle((x+c*cell,y+r*cell),cell,cell,
                    facecolor=C['pale'] if c==col else C['white'],
                    edgecolor=C['line'],linewidth=.7))
        ax.add_patch(Rectangle((x+col*cell,y),cell,8*cell,fill=False,
                              edgecolor=C['teal'],linewidth=1.8))
        ax.add_patch(Circle((x+(col+.5)*cell,y+(row+.5)*cell),9,facecolor=C['violet']))
        text(x+(col+.5)*cell,y+(row+.5)*cell,'P',12,'white','bold',ha='center',va='center')
        for i in range(8):
            text(x+(i+.5)*cell,y-18,str(i),11,'muted',ha='center')
            text(x-12,y+(i+.5)*cell,str(i),11,'muted',ha='center',va='center')
        text(x+112,y+241,f'rows {row_axis} · columns {col_axis}',18,'muted',ha='center')
    small_label(60,40,'THE INTERDEPENDENCY / WEAVE · CONSTRUCTION VIEW')
    text(60,80,'Whole glyphs. New axes.',58,'ink','bold')
    text(60,157,'Eight positions per axis. Every occurrence stays addressable.',26,'muted')

    box(50,220,1000,275)
    small_label(80,244,'DECLARED UNIT')
    text(80,275,'Each cell holds a whole UCNS object.',32,'ink','bold')
    box(82,333,110,110,'lavender',radius=14)
    text(137,344,'Ω',56,'violet',ha='center')
    text(137,408,'occurrence #2',13,'ink',ha='center')
    text(225,337,'Glyph identity + retained construction + provenance',24,'ink','bold')
    text(225,380,'Its address records where this occurrence participates.',22,'muted')
    text(80,459,'Equal glyphs can recur; their occurrence addresses remain distinct.',22,'ink')

    box(50,520,1000,620)
    small_label(80,544,'ADDRESS ROTATION')
    text(80,578,'The row becomes a column.',34,'ink','bold')
    small_label(106,627,'BEFORE')
    small_label(652,627,'AFTER')
    grid(106,690); grid(652,690,True)
    text(545,802,'90°',31,'teal','bold',ha='center')
    text(545,842,'clockwise',17,'ink',ha='center')
    ax.add_patch(FancyArrowPatch((468,888),(621,888),arrowstyle='-|>',mutation_scale=22,
                                color=C['teal'],linewidth=2))
    text(545,932,'(r, c)',18,'muted',ha='center')
    text(545,957,'↓',22,'teal',ha='center')
    text(545,988,'(c, 7 − r)',18,'muted',ha='center')
    text(80,1065,'Ω at (0, 2) → Ω at (2, 7). The same occurrence #2 moves.',23,'ink','bold')
    text(80,1101,'Four quarter-turns restore all 64 occurrences and their native objects.',21,'muted')

    box(50,1165,1000,515)
    small_label(80,1190,'EXACT COUNTS · AXIS-ALIGNED LINES AND SLICES')
    text(80,1223,'Add an axis: stack eight previous arrays.',31,'ink','bold')
    cols=[95,270,580,825]
    for x,s in zip(cols,['Axes d','Glyph occurrences','8-cell lines','8 × 8 slices']):
        text(x,1284,s,19,'muted','bold')
    for i,row in enumerate(evidence['dimensions']):
        y=1327+i*40
        if row['axes']==8: box(77,y-7,946,39,'pale',radius=7)
        weight='bold' if row['axes']==8 else 'normal'
        for x,key in zip(cols,['axes','occurrences','lines','square_slices']):
            text(x,y,f'{row[key]:,}',23,'ink',weight)
    text(80,1628,r'$8^d$ positions     $d\,8^{d-1}$ lines     $\binom{d}{2}8^{d-2}$ slices',23,'ink')

    box(50,1705,1000,490)
    small_label(80,1728,'SLICE + COLUMN INFORMATION')
    text(80,1762,'One occurrence, three coordinate views.',32,'ink','bold')
    text(80,1810,'Cube example: P = (x = 2, y = 5, z = 3).',23,'muted')
    slice_grid(100,1916,5,2,'y','x','Fix z = 3')
    slice_grid(439,1916,3,2,'z','x','Fix y = 5')
    slice_grid(778,1916,3,5,'z','y','Fix x = 2')

    box(50,2220,1000,237,'ink')
    text(80,2246,'What is established',28,'white','bold')
    text(80,2291,'CHECKED  ·  64 native glyph occurrences; exact address rotation.',22,'white')
    text(80,2326,'DERIVED  ·  Counts for 2–8 axes; full higher-axis closure remains open.',21,'white')
    text(80,2376,'hmmm: FF/00 tests bit interiors. Glyph matching needs its own',21,'white')
    text(80,2409,'declared relation. These measurements stay separately identified.',21,'white')
    text(60,2480,'UCNS 3f97f5292b0b · Stack 37e493d19465 · sources, scope and replay: README.md',16,'muted')
    text(60,2510,'GPT generated; context, prompt Erin Spencer.  •  04 November 2026',16,'muted')

    out.mkdir(parents=True,exist_ok=True)
    base=out/'glyph-axis-infographic'
    fig.savefig(base.with_suffix('.svg'),metadata={'Date':None,'Title':'Whole glyphs. New axes.',
        'Description':'Eight positions per axis; whole native glyph participants retain occurrence identities. See README.md for complete accessible text and evidence.'})
    fig.savefig(base.with_suffix('.png'),dpi=140,metadata={'Title':'Whole glyphs. New axes.'})
    fig.savefig(base.with_suffix('.pdf'),metadata={'CreationDate':None,'ModDate':None,
        'Title':'Whole glyphs. New axes.','Author':'GPT generated; context, prompt Erin Spencer'})
    plt.close(fig)
    pairs=[('ink','white'),('muted','white'),('ink','paper'),('muted','paper'),
           ('ink','pale'),('teal','white'),('violet','white'),('violet','lavender'),('white','ink')]
    evidence['text_contrast_ratios']={f'{a}/{b}':round(contrast(C[a],C[b]),3) for a,b in pairs}
    if min(evidence['text_contrast_ratios'].values())<4.5:
        raise AssertionError('text contrast below 4.5:1')
    evidence['figure_files']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (base.with_suffix('.svg'),base.with_suffix('.png'),base.with_suffix('.pdf'))}
    evidence['renderer_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    evidence['matplotlib_version']=matplotlib.__version__
    (out/'evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'outputs':list(evidence['figure_files']),'native_occurrences_checked':64,
                      'minimum_text_contrast':min(evidence['text_contrast_ratios'].values())}))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ucns-source',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args()
    render(args.output,checked_example(args.ucns_source))


if __name__=='__main__':
    main()
