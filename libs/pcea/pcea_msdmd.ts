import { defineMsdmdCollection } from "./.agents/skills/msdmd/collection";

export default defineMsdmdCollection({
  "declarations": [
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_validate_seed, _contributors, _encrypt_element, _decrypt_element",
        "module_kind": "engine",
        "module_name": "cipher",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "encrypt_seed, decrypt_seed, encrypt_state, decrypt_state, CIRCLE_COUNT, TENSOR_COUNT, DEFAULT_WORD_BITS",
        "requires": "pcea_codec, pcea_kdf, pcea_primes",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "prime-circular Mobius disk cipher: fixed-width base-p digit encode with SHA-256 keyed additive shift",
        "tests": "tests.test_cipher",
        "unresolved": "security-critical module; changes require independent crypto review",
        "user_data_boundary": "none"
      },
      "file": "pcea/cipher.py",
      "id": "pcea_cipher"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "adapter",
        "module_name": "codec",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "mobius_encode, mobius_decode, digit_count, to_fixed, from_fixed",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Mobius disk codec: signed<->unsigned position mapping and fixed-width base-p digit encoding",
        "tests": "tests.test_codec",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "pcea/codec.py",
      "id": "pcea_codec"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "contract",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "DECISION, SECURITY_INVARIANT, FORBIDDEN_UCNS_SYMBOLS, RUNTIME_MODULES, contract_statement",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "PCEA<->UCNS interface-contract constants and guardrails (single source of truth)",
        "tests": "tests.test_contract_spec",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "pcea/contract.py",
      "id": "pcea_contract"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_zero_seed",
        "module_kind": "service",
        "module_name": "instance",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "PCEAInstance",
        "requires": "pcea_cipher",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "stateful PCEA session that auto-advances last_state so sender/receiver stay synchronized",
        "tests": "tests.test_instance",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "pcea/instance.py",
      "id": "pcea_instance"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "kdf",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "key_stream",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "hash-based key-stream derivation keyed by hierarchical address plus heptagram neighbors",
        "tests": "tests.test_kdf",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "pcea/kdf.py",
      "id": "pcea_kdf"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_sieve",
        "module_kind": "schema",
        "module_name": "primes",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "prime_at, PRIME_CIRCLE, CIRCLE_SIZE",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "fixed 53-prime circle used as the circular bases for prime-circular base encryption",
        "tests": "tests.test_primes",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "pcea/primes.py",
      "id": "pcea_primes"
    }
  ],
  "edges": [
    {
      "from": "pcea_cipher",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_cipher",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_cipher",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_cipher",
      "to": "pcea_codec"
    },
    {
      "from": "pcea_cipher",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_cipher",
      "to": "pcea_kdf"
    },
    {
      "from": "pcea_cipher",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_cipher",
      "to": "pcea_primes"
    },
    {
      "from": "pcea_codec",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_codec",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_codec",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_codec",
      "to": "none"
    },
    {
      "from": "pcea_contract",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_contract",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_contract",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_contract",
      "to": "none"
    },
    {
      "from": "pcea_instance",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_instance",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_instance",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_instance",
      "to": "pcea_cipher"
    },
    {
      "from": "pcea_kdf",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_kdf",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_kdf",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_kdf",
      "to": "none"
    },
    {
      "from": "pcea_primes",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_primes",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_primes",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_primes",
      "to": "none"
    }
  ],
  "gaps": [],
  "repo": "pcea",
  "source_commit": "fea83bb"
});
