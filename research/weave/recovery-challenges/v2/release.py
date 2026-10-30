# ratios: loc_comments=17:159 imports_exports=7:7 calls_definitions=50:7
"""Operator-only staged exports and exact-byte grading.

Run: python release.py release --private /operator --id OPAQUE_ID --level 0 --out /new/attempt
     python release.py grade --private /operator --id OPAQUE_ID --candidate /submission.bin
Give the attacker only the exported directory. File separation here is an information
protocol, not a sandbox. No original plaintext or answer digest is exported at any level.
"""
# === MODULE_BUILD ===
# id: challenge_disclosure
#   module_name: release
#   module_kind: instrument
#   summary: release cumulative case-specific clues without handing over evaluator answers
#   owner: Erin Spencer
#   public_surface: export, grade
#   internal_surface: source-copy allowlist and stage-specific parameter projections
#   tests: test_harness.py
#   rollout: operator controlled levels zero through six
#   rollback: stop releasing additional levels
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: staged_disclosure
#   given: a case and a requested clue level
#   then: export only cumulative authorized clues, never plaintext or an answer digest
# id: exact_grading
#   given: a frozen candidate submission
#   then: compare complete bytes without accepting readable prefixes or paraphrases
# === END CONTRACTS ===
from pathlib import Path
from hashlib import sha256
import argparse
import json
import shutil
import operations as o
from matrix import LINE

BASE = '''# Exact-byte recovery attempt

Recover the original bytes of `challenge.bin`. Save your candidate as a binary
file. Record your inputs, methods, elapsed time, resource use, and result. A readable
fragment is partial recovery; guessing a phrase is not exact recovery. Before
asking for another clue, freeze your code, candidate and attempt log. The evaluator
can check that frozen submission privately. Do not seek unreleased evaluator files.

An independent no-clue attempt requires a fresh context and only this level-zero
directory. Later levels are cumulative. Prior exposure from another challenge must
be recorded. No-clue means no supplied explanation; any structure naturally visible
in the bytes is fair evidence. There is no promise that every file conceals its text.
'''


def read_case(root, case_id):
    plan = json.loads((root/'private.json').read_text())
    matches = [r for r in plan['cases'] if r['id'] == case_id]
    if len(matches) != 1:
        raise ValueError('unknown or duplicate opaque case ID')
    return matches[0]


def structural(p):
    keys = ('scope', 'bucket_bytes', 'initial_lanes', 'thread_count', 'inter_arity')
    value = {k: p[k] for k in keys}
    value['spec'] = {k: p['spec'][k] for k in ('arities', 'end_order')}
    if 'rounds' in p:
        value['rounds'] = [{k: r[k] for k in ('arities', 'end_order')} for r in p['rounds']]
    return value


