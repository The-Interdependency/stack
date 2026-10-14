"""Execute U1/U2/U4/U6 unchanged against a disposable, synthetic VM.

All subprocesses, account operations, and absolute VM paths are intercepted.
Only fixture files in TemporaryDirectory are read/written; no sudo, service,
installer, network, or real credential action is executed. This is a behavioral
runbook witness, not live VM acceptance or an emulation of systemd/GNU tar.
"""
from __future__ import annotations

import builtins
from contextlib import redirect_stdout
import copy
from decimal import Decimal
import hashlib
import io
import itertools
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import tarfile
import tempfile
import types
import unittest

RUNBOOK = Path(__file__).resolve().parents[1] / "deploy" / "VM_CONTACT.md"
PIN = "e74ce1ee8a2cea50b0a6acce7697a6d3d9b2e128"
UNITS = ("vm-mcp.service", "vm-mcp-admin.service")


def payload(step):
    section = RUNBOOK.read_text().split(f"### {step}.", 1)[1].split("\n### ", 1)[0]
    return re.search(r"python3 (?:-I )?- <<'PY'\n(.*?)\nPY", section, re.S)[1]


class SyntheticVM:
    """Explicit process allowlist plus real tempfile filesystem/archive bytes."""

    def __init__(self, directory):
        self.base = Path(directory).resolve()
        self.home = "/srv/existing/.vm-mcp-home"
        self.uid = 987
        self.units = {u: dict(LoadState="loaded", ActiveState="inactive",
                              UnitFileState="disabled") for u in UNITS}
        self.commands = []
        self.env = {"ROOT_SRC": "/root/source", "TOKEN_OVERRIDE": ""}
        self.fail_compare = False
        self.fail_snapshot = False
        self.fail_extract = False
        self.tar_warning = False
        self.copy_warning = False
        self.install_rc = 0
        self.running_processes = False
        self.installer_env = None
        self.write_paths = "/srv/existing"
        self.protect_system = "strict"
        self.target_at_first_stop = None
        for directory in ("/root", "/etc", "/opt", "/srv/existing"):
            self.path(directory).mkdir(parents=True, exist_ok=True)
        self.write("/srv/existing/data.txt", "untouched workspace")
        self.write("/opt/vm-mcp/old.py", "old code")
        self.write("/etc/vm-mcp.env", 'VM_MCP_ROOT="/srv/existing"\nVM_MCP_SHELL_ENABLED=0\n')
        for unit in UNITS:
            self.write("/etc/systemd/system/" + unit, "old unit " + unit)
        self.write("/root/test-token", "synthetic_only_" + "x" * 40 + "\n")
        self.path("/root/test-token").chmod(0o600)

    def path(self, value):
        p = Path(value)
        if p.is_absolute():
            try:
                p.relative_to(self.base)
            except ValueError:
                p = self.base / str(p).lstrip("/")
        else:
            p = self.base / p
        # Fixtures never contain symlinks. Deny accidental .. escape as well.
        if not p.resolve().is_relative_to(self.base):
            raise AssertionError("fixture filesystem escape")
        return p

    def write(self, path, content):
        p = self.path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)

    def backup(self):
        return self.path(self.path("/root/vm-mcp-upgrade.latest").read_text().strip())

    def state(self):
        return json.loads((self.backup() / "state.json").read_text())

    def target(self):
        return json.loads((self.backup() / "target.json").read_text())

    def run(self, args, **kwargs):
        args = [str(a) for a in args]
        self.commands.append((args, kwargs))
        result = types.SimpleNamespace(returncode=0, stdout="", stderr=b"")
        if args[0] == "tar":
            if self.tar_warning:
                result.stderr = b"tar: ACL operation not supported"
            if "-cpf" in args:
                if self.fail_snapshot:
                    raise subprocess.CalledProcessError(2, args)
                with tarfile.open(self.path(args[args.index("-cpf") + 1]), "w") as archive:
                    for name in args[args.index("--") + 1:]:
                        def metadata(info):
                            actual = self.path("/" + info.name)
                            ns = actual.lstat().st_mtime_ns
                            info.pax_headers["mtime"] = str(Decimal(ns) / Decimal(1000000000))
                            for key in os.listxattr(actual, follow_symlinks=False):
                                info.pax_headers["TEST.xattr." + key] = os.getxattr(actual, key, follow_symlinks=False).hex()
                            return info
                        archive.add(self.path("/" + name), arcname=name, filter=metadata)
            elif "--compare" in args:
                if self.fail_compare:
                    raise subprocess.CalledProcessError(1, args)
            elif "-xpf" in args:
                if self.fail_extract:
                    raise subprocess.CalledProcessError(2, args)
                with tarfile.open(self.path(args[args.index("-xpf") + 1])) as archive:
                    # Only synthetic archive entries created by this fixture.
                    stage = self.path(args[args.index("-C") + 1])
                    archive.extractall(stage, filter="data")
                    for member in archive.getmembers():
                        restored = stage / member.name
                        ns = int(Decimal(member.pax_headers["mtime"]) * Decimal(1000000000))
                        os.utime(restored, ns=(ns, ns), follow_symlinks=False)
                        for key, value in member.pax_headers.items():
                            if key.startswith("TEST.xattr."):
                                os.setxattr(restored, key[len("TEST.xattr."):], bytes.fromhex(value), follow_symlinks=False)
            else:
                raise AssertionError("unmodelled tar invocation")
        elif args[0] == "systemctl":
            action = args[1]
            if action == "daemon-reload":
                for unit in UNITS:
                    if not self.path("/etc/systemd/system/" + unit).exists():
                        self.units[unit] = dict(LoadState="not-found", ActiveState="inactive", UnitFileState="absent")
            else:
                unit = args[2]
                state = self.units[unit]
                if action == "show" and "--property=ReadWritePaths,ProtectSystem" in args:
                    result.stdout = "ReadWritePaths=" + self.write_paths + "\nProtectSystem=" + self.protect_system + "\n"
                elif action == "show":
                    result.stdout = (state["LoadState"] + "\n" if "--value" in args else
                                     "".join(k + "=" + v + "\n" for k, v in state.items()))
                elif action == "stop":
                    if self.target_at_first_stop is None and (self.backup() / "target.json").exists():
                        self.target_at_first_stop = self.target()
                    state["ActiveState"] = "inactive"
                elif action == "disable":
                    if state["UnitFileState"] != "static":
                        state["UnitFileState"] = "disabled"
                elif action == "enable":
                    state["UnitFileState"] = "enabled"
                elif action == "start":
                    state["ActiveState"] = "active"
                else:
                    raise AssertionError("unmodelled systemctl invocation")
        elif args[0] == "pgrep":
            result.returncode = 0 if self.running_processes else 1
        elif args[0] == "usermod":
            assert args[1] == "--home" and args[3] == "vmmcp"
            self.home = args[2]
        elif args[0] == "cp":
            if self.copy_warning:
                result.stderr = b"cp: metadata warning"
            assert args[1:3] == ["-a", "--"]
            source, destination = map(self.path, args[3:])
            if source.is_dir():
                shutil.copytree(source, destination, symlinks=True)
            else:
                shutil.copy2(source, destination)
        elif args == ["bash", self.env["ROOT_SRC"] + "/skill-lib/vm-mcp/install.sh"]:
            self.installer_env = kwargs["env"].copy()
            result.returncode = self.install_rc
            if not result.returncode:
                self.write("/opt/vm-mcp/SOURCE_COMMIT", PIN + "\n")
        else:
            raise AssertionError("forbidden/unmodelled subprocess: " + repr(args))
        return result

    def execute(self, step):
        vm = self

        class SandboxPath(type(Path())):
            def __new__(cls, *parts):
                return super().__new__(cls, vm.path(Path(*parts)))

            def __init__(self, *parts):
                # pathlib initializes in __new__ on 3.11, in __init__ on 3.12+.
                if type(Path()).__init__ is not object.__init__:
                    super().__init__(vm.path(Path(*parts)))

            def open(self, *args, **kwargs):
                return vm.path(self).open(*args, **kwargs)

            def relative_to(self, other, *args, **kwargs):
                return Path(str(self)).relative_to(vm.path(other), *args, **kwargs)

            def replace(self, target):
                return super().replace(vm.path(target))

        def root_stat(value):
            fields = {name: getattr(value, name) for name in dir(value) if name.startswith("st_")}
            fields["st_uid"] = 0  # Only fixture ownership is modeled as root.
            return types.SimpleNamespace(**fields)

        fake_os = types.SimpleNamespace(
            environ=self.env.copy(), umask=lambda mode: None,
            path=types.SimpleNamespace(lexists=lambda p: os.path.lexists(self.path(p))),
            open=lambda p, flags: os.open(self.path(p), flags), fdopen=os.fdopen,
            fstat=lambda fd: root_stat(os.fstat(fd)), lstat=lambda p: root_stat(os.lstat(self.path(p))),
            listxattr=lambda p, **kw: os.listxattr(self.path(p), **kw),
            getxattr=lambda p, name, **kw: os.getxattr(self.path(p), name, **kw),
            readlink=lambda p: os.readlink(self.path(p)),
            O_RDONLY=os.O_RDONLY, O_NOFOLLOW=os.O_NOFOLLOW, O_NONBLOCK=os.O_NONBLOCK)
        modules = dict(hashlib=hashlib, json=json, re=re, shlex=shlex, stat=stat,
                       tarfile=tarfile, os=fake_os,
                       pathlib=types.SimpleNamespace(Path=SandboxPath),
                       pwd=types.SimpleNamespace(getpwnam=lambda name: types.SimpleNamespace(
                           pw_uid=self.uid, pw_dir=self.home)),
                       subprocess=types.SimpleNamespace(run=self.run),
                       tempfile=types.SimpleNamespace(mkdtemp=lambda *, prefix, dir:
                           tempfile.mkdtemp(prefix=prefix, dir=self.path(dir))),
                       shutil=types.SimpleNamespace(move=lambda source, dest:
                           shutil.move(self.path(source), self.path(dest))),
                       time=types.SimpleNamespace(sleep=lambda seconds: None))

        def imports(name, globals=None, locals=None, fromlist=(), level=0):
            if level or name not in modules:
                raise AssertionError("forbidden import: " + name)
            return modules[name]

        safe_builtins = dict(vars(builtins), __import__=imports,
                             open=lambda p, *a, **kw: open(self.path(p), *a, **kw))
        output = io.StringIO()
        with redirect_stdout(output):
            exec(compile(payload(step), f"{RUNBOOK.name}:{step}", "exec"),
                 {"__builtins__": safe_builtins})
        return output.getvalue()


class UpgradeRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vm-contact-test-")
        self.addCleanup(self.temp.cleanup)
        self.vm = SyntheticVM(self.temp.name)

    def snapshot_target(self):
        self.vm.execute("U1")
        self.vm.execute("U2")
        target = self.vm.target()
        target["token_file"] = "/root/test-token"
        (self.vm.backup() / "target.json").write_text(json.dumps(target))

    def destructive(self):
        return [args for args, _ in self.vm.commands if
                args[0] in {"cp", "usermod", "bash"} or
                (args[0] == "systemctl" and args[1] != "show")]

    def test_archive_warnings_fail_before_snapshot_or_rollback_mutation(self):
        self.vm.tar_warning = True
        with self.assertRaisesRegex(AssertionError, "archive operation warned"):
            self.vm.execute("U1")
        self.assertFalse(self.vm.path("/root/vm-mcp-upgrade.latest").exists())
        self.vm.tar_warning = False
        self.snapshot_target()
        self.vm.tar_warning = True
        self.vm.commands.clear()
        with self.assertRaisesRegex(AssertionError, "archive operation warned"):
            self.vm.execute("U6")
        self.assertEqual(self.destructive(), [])

    def test_upgrade_safety_is_not_removed_by_python_optimization(self):
        import ast
        for step in ("U1", "U2", "U4", "U6"):
            tree = ast.parse(payload(step))
            self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
            require = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "require")
            namespace = {}
            exec(compile(ast.Module(body=[require], type_ignores=[]), "fixture", "exec", optimize=2), namespace)
            with self.assertRaises(AssertionError):
                namespace["require"](False, "still checked")
        for line in RUNBOOK.read_text().splitlines():
            if "python3" in line and "<<'PY'" in line:
                self.assertIn("python3 -I -", line)

    def test_incomplete_snapshot_never_publishes_marker_or_latest(self):
        for failure in ("fail_snapshot", "fail_compare"):
            with self.subTest(failure=failure):
                setattr(self.vm, failure, True)
                with self.assertRaises(subprocess.CalledProcessError):
                    self.vm.execute("U1")
                self.assertFalse(self.vm.path("/root/vm-mcp-upgrade.latest").exists())
                self.assertFalse(list(self.vm.path("/root").glob("vm-mcp-upgrade.*/COMPLETE")))
                setattr(self.vm, failure, False)
        self.assertEqual(self.destructive(), [])

    def test_failed_new_snapshot_keeps_existing_latest(self):
        self.vm.execute("U1")
        old = self.vm.backup()
        self.vm.fail_compare = True
        with self.assertRaises(subprocess.CalledProcessError):
            self.vm.execute("U1")
        self.assertEqual(self.vm.backup(), old)
        self.assertEqual((old / "COMPLETE").read_text(), "complete\n")

    def test_shell_metacharacters_and_spaces_roundtrip_without_evaluation(self):
        root = '/srv/a workspace;$(touch /tmp/never-created)`id`'
        self.vm.home = root + "/.vm-mcp-home"
        self.vm.write("/etc/vm-mcp.env", "VM_MCP_ROOT=" + shlex.quote(root) + "\nVM_MCP_SHELL_ENABLED=yes\n")
        self.vm.execute("U1")
        self.vm.commands.clear()
        self.vm.execute("U2")
        self.assertEqual(self.vm.target()["root"], root)
        self.assertEqual(self.vm.target()["profile"], "workspace")
        self.assertEqual(self.vm.commands, [])
        self.assertFalse(self.vm.path("/tmp/never-created").exists())
        self.vm.write(root + "/data", "fixture")
        with self.assertRaisesRegex(AssertionError, "cannot represent"):
            self.vm.execute("U4")
        self.assertEqual(self.destructive(), [])

    def test_token_override_is_persisted_before_stop_and_passed_to_installer(self):
        self.snapshot_target()
        self.vm.env.update(TOKEN_OVERRIDE="/root/test-token", VM_MCP_ROOT="/bad",
                           VM_MCP_SHELL_ENABLED="1", VM_MCP_AUTH_TOKEN="must-be-stripped", rc="93")
        target = self.vm.target()
        target["token_file"] = "/root/unselected-token"
        (self.vm.backup() / "target.json").write_text(json.dumps(target))
        output = self.vm.execute("U4")
        self.assertEqual(self.vm.target_at_first_stop["token_file"], "/root/test-token")
        self.assertEqual(self.vm.target()["token_file"], "/root/test-token")
        env = self.vm.installer_env
        for key, name in (("VM_MCP_ROOT", "root"), ("VM_MCP_PROFILE", "profile"),
                          ("VM_MCP_PORT", "port"), ("VM_MCP_ADMIN_SOCKET", "admin_socket"),
                          ("VM_MCP_AUTH_TOKEN_FILE", "token_file")):
            self.assertEqual(env[key], self.vm.target()[name])
        self.assertNotIn("VM_MCP_SHELL_ENABLED", env)
        self.assertNotIn("VM_MCP_AUTH_TOKEN", env)
        self.assertIn("rc=0", output)

    def test_custom_socket_is_preserved_as_data_but_blocks_pinned_installer(self):
        self.vm.write("/etc/vm-mcp.env", 'VM_MCP_ROOT="/srv/existing"\nVM_MCP_ADMIN_SOCKET="/run/custom/admin.sock"\n')
        self.snapshot_target()
        self.assertEqual(self.vm.target()["admin_socket"], "/run/custom/admin.sock")
        with self.assertRaisesRegex(AssertionError, "cannot preserve a custom socket"):
            self.vm.execute("U4")
        self.assertEqual(self.destructive(), [])
        self.assertIsNone(self.vm.installer_env)

    def test_external_write_followed_symlink_blocks_snapshot(self):
        self.vm.write("/elsewhere/version", "external version")
        self.vm.path("/opt/vm-mcp/SOURCE_COMMIT").symlink_to(self.vm.path("/elsewhere/version"))
        with self.assertRaisesRegex(AssertionError, "symlink escapes backup"):
            self.vm.execute("U1")
        self.assertFalse(self.vm.path("/root/vm-mcp-upgrade.latest").exists())
        self.assertEqual(self.vm.path("/elsewhere/version").read_text(), "external version")
        self.assertEqual(self.destructive(), [])

    def test_standard_interpreter_and_internal_venv_symlinks_are_backed_up(self):
        self.vm.write("/usr/bin/python3.11", "synthetic interpreter")
        self.vm.path("/opt/vm-mcp/.venv/bin").mkdir(parents=True)
        self.vm.path("/opt/vm-mcp/.venv/bin/python3").symlink_to(self.vm.path("/usr/bin/python3.11"))
        self.vm.path("/opt/vm-mcp/.venv/lib").mkdir()
        self.vm.path("/opt/vm-mcp/.venv/lib64").symlink_to("lib")
        self.vm.execute("U1")
        self.assertTrue((self.vm.backup() / "COMPLETE").exists())

    def test_installer_failure_uses_current_returncode_not_stale_shell_rc(self):
        self.snapshot_target()
        self.vm.env["rc"] = "0"
        self.vm.install_rc = 8
        with self.assertRaises(SystemExit) as error:
            self.vm.execute("U4")
        self.assertEqual(error.exception.code, 8)

    def test_invalid_token_and_drift_fail_before_service_stop(self):
        self.snapshot_target()
        self.vm.path("/root/test-token").chmod(0o644)
        with self.assertRaisesRegex(AssertionError, "unsafe token"):
            self.vm.execute("U4")
        self.assertEqual(self.destructive(), [])
        self.vm.path("/root/test-token").chmod(0o600)
        self.vm.units[UNITS[0]]["ActiveState"] = "active"
        with self.assertRaisesRegex(AssertionError, "unit state changed"):
            self.vm.execute("U4")
        self.assertEqual(self.destructive(), [])

    def test_preservation_checks_exit_nonzero_for_each_mismatch(self):
        self.snapshot_target()
        target = self.vm.target()
        def environment():
            return "\n".join(key + "=" + shlex.quote(target[field]) for key, field in
                (("VM_MCP_ROOT", "root"), ("VM_MCP_PROFILE", "profile"),
                 ("VM_MCP_PORT", "port"), ("VM_MCP_ADMIN_SOCKET", "admin_socket"))) + "\n"
        self.vm.write("/etc/vm-mcp.env", environment())
        with self.assertRaises(SystemExit) as ok:
            self.vm.execute("U5")
        self.assertEqual(ok.exception.code, 0)
        for key in ("VM_MCP_ROOT", "VM_MCP_PROFILE", "VM_MCP_PORT", "VM_MCP_ADMIN_SOCKET"):
            self.vm.write("/etc/vm-mcp.env", environment() + key + "=/wrong\n")
            with self.subTest(key=key), self.assertRaises(SystemExit) as failure:
                self.vm.execute("U5")
            self.assertEqual(failure.exception.code, 1)
        self.vm.write("/etc/vm-mcp.env", environment())
        self.vm.home = "/wrong-home"
        with self.assertRaises(SystemExit) as failure:
            self.vm.execute("U5")
        self.assertEqual(failure.exception.code, 1)
        self.vm.home = target["root"] + "/.vm-mcp-home"
        # The preserved root may be empty, but it must still exist.
        self.vm.path("/srv/existing/data.txt").unlink()
        with self.assertRaises(SystemExit) as ok:
            self.vm.execute("U5")
        self.assertEqual(ok.exception.code, 0)
        shutil.rmtree(self.vm.path("/srv/existing"))
        with self.assertRaises(SystemExit) as failure:
            self.vm.execute("U5")
        self.assertEqual(failure.exception.code, 1)
        self.assertEqual(self.destructive(), [])

    def test_every_archive_phase_requests_all_xattr_namespaces(self):
        self.snapshot_target()
        self.vm.execute("U4")
        self.vm.execute("U6")
        commands = [args for args, _ in self.vm.commands if args[0] == "tar"]
        self.assertGreaterEqual(len(commands), 4)
        for args in commands:
            self.assertIn("--xattrs-include=*", args)

    def test_real_gnu_tar_roundtrips_xattrs_and_detects_exclusion_control(self):
        # Only user metadata on disposable files; never grant a file capability.
        if not shutil.which("tar") or not hasattr(os, "setxattr"):
            self.skipTest("GNU tar/xattr support unavailable")
        version = subprocess.run(["tar", "--version"], capture_output=True, text=True, check=True)
        if "GNU tar" not in version.stdout:
            self.skipTest("GNU tar required for metadata witness")
        # This witness isolates xattrs; ACL warnings are covered by fail-closed mocks.
        with tempfile.TemporaryDirectory(prefix=".xattr-witness-", dir=RUNBOOK.parent) as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            fixture = source / "fixture"
            fixture.write_bytes(b"synthetic metadata fixture")
            os.utime(fixture, ns=(1700000000123456789, 1700000000123456789))
            try:
                os.setxattr(fixture, "user.vm_mcp_fixture", b"preserved")
            except OSError as error:
                self.skipTest("fixture filesystem xattrs unavailable: " + str(error.errno))
            archive = root / "state.tar"
            flags = ["--xattrs", "--xattrs-include=*"]
            def tar(*args):
                result = subprocess.run(["tar", *flags, *map(str, args)], capture_output=True, check=True)
                self.assertFalse(result.stderr, result.stderr)
            tar("-cpf", archive, "-C", source, "fixture")
            tar("--compare", "-f", archive, "-C", source)
            with tarfile.open(archive) as saved:
                self.assertEqual(saved.getmember("fixture").pax_headers["SCHILY.xattr.user.vm_mcp_fixture"], "preserved")
            for exclude in (False, True):
                restored = root / ("excluded" if exclude else "restored")
                restored.mkdir()
                extra = ["--xattrs-exclude=*"] if exclude else []
                tar(*extra, "-xpf", archive, "-C", restored)
                self.assertEqual((restored / "fixture").read_bytes(), fixture.read_bytes())
                self.assertEqual((restored / "fixture").stat().st_mtime_ns, fixture.stat().st_mtime_ns)
                if exclude:
                    self.assertNotIn("user.vm_mcp_fixture", os.listxattr(restored / "fixture"))
                else:
                    self.assertEqual(os.getxattr(restored / "fixture", "user.vm_mcp_fixture"), b"preserved")

    def test_real_gnu_tar_selects_nonuser_xattrs_without_granting_capabilities(self):
        # Exercise GNU tar's actual default-vs-include namespace selection while
        # replacing only setxattr syscalls. No capability is installed on a file.
        if not shutil.which("tar") or not shutil.which("cc") or not hasattr(os, "listxattr"):
            self.skipTest("GNU tar, C compiler and xattr inspection required")
        version = subprocess.run(["tar", "--version"], capture_output=True, text=True, check=True)
        if "GNU tar" not in version.stdout:
            self.skipTest("GNU tar required for namespace selection witness")
        with tempfile.TemporaryDirectory(prefix="nonuser-xattr-witness-") as directory:
            root = Path(directory)
            source = root / "record_xattr.c"
            source.write_text(r'''#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
static int record(const char *name) {
    FILE *out = fopen(getenv("XATTR_LOG"), "a");
    if (!out) return -1;
    fprintf(out, "%s\n", name);
    fclose(out);
    return 0;
}
int setxattr(const char *p, const char *n, const void *v, size_t s, int f) { return record(n); }
int lsetxattr(const char *p, const char *n, const void *v, size_t s, int f) { return record(n); }
int fsetxattr(int fd, const char *n, const void *v, size_t s, int f) { return record(n); }
''')
            library = root / "record_xattr.so"
            subprocess.run(["cc", "-shared", "-fPIC", "-o", str(library), str(source)],
                           check=True, capture_output=True)
            archive = root / "synthetic.tar"
            with tarfile.open(archive, "w", format=tarfile.PAX_FORMAT) as saved:
                member = tarfile.TarInfo("fixture")
                member.size = 1
                # Intentionally invalid capability bytes, even if interception fails.
                member.pax_headers["SCHILY.xattr.security.capability"] = "synthetic-not-a-capability"
                saved.addfile(member, io.BytesIO(b"x"))
            for include_all in (False, True):
                dest = root / str(include_all)
                dest.mkdir()
                log = root / (str(include_all) + ".log")
                env = dict(os.environ, LD_PRELOAD=str(library), XATTR_LOG=str(log))
                flags = ["--xattrs-include=*"] if include_all else []
                result = subprocess.run(["tar", "--xattrs", *flags, "-xf", str(archive), "-C", str(dest)],
                                        env=env, capture_output=True, check=True)
                self.assertFalse(result.stderr, result.stderr)
                selected = log.read_text().splitlines() if log.exists() else []
                self.assertEqual(selected, ["security.capability"] if include_all else [])
                self.assertNotIn("security.capability", os.listxattr(dest / "fixture"))

    def test_recursive_additions_and_metadata_drift_block_install(self):
        for drift in ("added_dropin", "added_code", "xattr", "mode"):
            with self.subTest(drift=drift), tempfile.TemporaryDirectory() as directory:
                vm = SyntheticVM(directory)
                vm.write("/etc/systemd/system/vm-mcp.service.d/workspace.conf", "original drop-in")
                vm.execute("U1")
                vm.execute("U2")
                vm.commands.clear()
                if drift == "added_dropin":
                    vm.write("/etc/systemd/system/vm-mcp.service.d/new.conf", "unexpected override")
                elif drift == "added_code":
                    vm.write("/opt/vm-mcp/new.py", "unexpected module")
                elif drift == "xattr":
                    os.setxattr(vm.path("/opt/vm-mcp/old.py"), "user.fixture", b"changed")
                else:
                    vm.path("/opt/vm-mcp/old.py").chmod(0o600)
                with self.assertRaisesRegex(AssertionError, "deployment changed"):
                    vm.execute("U4")
                self.assertFalse(any(args[0] in {"bash", "usermod", "cp"} or
                                     (args[0] == "systemctl" and args[1] != "show") for args, _ in vm.commands))
                self.assertIsNone(vm.installer_env)

    def test_manifest_detects_addition_even_with_parent_mtime_restored(self):
        self.snapshot_target()
        parent = self.vm.path("/opt/vm-mcp")
        before = parent.stat()
        self.vm.write("/opt/vm-mcp/added.py", "not in archive")
        os.utime(parent, ns=(before.st_atime_ns, before.st_mtime_ns))
        with self.assertRaisesRegex(AssertionError, "deployment changed"):
            self.vm.execute("U4")
        self.assertEqual(self.destructive(), [])

    def test_effective_unit_boundary_mismatch_blocks_acceptance(self):
        self.snapshot_target()
        target = self.vm.target()
        self.vm.write("/etc/vm-mcp.env", "\n".join(key + "=" + shlex.quote(target[field]) for key, field in
            (("VM_MCP_ROOT", "root"), ("VM_MCP_PROFILE", "profile"),
             ("VM_MCP_PORT", "port"), ("VM_MCP_ADMIN_SOCKET", "admin_socket"))))
        for paths in ("", "/wrong", "/srv/existing /", "/srv/existing /tmp"):
            self.vm.write_paths = paths
            with self.subTest(paths=paths), self.assertRaises(SystemExit) as error:
                self.vm.execute("U5")
            self.assertEqual(error.exception.code, 1)
        self.vm.write_paths = target["root"]
        self.vm.protect_system = "no"
        with self.assertRaises(SystemExit) as error:
            self.vm.execute("U5")
        self.assertEqual(error.exception.code, 1)
        self.assertEqual(self.destructive(), [])

    def test_client_transfer_commands_use_installed_token_copy(self):
        section = RUNBOOK.read_text().split("## Connect the MCP client privately", 1)[1].split("## First end-to-end calls", 1)[0]
        transfer_lines = [line for line in section.splitlines() if "cat " in line]
        self.assertGreaterEqual(len(transfer_lines), 4)
        for line in transfer_lines:
            self.assertIn("cat /etc/credstore/vm-mcp-token", line)
            self.assertNotIn("cat /root/vm-mcp.token", line)

    def test_manifest_logic_is_identical_for_snapshot_preflight_and_rollback(self):
        import ast
        manifests = []
        for step in ("U1", "U4", "U6"):
            node = next(n for n in ast.parse(payload(step)).body if isinstance(n, ast.FunctionDef) and n.name == "deployment_manifest")
            manifests.append(ast.dump(node, include_attributes=False))
        self.assertEqual(manifests, [manifests[0]] * 3)

    def test_corrupt_backup_never_stops_or_displaces_live_artifacts(self):
        self.snapshot_target()
        (self.vm.backup() / "state.tar").write_bytes(b"corrupt")
        for step in ("U4", "U6"):
            with self.subTest(step=step), self.assertRaisesRegex(AssertionError, "checksum"):
                self.vm.execute(step)
        self.assertEqual(self.destructive(), [])
        self.assertEqual(self.vm.path("/opt/vm-mcp/old.py").read_text(), "old code")
        self.assertFalse(list(self.vm.backup().glob("displaced.*")))

    def test_failed_staging_never_touches_live_deployment(self):
        self.snapshot_target()
        self.vm.fail_extract = True
        with self.assertRaises(subprocess.CalledProcessError):
            self.vm.execute("U6")
        self.assertEqual(self.destructive(), [])
        self.assertFalse(list(self.vm.backup().glob("displaced.*")))

    def test_rollback_restores_all_active_enablement_combinations_and_home_first(self):
        combinations = list(itertools.product(("active", "inactive"), ("enabled", "disabled")))
        for main, broker in itertools.product(combinations, repeat=2):
            with self.subTest(main=main, broker=broker), tempfile.TemporaryDirectory() as directory:
                vm = SyntheticVM(directory)
                for unit, (active, enabled) in zip(UNITS, (main, broker)):
                    vm.units[unit].update(ActiveState=active, UnitFileState=enabled)
                expected = copy.deepcopy(vm.units)
                vm.execute("U1")
                vm.home = "/srv/changed/.vm-mcp-home"
                for state in vm.units.values():
                    state.update(ActiveState="active", UnitFileState="enabled")
                vm.write("/opt/vm-mcp/old.py", "new code")
                vm.commands.clear()
                vm.execute("U6")
                self.assertEqual(vm.units, expected)
                self.assertEqual(vm.home, "/srv/existing/.vm-mcp-home")
                self.assertEqual(vm.path("/opt/vm-mcp/old.py").read_text(), "old code")
                commands = [args for args, _ in vm.commands]
                home_index = next(i for i, a in enumerate(commands) if a[0] == "usermod")
                starts = [a[2] for i, a in enumerate(commands) if a[:2] == ["systemctl", "start"]
                          and self.assertGreater(i, home_index) is None]
                self.assertEqual(starts, [u for u in reversed(UNITS) if expected[u]["ActiveState"] == "active"])
                self.assertEqual(vm.path("/srv/existing/data.txt").read_text(), "untouched workspace")

    def test_rollback_removes_previously_absent_code_env_and_units(self):
        shutil.rmtree(self.vm.path("/opt/vm-mcp"))
        self.vm.path("/etc/vm-mcp.env").unlink()
        for unit in UNITS:
            self.vm.path("/etc/systemd/system/" + unit).unlink()
            self.vm.units[unit] = dict(LoadState="not-found", ActiveState="inactive", UnitFileState="absent")
        self.vm.execute("U1")
        self.vm.write("/opt/vm-mcp/new.py", "new code")
        self.vm.write("/etc/vm-mcp.env", "new env")
        for unit in UNITS:
            self.vm.write("/etc/systemd/system/" + unit, "new unit")
            self.vm.units[unit] = dict(LoadState="loaded", ActiveState="active", UnitFileState="enabled")
        self.vm.execute("U6")
        for path in ("/opt/vm-mcp", "/etc/vm-mcp.env"):
            self.assertFalse(self.vm.path(path).exists())
        displaced = next(self.vm.backup().glob("displaced.*"))
        self.assertEqual((displaced / "opt/vm-mcp/new.py").read_text(), "new code")
        self.assertEqual((displaced / "etc/vm-mcp.env").read_text(), "new env")
        self.assertTrue(all(s["UnitFileState"] == "absent" for s in self.vm.units.values()))


if __name__ == "__main__":
    unittest.main()
