# ratios: loc_comments=70:5 imports_exports=9:1 calls_definitions=42:1
"""Verify UCHC's paired epicycle results and Stack's 16 b rad profile.

Usage: python -I integration/uchc/verify_halving.py WHEEL STACK_UCNS_ROOT
after installing the wheel and its pinned halving producer in this interpreter.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from importlib.metadata import distribution
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
from zipfile import ZipFile

import uchc_halving as h


def verify(wheel, stack_native):
    workspace = Path(__file__).resolve().parents[2]
    lock = Path(__file__).with_name('halving-requirements.txt').read_text().strip()
    url, expected = lock.removeprefix('uchc @ ').split(' --hash=sha256:')
    actual = sha256(wheel.read_bytes()).hexdigest()
    if wheel.name != url.rsplit('/', 1)[1] or actual != expected:
        raise ValueError('RELEASE_WHEEL_MISMATCH')
    base = json.loads((workspace / 'research/english-gonol/BASE.json').read_text())['ordinal_halving_consumer']
    graph = json.loads((workspace / 'stack-manifest.json').read_text())
    rows = {r['participant_id']: r for r in graph['research_participants']
            if r['workspace'] == 'integration/uchc/'}
    if (base['wheel_url'] != url or base['wheel_sha256'] != actual
            or rows['ordinal-halving-wheel']['artifact_sha256'] != actual
            or base['source_commit'] != rows['ordinal-halving-language']['commit']
            or base['geometry_commit'] != h.authority()['commit']
            or rows['ordinal-halving-geometry']['commit'] != base['geometry_commit']):
        raise ValueError('HALVING_WORK_GRAPH_MISMATCH')
    installed = distribution('uchc')
    with ZipFile(wheel) as archive:
        for name in archive.namelist():
            if '.dist-info/' not in name and not name.endswith('/'):
                if archive.read(name) != Path(installed.locate_file(name)).read_bytes():
                    raise ValueError('INSTALLED_RELEASE_MISMATCH')
        if archive.read('uchc_halving/__init__.py') != Path(h.__file__).read_bytes():
            raise ValueError('SHADOWED_HALVING_IMPORT')
    word = h.construct_text('bull')
    expected_radii = [Fraction(1, d) for d in (16, 8, 4, 2)]
    if [ray.radius for ray in word.rays] != expected_radii:
        raise ValueError('ORDINAL_HALVING_REQUIRED')
    phrase = h.construct_sequence((word, word), placement_radius=3)
    packet = h.closed_record(phrase)
    copy = h.replay_closed(packet)
    first, second = (p.interior for p in copy.participants)
    if ([r.radius for r in copy.rays] != [Fraction(3, 4), Fraction(3, 2)]
            or first is not second or first.rays != word.rays or ''.join(copy.recover()) != 'bullbull'):
        raise ValueError('RECURSIVE_HALVING_REQUIRED')
    endpoint = h.resultant(copy)
    additive = h.additive_resultant(copy)
    if (additive != h.additive_resultant(word).scaled(6) or endpoint == additive
            or packet['record_version'] != 2 or packet['vectors'] != {
                'placement_endpoint': endpoint.record(), 'additive_resultant': additive.record()}):
        raise ValueError('PAIRED_EPICYCLE_RESULTS_REQUIRED')
    # Exercise the source-owned Stack research adapter alongside the installed package.
    src = workspace / 'research/english-gonol/english_gonol/unicode_construction.py'
    spec = spec_from_file_location('stack_bit_radius', src)
    research = module_from_spec(spec)
    spec.loader.exec_module(research)
    glyph = research.construct_glyph('A', ucns_source_root=stack_native)
    if glyph.bit_radius != 16 or glyph.utf32_be != bytes.fromhex('00 00 00 41'):
        raise ValueError('STACK_ENCODING_DRIFT')
    return {'profile': h.PROFILE, 'version': installed.version, 'wheel_sha256': actual,
            'source': url, 'glyph_radii': [str(r.radius) for r in word.rays],
            'closed_word_radii': [str(r.radius) for r in copy.rays],
            'word_receipt': word.receipt, 'sentence_receipt': copy.receipt,
            'epicycle_vectors': packet['vectors'],
            'stack_bit_radius': glyph.bit_radius, 'stack_A_hex': glyph.utf32_be.hex()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('wheel', type=Path)
    parser.add_argument('stack_native', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.wheel, args.stack_native), sort_keys=True))
# ratios: loc_comments=70:5 imports_exports=9:1 calls_definitions=42:1
