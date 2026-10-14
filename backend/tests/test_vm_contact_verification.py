"""Isolated executable witnesses for VM_CONTACT.md verification b/e/f.

Usage: python -m unittest backend.tests.test_vm_contact_verification
Executes the published Python snippets with file, HTTP, process and time boundaries
mocked. No VM access, real credentials, service changes or network requests occur.
Pinned result schema: skill-lib@023ae12 vm-mcp/admin_broker.py:execute_request.
These tests prove runbook checks, not live deployment acceptance.
"""
from __future__ import annotations

import ast
from contextlib import ExitStack, redirect_stdout
import copy
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import types
import unittest
from unittest.mock import patch

RUNBOOK = Path(__file__).resolve().parents[1] / "deploy" / "VM_CONTACT.md"
TARGET = {"root": "/srv/existing", "profile": "personal-console", "port": 9987,
          "admin_socket": "/run/custom/broker.sock", "token_file": "/root/custom-token"}
TOKEN = "test-only-token-" + "x" * 32
SHA = hashlib.sha256(b"id -u").hexdigest()
ROOT_RESULT = {"ok": True, "request_id": "exec_this_call", "mode": "admin", "run_as": "root",
               "uid": 0, "exit_code": 0, "stdout": "0\n", "timed_out": False,
               "stdout_truncated": False, "command_sha256": SHA, "cwd": "/"}
RECEIPT = {k: ROOT_RESULT[k] for k in
           ("request_id", "mode", "run_as", "exit_code", "timed_out", "command_sha256", "cwd")}
RECEIPT["event"] = "vm_mcp_exec"


def snippet(section):
    text = RUNBOOK.read_text().split(f"### {section}.", 1)[1].split("\n### ", 1)[0]
    return re.search(r"python3 (?:-I )?- <<'PY'\n(.*?)\nPY", text, re.S)[1]


