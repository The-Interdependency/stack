#!/usr/bin/env node
"use strict";

/**
 * Clean-room URPCS v1 decoder for the committed bounded harness profile.
 *
 * Usage:
 *   node research/urpcs/urpcs_v1_independent.js --kat
 *   node research/urpcs/urpcs_v1_independent.js \
 *     --vector empty_r0 research/urpcs/vectors/urpcs-v1-vectors.json
 *
 * The decoder consumes only ciphertext, initial state, and associated-data
 * bytes. Vector plaintext, receipt, and successor state are comparison outputs,
 * not decoder inputs. This is Stack-local interoperability research, not a
 * confidentiality or production-security construction.
 */

const crypto = require("node:crypto");
const fs = require("node:fs");

// === MODULE_BUILD ===
// id: urpcs_v1_clean_room_decoder
//   module_name: URPCS v1 clean-room decoder
//   module_kind: experiment
//   summary: independently decodes the committed URPCS v1 profile from the public contract
//   owner: The-Interdependency/stack URPCS research
//   public_surface: decode, kmac256, command-line vector replay
//   internal_surface: deterministic CBOR, Keccak-f1600, witness validation, reverse expansion, state advance
//   auth_boundary: none
//   storage_boundary: read
//   network_boundary: none
//   user_data_boundary: none
//   admin_only: false
//   tests: research/urpcs/tests/test_independent_decoder.js
//   rollout: manual research gate and CI check
//   rollback: remove the independent module, test, and CI step
// === END MODULE_BUILD ===

// === CONTRACTS ===
// id: urpcs_independent_positive_replay
//   given: committed ciphertext, initial state, and associated data for a positive vector
//   then: recovered plaintext, deterministic receipt, and successor state equal the committed outputs
//   class: evidence
//
// id: urpcs_independent_authentication_boundary
//   given: wrong associated data or an authenticated-body mutation
//   then: decoding fails at tag verification before bootstrap parsing or state advance
//   class: correctness
//
// id: urpcs_independent_kmac_known_answer
//   given: NIST SP 800-185 KMAC Sample 4 inputs
//   then: the independent KMAC256 primitive emits the official 512-bit output
//   class: evidence
// === END CONTRACTS ===

const PROFILE = Object.freeze({
  xBytes: 1,
  M: 8,
  maxInputBytes: 1,
  maxIntermediateBytes: 1 << 20,
  maxLayerWireBytes: 1 << 20,
  maxBetaBytes: 4 << 20,
  maxC0Bytes: 8 << 20,
  maxTraceWireBytes: 16 << 20,
});

const ASCII = Object.freeze({
  frame: Buffer.from("URPCF001", "ascii"),
  bootstrap: Buffer.from("URPCS001", "ascii"),
  layer: Buffer.from("URGON001", "ascii"),
  origin: Buffer.from([0x4f, 0x52, 0x47, 0x01]),
  occurrence: Buffer.from([0x4f, 0x43, 0x43, 0x01]),
  pair: Buffer.from("URPCS/PAIR/v1", "ascii"),
  tag: Buffer.from("URPCS/TAG/v1", "ascii"),
  receipt: Buffer.from("URPCS/RECEIPT/v1", "ascii"),
  advancePair: Buffer.from("URPCS/ADV/PAIR/v1", "ascii"),
  advanceIntegrity: Buffer.from("URPCS/ADV/INTEGRITY/v1", "ascii"),
  advanceRoot: Buffer.from("URPCS/ADV/ROOT/v1", "ascii"),
});

const MASK64 = (1n << 64n) - 1n;
const MOD256 = 1n << 256n;
const ROTATION = Object.freeze([
  0, 1, 62, 28, 27,
  36, 44, 6, 55, 20,
  3, 10, 43, 25, 39,
  41, 45, 15, 21, 8,
  18, 2, 61, 56, 14,
]);
const ROUND_CONSTANTS = Object.freeze([
  0x0000000000000001n, 0x0000000000008082n,
  0x800000000000808an, 0x8000000080008000n,
  0x000000000000808bn, 0x0000000080000001n,
  0x8000000080008081n, 0x8000000000008009n,
  0x000000000000008an, 0x0000000000000088n,
  0x0000000080008009n, 0x000000008000000an,
  0x000000008000808bn, 0x800000000000008bn,
  0x8000000000008089n, 0x8000000000008003n,
  0x8000000000008002n, 0x8000000000000080n,
  0x000000000000800an, 0x800000008000000an,
  0x8000000080008081n, 0x8000000000008080n,
  0x0000000080000001n, 0x8000000080008008n,
]);

class URPCSError extends Error {
  constructor(stage, message) {
    super(`${stage}: ${message}`);
    this.name = "URPCSError";
    this.stage = stage;
  }
}

function demand(condition, stage, message) {
  if (!condition) throw new URPCSError(stage, message);
}

function asBytes(value, stage, name) {
  demand(Buffer.isBuffer(value), stage, `${name} must be bytes`);
  return value;
}

function asArray(value, stage, name, length = null) {
  demand(Array.isArray(value), stage, `${name} must be an array`);
  if (length !== null) demand(value.length === length, stage, `${name} length`);
  return value;
}

function concat(...parts) {
  return Buffer.concat(parts);
}

function equalBytes(a, b) {
  return a.length === b.length && a.equals(b);
}

function compareBytes(a, b) {
  return Buffer.compare(a, b);
}

function hexKey(value) {
  return value.toString("hex");
}

function rotl64(value, shift) {
  if (shift === 0) return value & MASK64;
  const amount = BigInt(shift);
  return ((value << amount) | (value >> (64n - amount))) & MASK64;
}

