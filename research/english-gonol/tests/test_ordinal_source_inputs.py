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
    baseline = 'e3eb83764355b4b760a79323cda6a6d75c3a501a'
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
