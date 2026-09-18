# First principles and a UCNS composition option set: candidate v0

Recorded: 2026-09-18 UTC. Standing: **PROPOSED / UNRESOLVED**.

Goal: identify first principles sufficient for an irreducibly complete model of
reality from subatomic through cosmic scales, offered as an option set for UCNS
composition. The [Tensored Human](tensored-human-scaffold.md) is application
scaffolding within that objective.

The formulas below are an assistant-proposed research formalization. Exact results
inside a specified mathematical example do not establish universal or empirical
adequacy. No METAPAT root definition, UCNS operation, or physical law is amended.
Exact document identities are in [the provenance record](composition-option-set-provenance.md).

## 1. A bounded boundary derivation

For this example only, let $X$ be a finite set of **things**, and let
$R\subseteq X\times X$ be a binary **relation**. This is a directed simple-graph
model: it does not yet preserve multiple relation instances, relation types,
arbitrary arity, continuous interfaces, or joint state.

For a selected collection $A\subseteq X$, define the crossing-relation boundary:

$$
\partial_R A=\{(x,y)\in R:(x\in A)\ne(y\in A)\}.
$$

Take $X=\{a,b,c\}$ and $R=\{(a,b),(b,c)\}$. Then:

$$
\partial_R\{a\}=\{(a,b)\},\qquad
\partial_R\{a,b\}=\{(b,c)\}.
$$

All nontrivial **oriented partitions with their crossing relations** form:

$$
\mathcal B_{\mathrm{all}}(X,R)=
\{(A,X\setminus A,\partial_R A):\varnothing\ne A\subsetneq X\}.
$$

The example has six oriented partition records and three distinct crossing sets.
Complementary collections have the same crossing set:

$$\partial_R A=\partial_R(X\setminus A).$$

Consequently the crossing set alone does not retain the side labels. A disconnected
model can also have nontrivial partitions with an empty crossing set. Preserve
membership explicitly rather than reconstructing it from crossing relations.

**Derived result within this model:** $X$ and $R$ determine all these possible cuts.
Selecting one requires a grouping or selection rule. A physical-domain admission
predicate would restrict the mathematical options:

$$
\mathcal B_{\mathrm{allowed}}=
\{b\in\mathcal B_{\mathrm{all}}:\operatorname{AdmissibleBoundary}(b)\}.
$$

That predicate has not been supplied. This construction neither proves that every
physical boundary is a graph cut nor eliminates METAPAT's boundary primitive.
The local term is `composition-options.relational-cut-boundary`; its scope is the
model above. Its relation to METAPAT's broader boundary sense is **provisional**.

For relations of higher arity, a candidate extension can keep each relation
instance $r$ and its ordered, possibly repeated incidence tuple. If
$\operatorname{supp}(r)$ denotes its participating things, select crossing
instances by:

$$
\partial_{\mathcal R}A=
\{r\in\mathcal R:
\operatorname{supp}(r)\cap A\ne\varnothing\ \land
\operatorname{supp}(r)\cap(X\setminus A)\ne\varnothing\}.
$$

The support set is used only for this predicate. The original instance identity,
ordered tuple, multiplicity, type, and state must remain available. Sufficiency of
this extension is unresolved.

## 2. Recursive composition as a proposed partial algebra

Let $\mathcal P$ contain starting objects, and $\mathcal C_k$ contain partial
constructors taking $k$ objects. A partial constructor has an explicit domain of
admissible inputs. Starting objects are candidates for a basis, not assumed
physically fundamental particles.

$$\mathcal O_0=\mathcal P,$$

$$
\mathcal O_{n+1}=\mathcal O_n\cup
\left\{c(x_1,\ldots,x_k):
\begin{array}{l}
k\ge1,\ c\in\mathcal C_k,\ x_i\in\mathcal O_n,\\
(x_1,\ldots,x_k)\in\operatorname{dom}(c)
\end{array}\right\},
$$

$$\mathcal O_\infty=\bigcup_{n\ge0}\mathcal O_n.$$

This is closure under finite admissible construction. It does not imply a finite
number of options, decidable admission, finite generation cost, or coverage of
continuous limits, infinite composites, and feedback dynamics. Each such capability
needs its own representation and rule. Nullary constructors, if needed, supply
additional starting objects.

Each admitted composite must declare its constituent identities, relations,
boundary representation, admissible joint-state space, and current state. A
composite may participate as one thing while retaining its internal construction.
The meaning of "same composite" and any permitted information loss must be explicit.

Neither $\mathcal P$ nor the constructors and their domains have been selected.
These equations specify a research contract; they do not supply physical dynamics.

## 3. A quantum joint-state witness

For the standard two-qubit model, define:

$$
|\Phi_+\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2},\qquad
|\Phi_-\rangle=\frac{|00\rangle-|11\rangle}{\sqrt2}.
$$

These are orthogonal joint states, while their individual reduced states agree:

$$
\rho_A^+=\rho_A^-=I_2/2,\qquad
\rho_B^+=\rho_B^-=I_2/2.
$$

Their distinguishing joint information is observable in the standard model. With
$\sigma_x$ the operator that exchanges $|0\rangle$ and $|1\rangle$:

