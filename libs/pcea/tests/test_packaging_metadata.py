# ratios: loc_comments=10:2 imports_exports=2:2 calls_definitions=2:2
# GPT/Claude generated; context, prompt Erin Spencer
"""Packaging metadata regression checks."""

from __future__ import annotations

import pathlib


def test_pyproject_declares_readme_and_spdx_license() -> None:
    pyproject = pathlib.Path("pyproject.toml").read_text(encoding="utf-8")

    assert 'readme = "README.md"' in pyproject
    assert 'license = "MIT"' in pyproject


def test_package_discovery_excludes_research_workspace() -> None:
    pyproject = pathlib.Path("pyproject.toml").read_text(encoding="utf-8")

    assert 'include = ["pcea", "pcea.*"]' in pyproject
    assert 'include = ["pcea*"]' not in pyproject
# ratios: loc_comments=10:2 imports_exports=2:2 calls_definitions=2:2
