#!/usr/bin/env node
"use strict";

/**
 * Independent URPCS replay gate.
 *
 * Usage:
 *   node research/urpcs/tests/test_independent_decoder.js
 *
 * The decoder receives only ciphertext, initial state, and associated data.
 * Expected plaintext, receipt, and next state are read only by this comparison
 * harness after decoding returns.
 */

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const decoderPath = path.resolve(__dirname, "..", "urpcs_v1_independent.js");
const vectorsPath = path.resolve(__dirname, "..", "vectors", "urpcs-v1-vectors.json");
const decoder = require(decoderPath);

// === CHECKS ===
// id: check_urpcs_independent_positive_replay
//   proves: urpcs_independent_positive_replay
//   call: self::testPositiveReplay
//   requires: node
//   timeout: 120
//   mutates: none
//   cleanup: none
//
// id: check_urpcs_independent_authentication_boundary
//   proves: urpcs_independent_authentication_boundary
//   call: self::testAuthenticationBoundary
//   requires: node
//   timeout: 30
//   mutates: none
//   cleanup: none
//
// id: check_urpcs_independent_kmac_known_answer
//   proves: urpcs_independent_kmac_known_answer
//   call: self::testKmacKnownAnswer
//   requires: node
//   timeout: 10
//   mutates: none
//   cleanup: none
//
// id: check_urpcs_independent_profile_boundary
//   proves: urpcs_independent_profile_boundary
//   call: self::testProfileBoundary
//   requires: node
//   timeout: 10
//   mutates: none
//   cleanup: none
// === END CHECKS ===

const document = JSON.parse(fs.readFileSync(vectorsPath, "utf8"));
const byId = new Map(document.vectors.map((entry) => [entry.id, entry]));

function stateJson(value) {
  return decoder.stateToJson(value);
}

function testKmacKnownAnswer() {
  const expected = [
    "20c570c31346f703c9ac36c61c03cb64c3970d0cfc787e9b79599d273a68d2f7",
    "f69d4cc3de9d104a351689f27cf6f5951f0103f33f4f24871024d9c27773a8dd",
  ].join("");
  assert.equal(decoder.runKat(), expected);
}

function testProfileBoundary() {
  const input = decoder.vectorInput(byId.get("empty_r0"));
  const outOfProfileState = { ...input.state, RCap: 2 };
  assert.throws(
    () => decoder.decode(input.ciphertext, outOfProfileState, input.associatedData),
    (error) => error instanceof decoder.URPCSError && error.stage === "state",
    "R_cap above the committed bounded profile must fail at state validation",
  );
}

function testPositiveReplay() {
  const results = [];
  for (const id of ["empty_r0", "empty_r1", "odd_09_r0"]) {
    const vector = byId.get(id);
    const input = decoder.vectorInput(vector);
    const result = decoder.decode(input.ciphertext, input.state, input.associatedData);
    assert.equal(result.plaintext.toString("hex"), vector.plaintext_hex, `${id} plaintext`);
    assert.equal(result.receipt.toString("hex"), vector.receipt_hex, `${id} receipt`);
    assert.deepEqual(stateJson(result.nextState), vector.next_state, `${id} next state`);
    results.push({
      id,
      plaintext_hex: result.plaintext.toString("hex"),
      receipt_hex: result.receipt.toString("hex"),
      next_state: stateJson(result.nextState),
    });
  }
  return results;
}

function expectTagFailure(ciphertext, state, associatedData, label) {
  assert.throws(
    () => decoder.decode(ciphertext, state, associatedData),
    (error) => error instanceof decoder.URPCSError && error.stage === "tag",
    label,
  );
}

function testAuthenticationBoundary() {
  const base = byId.get("odd_09_r0");
  const input = decoder.vectorInput(base);
  const wrongAssociatedData = Buffer.from(byId.get("wrong_ad").wrong_ad_hex, "hex");
  expectTagFailure(input.ciphertext, input.state, wrongAssociatedData, "wrong AD");

  const mutation = Buffer.from(byId.get("authenticated_body_mutation").mutated_ciphertext_hex, "hex");
  expectTagFailure(mutation, input.state, input.associatedData, "authenticated body mutation");
}

function testIndependenceSurface() {
  const source = fs.readFileSync(decoderPath, "utf8");
  assert.equal(source.includes("urpcs_v1_reference"), false);
  assert.equal(source.includes("child_process"), false);
}

function main() {
  testIndependenceSurface();
  testKmacKnownAnswer();
  testProfileBoundary();
  const results = testPositiveReplay();
  testAuthenticationBoundary();
  process.stdout.write(`${JSON.stringify({
    classification: "SURVIVED_INDEPENDENTLY",
    positives: results,
    wrong_associated_data: "rejected_at_tag",
    authenticated_body_mutation: "rejected_at_tag",
    kmac256_nist_sample_4: "pass",
  }, null, 2)}\n`);
}

module.exports = {
  testAuthenticationBoundary,
  testKmacKnownAnswer,
  testProfileBoundary,
  testPositiveReplay,
};

if (require.main === module) main();
