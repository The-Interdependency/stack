# === MODULE_BUILD ===
# id: weave_atomic_output
#   module_name: safe_output
#   module_kind: io
#   summary: no-clobber publication of a fully written and closed research output
#   owner: Erin Spencer
#   public_surface: write_new
#   storage_boundary: write
#   network_boundary: none
#   tests: tests/test_cycle_repairs.py
#   rollback: retain equivalent no-partial-output and no-overwrite guarantees
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: weave_output_atomic_no_clobber
#   given: bytes and a target path on a hard-link-capable filesystem
#   then: install only after successful write, flush, fsync and close; never overwrite an existing path
# === END CONTRACTS ===
"""Usage: write_new(Path('result.wvc'), complete_record).

A temporary sibling is created with owner-only permissions. Successful close
precedes atomic no-clobber linking. Write/flush/fsync/close failures leave no
partial destination. Unsupported filesystem semantics refuse; they do not fall
back to an overwrite-prone rename. Process-crash cleanup/directory durability
are not guaranteed by this helper; ordinary failure cleans its temporary file.
"""
import os
from pathlib import Path
import tempfile


def write_new(path: Path, data: bytes) -> None:
    if type(data) is not bytes:
        raise TypeError('complete bytes required')
    path = Path(path)
    fd, name = tempfile.mkstemp(prefix='.'+path.name+'.', suffix='.tmp', dir=path.parent)
    temporary = Path(name)
    try:
        try:
            target = os.fdopen(fd, 'wb')
        except BaseException:
            os.close(fd)
            raise
        with target:
            if target.write(data) != len(data):
                raise OSError('short output write')
            target.flush()
            os.fsync(target.fileno())
        os.link(temporary, path)  # atomic create; existing files/symlinks fail
    finally:
        temporary.unlink(missing_ok=True)