function keccakF1600(state) {
  for (const roundConstant of ROUND_CONSTANTS) {
    const columns = new Array(5).fill(0n);
    for (let x = 0; x < 5; x += 1) {
      for (let y = 0; y < 5; y += 1) columns[x] ^= state[x + 5 * y];
    }
    const deltas = new Array(5);
    for (let x = 0; x < 5; x += 1) {
      deltas[x] = columns[(x + 4) % 5] ^ rotl64(columns[(x + 1) % 5], 1);
    }
    for (let x = 0; x < 5; x += 1) {
      for (let y = 0; y < 5; y += 1) state[x + 5 * y] ^= deltas[x];
    }

    const moved = new Array(25).fill(0n);
    for (let x = 0; x < 5; x += 1) {
      for (let y = 0; y < 5; y += 1) {
        const newX = y;
        const newY = (2 * x + 3 * y) % 5;
        moved[newX + 5 * newY] = rotl64(state[x + 5 * y], ROTATION[x + 5 * y]);
      }
    }

    for (let y = 0; y < 5; y += 1) {
      for (let x = 0; x < 5; x += 1) {
        const current = moved[x + 5 * y];
        const next = moved[((x + 1) % 5) + 5 * y];
        const nextNext = moved[((x + 2) % 5) + 5 * y];
        state[x + 5 * y] = (current ^ ((~next & MASK64) & nextNext)) & MASK64;
      }
    }
    state[0] ^= roundConstant;
  }
}

function xorBlockIntoState(state, block, rateBytes) {
  for (let offset = 0; offset < rateBytes; offset += 8) {
    let lane = 0n;
    for (let index = 0; index < 8; index += 1) {
      lane |= BigInt(block[offset + index]) << BigInt(8 * index);
    }
    state[offset / 8] ^= lane;
  }
}

function stateRateBytes(state, rateBytes) {
  const output = Buffer.alloc(rateBytes);
  for (let offset = 0; offset < rateBytes; offset += 8) {
    const lane = state[offset / 8];
    for (let index = 0; index < 8; index += 1) {
      output[offset + index] = Number((lane >> BigInt(8 * index)) & 0xffn);
    }
  }
  return output;
}

function keccakSponge(message, suffix, outputBytes, rateBytes = 136) {
  const remainder = message.length % rateBytes;
  const paddingLength = remainder === 0 ? rateBytes : rateBytes - remainder;
  const padded = Buffer.alloc(message.length + paddingLength);
  message.copy(padded);
  padded[message.length] = suffix;
  padded[padded.length - 1] |= 0x80;

  const state = new Array(25).fill(0n);
  for (let offset = 0; offset < padded.length; offset += rateBytes) {
    xorBlockIntoState(state, padded.subarray(offset, offset + rateBytes), rateBytes);
    keccakF1600(state);
  }

  const chunks = [];
  let remaining = outputBytes;
  while (remaining > 0) {
    const block = stateRateBytes(state, rateBytes);
    chunks.push(block.subarray(0, Math.min(remaining, rateBytes)));
    remaining -= Math.min(remaining, rateBytes);
    if (remaining > 0) keccakF1600(state);
  }
  return Buffer.concat(chunks);
}

function encodeUnsigned(value) {
  let number = BigInt(value);
  demand(number >= 0n, "primitive", "negative encoding input");
  let width = 1;
  while (number >= (1n << BigInt(8 * width))) width += 1;
  const output = Buffer.alloc(width);
  for (let index = width - 1; index >= 0; index -= 1) {
    output[index] = Number(number & 0xffn);
    number >>= 8n;
  }
  return output;
}

function leftEncode(value) {
  const encoded = encodeUnsigned(value);
  return concat(Buffer.from([encoded.length]), encoded);
}

function rightEncode(value) {
  const encoded = encodeUnsigned(value);
  return concat(encoded, Buffer.from([encoded.length]));
}

function encodeString(value) {
  return concat(leftEncode(BigInt(value.length) * 8n), value);
}

function bytepad(value, width) {
  const prefixed = concat(leftEncode(width), value);
  const padding = (width - (prefixed.length % width)) % width;
  return concat(prefixed, Buffer.alloc(padding));
}

function cshake256(message, outputBytes, functionName, customization) {
  if (functionName.length === 0 && customization.length === 0) {
    return keccakSponge(message, 0x1f, outputBytes);
  }
  const prefix = bytepad(concat(encodeString(functionName), encodeString(customization)), 136);
  return keccakSponge(concat(prefix, message), 0x04, outputBytes);
}

function kmac256(key, message, outputBytes = 32, customization = Buffer.alloc(0)) {
  demand(Buffer.isBuffer(key) && Buffer.isBuffer(message), "primitive", "KMAC byte inputs");
  const encodedKey = bytepad(encodeString(key), 136);
  const payload = concat(encodedKey, message, rightEncode(BigInt(outputBytes) * 8n));
  return cshake256(payload, outputBytes, Buffer.from("KMAC", "ascii"), customization);
}

function sha3_256(message) {
  return crypto.createHash("sha3-256").update(message).digest();
}

function cborHead(major, length) {
  const value = BigInt(length);
  demand(value >= 0n, "cbor", "negative length");
  if (value < 24n) return Buffer.from([(major << 5) | Number(value)]);
  if (value <= 0xffn) return Buffer.from([(major << 5) | 24, Number(value)]);
  if (value <= 0xffffn) {
    const output = Buffer.alloc(3);
    output[0] = (major << 5) | 25;
    output.writeUInt16BE(Number(value), 1);
    return output;
  }
  if (value <= 0xffffffffn) {
    const output = Buffer.alloc(5);
    output[0] = (major << 5) | 26;
    output.writeUInt32BE(Number(value), 1);
    return output;
  }
  demand(value <= 0xffffffffffffffffn, "cbor", "length exceeds uint64");
  const output = Buffer.alloc(9);
  output[0] = (major << 5) | 27;
  output.writeBigUInt64BE(value, 1);
  return output;
}

