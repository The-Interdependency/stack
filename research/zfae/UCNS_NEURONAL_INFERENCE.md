# UCNS neuronal inference candidate

Status: **stack-local research candidate**.

This document records the current construction reached from the UCHC/UCNS inference thread. It does not transfer authority to Stack, does not establish a biological equivalence claim, and does not by itself retire PTCNA.

## Core construction

A single inference node is modeled as an operation over a tensor of UCNS gonols:

\[
\mathcal N:\bigotimes_{i=1}^{k} G_i \rightarrow G_o
\]

where every \(G_i\) and the result \(G_o\) are UCNS gonols.

The tensor preserves simultaneous gonol distinctions rather than flattening them into one scalar coordinate or ordinary weighted-sum input. The inference result remains a gonol, so it can participate recursively in later inference.

The candidate primitive is therefore:

\[
\boxed{\text{UCNS neuronal inference node}}
\]

with gonols as native operands and result.

## UCHC placement

UCHC constructs these nodes from language construction.

Current intended sequence:

\[
\text{glyph gonols}
\rightarrow
\text{closed word gonol}
\rightarrow
\text{word axis / inference node}
\]

and recursively:

\[
G_{\text{word}_1}\otimes G_{\text{word}_2}\otimes\cdots
\xrightarrow{\mathcal N}
G_{\text{construct}}
\]

The higher-scale result remains a gonol and may become an operand in another inference node.

This preserves the existing UCHC requirement that a closed word becomes its own higher-scale axis rather than remaining permanently reducible to its constituent glyph coordinates.

## Thread conclusions

1. One neuron is a sufficient minimum computational unit for an inference primitive; a network is not required merely to define inference.
2. The UCNS candidate is not "a neuron as an arbitrary tensor". It is **inference over tensors of gonols**.
3. Gonols are the native operands.
4. The inferred result is also a gonol.
5. UCHC creates the language-derived UCNS neuronal inference nodes.
6. Closed words become higher-scale axes/nodes after glyph composition.
7. Higher language inference recursively composes those nodes.
8. Inference therefore stays inside UCNS-native construction rather than flattening semantic construction into Cartesian coordinates or scalar weights first.

Compactly:

\[
\boxed{
\text{UCHC construction}
\rightarrow
\text{tensor of gonols}
\rightarrow
\text{UCNS neuronal inference}
\rightarrow
\text{gonol}
}
\]

## PTCNA capability-difference test

PTCNA is no longer assumed necessary merely because the system requires neural inference.

The surviving question is:

> Does PTCNA provide any necessary operation that cannot be represented as construction, composition, state transition, learning, recurrence, transport, interference, or collective-state formation among UCNS neuronal inference nodes?

Possible outcomes:

- **SURVIVED** — at least one necessary PTCNA operation remains irreducible to UCNS neuronal inference composition.
- **FALSIFIED AS REQUIRED LAYER** — every required PTCNA operation is representable without an independent PTCNA layer.
- **UNRESOLVED** — the required UCNS neuronal inference law or the relevant PTCNA operation is not yet specified strongly enough to compare.
- **BLOCKED** — producer identities or executable witnesses needed for the comparison are unavailable.

PTCNA's own repository retains authority over PTCNA. This Stack candidate only tests whether PTCNA remains architecturally necessary to the composed inference path.

## Acceptance obligations

This candidate is not complete until something can fail.

A future implementation must at minimum demonstrate:

1. **gonol preservation** — node input and output identities remain valid UCNS gonols;
2. **tensor distinction preservation** — changing operand identity, ordering, multiplicity, or declared relation can be observed independently where the construction says it matters;
3. **non-flattening** — no hidden projection into an ordinary scalar/vector representation is allowed to stand in for the claimed gonol tensor relation without an explicit reversible boundary;
4. **recursive closure** — a node output can be admitted as an operand to another node without changing its identity merely to fit the next layer;
5. **UCHC construction witness** — an actual UCHC glyph/word/construct path creates the corresponding node operands from source-bound gonols;
6. **inference witness** — the node produces a state/result not obtainable merely by replaying an identity-preserving serializer;
7. **intervention test** — a preregistered change to one participating gonol relation changes or preserves the result according to the declared inference law;
8. **PTCNA difference test** — enumerate each still-claimed PTCNA necessity and test whether UCNS neuronal inference composition represents it without semantic substitution.

Passing structure checks alone does not establish useful inference, learning, biological fidelity, consciousness, semantic truth, or task performance.

## Authority boundary

- **UCNS** owns gonol geometry and any canonical neuronal-inference primitive admitted into UCNS.
- **UCHC** owns its language construction and, if adopted, the construction of language-derived UCNS neuronal inference nodes.
- **Stack** owns this cross-project research candidate and its comparison evidence.
- **PTCNA** owns PTCNA; this candidate may falsify its necessity in the composed architecture without rewriting PTCNA's own historical or project-local claims.
- **EDCM** may measure resulting behavior but does not define the construction.
- **ZFAE** may consume the inference construction, but its conceptual inference-event boundary does not establish the UCNS neuronal law.

## Nonclaims

This document does not yet provide:

- the UCNS tensor-product law for gonols;
- the neuronal inference operator;
- a learning/update law;
- a recurrence or propagation law;
- a canonical scalar field;
- a biological-neuron equivalence proof;
- a semantic correctness claim;
- a PTCNA deprecation decision.

## hmmm

The missing executable object is the exact UCNS law for:

\[
\bigotimes_i G_i \xrightarrow{\mathcal N} G_o
\]

Until that law exists with failure-bearing witnesses, **UCNS neuronal inference** is a well-placed construction candidate, not a demonstrated inference mechanism.

PTCNA remains a hypothesis about additional necessary architecture pending the capability-difference test.