class VerificationTests(unittest.TestCase):
    def exercise(self, section="f", target=None, root_result=None, receipt=None, *,
                 sse=False, text_content=False, rpc_error=False, tool_error=False,
                 journal_failure=False, info_override=None, pointer=True, bad_target=False,
                 listeners=None, broker_active=None, socket_exists=None, lower_result=None, resolved_root=None):
        target = copy.deepcopy(TARGET if target is None else target)
        root_result = copy.deepcopy(ROOT_RESULT if root_result is None else root_result)
        receipt = copy.deepcopy(RECEIPT if receipt is None else receipt)
        # Replace only file reading; every target validation/check remains executable.
        tree = ast.parse(snippet(section))
        tree.body = [node for node in tree.body if not
                     (isinstance(node, ast.FunctionDef) and node.name == "private_text")]
        requests, commands, reads = [], [], []
        effective = target if pointer else dict(TARGET, port=8765, profile="personal-console",
                                               root="/srv/vm-mcp/workspace", admin_socket="/run/vm-mcp/admin.sock",
                                               token_file="/etc/credstore/vm-mcp-token")

        def private_text(path):
            path = str(path)
            reads.append(path)
            if path == "/root/vm-mcp-upgrade.latest":
                return "/root/backup-verified\n"
            if path == "/root/backup-verified/target.json":
                if bad_target:
                    raise OSError("unreadable")
                return json.dumps(target)
            if path == effective["token_file"]:
                return TOKEN + "\n"
            raise AssertionError("Unexpected file read: " + path)

        def open_request(req, timeout):
            requests.append(req)
            self.assertEqual(timeout, 15)
            self.assertEqual(req.full_url, f'http://127.0.0.1:{effective["port"]}/mcp')
            payload = json.loads(req.data)
            auth = req.get_header("Authorization", "")
            accepted = auth in ("Bearer " + TOKEN, "bearer " + TOKEN)
            response = {"jsonrpc": "2.0", "id": payload["id"], "result": {}}
            if payload["method"] == "tools/list":
                response["result"] = {"tools": [{"name": "admin_exec"}]}
            if payload["method"] == "tools/call":
                name = payload["params"]["name"]
                if name == "vm_info":
                    value = {"ok": True, "profile": effective["profile"],
                             "admin_socket": effective["admin_socket"],
                             "root": effective["root"], "root_exists": True}
                    value.update(info_override or {})
                else:
                    self.assertEqual(name, "admin_exec")
                    if effective["profile"] == "personal-console":
                        self.assertEqual(payload["params"]["arguments"], {"command": "id -u", "cwd": "/"})
                        value = root_result
                    else:
                        self.assertTrue(payload["params"]["arguments"]["command"].startswith("id -u # vm-mcp-policy-check-"))
                        value = lower_result if lower_result is not None else {"ok": False, "error_type": "PermissionError",
                                 "error": "host execution is disabled; set VM_MCP_PROFILE=personal-console"}
                response["result"] = ({"content": [{"type": "text", "text": json.dumps(value)}]}
                                      if text_content else {"structuredContent": value})
                if name == "admin_exec" and rpc_error:
                    response = {"jsonrpc": "2.0", "id": payload["id"], "error": {"code": -1}}
                if name == "admin_exec" and tool_error:
                    response["result"]["isError"] = True
            body = json.dumps(response)
            if sse:
                body = "event: message\ndata: " + body + "\n\n"
            stream = io.BytesIO(body.encode())
            stream.status = 200 if accepted else 401
            return stream

        def run(args, **kwargs):
            commands.append(args)
            if args[0] == "journalctl":
                self.assertIn("--since", args)
                self.assertEqual(args[args.index("--since") + 1], "@1000.0")
                return types.SimpleNamespace(returncode=int(journal_failure), stdout=json.dumps(receipt))
            if args[0] == "ss":
                addresses = listeners if listeners is not None else [f'127.0.0.1:{effective["port"]}']
                return types.SimpleNamespace(returncode=0, stdout="\n".join(
                    "LISTEN 0 128 " + address + " 0.0.0.0:*" for address in addresses))
            if args[0] == "systemctl":
                if "User" in args:
                    output = "vmmcp"
                elif "ActiveState" in args:
                    output = broker_active or "inactive"
                else:
                    output = broker_active or "active"
                return types.SimpleNamespace(returncode=0, stdout=output)
            raise AssertionError("Unexpected process call: " + repr(args))

        def lexists(path):
            if str(path) == "/root/vm-mcp-upgrade.latest":
                return pointer
            self.assertEqual(str(path), effective["admin_socket"])
            return bool(socket_exists)

        def lstat(path):
            self.assertIn(str(path), [effective["admin_socket"], str(Path(effective["admin_socket"]).parent)])
            is_socket = str(path) == effective["admin_socket"]
            return types.SimpleNamespace(st_uid=0, st_gid=123,
                st_mode=(stat.S_IFSOCK | 0o660) if is_socket else (stat.S_IFDIR | 0o750))

        output = io.StringIO()
        with ExitStack() as stack:
            stack.enter_context(patch("os.path.lexists", side_effect=lexists))
            stack.enter_context(patch("os.lstat", side_effect=lstat))
            stack.enter_context(patch("pathlib.Path.resolve", lambda p, strict=False: Path(resolved_root or str(p))))
            stack.enter_context(patch("grp.getgrnam", return_value=types.SimpleNamespace(gr_gid=123)))
            stack.enter_context(patch("subprocess.run", side_effect=run))
            stack.enter_context(patch("urllib.request.build_opener", return_value=types.SimpleNamespace(open=open_request)))
            stack.enter_context(patch("time.time", return_value=1000.0))
            stack.enter_context(patch("uuid.uuid4", return_value=types.SimpleNamespace(hex="fixed-test-nonce")))
            stack.enter_context(patch("time.monotonic", side_effect=[0, 1, 61]))
            stack.enter_context(patch("time.sleep"))
            stack.enter_context(redirect_stdout(output))
            with self.assertRaises(SystemExit) as exited:
                exec(compile(tree, "VM_CONTACT.md", "exec"), {"private_text": private_text})
        return exited.exception.code, output.getvalue(), requests, commands, reads

    def test_custom_target_used_independently_by_all_checks(self):
        for section in ("b", "e", "f"):
            with self.subTest(section=section):
                code, output, _, _, reads = self.exercise(section)
                self.assertEqual(code, 0, output)
                self.assertIn("/root/backup-verified/target.json", reads)
                if section != "b":
                    self.assertIn(TARGET["token_file"], reads)
                self.assertNotIn(TOKEN, output)

    def test_fresh_defaults_only_when_pointer_absent(self):
        for section in ("b", "e", "f"):
            self.assertEqual(self.exercise(section, pointer=False)[0], 0)
            code, _, requests, commands, _ = self.exercise(section, bad_target=True)
            self.assertTrue(code)
            self.assertEqual(requests, [])
            self.assertEqual(commands, [])

    def test_lower_profiles_require_policy_refusal(self):
        for profile in ("read-only", "workspace"):
            for section in ("b", "e", "f"):
                code, output, requests, commands, _ = self.exercise(section, target=dict(TARGET, profile=profile))
                self.assertEqual(code, 0, output)
                if section == "f":
                    self.assertIn("PASS privileged call refused", output)
                    self.assertIn("PASS no broker receipt", output)
                    self.assertTrue(any(b'admin_exec' in r.data for r in requests))
            self.assertTrue(self.exercise("f", target=dict(TARGET, profile=profile), journal_failure=True)[0])

    def test_lower_profile_wrong_refusal_or_receipt_fails(self):
        target = dict(TARGET, profile="read-only")
        for result in (ROOT_RESULT, {"ok": False, "error_type": "OSError", "error": "connection refused"}):
            self.assertTrue(self.exercise(target=target, lower_result=result)[0])
        digest = hashlib.sha256(b"id -u # vm-mcp-policy-check-fixed-test-nonce").hexdigest()
        self.assertTrue(self.exercise(target=target, receipt=dict(RECEIPT, command_sha256=digest))[0])

    def test_lower_profile_active_broker_or_socket_fails(self):
        lower = dict(TARGET, profile="workspace")
        self.assertTrue(self.exercise("b", target=lower, broker_active="active")[0])
        self.assertTrue(self.exercise("b", target=lower, socket_exists=True)[0])

    def test_wildcard_and_duplicate_listeners_fail(self):
        self.assertTrue(self.exercise("b", listeners=["0.0.0.0:9987"])[0])
        self.assertTrue(self.exercise("b", listeners=["127.0.0.1:9987", "[::]:9987"])[0])

    def test_sse_and_text_content_results(self):
        for sse in (False, True):
            for text_content in (False, True):
                self.assertEqual(self.exercise(sse=sse, text_content=text_content)[0], 0)

    def test_profile_or_socket_mismatch_prevents_privilege(self):
        for override in ({"profile": "workspace"}, {"admin_socket": "/wrong"},
                         {"root": "/wrong-workspace"}, {"root_exists": False}, {"root": None}):
            code, _, requests, _, _ = self.exercise(info_override=override)
            self.assertTrue(code)
            self.assertFalse(any(b'admin_exec' in req.data for req in requests))

    def test_effective_workspace_must_match_resolved_target(self):
        target = dict(TARGET, root="/fixture-alias")
        self.assertEqual(self.exercise(target=target, resolved_root="/fixture-real",
                                       info_override={"root": "/fixture-real"})[0], 0)
        code, _, requests, *_ = self.exercise(target=target, resolved_root="/fixture-real",
                                              info_override={"root": "/fixture-alias"})
        self.assertTrue(code)
        self.assertFalse(any(b'admin_exec' in req.data for req in requests))

    def test_bad_root_response_cannot_pass_on_matching_digest(self):
        for key, value in (("stdout", "1000\n"), ("mode", "user"), ("run_as", "someone"),
                           ("uid", 1000), ("exit_code", 1), ("ok", False), ("timed_out", True),
                           ("stdout_truncated", True), ("request_id", ""), ("uid", False)):
            with self.subTest(key=key, value=value):
                code, output, *_ = self.exercise(root_result=dict(ROOT_RESULT, **{key: value}))
                self.assertTrue(code)
                self.assertIn("FAIL privileged root", output)

    def test_bad_receipt_cannot_pass_on_matching_digest(self):
        for key, value in (("request_id", "exec_old_call"), ("mode", "user"), ("run_as", "someone"),
                           ("exit_code", 1), ("timed_out", True), ("event", "other"), ("exit_code", False)):
            with self.subTest(key=key):
                code, output, *_ = self.exercise(receipt=dict(RECEIPT, **{key: value}))
                self.assertTrue(code)
                self.assertIn("FAIL broker receipt", output)
        self.assertTrue(self.exercise(journal_failure=True)[0])

    def test_json_rpc_and_mcp_errors_fail(self):
        self.assertTrue(self.exercise(rpc_error=True)[0])
        self.assertTrue(self.exercise(tool_error=True)[0])

    def test_invalid_preserved_target_fails_before_inspection(self):
        for change in ({"profile": "unknown"}, {"port": 0}, {"port": 65536},
                       {"token_file": "relative"}, {"admin_socket": "relative"}):
            for section in ("b", "e", "f"):
                code, _, requests, commands, _ = self.exercise(section, target=dict(TARGET, **change))
                self.assertTrue(code)
                self.assertEqual(requests, [])
                self.assertEqual(commands, [])

    def test_private_reader_requires_root_only_regular_file(self):
        tree = ast.parse(snippet("e"))
        definition = next(node for node in tree.body
                          if isinstance(node, ast.FunctionDef) and node.name == "private_text")
        import os
        namespace = {"os": os, "stat": stat}
        exec(compile(ast.Module(body=[definition], type_ignores=[]), "reader", "exec"), namespace)
        for uid, mode, succeeds in ((0, stat.S_IFREG | 0o600, True),
                                    (1, stat.S_IFREG | 0o600, False),
                                    (0, stat.S_IFREG | 0o640, False),
                                    (0, stat.S_IFDIR | 0o600, False)):
            stream = io.StringIO("test-only-value")
            stream.fileno = lambda: 41
            with patch("os.open", return_value=41) as opened, patch("os.fdopen", return_value=stream), patch(
                    "os.fstat", return_value=types.SimpleNamespace(st_mode=mode, st_uid=uid)):
                if succeeds:
                    self.assertEqual(namespace["private_text"]("fixture"), "test-only-value")
                else:
                    with self.assertRaises(ValueError):
                        namespace["private_text"]("fixture")
                opened.assert_called_once_with("fixture", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)

    def test_all_python_payloads_parse_and_never_eval(self):
        for section in ("b", "e", "f"):
            ast.parse(snippet(section))
            self.assertNotIn("eval(", snippet(section))


if __name__ == "__main__":
    unittest.main()
