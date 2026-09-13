import { defineMsdmdCollection } from "./.agents/skills/msdmd/collection";

export default defineMsdmdCollection({
  "declarations": [
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "encrypt_seed receives any plaintext element outside the signed word_bits range",
        "then": "raises ValueError before emitting ciphertext"
      },
      "file": "pcea/cipher.py",
      "id": "cipher_rejects_plaintext_outside_word_range"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "decrypt_seed receives valid fixed-width ciphertext but a mismatched last_seed",
        "then": "returns deterministic signed word_bits values instead of surfacing unused code-point overflow"
      },
      "file": "pcea/cipher.py",
      "id": "cipher_wrong_key_decrypt_returns_signed_words"
    },
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
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "mobius_encode receives a value outside the signed word_bits range",
        "then": "raises ValueError instead of wrapping to a different plaintext"
      },
      "file": "pcea/codec.py",
      "id": "codec_rejects_out_of_range_signed_words"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "to_fixed receives an unsigned value that cannot fit in k base-p digits",
        "then": "raises ValueError instead of truncating high-order digits"
      },
      "file": "pcea/codec.py",
      "id": "fixed_width_codec_rejects_overflow"
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
        "summary": "Mobius disk codec: signed<->unsigned position mapping and fixed-width base-p digit encoding with explicit word-range guards",
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
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_encrypt_seed_rejects_plaintext_outside_word_range",
        "cleanup": "none",
        "mutates": "none",
        "proves": "cipher_rejects_plaintext_outside_word_range",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_cipher.py",
      "id": "check_cipher_rejects_plaintext_outside_word_range"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_decrypt_seed_with_wrong_key_returns_signed_words",
        "cleanup": "none",
        "mutates": "none",
        "proves": "cipher_wrong_key_decrypt_returns_signed_words",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_cipher.py",
      "id": "check_cipher_wrong_key_decrypt_returns_signed_words"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_encode_rejects_values_outside_signed_word_range",
        "cleanup": "none",
        "mutates": "none",
        "proves": "codec_rejects_out_of_range_signed_words",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_codec.py",
      "id": "check_codec_rejects_out_of_range_signed_words"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_to_fixed_rejects_overflow",
        "cleanup": "none",
        "mutates": "none",
        "proves": "fixed_width_codec_rejects_overflow",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_codec.py",
      "id": "check_fixed_width_codec_rejects_overflow"
    }
  ],
  "edges": [
    {
      "from": "check_cipher_rejects_plaintext_outside_word_range",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_cipher_rejects_plaintext_outside_word_range",
      "to": "self::test_encrypt_seed_rejects_plaintext_outside_word_range"
    },
    {
      "from": "check_cipher_rejects_plaintext_outside_word_range",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_cipher_rejects_plaintext_outside_word_range",
      "to": "cipher_rejects_plaintext_outside_word_range"
    },
    {
      "from": "check_cipher_rejects_plaintext_outside_word_range",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_cipher_rejects_plaintext_outside_word_range",
      "to": "python3"
    },
    {
      "from": "check_cipher_wrong_key_decrypt_returns_signed_words",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_cipher_wrong_key_decrypt_returns_signed_words",
      "to": "self::test_decrypt_seed_with_wrong_key_returns_signed_words"
    },
    {
      "from": "check_cipher_wrong_key_decrypt_returns_signed_words",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_cipher_wrong_key_decrypt_returns_signed_words",
      "to": "cipher_wrong_key_decrypt_returns_signed_words"
    },
    {
      "from": "check_cipher_wrong_key_decrypt_returns_signed_words",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_cipher_wrong_key_decrypt_returns_signed_words",
      "to": "python3"
    },
    {
      "from": "check_codec_rejects_out_of_range_signed_words",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_codec_rejects_out_of_range_signed_words",
      "to": "self::test_encode_rejects_values_outside_signed_word_range"
    },
    {
      "from": "check_codec_rejects_out_of_range_signed_words",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_codec_rejects_out_of_range_signed_words",
      "to": "codec_rejects_out_of_range_signed_words"
    },
    {
      "from": "check_codec_rejects_out_of_range_signed_words",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_codec_rejects_out_of_range_signed_words",
      "to": "python3"
    },
    {
      "from": "check_fixed_width_codec_rejects_overflow",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_fixed_width_codec_rejects_overflow",
      "to": "self::test_to_fixed_rejects_overflow"
    },
    {
      "from": "check_fixed_width_codec_rejects_overflow",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_fixed_width_codec_rejects_overflow",
      "to": "fixed_width_codec_rejects_overflow"
    },
    {
      "from": "check_fixed_width_codec_rejects_overflow",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_fixed_width_codec_rejects_overflow",
      "to": "python3"
    },
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
  "repo": "pcea"
});
