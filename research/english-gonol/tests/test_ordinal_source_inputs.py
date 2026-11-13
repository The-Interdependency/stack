"""Exercise the workflow's actual participant admission loop, without network."""
import ast
from pathlib import Path
from types import SimpleNamespace
import pytest
import yaml

# === CHECKS ===
# id: ordinal_workflow_complete_input_mapping
#   proves: english_expanded_repertoire
#   call: self::test_participant_mapping_refuses_changes
# id: check_test_workflow_graph_accepts_current_projection
#   proves: english_ordinal_workflow_provenance
#   call: self::test_workflow_graph_accepts_current_projection
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files or in-memory values
#   cleanup: pytest fixtures
# id: check_test_workflow_graph_rejects_rebound_claims
#   proves: english_ordinal_workflow_provenance
#   call: self::test_workflow_graph_rejects_rebound_claims
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files or in-memory values
#   cleanup: pytest fixtures
# === END CHECKS ===


def _program():
    root = Path(__file__).resolve().parents[3]
    workflow = yaml.safe_load((root / '.github/workflows/english-ordinal-affixiation.yml').read_text())
    step = next(s for s in workflow['jobs']['full-corpus']['steps']
                if s.get('name') == 'Verify exact participant graph and unchanged source reader')
    source = step['run'].split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
    tree = ast.parse(source)
    first = next(i for i, n in enumerate(tree.body) if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'baseline_key' for t in n.targets))
    last = next(i for i, n in enumerate(tree.body) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'active_base' for t in n.targets))
    return compile(ast.Module(body=tree.body[first:last], type_ignores=[]), '<workflow-inputs>', 'exec')


def _run(change):
    baseline = '05d235f17c1e4cd0cce35836ae3561d9bc96bd2f'
    actual = 'a' * 40
    entries = [{'repository': 'fixture/repo', 'commit': actual},
               {'repository': 'The-Interdependency/stack', 'commit': baseline}]
    change(entries)
    def git(args, text):
        return actual + '\n' if '-C' in args else baseline + '\n'
    env = {'git_roots': {('fixture/repo', actual): 'fixture-checkout'},
           'artifact_roots': {}, 'graph': {'repositories': entries},
           'subprocess': SimpleNamespace(check_output=git)}
    exec(_program(), env)


def test_participant_mapping_accepts_complete_inventory():
    _run(lambda rows: None)


@pytest.mark.parametrize('change', [
    lambda rows: rows.append({'repository': 'unmapped/repo', 'commit': 'b' * 40}),
    lambda rows: rows[0].update(commit='b' * 40),
    lambda rows: rows.pop(),
    lambda rows: rows.append(dict(rows[0])),
])
def test_participant_mapping_refuses_changes(change):
    with pytest.raises(AssertionError):
        _run(change)


def _graph_validator():
    import hashlib
    import json
    root = Path(__file__).resolve().parents[3]
    workflow = yaml.safe_load((root / '.github/workflows/english-ordinal-affixiation.yml').read_text())
    step = next(s for s in workflow['jobs']['full-corpus']['steps']
                if s.get('name') == 'Verify exact participant graph and unchanged source reader')
    source = step['run'].split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'validate_graph')
    env = {'hashlib': hashlib, 'json': json}
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<workflow-graph>', 'exec'), env)
    graph = json.loads((root / 'research/english-gonol/docs/ordinal-work-graph.json').read_text())
    manifest = json.loads((root / 'stack-manifest.json').read_text())
    return env['validate_graph'], graph, manifest


def test_workflow_graph_accepts_current_projection():
    validate, graph, manifest = _graph_validator()
    validate(graph, manifest)


@pytest.mark.parametrize('change', [
    lambda g: g.update(schema='unsupported'),
    lambda g: g.update(version='2.0.0'),
    lambda g: g['boundaries'].update(authority_transfer=True),
    lambda g: g['boundaries'].update(proof_status_transfer=True),
    lambda g: g['boundaries'].update(measurement_status_transfer=True),
    lambda g: g['boundaries'].update(authority_transfer=0),
    lambda g: g['repositories'][0].update(commit='0' * 40),
])
def test_workflow_graph_rejects_rebound_claims(change):
    import hashlib
    import json
    validate, graph, manifest = _graph_validator()
    change(graph)
    body = {k: graph[k] for k in ('repositories', 'boundaries')}
    graph['work_graph_sha256'] = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    with pytest.raises(AssertionError):
        validate(graph, manifest)
