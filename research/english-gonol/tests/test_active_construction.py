"""Run with pytest; routing witnesses do not claim complete-corpus replay."""
# === CHECKS ===
# id: english_active_routing_regression
#   proves: english_active_no_legacy_fallback
#   call: self::test_only_ordinal_routes
#   requires: python3, pytest
#   timeout: 60
#   mutates: monkeypatched in-memory functions only
#   cleanup: pytest monkeypatch
# id: english_active_profile_regression
#   proves: english_profile_without_compute
#   call: self::test_profile_and_help_do_not_load_constructor
#   requires: python3, pytest
#   timeout: 60
#   mutates: isolated subprocess only
#   cleanup: process exit
# === END CHECKS ===
import json
from pathlib import Path
import subprocess
import sys

import pytest
from english_gonol import __main__ as entry
from english_gonol import ordinal_construct


@pytest.mark.parametrize('args,method,expected', [
    (['build', 'admission', 'ucd', 'output'], 'build', (Path('admission'), Path('ucd'), Path('output'))),
    (['verify', 'output'], 'verify', (Path('output'),)),
    (['query', 'output', 'the geometry'], 'query', (Path('output'), 'the geometry')),
])
def test_only_ordinal_routes(monkeypatch, capsys, args, method, expected):
    calls = []
    def witness(*values):
        calls.append(values)
        return {'called': method}
    monkeypatch.setattr(ordinal_construct, method, witness)
    entry.main(args)
    assert calls == [expected]
    assert json.loads(capsys.readouterr().out) == {'called': method}


@pytest.mark.parametrize('command', ['legacy', 'structural', 'full-v2'])
def test_retired_commands_refuse(command):
    with pytest.raises(SystemExit) as error:
        entry.main([command])
    assert error.value.code == 2


def test_selection_drift_refuses(monkeypatch):
    selection = entry.active_profile()
    selection['active_profile'] = 'retired-profile'
    monkeypatch.setattr(entry, 'active_profile', lambda: selection)
    with pytest.raises(ValueError, match='no legacy fallback'):
        entry.main(['verify', 'never-opened'])


def test_profile_and_help_do_not_load_constructor():
    for args in (['profile'], ['--help']):
        script = ("import sys; from english_gonol.__main__ import main\n"
                  "try: main(" + repr(args) + ")\n"
                  "except SystemExit as exc: assert exc.code == 0\n"
                  "assert 'english_gonol.ordinal_construct' not in sys.modules\n")
        result = subprocess.run([sys.executable, '-c', script], text=True, capture_output=True)
        assert result.returncode == 0, result.stderr
        assert result.stdout


def test_active_selection_matches_exact_constructor():
    profile = entry.active_profile()
    assert profile['active_profile'] == ordinal_construct.PROFILE
    assert profile['geometry_commit'] == ordinal_construct.UCNS_COMMIT
    assert profile['fallback'] == 'none'
    assert profile['deprecated_as_completed_geometry']
    assert profile['hmmm']


def test_active_inputs_are_registered_in_root_provenance():
    import hashlib
    workspace = Path(entry.__file__).resolve().parents[1]
    root = workspace.parents[1]
    profile = entry.active_profile()
    manifest = json.loads((root / 'stack-manifest.json').read_text())
    base = json.loads((workspace / 'BASE.json').read_text())
    graph = json.loads((workspace / profile['input_graph']).read_text())
    human = (root / 'STACK_MANIFEST.md').read_text()
    records = [r for r in manifest['research_participants']
               if r['workspace'] == 'research/english-gonol/']
    keyed = {r['participant_id']: r for r in records}
    assert len(keyed) == len(records), 'duplicate source-qualified participant'
    source_pairs = {(r['repository'], r['commit']) for r in records}
    assert all((r['repository'], r['commit']) in source_pairs
               for r in graph['repositories'])
    assert keyed['ordinal-geometry']['commit'] == profile['geometry_commit']
    assert base['ucns_prerequisite']['commit'] == profile['geometry_commit']
    assert base['active_construction']['selection'] == 'ACTIVE_CONSTRUCTION.json'
    assert base['active_construction']['source_commit'] == keyed['ordinal-source']['commit']
    assert all(r['authority_transfer'] is False for r in records)
    payload = {k: manifest[k] for k in ('repositories', 'research_participants', 'boundaries')}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert digest == manifest['work_graph_sha256']
    assert digest in human
    for participant_id, record in keyed.items():
        assert record['commit'] in human
        if participant_id.startswith('ordinal-'):
            assert participant_id in human


def test_full_workflow_covers_admission_dependencies():
    from fnmatch import fnmatch
    import yaml
    workspace = Path(entry.__file__).resolve().parents[1]
    root = workspace.parents[1]
    workflow = yaml.load((root / '.github/workflows/english-ordinal-affixiation.yml').read_text(),
                         Loader=yaml.BaseLoader)
    filters = workflow['on']['pull_request']['paths']
    closure = {'structural_construct.py', 'structural_rules.py', 'structural_query.py'}
    closure.update(p.name for p in (workspace / 'english_gonol').glob('*.py'))
    for name in closure:
        path = f'research/english-gonol/english_gonol/{name}'
        assert any(fnmatch(path, pattern) for pattern in filters), path