function cborEncode(value) {
  if (Buffer.isBuffer(value)) return concat(cborHead(2, value.length), value);
  if (Array.isArray(value)) {
    return concat(cborHead(4, value.length), ...value.map((entry) => cborEncode(entry)));
  }
  if (value === false) return Buffer.from([0xf4]);
  if (value === true) return Buffer.from([0xf5]);
  throw new URPCSError("cbor", "unsupported value type");
}

class CborReader {
  constructor(data) {
    this.data = data;
    this.offset = 0;
    this.elements = 0;
  }

  readByte() {
    demand(this.offset < this.data.length, "cbor", "truncated input");
    const value = this.data[this.offset];
    this.offset += 1;
    return value;
  }

  readLength(additional) {
    if (additional < 24) return additional;
    let value;
    if (additional === 24) value = BigInt(this.readByte());
    else if (additional === 25) {
      demand(this.offset + 2 <= this.data.length, "cbor", "truncated uint16 length");
      value = BigInt(this.data.readUInt16BE(this.offset));
      this.offset += 2;
    } else if (additional === 26) {
      demand(this.offset + 4 <= this.data.length, "cbor", "truncated uint32 length");
      value = BigInt(this.data.readUInt32BE(this.offset));
      this.offset += 4;
    } else if (additional === 27) {
      demand(this.offset + 8 <= this.data.length, "cbor", "truncated uint64 length");
      value = this.data.readBigUInt64BE(this.offset);
      this.offset += 8;
    } else {
      throw new URPCSError("cbor", "indefinite or reserved length");
    }
    demand(value <= BigInt(Number.MAX_SAFE_INTEGER), "cbor", "length exceeds safe range");
    return Number(value);
  }

  read(depth = 0) {
    demand(depth <= 64, "cbor", "nesting limit");
    this.elements += 1;
    demand(this.elements <= 2_000_000, "cbor", "element limit");
    const initial = this.readByte();
    const major = initial >> 5;
    const additional = initial & 0x1f;
    if (major === 2) {
      const length = this.readLength(additional);
      demand(this.offset + length <= this.data.length, "cbor", "truncated byte string");
      const value = Buffer.from(this.data.subarray(this.offset, this.offset + length));
      this.offset += length;
      return value;
    }
    if (major === 4) {
      const length = this.readLength(additional);
      const value = [];
      for (let index = 0; index < length; index += 1) value.push(this.read(depth + 1));
      return value;
    }
    if (major === 7 && additional === 20) return false;
    if (major === 7 && additional === 21) return true;
    throw new URPCSError("cbor", "forbidden major type");
  }
}

function cborDecodeCanonical(data, stage = "cbor") {
  try {
    const reader = new CborReader(data);
    const value = reader.read();
    demand(reader.offset === data.length, stage, "trailing CBOR bytes");
    demand(equalBytes(cborEncode(value), data), stage, "non-canonical CBOR");
    return value;
  } catch (error) {
    if (error instanceof URPCSError && error.stage === stage) throw error;
    if (error instanceof URPCSError) throw new URPCSError(stage, error.message);
    throw error;
  }
}

function natural(value) {
  let number = BigInt(value);
  demand(number >= 0n, "number", "negative natural");
  if (number === 0n) return Buffer.alloc(0);
  const output = encodeUnsigned(number);
  demand(output[0] !== 0, "number", "leading zero");
  return output;
}

function decodeNaturalBig(value, stage, name) {
  const bytes = asBytes(value, stage, name);
  demand(bytes.length === 0 || bytes[0] !== 0, stage, `${name} leading zero`);
  let number = 0n;
  for (const byte of bytes) number = (number << 8n) | BigInt(byte);
  return number;
}

function decodeNatural(value, stage, name) {
  const number = decodeNaturalBig(value, stage, name);
  demand(number <= BigInt(Number.MAX_SAFE_INTEGER), stage, `${name} exceeds safe range`);
  return Number(number);
}

function fixed32(value) {
  let number = BigInt(value);
  demand(number >= 0n && number < MOD256, "state", "BE256 range");
  const output = Buffer.alloc(32);
  for (let index = 31; index >= 0; index -= 1) {
    output[index] = Number(number & 0xffn);
    number >>= 8n;
  }
  return output;
}

function bytesToBigInt(value) {
  let number = 0n;
  for (const byte of value) number = (number << 8n) | BigInt(byte);
  return number;
}

function validateSortedSet(rows, stage, name) {
  asArray(rows, stage, name);
  let previous = null;
  for (const row of rows) {
    const encoded = cborEncode(row);
    if (previous !== null) demand(compareBytes(previous, encoded) < 0, stage, `${name} ordering`);
    previous = encoded;
  }
}

function compareRowSets(actual, expected, stage, name) {
  const actualBytes = actual.map((row) => cborEncode(row));
  const expectedBytes = expected.map((row) => cborEncode(row)).sort(compareBytes);
  demand(actualBytes.length === expectedBytes.length, stage, `${name} count`);
  for (let index = 0; index < actualBytes.length; index += 1) {
    demand(equalBytes(actualBytes[index], expectedBytes[index]), stage, `${name} row ${index}`);
  }
}

