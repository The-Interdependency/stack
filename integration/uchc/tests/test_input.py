# ratios: loc_comments=41:16 imports_exports=5:2 calls_definitions=24:3
"""Run against a clean installed wheel, with UCHC_INPUT_LOCK selecting its lock.

python -m pytest -q integration/uchc/tests/test_input.py
These integration tests do not import the Stack English source implementation.
"""
# === CHECKS ===
# id: zfae_uchc_artifact_witness
#   proves: zfae_consumes_exact_uchc_artifact
#   call: self::test_install_identity_and_mismatch
#   mutates: none
#   cleanup: none
# id: zfae_uchc_source_witness
#   proves: zfae_input_admission_is_not_neural_readiness
#   call: self::test_actual_uchc_input_is_preserved
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===
import importlib.util
import json
import os
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[3] / 'research/zfae'
spec = importlib.util.spec_from_file_location('stack_uchc_input', HERE / 'uchc_input.py')
consumer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(consumer)


def _lock():
    return json.loads(Path(os.environ.get('UCHC_INPUT_LOCK', HERE / 'UCHC_INPUT.json')).read_text())


def test_install_identity_and_mismatch():
    lock = _lock()
    evidence = consumer.verify_install(lock)
    assert evidence['wheel_sha256'] == lock['wheel_sha256']
    assert evidence['verified_files'] > 0
    for field, value in [('wheel_sha256', '0' * 64), ('package_version', 'other'),
                         ('schema', 'other'), ('version', '0')]:
        changed = dict(lock); changed[field] = value
        with pytest.raises(consumer.InputArtifactError):
            consumer.verify_install(changed)


def test_actual_uchc_input_is_preserved():
    path = Path(os.environ['UCHC_INPUT_DATABASE'])
    with consumer.load_input(path, _lock()) as corpus:
        text = 'alpha letter alpha'
        frame = corpus.resolve_text(text, source_id='stack:zfae-input')
        frame.require_complete()
        assert frame.recover_utf8() == text.encode()
        assert corpus.replay(frame.to_bytes()) == frame
        assert frame.words
        assert all(word.construct_receipt == corpus.identity.logical_receipt for word in frame.words)
        for word in frame.words:
            for definition_id in word.definition_ids:
                definition = corpus.definition(definition_id)
                assert definition.gonol.origin_word_id == word.gonol.word_id
                assert corpus.recover_definition(definition) == definition.text
        unsupported = corpus.resolve_text('🧪🧪', source_id='stack:unadmitted')
        assert unsupported.recover_utf8() == '🧪🧪'.encode()
        with pytest.raises(ValueError):
            unsupported.require_complete()
        assert not hasattr(frame, 'neural_ready')
# ratios: loc_comments=41:16 imports_exports=5:2 calls_definitions=24:3