def clue_text(row, level):
    texts = [BASE]
    if level >= 1:
        texts.append('## Level 1 — family and scale\n\n'
            f"Family: `{row['family']}`. Forward primitive instances: {len(row['schedule'])}. "
            'The experiment uses reversible representations, native sequence placement, '
            'or permutations. There is no added conventional encryption wrapper. '
            'Repeated operations are allowed, with at most three uses of any one operation.\n')
    if level >= 2:
        texts.append('## Level 2 — exact source and formats\n\n'
            'The `source/` directory contains the pinned source and the actual adapters. '
            'Inspect WNM, WAF, WNC and WVC as applicable. The WRA1 adapter carries a '
            '32-byte native origin root before WAF. WLN1 transparently serializes bit lanes. '
            'N normalizes, A affixes native sequences, U writes a literal numeral packet, '
            'S applies prime-controlled section interleaving, W interleaves the whole stream, '
            'B reverses bits within bytes, R reverses each exact three-byte record. '
            'Historical transport: X splits, J joins, C routes from actual corpus bits, '
            'I applies balanced section interleaving. This is source disclosure; selected '
            'per-file parameters are still withheld.\n')
    if level >= 3:
        texts.append('## Level 3 — selected order and structural controls\n\n'
            f"Forward order: `{' '.join(row['schedule'])}`. Invert in reverse order. "
            'The `structure.json` file gives the selected scope, sizes and non-coordinate '
            'controls. Every stage consumes the previous stage output. WVC cycle records '
            'retain the unchanged native cycle framing. Other byte compositions use the '
            'explicit operations.py adapters. No encoder trace is supplied.\n')
    if level >= 4:
        texts.append('## Level 4 — known plaintext structure and targeted recovery advice\n\n'
            'The message is two UTF-8 lines, ending with LF. The first starts with '
            '`Prediction ` followed by a private random 32-character lowercase hex trial tag, '
            'a colon, a space, and an English probable-outcome prediction. Some first lines '
            'have trailing alignment spaces. The entire second line is:\n\n'
            f'```text\n{LINE}\n```\n\n'
            'U stores literal payloads. N stores a length at bytes 4:12 and then message '
            'bytes beginning at byte 44. Corpus checks happen after that representation '
            'is reconstructed. A stores literal definitions with circle coordinates; '
            'placement, not another hidden byte cipher, is the obstacle. S and W only '
            'reorder bits. B and R are involutions and commute with each other. '
            'Transport C consumes left/right source ends according to corpus bits. '
            'Use these facts to test equivalent schedules and intermediate-frame structure.\n')
    if level >= 5:
        texts.append('## Level 5 — selected geometry and route controls\n\n'
            '`parameters-without-corpus.json` supplies the exact selected parameters '
            'except corpus bytes: prime paths, circle order, spaces, offsets and lane '
            'rotation are now disclosed. Try recovering the content while bypassing '
            'validation that is not required to reconstruct bytes. This level does not '
            'claim these controls are public in the intended complete design.\n')
    if level >= 6:
        texts.append('## Level 6 — full receiver material\n\n'
            'All selected receiver inputs, including the corpus, are in `request.json`. '
            'This is key-assisted completion, not an unaided cryptanalytic break. '
            'The original message and its digest are still withheld. The supplied inverse '
            'uses only the ciphertext and these inputs. Run from this directory:\n\n'
            '```sh\npython3 source/research/weave/recovery-challenges/v2/operations.py receive '
            '--request request.json --output restored.bin\n```\n\n'
            'Submit restored.bin for exact private grading. If it fails, report a harness '
            'or environment error; do not invent plaintext or label the case secure.\n')
    return '\n'.join(texts)


def copy_sources(destination):
    lock = json.loads((o.HERE/'SOURCE.json').read_text())
    for row in lock['files']:
        target = destination/row['path']; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(o.CHECKOUT/row['path'], target)
    target = destination/'research/weave/recovery-challenges/v2'
    target.mkdir(parents=True, exist_ok=True)
    for name in ('SOURCE.json', 'operations.py', 'transport_cases.py'):
        shutil.copyfile(o.HERE/name, target/name)


def export(root, case_id, level, out):
    if type(level) is not int or level not in range(7):
        raise ValueError('level must be an integer zero through six')
    root, out = root.resolve(), out.absolute()
    if out.is_symlink() or out.exists() or out.resolve().is_relative_to(root):
        raise ValueError('use a new output directory outside the private archive')
    row = read_case(root, case_id)
    wire_path = root/'ciphertexts'/f'{case_id}.bin'
    if wire_path.is_symlink():
        raise ValueError('ciphertext may not be a symlink')
    out.mkdir(mode=0o700, parents=True)
    shutil.copyfile(wire_path, out/'challenge.bin')
    (out/'README.md').write_text(clue_text(row, level))
    if level >= 2:
        copy_sources(out/'source')
    if level >= 3:
        (out/'structure.json').write_text(json.dumps(structural(row['parameters']), indent=2)+'\n')
    if level >= 5:
        p = {k: v for k, v in row['parameters'].items() if k != 'corpus_hex'}
        (out/'parameters-without-corpus.json').write_text(json.dumps(p, indent=2)+'\n')
    if level >= 6:
        request = {k: row[k] for k in ('family', 'schedule', 'parameters')}
        request['wire_hex'] = wire_path.read_bytes().hex()
        (out/'request.json').write_text(json.dumps(request, indent=2)+'\n')
    return out


def grade(root, case_id, candidate):
    original = bytes.fromhex(read_case(root, case_id)['message_hex'])
    data = candidate.read_bytes()
    return {'exact': data == original, 'candidate_sha256': sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['release', 'grade'])
    parser.add_argument('--private', type=Path, required=True)
    parser.add_argument('--id', required=True)
    parser.add_argument('--level', type=int)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--candidate', type=Path)
    args = parser.parse_args()
    if args.command == 'release':
        if args.out is None:
            parser.error('--out required')
        print(export(args.private, args.id, args.level, args.out))
    else:
        if args.candidate is None:
            parser.error('--candidate required')
        print(json.dumps(grade(args.private, args.id, args.candidate)))


if __name__ == '__main__':
    main()
# ratios: loc_comments=17:159 imports_exports=7:7 calls_definitions=50:7
