# ratios: loc_comments=26:16 imports_exports=2:3 calls_definitions=18:3


"""A0 instance nomenclature.

The canonical naming grammar is ``owner( a0( <energy> ) <auditor/teacher> )``:

- the wrapper is the owning user/lineage;
- the energy inside ``a0( … )`` names the interchangeable provider;
- the trailing auditor/teacher names an outer model when one is attached.

For a bare-model A0 on DeepSeek energy the name is ``a0(deepseek)``. The
energy slot accepts any registered provider, so the same grammar covers
``a0(openai)``, ``a0(xai)``, or any runtime-registered provider.
"""

from __future__ import annotations

import re

_LABEL_RE = re.compile(r"^a0\(([A-Za-z0-9_.-]+)\)$")


def energy_label(provider_name: str) -> str:
    """Return the bare-instance label for an energy provider."""
    if not isinstance(provider_name, str) or not provider_name:
        raise ValueError("provider name must be non-empty text")
    return f"a0({provider_name})"


def parse_energy_label(label: str) -> str | None:
    """Return the provider name encoded by ``a0(<provider>)``, else ``None``."""
    match = _LABEL_RE.match(label or "")
    return match.group(1) if match else None


def instance_label(
    provider_name: str,
    *,
    owner: str | None = None,
    auditor: str | None = None,
) -> str:
    """Build a full instance label from the canonical grammar.

    ``instance_label("deepseek")`` -> ``a0(deepseek)``;
    ``instance_label("deepseek", owner="wayseer", auditor="deepseek-v4-pro")``
    -> ``wayseer(a0(deepseek)deepseek-v4-pro)``.
    """
    body = energy_label(provider_name)
    if auditor:
        if not isinstance(auditor, str) or not auditor:
            raise ValueError("auditor must be non-empty text")
        body += auditor
    if owner:
        if not isinstance(owner, str) or not owner:
            raise ValueError("owner must be non-empty text")
        body = f"{owner}({body})"
    return body
# ratios: loc_comments=26:16 imports_exports=2:3 calls_definitions=18:3