function parseAxis(axis) {
  const value = cborDecodeCanonical(axis, "axis");
  asArray(value, "axis", "axis", 2);
  const q = decodeNatural(value[0], "axis", "q");
  const packed = asBytes(value[1], "axis", "packed");
  demand(q > 0, "axis", "empty primitive axis");
  demand(packed.length === Math.ceil(q / 8), "axis", "packed length");
  if (q % 8 !== 0) {
    const unusedMask = (1 << (8 - (q % 8))) - 1;
    demand((packed[packed.length - 1] & unusedMask) === 0, "axis", "nonzero padding bits");
  }
  const bits = [];
  for (let index = 0; index < q; index += 1) {
    bits.push((packed[Math.floor(index / 8)] >> (7 - (index % 8))) & 1);
  }
  return { q, packed, bits };
}

function packBits(bits) {
  const output = Buffer.alloc(Math.ceil(bits.length / 8));
  for (let index = 0; index < bits.length; index += 1) {
    output[Math.floor(index / 8)] |= bits[index] << (7 - (index % 8));
  }
  return output;
}

function bufferBits(value) {
  const bits = [];
  for (const byte of value) {
    for (let shift = 7; shift >= 0; shift -= 1) bits.push((byte >> shift) & 1);
  }
  return bits;
}

function axisForBits(bits) {
  return cborEncode([natural(bits.length), packBits(bits)]);
}

function occurrenceId(origin, position, axis) {
  return concat(ASCII.occurrence, cborEncode([origin, natural(position), axis]));
}

function originId(state, r, j) {
  return concat(ASCII.origin, cborEncode([state.nuOrigin, natural(r), natural(j)]));
}

function pairGonolId(origin, first, second) {
  return concat(Buffer.from([1]), cborEncode([origin, first, second]));
}

function carryGonolId(origin, occurrence) {
  return concat(Buffer.from([0]), cborEncode([origin, occurrence]));
}

function detect(regionBytes, origin) {
  const bits = bufferBits(regionBytes);
  const rows = [];
  let position = 0;
  while (position < bits.length) {
    let selected = 1;
    for (let q = 2; position + q <= bits.length; q += 1) {
      let repeated = false;
      for (let witness = 0; witness + q <= bits.length; witness += 1) {
        if (witness === position) continue;
        const disjoint = position + q <= witness || witness + q <= position;
        if (!disjoint) continue;
        let equal = true;
        for (let offset = 0; offset < q; offset += 1) {
          if (bits[position + offset] !== bits[witness + offset]) {
            equal = false;
            break;
          }
        }
        if (equal) {
          repeated = true;
          break;
        }
      }
      if (repeated) selected = q;
    }
    const axis = axisForBits(bits.slice(position, position + selected));
    const occurrence = occurrenceId(origin, position, axis);
    rows.push([axis, origin, natural(position), occurrence]);
    position += selected;
  }
  return rows;
}

function validateState(state) {
  const normalized = {
    kPair: Buffer.from(state.kPair),
    kIntegrity: Buffer.from(state.kIntegrity),
    kAdvance: Buffer.from(state.kAdvance),
    nuOrigin: Buffer.from(state.nuOrigin),
    RCap: state.RCap,
  };
  for (const [name, value] of Object.entries({
    kPair: normalized.kPair,
    kIntegrity: normalized.kIntegrity,
    kAdvance: normalized.kAdvance,
    nuOrigin: normalized.nuOrigin,
  })) demand(value.length === 32, "state", `${name} length`);
  demand(!equalBytes(normalized.kPair, normalized.kIntegrity), "state", "distinct keys");
  demand(!equalBytes(normalized.kPair, normalized.kAdvance), "state", "distinct keys");
  demand(!equalBytes(normalized.kIntegrity, normalized.kAdvance), "state", "distinct keys");
  demand(Number.isInteger(normalized.RCap) && normalized.RCap >= 0 && normalized.RCap <= 0xffffffff,
    "state", "R_cap range");
  demand(bytesToBigInt(normalized.nuOrigin) !== MOD256 - 1n, "state", "origin chain exhausted");
  return normalized;
}

