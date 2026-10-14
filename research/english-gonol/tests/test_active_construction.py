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