def test_workflow_tests_merge_tree_and_binds_selected_source_bytes():
    import yaml
    workspace = Path(entry.__file__).resolve().parents[1]
    root = workspace.parents[1]
    workflow = yaml.load((root / '.github/workflows/english-ordinal-affixiation.yml').read_text(),
                         Loader=yaml.BaseLoader)
    steps = workflow['jobs']['full-corpus']['steps']
    checkout = next(step for step in steps if step.get('uses', '').startswith('actions/checkout@'))
    assert 'ref' not in checkout.get('with', {}), 'PR tests must use the generated merge tree'
    graph_check = next(step['run'] for step in steps
                       if step.get('name') == 'Verify exact participant graph and unchanged source reader')
    assert "['active_construction']['source_commit']" in graph_check
    assert "['git','show',selected+':'+path]" in graph_check
    assert "pathlib.Path(path).read_bytes()==subprocess.check_output" in graph_check
    acquisition = next(step for step in steps
                       if step.get('name') == 'Acquire declared Unicode release and license')
    assert 'stack-tested-merge.txt' in acquisition['run']
    assert 'SOURCE_HEAD' in acquisition['env']


def test_provenance_repins_trigger_exact_source_gate():
    from fnmatch import fnmatch
    import yaml
    root = Path(entry.__file__).resolve().parents[3]
    workflow = yaml.load((root / '.github/workflows/english-ordinal-affixiation.yml').read_text(),
                         Loader=yaml.BaseLoader)
    filters = workflow['on']['pull_request']['paths']
    for path in ('research/english-gonol/BASE.json', 'stack-manifest.json',
                 'STACK_MANIFEST.md', 'research/english-gonol/ACTIVE_CONSTRUCTION.json',
                 'research/english-gonol/docs/ordinal-work-graph.json'):
        assert any(fnmatch(path, pattern) for pattern in filters), path


def test_selection_and_source_graph_are_exact_pinned_inputs():
    import ast
    import yaml
    root = Path(entry.__file__).resolve().parents[3]
    workflow = yaml.load((root / '.github/workflows/english-ordinal-affixiation.yml').read_text(),
                         Loader=yaml.BaseLoader)
    steps = workflow['jobs']['full-corpus']['steps']
    command = next(step['run'] for step in steps
                   if step.get('name') == 'Verify exact participant graph and unchanged source reader')
    python = command.split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
    tree = ast.parse(python)
    loop = next(node for node in ast.walk(tree) if isinstance(node, ast.For)
                and isinstance(node.target, ast.Name) and node.target.id == 'relative')
    inputs = ast.literal_eval(loop.iter)
    assert set(inputs) == {'english_gonol/ordinal_construct.py', 'english_gonol/__main__.py',
                           'ACTIVE_CONSTRUCTION.json', 'docs/ordinal-work-graph.json'}
    assert any(isinstance(node, ast.Assert) for node in loop.body)


def test_auxiliary_source_graph_is_outside_verified_construction():
    import shlex
    import yaml
    root = Path(entry.__file__).resolve().parents[3]
    workflow = yaml.load((root / '.github/workflows/english-ordinal-affixiation.yml').read_text(),
                         Loader=yaml.BaseLoader)
    copies = []
    for step in workflow['jobs']['full-corpus']['steps']:
        for line in step.get('run', '').splitlines():
            if line.strip().startswith('cp '):
                words = shlex.split(line)
                if 'research/english-gonol/docs/ordinal-work-graph.json' in words:
                    copies.append(words[-1])
    assert copies == ['_evidence/source-work-graph.json']


def test_full_workflow_uses_baseline_owned_admission_inventory():
    import yaml
    root = Path(entry.__file__).resolve().parents[3]
    workflow = yaml.load((root / '.github/workflows/english-ordinal-affixiation.yml').read_text(),
                         Loader=yaml.BaseLoader)
    steps = workflow['jobs']['full-corpus']['steps']
    command = next(step['run'] for step in steps
                   if step.get('name') == 'Verify exact participant graph and unchanged source reader')
    assert "git','show',base+':'+baseline_path" in command
    assert "ast.literal_eval(assignment.value)" in command
    assert "from english_gonol.structural_construct import IMPLEMENTATION_FILES" not in command


def test_general_workflow_isolates_ordinal_ucns_package():
    import yaml
    root = Path(entry.__file__).resolve().parents[3]
    workflow = yaml.load((root / '.github/workflows/english-gonol.yml').read_text(),
                         Loader=yaml.BaseLoader)
    steps = workflow['jobs']['english-gonol-tests']['steps']
    install = next(step['run'] for step in steps if step.get('name') == 'Install construction prerequisites')
    historical = next(step['run'] for step in steps if step.get('name') == 'Historical English Gonol tests')
    ordinal = next(step['run'] for step in steps if step.get('name') == 'Isolated ordinal construction tests')
    assert './_deps/ucns-ordinal' not in install.splitlines()[0]
    assert '_deps/ordinal-venv' in install
    assert '--ignore=tests/test_ordinal_construct.py' in historical
    assert '--ignore=tests/test_active_construction.py' in historical
    assert '../../_deps/ordinal-venv/bin/python' in ordinal