function analyzeWitness(beta, state) {
  demand(beta.length <= PROFILE.maxBetaBytes, "witness", "beta cap");
  const wire = cborDecodeCanonical(beta, "witness");
  asArray(wire, "witness", "Wire", 5);
  const [aRows, relations, deltaRows, traversal, halt] = wire;
  asArray(relations, "witness", "R", 5);
  const [originRows, pairRows, memberRows, occurRows, attachRows] = relations;
  for (const [name, rows] of Object.entries({
    A: aRows,
    R_origin: originRows,
    R_pair: pairRows,
    R_member: memberRows,
    R_occur: occurRows,
    R_attach: attachRows,
    Delta: deltaRows,
  })) validateSortedSet(rows, "witness", name);

  asArray(traversal, "witness", "T", 2);
  demand(Array.isArray(traversal[0]) && traversal[0].length === 0 && traversal[1] === true,
    "witness", "finished traversal cursor");
  asArray(halt, "witness", "L", 2);
  demand(decodeNatural(halt[0], "witness", "halt q") === 32, "witness", "halt q");
  const haltPacked = asBytes(halt[1], "witness", "halt packed");
  demand(haltPacked.length === 4 && haltPacked.readUInt32BE(0) === state.RCap,
    "witness", "R_cap halt seed");

  const originsById = new Map();
  const originsByKey = new Map();
  const originsByLayer = new Map();
  for (const row of originRows) {
    asArray(row, "witness", "origin row", 3);
    const r = decodeNatural(row[0], "witness", "origin r");
    const j = decodeNatural(row[1], "witness", "origin j");
    const origin = asBytes(row[2], "witness", "origin id");
    demand(r <= state.RCap, "witness", "origin layer range");
    demand(equalBytes(origin, originId(state, r, j)), "witness", "origin derivation");
    const key = `${r}:${j}`;
    demand(!originsByKey.has(key) && !originsById.has(hexKey(origin)), "witness", "duplicate origin");
    const record = { r, j, origin, key, occurrences: [], gonols: [] };
    originsByKey.set(key, record);
    originsById.set(hexKey(origin), record);
    if (!originsByLayer.has(r)) originsByLayer.set(r, []);
    originsByLayer.get(r).push(record);
  }
  for (let r = 0; r <= state.RCap; r += 1) {
    demand(originsByLayer.has(r), "witness", `missing origin layer ${r}`);
  }

  const occurrencesById = new Map();
  for (const row of occurRows) {
    asArray(row, "witness", "occurrence row", 4);
    const axis = asBytes(row[0], "witness", "axis");
    const origin = asBytes(row[1], "witness", "occurrence origin");
    const position = decodeNatural(row[2], "witness", "occurrence position");
    const occurrence = asBytes(row[3], "witness", "occurrence id");
    const originRecord = originsById.get(hexKey(origin));
    demand(originRecord, "witness", "occurrence origin missing");
    const axisValue = parseAxis(axis);
    demand(equalBytes(occurrence, occurrenceId(origin, position, axis)),
      "witness", "occurrence derivation");
    demand(!occurrencesById.has(hexKey(occurrence)), "witness", "duplicate occurrence");
    const record = { row, axis, axisValue, origin, originRecord, position, occurrence };
    occurrencesById.set(hexKey(occurrence), record);
    originRecord.occurrences.push(record);
  }

  const aByG = new Map();
  for (const row of aRows) {
    asArray(row, "witness", "A row", 4);
    const r = decodeNatural(row[0], "witness", "A r");
    const j = decodeNatural(row[1], "witness", "A j");
    const g = asBytes(row[2], "witness", "gonol id");
    const shape = asArray(row[3], "witness", "A shape", 2);
    const nChildren = decodeNatural(shape[0], "witness", "child count");
    const nLeftover = decodeNatural(shape[1], "witness", "leftover count");
    demand(nLeftover === 0 || nLeftover === 1, "witness", "leftover shape");
    demand(!aByG.has(hexKey(g)), "witness", "duplicate gonol id");
    aByG.set(hexKey(g), { row, r, j, g, nChildren, nLeftover });
  }

  const membersByG = new Map();
  const memberByOccurrence = new Map();
  for (const row of memberRows) {
    asArray(row, "witness", "member row", 2);
    const occurrence = asBytes(row[0], "witness", "member occurrence");
    const g = asBytes(row[1], "witness", "member gonol");
    const occurrenceRecord = occurrencesById.get(hexKey(occurrence));
    demand(occurrenceRecord, "witness", "member occurrence missing");
    demand(aByG.has(hexKey(g)), "witness", "member gonol missing");
    demand(!memberByOccurrence.has(hexKey(occurrence)), "witness", "occurrence in two gonols");
    memberByOccurrence.set(hexKey(occurrence), g);
    if (!membersByG.has(hexKey(g))) membersByG.set(hexKey(g), []);
    membersByG.get(hexKey(g)).push(occurrenceRecord);
  }
  demand(memberByOccurrence.size === occurrencesById.size, "witness", "occurrence membership partition");

  for (const row of pairRows) {
    asArray(row, "witness", "pair row", 3);
    const r = decodeNatural(row[0], "witness", "pair r");
    const first = asBytes(row[1], "witness", "pair first");
    const second = asBytes(row[2], "witness", "pair second");
    demand(compareBytes(first, second) < 0, "witness", "pair ordering");
    const firstRecord = occurrencesById.get(hexKey(first));
    const secondRecord = occurrencesById.get(hexKey(second));
    demand(firstRecord && secondRecord, "witness", "pair endpoint missing");
    demand(firstRecord.originRecord === secondRecord.originRecord, "witness", "cross-origin pair");
    demand(r === firstRecord.originRecord.r, "witness", "pair layer");
  }

  const expectedPairRows = [];
  const expectedMembersByG = new Map();
  const expectedOriginForG = new Map();
  for (const originRecord of originsById.values()) {
    const ranked = originRecord.occurrences.map((entry) => ({
      entry,
      rank: kmac256(state.kPair, cborEncode([originRecord.origin, entry.occurrence]), 32, ASCII.pair),
    }));
    ranked.sort((left, right) => compareBytes(left.rank, right.rank)
      || compareBytes(left.entry.occurrence, right.entry.occurrence));
    const pairGonols = [];
    for (let index = 0; index + 1 < ranked.length; index += 2) {
      const members = [ranked[index].entry, ranked[index + 1].entry]
        .sort((left, right) => compareBytes(left.occurrence, right.occurrence));
      expectedPairRows.push([natural(originRecord.r), members[0].occurrence, members[1].occurrence]);
      const g = pairGonolId(originRecord.origin, members[0].occurrence, members[1].occurrence);
      pairGonols.push(g);
      expectedMembersByG.set(hexKey(g), members);
      expectedOriginForG.set(hexKey(g), originRecord);
    }
    pairGonols.sort(compareBytes);
    originRecord.gonols.push(...pairGonols);
    if (ranked.length % 2 === 1) {
      const carry = ranked[ranked.length - 1].entry;
      const g = carryGonolId(originRecord.origin, carry.occurrence);
      originRecord.gonols.push(g);
      expectedMembersByG.set(hexKey(g), [carry]);
      expectedOriginForG.set(hexKey(g), originRecord);
    }
  }
  compareRowSets(pairRows, expectedPairRows, "witness", "pair set");
  demand(aByG.size === expectedMembersByG.size, "witness", "gonol count");
  demand(membersByG.size === expectedMembersByG.size, "witness", "member gonol count");

  for (const [gKey, expectedMembers] of expectedMembersByG) {
    const aRecord = aByG.get(gKey);
    const actualMembers = membersByG.get(gKey);
    const originRecord = expectedOriginForG.get(gKey);
    demand(aRecord && actualMembers, "witness", "expected gonol absent");
    demand(aRecord.r === originRecord.r && aRecord.j === originRecord.j,
      "witness", "gonol region");
    actualMembers.sort((left, right) => compareBytes(left.occurrence, right.occurrence));
    demand(actualMembers.length === expectedMembers.length, "witness", "member count");
    for (let index = 0; index < actualMembers.length; index += 1) {
      demand(equalBytes(actualMembers[index].occurrence, expectedMembers[index].occurrence),
        "witness", "member identity");
    }
    for (const occurrence of expectedMembers) {
      demand(equalBytes(memberByOccurrence.get(hexKey(occurrence.occurrence)), aRecord.g),
        "witness", "membership target");
    }
  }

  const expectedAttachRows = [];
  const expectedDeltaRows = [];
  const phaseByG = new Map();
  const childCount = new Map();
  for (const originRecord of originsById.values()) {
    for (const g of originRecord.gonols) childCount.set(hexKey(g), 0);
    if (originRecord.gonols.length > 0) phaseByG.set(hexKey(originRecord.gonols[0]), 0);
    for (let index = 1; index < originRecord.gonols.length; index += 1) {
      const parentIndex = Math.floor((index - 1) / 2);
      const parent = originRecord.gonols[parentIndex];
      const child = originRecord.gonols[index];
      const delta = 1 + ((index - 1) % (PROFILE.M - 1));
      expectedAttachRows.push([parent, child, natural(originRecord.r)]);
      expectedDeltaRows.push([parent, child, natural(delta)]);
      childCount.set(hexKey(parent), childCount.get(hexKey(parent)) + 1);
      phaseByG.set(hexKey(child), (phaseByG.get(hexKey(parent)) + delta) % PROFILE.M);
    }
  }
  for (const row of attachRows) {
    asArray(row, "witness", "attach row", 3);
    asBytes(row[0], "witness", "attach parent");
    asBytes(row[1], "witness", "attach child");
    decodeNatural(row[2], "witness", "attach r");
  }
  for (const row of deltaRows) {
    asArray(row, "witness", "delta row", 3);
    asBytes(row[0], "witness", "delta parent");
    asBytes(row[1], "witness", "delta child");
    const delta = decodeNatural(row[2], "witness", "delta");
    demand(delta >= 0 && delta < PROFILE.M, "witness", "delta range");
  }
  compareRowSets(attachRows, expectedAttachRows, "witness", "attachment set");
  compareRowSets(deltaRows, expectedDeltaRows, "witness", "delta set");

  for (const [gKey, aRecord] of aByG) {
    const expectedMembers = expectedMembersByG.get(gKey);
    demand(aRecord.nChildren === childCount.get(gKey), "witness", "child shape");
    demand(aRecord.nLeftover === (expectedMembers.length === 1 ? 1 : 0),
      "witness", "leftover shape");
  }

  return {
    beta,
    wire,
    aByG,
    originsById,
    originsByKey,
    occurrencesById,
    expectedMembersByG,
    phaseByG,
  };
}

