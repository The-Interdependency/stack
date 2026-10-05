# === MODULE_BUILD ===
# id: weave_native_binary_binding
#   module_name: cycle_native
#   module_kind: adapter
#   summary: loads the exact UCHC binary producer which consumes the pinned native UCNS constructors
#   owner: Erin Spencer
#   public_surface: load_native
#   internal_surface: locked source loading
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_cycle.py
#   rollout: required source-locked native dependency for the explicit cycle profile
#   rollback: remove with the cycle consumer, never substitute fixture geometry
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: cycle_native_source_pinned
#   given: supplied UCNS and UCHC checkouts
#   then: execute only the declared exact source modules or refuse before processing data
# === END CONTRACTS ===
"""Usage: api, geometry = load_native('/checkouts-containing-ucns-and-uchc').

Reads source-locked producer buffers and executes those exact buffers. There is
no network access, mutable upstream vendoring, or reconstruction from labels.
The producer's scoped constructors retain their own status and authority.
"""
from hashlib import sha1
from pathlib import Path
from types import ModuleType
import json
import sys
from numeral import Refused

ROOT = Path(__file__).resolve().parent


def load_native(sources: str | Path):
    lock = json.loads((ROOT/'CYCLE_NATIVE.json').read_text())
    entry = lock['uchc_source']
    path = Path(sources)/'uchc'/entry['path']
    try:
        with path.open('rb') as source:
            data = source.read(65537)
    except OSError as exc:
        raise Refused(f'native UCHC source unavailable: {path}') from exc
    actual = sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if len(data)>65536 or actual != entry['git_blob']:
        raise Refused('native UCHC source does not match CYCLE_NATIVE.json')
    name = '_weave_uchc_'+actual
    if name not in sys.modules:
        module = ModuleType(name)
        module.__file__ = str(path)
        sys.modules[name] = module
        try:
            exec(compile(data,str(path),'exec'),module.__dict__)
        except BaseException:
            sys.modules.pop(name,None)
            raise
    api = sys.modules[name]
    if api.UCNS_COMMIT != lock['ucns_commit'] or api.UCNS_BLOBS != lock['ucns_sources']:
        raise Refused('producer and consumer native dependency locks disagree')
    return api, api.Geometry(Path(sources)/'ucns')
