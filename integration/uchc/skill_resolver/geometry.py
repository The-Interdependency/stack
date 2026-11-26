# ratios: loc_comments=131:12 imports_exports=2:4 calls_definitions=72:14
"""Reversible skill records on UCHC's ordinal-halving construction.

Use encode_record(record) to obtain a JSON-serializable native UCHC packet.
decode_record(packet) replays its geometry before interpreting the skill profile.
The caller owns the source lock and which fields enter a record.
"""

import math

import uchc_halving as halving


PROFILE = "stack.skill-resolver.geometry/1"
BEARING = "root-endpoint-v1"


def _close_record(record, options):
    if type(record) is not dict:
        raise TypeError("skill geometry requires an object at the root")

    leaves = {}
    markers = {}

    def leaf(text):
        if text not in leaves:
            leaves[text] = halving.construct_text(text, source=PROFILE, **options)
        return leaves[text]

    def sequence(kind, children):
        if kind not in markers:
            markers[kind] = halving.construct_glyph(kind, **options)
        return halving.construct_sequence(
            (markers[kind], *children), source=PROFILE, bearing=BEARING, **options
        )

    def close(value):
        # Type tags are native scalar participants. The first letter of an
        # admitted string remains literal even when it is itself a type tag.
        if type(value) is str:
            return leaf("s" + value)
        if type(value) is dict:
            if any(type(key) is not str for key in value):
                raise TypeError("skill object keys must be strings")
            fields = (
                sequence("p", (close(key), close(value[key]))) for key in sorted(value)
            )
            return sequence("o", fields)
        if type(value) is list:
            return sequence("a", (close(item) for item in value))
        if value is None:
            return leaf("n")
        if type(value) is bool:
            return leaf("t" if value else "f")
        if type(value) is int:
            return leaf("i" + str(value))
        if type(value) is float and math.isfinite(value):
            return leaf("d" + value.hex())
        raise ValueError("skill record contains an unsupported JSON value")

    return close(record)


def encode_record(record: dict, *, ucns_source_root=None) -> dict:
    """Close a JSON object. Maps sort Unicode keys; arrays retain occurrence order."""
    options = {"ucns_source_root": ucns_source_root}
    return halving.closed_record(_close_record(record, options), **options)


def _literal(text):
    tag, body = text[0], text[1:]
    if tag == "s":
        return body
    if text in ("n", "t", "f"):
        return {"n": None, "t": True, "f": False}[text]
    if tag == "i":
        number = int(body)
        if str(number) == body:
            return number
    if tag == "d":
        number = float.fromhex(body)
        if math.isfinite(number) and number.hex() == body:
            return number
    raise ValueError("invalid skill literal")


def _replay(closed, options):
    if type(closed) is not dict or closed.get("record_version") != 2:
        raise ValueError("skill geometry requires a current UCHC packet")
    return halving.replay_closed(closed, **options)


def _check_node(node):
    if node.source != PROFILE or node.radius != 1:
        raise ValueError("unexpected skill geometry profile or placement radius")


def _parts(node):
    _check_node(node)
    if node.relation != halving.PROFILE + ":sequence":
        raise ValueError("expected a skill sequence")
    marker, *children = node.participants
    if hasattr(marker, "interior") or any(
        getattr(child, "bearing", None) != BEARING for child in children
    ):
        raise ValueError("invalid skill sequence operands or bearing")
    return marker.identity, [child.interior for child in children]


def _recover_record(root):
    def recover(node):
        _check_node(node)
        if node.relation == halving.PROFILE + ":text":
            # replay_closed checked the literal against the actual scalar sequence.
            return _literal(node.identity)
        tag, children = _parts(node)
        if tag == "a":
            return [recover(child) for child in children]
        if tag != "o":
            raise ValueError("expected a skill object or array")

        result = {}
        previous = None
        for field in children:
            kind, pair = _parts(field)
            if kind != "p" or len(pair) != 2:
                raise ValueError("expected an ordered key/value pair")
            key = recover(pair[0])
            if type(key) is not str or (previous is not None and key <= previous):
                raise ValueError("skill object keys must be unique strings in canonical order")
            result[key] = recover(pair[1])
            previous = key
        return result

    decoded = recover(root)
    if type(decoded) is not dict:
        raise ValueError("skill geometry root must be an object")
    return decoded


def decode_record(closed, *, ucns_source_root=None) -> dict:
    """Verify a current native packet and recover its record from the closed operands."""
    return _recover_record(_replay(closed, {"ucns_source_root": ucns_source_root}))


def compose_bundle(packets: list[dict], resolution: dict, *, ucns_source_root=None) -> dict:
    """Place exact closed skill interiors and an independently closed decision in one bundle."""
    options = {"ucns_source_root": ucns_source_root}
    records = []
    for packet in packets:
        root = _replay(packet, options)
        _recover_record(root)
        records.append(root)
    order = halving.construct_sequence(
        (halving.construct_glyph("l", **options), *records),
        source=PROFILE, bearing=BEARING, **options,
    )
    decision = _close_record(resolution, options)
    bundle = halving.construct_sequence(
        (halving.construct_glyph("b", **options), order, decision),
        source=PROFILE, bearing=BEARING, **options,
    )
    return halving.closed_record(bundle, **options)


def replay_bundle(packet, *, ucns_source_root=None) -> tuple[list[dict], dict]:
    """Recover the ordered skill sequence and the resolution from one verified native graph."""
    root = _replay(packet, {"ucns_source_root": ucns_source_root})
    tag, children = _parts(root)
    if tag != "b" or len(children) != 2:
        raise ValueError("expected a skill activation bundle")
    group, decision = children
    tag, records = _parts(group)
    if tag != "l":
        raise ValueError("expected an ordered group of skills")
    return [_recover_record(skill) for skill in records], _recover_record(decision)
# ratios: loc_comments=131:12 imports_exports=2:4 calls_definitions=72:14