function parseLayer(wire, model, expectedR, body = false) {
  demand(wire.length <= PROFILE.maxLayerWireBytes, "layer", "layer wire cap");
  demand(wire.length >= ASCII.layer.length && equalBytes(wire.subarray(0, 8), ASCII.layer),
    "layer", "layer magic");
  const value = cborDecodeCanonical(wire.subarray(8), "layer");
  demand(equalBytes(concat(ASCII.layer, cborEncode(value)), wire), "layer", "layer re-encoding");
  asArray(value, "layer", "layer", 3);
  const r = decodeNatural(value[0], "layer", "layer r");
  const length = decodeNatural(value[1], "layer", "layer data length");
  const regionRows = asArray(value[2], "layer", "regions");
  demand(r === expectedR, "layer", body ? "terminal layer index" : "layer index");
  demand(length <= PROFILE.maxIntermediateBytes, "layer", "intermediate cap");
  const expectedRegionCount = length === 0 ? 1 : Math.ceil(length / PROFILE.xBytes);
  demand(regionRows.length === expectedRegionCount, "layer", "region count");

  const regions = [];
  for (let index = 0; index < regionRows.length; index += 1) {
    const row = asArray(regionRows[index], "layer", "region", 4);
    const j = decodeNatural(row[0], "layer", "region j");
    const regionLength = decodeNatural(row[1], "layer", "region byte length");
    const origin = asBytes(row[2], "layer", "region origin");
    const gonolRows = asArray(row[3], "layer", "region gonols");
    demand(j === index, "layer", "region ordering");
    if (length === 0) demand(regionLength === 0, "layer", "empty region length");
    else if (index + 1 < regionRows.length) demand(regionLength === PROFILE.xBytes, "layer", "nonfinal region length");
    else demand(regionLength >= 1 && regionLength <= PROFILE.xBytes, "layer", "final region length");
    const originRecord = model.originsByKey.get(`${r}:${j}`);
    demand(originRecord && equalBytes(originRecord.origin, origin), "layer", "region origin");
    demand(gonolRows.length === originRecord.gonols.length, "layer", "gonol count");
    for (let gIndex = 0; gIndex < gonolRows.length; gIndex += 1) {
      const gonolRow = asArray(gonolRows[gIndex], "layer", "gonol", 3);
      const g = asBytes(gonolRow[0], "layer", "gonol id");
      const phase = decodeNatural(gonolRow[1], "layer", "gonol phase");
      const memberPhases = asArray(gonolRow[2], "layer", "member phases");
      const expectedG = originRecord.gonols[gIndex];
      demand(equalBytes(g, expectedG), "layer", "gonol ordering");
      demand(phase === model.phaseByG.get(hexKey(g)), "layer", "gonol phase");
      const expectedMembers = model.expectedMembersByG.get(hexKey(g));
      demand(memberPhases.length === expectedMembers.length, "layer", "phase member count");
      for (let memberIndex = 0; memberIndex < memberPhases.length; memberIndex += 1) {
        const memberRow = asArray(memberPhases[memberIndex], "layer", "phase member", 2);
        const occurrence = asBytes(memberRow[0], "layer", "phase occurrence");
        const theta = decodeNatural(memberRow[1], "layer", "member phase");
        demand(equalBytes(occurrence, expectedMembers[memberIndex].occurrence),
          "layer", "phase member ordering");
        const displacement = expectedMembers.length === 2 && memberIndex === 1
          ? Math.floor(PROFILE.M / 2) : 0;
        demand(theta === (phase + displacement) % PROFILE.M, "layer", "member phase");
      }
    }
    regions.push({ j, length: regionLength, origin, originRecord });
  }
  return { r, length, regions, wire: Buffer.from(wire), value };
}

