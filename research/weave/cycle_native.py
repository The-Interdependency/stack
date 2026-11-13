# === MODULE_BUILD ===
# id: weave_native_binary_binding
#   module_name: cycle_native
#   module_kind: adapter
#   summary: loads this forge's exact binary candidate and its unchanged native UCNS producers
#   owner: Erin Spencer
#   public_surface: load_native
#   internal_surface: fresh checked-buffer module loading
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   tests: tests/test_cycle.py, tests/test_cycle_repairs.py
#   rollout: research only; no UCHC package, graduation, or geometry replacement
#   rollback: remove with the native binary cycle
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: cycle_native_source_pinned
#   given: the local source lock and a supplied UCNS checkout
#   then: execute freshly verified native buffers or refuse before processing data
# === END CONTRACTS ===
"""Usage: api, geometry = load_native('/directory-containing-ucns').

The binary construction is Stack-owned research. UCHC supplies its architecture
reference, not a falsely graduated runtime package. UCNS remains geometry owner.
There is no cache reuse, network fallback, or fabricated native object.
"""
from hashlib import sha1
from pathlib import Path
from types import ModuleType
from uuid import uuid4
import json
import sys
from numeral import Refused

ROOT = Path(__file__).resolve().parent


def load_native(sources: str | Path):
    lock = json.loads((ROOT/'CYCLE_NATIVE.json').read_text())
    if lock.get('schema') != 'weave.native-inputs/v2':
        raise Refused('unsupported native source lock')
    entry = lock['binary_source']
    if entry['path'] != 'native_binary.py' or entry['owner'] != 'The-Interdependency/stack':
        raise Refused('binary candidate must remain in its declared forge')
    path = ROOT/entry['path']
    try:
        with path.open('rb') as source:
            data = source.read(65537)
    except OSError as exc:
        raise Refused(f'native binary source unavailable: {path}') from exc
    actual = sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if len(data)>65536 or actual != entry['git_blob']:
        raise Refused('native binary source does not match CYCLE_NATIVE.json')
    name = '_weave_binary_' + actual + '_' + uuid4().hex
    api = ModuleType(name)
    api.__file__ = str(path)
    sys.modules[name] = api
    try:
        exec(compile(data,str(path),'exec'),api.__dict__)
    finally:
        if sys.modules.get(name) is api:
            del sys.modules[name]
    if api.UCNS_COMMIT != lock['ucns_commit'] or api.UCNS_BLOBS != lock['ucns_sources']:
        raise Refused('candidate and consumer native dependency locks disagree')
    try:
        geometry = api.Geometry(Path(sources)/'ucns')
    except api.BinaryError as exc:
        raise Refused(str(exc)) from exc
    return api, geometry