$$
\langle\Phi_\pm|\sigma_x\otimes\sigma_x|\Phi_\pm\rangle=\pm1.
$$

Thus reconstructing a composite solely from these individual reduced states loses
a distinction required by the model. This witnesses a failure of **local-state-only
reconstruction**, not a failure of all relational representations. A candidate
composition covering this case must retain the distinguishing joint information.
It supplies no evidence about consciousness, human coupling, or a UCNS substrate.
See [IBM's multiple-system quantum treatment](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/multiple-systems/quantum-information).

## 4. Proposed UCNS preservation obligations

Let $E$ encode a declared domain object geometrically, and let $\widehat c$ be the
corresponding UCNS operation. Require:

$$\operatorname{Decode}(E(x))\cong x,$$

$$
E(c(x_1,\ldots,x_k))\cong
\widehat c(E(x_1),\ldots,E(x_k)).
$$

The equivalence $\cong$ must be defined before testing. Its witnesses must preserve
every distinction selected as necessary, including identity, order, multiplicity,
joint state, and provenance when those are load-bearing. Source and target
equivalences have different typed domains and must each be stated explicitly.

These requirements apply to admitted source tuples. Tests must also ensure that
an operation rejected by the source admission rule cannot silently become an
accepted domain composition through the adapter. UCNS may independently represent
geometry that has no meaning in that source domain.

No $E$, decoder, general $\widehat c$, or preservation proof is supplied here.
UCNS owns its geometry and operation status; this note defines proposed consumer
obligations and introduces no competing UCNS algebra.

## 5. Completeness, irredundancy, and empirical adequacy

Let $\mathcal D$ be a declared target class. Let $P$ contain candidate primitive
objects and operations, and let $\langle P\rangle$ denote systems faithfully
representable under a fixed interpretation, host logic, admissibility rules, and
equivalence. Membership below means representability under that fixed contract.

Scoped completeness requires:

$$\mathcal D\subseteq\langle P\rangle.$$

Deletion-irredundancy within this formulation requires:

$$
\forall p\in P,\ \exists d\in\mathcal D:
d\notin\langle P\setminus\{p\}\rangle.
$$

Removal must also remove hidden uses of $p$ in macros and constructor definitions;
otherwise the witness is invalid. A faithful derivation from the remaining basis
would defeat the claim that $p$ is necessary. Deletion-irredundancy does not prove
global minimality against every alternative primitive vocabulary or encoding.

Empirical adequacy is a separate obligation: domain dynamics and observation maps
must yield predictions tested against specified observations and alternatives.
Round-trip fidelity, syntactic closure, and a proof about a finite graph do not
establish that obligation. No such empirical result is added here.

The target class "all reality" has not been operationally specified. Bounded target
classes allow useful falsification while the universal objective remains open.

## Claim ledger

| Claim | Standing and scope |
|---|---|
| Human needs and domain hierarchy | Author-declared application scaffold; separate file |
| Subatomic-to-cosmic completion | Author-declared research objective; achievement UNRESOLVED |
| Six oriented cuts / three crossing sets | Exact result for the supplied three-thing graph |
| Boundary universally derived from thing and relate | UNRESOLVED; graph-cut result does not establish it |
| Joint state determined by individual reduced states | FALSIFIED by the specified two-qubit example |
| Partial-constructor closure | Proposed representation contract; basis and laws unselected |
| General faithful UCNS composition | UNRESOLVED; equations are obligations, not implementation |
| Irreducibly complete model of reality | UNRESOLVED; neither completeness nor minimality established |

## Usage guidance and next falsifier

1. Read the author-declared scaffold and the provenance boundaries separately.
2. Freeze a target class, candidate basis, allowed definitions, observable
   distinctions, and equivalence before attempting a deletion test.
3. For the first boundary fixture, reproduce both cuts above, then compare $A$ and
   its complement. A representation retaining only the crossing set fails to
   reconstruct side membership unless that distinction is explicitly quotiented.
4. Test an isolated component and a higher-arity relation before extending the cut
   construction. Record a missing necessary distinction as a counterexample.
5. Before claiming physical coverage, supply and test domain-specific admission,
   state, dynamics, and observation maps. Keep a subatomic, a human, and a cosmic
   case distinct; shared notation does not transfer evidence between them.
6. Before claiming UCNS support, instantiate and test both preservation equations
   against an exact upstream operation. A hypothetical operation stays `hmmm`.

Use this document as a research specification. It is programming-language agnostic
and retains explicit English meanings. It is not an implemented physics engine.

## hmmm

- The first-principle basis and independence witnesses have not been selected.
- Physical boundary admission, dynamics, observation, and scale-transition laws.
- Whether relational-cut boundaries recover the distinctions needed in each domain.
- Higher-arity, continuous, cyclic, and infinite-system representation obligations.
- Faithful UCNS encoding and operations, including rejected-input behavior.
- The human tensor's state spaces and composition semantics.
- Universal completeness and minimality against alternative primitive bases.
- Whether such a representation improves AI reasoning is a separate experimental
  question. The author's speculative reflection about a more capable "djinn" is
  not used as a mathematical premise or evidence of a capability.