function expandLayer(layer, model) {
  const chunks = [];
  for (const region of layer.regions) {
    const bitLength = region.length * 8;
    const bits = new Array(bitLength).fill(null);
    for (const occurrence of region.originRecord.occurrences) {
      const { q, bits: payload } = occurrence.axisValue;
      demand(occurrence.position + q <= bitLength, "expand", "occurrence bounds");
      for (let index = 0; index < q; index += 1) {
        const target = occurrence.position + index;
        demand(bits[target] === null, "expand", "occurrence overlap");
        bits[target] = payload[index];
      }
    }
    demand(bits.every((bit) => bit !== null), "expand", "incomplete occurrence coverage");
    const bytes = packBits(bits);
    demand(bytes.length === region.length, "expand", "region byte length");
    const detected = detect(bytes, region.origin);
    const actual = region.originRecord.occurrences.map((entry) => entry.row);
    compareRowSets(actual, detected, "expand", "Detect replay");
    chunks.push(bytes);
  }
  const output = Buffer.concat(chunks);
  demand(output.length === layer.length, "expand", "layer data length");
  return output;
}

function frameHeader(c0Length) {
  const header = Buffer.alloc(24);
  ASCII.frame.copy(header, 0);
  header.writeUInt16BE(1, 8);
  header.writeUInt16BE(24, 10);
  header.writeBigUInt64BE(BigInt(c0Length), 12);
  header.writeUInt16BE(32, 20);
  header.writeUInt16BE(0, 22);
  return header;
}

function unframe(ciphertext) {
  demand(ciphertext.length >= 56, "frame", "minimum length");
  demand(equalBytes(ciphertext.subarray(0, 8), ASCII.frame), "frame", "magic");
  demand(ciphertext.readUInt16BE(8) === 1, "frame", "version");
  demand(ciphertext.readUInt16BE(10) === 24, "frame", "header length");
  const lengthBig = ciphertext.readBigUInt64BE(12);
  demand(lengthBig <= BigInt(PROFILE.maxC0Bytes), "frame", "C0 cap");
  const length = Number(lengthBig);
  demand(ciphertext.readUInt16BE(20) === 32 && ciphertext.readUInt16BE(22) === 0,
    "frame", "tag length or flags");
  demand(ciphertext.length === 24 + length + 32, "frame", "exact frame length");
  const header = ciphertext.subarray(0, 24);
  demand(equalBytes(header, frameHeader(length)), "frame", "canonical header");
  return {
    header: Buffer.from(header),
    c0: Buffer.from(ciphertext.subarray(24, 24 + length)),
    tag: Buffer.from(ciphertext.subarray(24 + length)),
  };
}

function verifyTag(framed, state, associatedData) {
  const transcript = cborEncode([framed.header, framed.c0, associatedData]);
  const expected = kmac256(state.kIntegrity, transcript, 32, ASCII.tag);
  demand(crypto.timingSafeEqual(expected, framed.tag), "tag", "verification failed");
}

function parseBootstrap(c0, state) {
  demand(c0.length >= 24, "bootstrap", "minimum length");
  demand(equalBytes(c0.subarray(0, 8), ASCII.bootstrap), "bootstrap", "magic");
  demand(c0.readUInt16BE(8) === 1, "bootstrap", "version");
  demand(c0.readUInt16BE(10) === 24, "bootstrap", "header length");
  const betaLengthBig = c0.readBigUInt64BE(12);
  demand(betaLengthBig <= BigInt(PROFILE.maxBetaBytes), "bootstrap", "beta cap");
  const betaLength = Number(betaLengthBig);
  demand(c0.readUInt32BE(20) === 0, "bootstrap", "flags");
  demand(betaLength <= c0.length - 24, "bootstrap", "witness boundary");
  const beta = Buffer.from(c0.subarray(24, 24 + betaLength));
  const body = Buffer.from(c0.subarray(24 + betaLength));
  const model = analyzeWitness(beta, state);
  return { beta, body, model };
}

