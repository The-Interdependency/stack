# Weave

Standing: **stack-local research; specification-first; no security claim**.

Weave is the replacement research workspace for Erin Spencer's intended encryption
system after retirement of the substituted URPCS implementation.

The system is **not** merely an interleaving permutation. The preserved architecture
contains multiple cooperating layers. Development may stage those layers for testing,
but no layer may be silently discarded or replaced by a familiar construction.

## Preserved architecture

### 1. Hyperspace / gonol plaintext construction

Plaintext is intended to be processed into a hyperspace gonol construction rather than
treated only as an opaque byte string. The information is represented as a nested gonol
set before or as part of encryption.

Recovery is intended to require a **private gonol** associated with the private key.
The exact reversible binding and key representation remain unresolved and must be
specified rather than invented.

### 2. Multiple threads

The encrypted construction uses multiple threads/data streams, with arity at least
three and contemplated thread counts including three, five, seven, or more.

Each thread must contribute to reconstruction. A single independently useful stream is
not the intended construction.

### 3. Thread-associated corpus/material

Threads may be associated with user-selected corpus/material such as literary works,
music, technical manuals, sounds, or other chosen source material.

The corpus/material is intended to participate in reconstruction as semi-secret
context, not merely as documentation or a label. Its exact derivation and binding rule
remain to be frozen.

### 4. Multi-arity bit interleaving

The bit transform is one load-bearing layer inside Weave.

For an ordered sequence of division arities, with at least three levels:

1. divide the working bit sequence into the declared number of sections;
2. within each section interleave inward from opposite ends:
   last bit, first bit, next-to-last bit, next-from-first bit, and so on;
3. repeat for the declared arity sequence, examples already given including fifths,
   sevenths, and thirds;
4. after the declared levels, interleave the resulting whole sequence in the same
   opposite-end manner.

Knowing the division choices, their order, and the number of levels is part of the
reconstruction problem unless an explicit later law changes that role.

### 5. Keying / recovery structure

The intended system ultimately requires asymmetric recovery structure with no silent
dependency on an external cryptographic system. The private side is intended to include
the private gonol and the structural information needed to reverse the construction.

The exact public/private derivation law is not yet specified. That absence is `hmmm`,
not permission to substitute RSA, ECC, Diffie-Hellman, a conventional KEM, or URPCS.

## Non-inheritance boundary

`research/urpcs/` is historical evidence of a substituted GPT-produced construction.
No URPCS law, codec, test, result, or security conclusion is an implementation
dependency of Weave.

URPCS may be consulted only as a specification-divergence witness: an example of what
must not happen again.

## Development discipline

The full architecture is preserved from the start, while implementation proceeds in
separable layers so each contribution can be falsified.

1. Freeze the complete dataflow and the inverse dependencies among gonol construction,
   threads, corpus/material, interleaving, and key structure.
2. Specify exact bit-level interleaving and inverse rules without changing the mechanism.
3. Specify thread formation and recombination.
4. Specify corpus/material derivation and binding.
5. Specify hyperspace/private-gonol construction and recovery.
6. Specify the asymmetric public/private relation.
7. Implement the smallest complete round-trip profile containing every required layer.
8. Build an independently structured decoder/recovery implementation from the written
   contract.
9. Perform adversarial analysis before making any confidentiality or production claim.

A reduced test harness may isolate one layer, but results from a reduced harness may not
be presented as results for Weave as a whole.

## Usage guidance

Start here:

```bash
cat research/weave/SPECIFICATION.md
cat research/weave/BASE.json
```

Do not use Weave to protect real secrets until an explicit security contract and
adversarial evidence justify that use.

## hmmm

Uneven section partitioning; exact ordering/composition of arity stages; thread
formation; corpus/material derivation; hyperspace/gonol encoding; private-gonol binding;
public/private key derivation; authentication, nonce/state, replay behavior; and the
threat model remain unresolved. They are preserved as required design boundaries, not
optional features and not invitations for model substitution.