function avoid(candidate, forbidden) {
  const base = bytesToBigInt(candidate);
  const blocked = new Set(forbidden.map((value) => hexKey(value)));
  for (let offset = 0; offset <= forbidden.length; offset += 1) {
    const value = fixed32((base + BigInt(offset)) % MOD256);
    if (!blocked.has(hexKey(value))) return value;
  }
  throw new URPCSError("advance", "Avoid exhausted");
}

function advance(state, ciphertext, receipt) {
  const context = cborEncode([state.nuOrigin, natural(state.RCap), ciphertext, receipt]);
  const kPair = kmac256(state.kAdvance, context, 32, ASCII.advancePair);
  const zIntegrity = kmac256(state.kAdvance, context, 32, ASCII.advanceIntegrity);
  const kIntegrity = avoid(zIntegrity, [kPair]);
  const zRoot = kmac256(state.kAdvance, context, 32, ASCII.advanceRoot);
  const kAdvance = avoid(zRoot, [kPair, kIntegrity]);
  return {
    kPair,
    kIntegrity,
    kAdvance,
    nuOrigin: fixed32(bytesToBigInt(state.nuOrigin) + 1n),
    RCap: state.RCap,
  };
}

function decode(ciphertextInput, stateInput, associatedDataInput) {
  const ciphertext = Buffer.from(ciphertextInput);
  const associatedData = Buffer.from(associatedDataInput);
  const state = validateState(stateInput);
  const framed = unframe(ciphertext);
  verifyTag(framed, state, associatedData);
  const bootstrap = parseBootstrap(framed.c0, state);
  const layers = new Array(state.RCap + 1);
  let layer = parseLayer(bootstrap.body, bootstrap.model, state.RCap, true);
  const recoveredRegionKeys = new Set();
  let plaintext = null;
  for (let r = state.RCap; r >= 0; r -= 1) {
    layers[r] = layer;
    for (const region of layer.regions) recoveredRegionKeys.add(`${r}:${region.j}`);
    const expanded = expandLayer(layer, bootstrap.model);
    if (r > 0) layer = parseLayer(expanded, bootstrap.model, r - 1, false);
    else plaintext = expanded;
  }
  demand(plaintext.length <= PROFILE.maxInputBytes, "profile", "plaintext cap");
  demand(recoveredRegionKeys.size === bootstrap.model.originsByKey.size,
    "expand", "recovered region set size");
  for (const key of bootstrap.model.originsByKey.keys()) {
    demand(recoveredRegionKeys.has(key), "expand", `missing recovered region ${key}`);
  }

  const traceWire = cborEncode([
    bootstrap.beta,
    layers.map((entry) => entry.wire),
  ]);
  demand(traceWire.length <= PROFILE.maxTraceWireBytes, "receipt", "trace cap");
  const receipt = sha3_256(cborEncode([ASCII.receipt, traceWire]));
  const nextState = advance(state, ciphertext, receipt);
  return { plaintext, receipt, nextState };
}

function stateFromJson(value) {
  return {
    kPair: Buffer.from(value.k_pair, "hex"),
    kIntegrity: Buffer.from(value.k_integrity, "hex"),
    kAdvance: Buffer.from(value.k_advance, "hex"),
    nuOrigin: Buffer.from(value.nu_origin, "hex"),
    RCap: value.R_cap,
  };
}

function stateToJson(value) {
  return {
    R_cap: value.RCap,
    k_advance: value.kAdvance.toString("hex"),
    k_integrity: value.kIntegrity.toString("hex"),
    k_pair: value.kPair.toString("hex"),
    nu_origin: value.nuOrigin.toString("hex"),
  };
}

function vectorInput(value) {
  return {
    ciphertext: Buffer.from(value.ciphertext_hex, "hex"),
    state: stateFromJson(value.initial_state),
    associatedData: Buffer.from(value.ad_hex, "hex"),
  };
}

function runKat() {
  const output = kmac256(
    Buffer.from("404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f", "hex"),
    Buffer.from("00010203", "hex"),
    64,
    Buffer.from("My Tagged Application", "ascii"),
  );
  return output.toString("hex");
}

function main(arguments_) {
  if (arguments_[0] === "--kat" && arguments_.length === 1) {
    process.stdout.write(`${runKat()}\n`);
    return;
  }
  if (arguments_[0] === "--vector" && (arguments_.length === 2 || arguments_.length === 3)) {
    const id = arguments_[1];
    const path = arguments_[2] || "research/urpcs/vectors/urpcs-v1-vectors.json";
    const document = JSON.parse(fs.readFileSync(path, "utf8"));
    const vector = document.vectors.find((entry) => entry.id === id);
    demand(vector && vector.expected === "success", "cli", `positive vector not found: ${id}`);
    const input = vectorInput(vector);
    const result = decode(input.ciphertext, input.state, input.associatedData);
    process.stdout.write(`${JSON.stringify({
      plaintext_hex: result.plaintext.toString("hex"),
      receipt_hex: result.receipt.toString("hex"),
      next_state: stateToJson(result.nextState),
    }, null, 2)}\n`);
    return;
  }
  throw new URPCSError("cli", "use --kat or --vector ID [vectors.json]");
}

module.exports = {
  URPCSError,
  cborEncode,
  decode,
  kmac256,
  runKat,
  stateFromJson,
  stateToJson,
  vectorInput,
};

if (require.main === module) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    process.stderr.write(`${error.stack || error}\n`);
    process.exitCode = 1;
  }
}
