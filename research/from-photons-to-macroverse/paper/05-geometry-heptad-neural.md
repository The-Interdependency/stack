
# 17. Möbius transport as a candidate memory geometry

## 17.1 Möbius quotient

**K:** A Möbius band is

\[
M
=
\frac{[0,1]\times[-w,w]}
{(0,u)\sim(1,-u)}.
\]

A centerline point returns after one longitudinal circuit, while a retained transverse frame reverses:

\[
(t,u)
\xrightarrow{1\ \mathrm{turn}}
(t,-u)
\xrightarrow{2\ \mathrm{turns}}
(t,u).
\]

For a twisted section,

\[
\psi(t+1)=-\psi(t),
\qquad
\psi(t+2)=\psi(t).
\]

The holonomy sign satisfies

\[
H_\gamma=-1,
\qquad
H_\gamma^2=+1.
\]

This is the precise content of framed 360-degree reversal and 720-degree restoration.

## 17.2 Candidate significance

**H:** Möbius transport is a candidate geometry for a state that returns to the same location while retaining traversal history in orientation or phase. It is relevant only if it supplies an invariant, prediction, or compression advantage unavailable from an untwisted loop.

**Repository-status note (September 6, 2026):** UCNS commit `ef98748309913588fb13f389f809d5ef6cb5fec3` contains an executable candidate exact visible-circle continuum-wave to finite-gonal boundary trace [32]. The equations and trace identities are exact within that declared candidate model. The representation is not ratified as selected UCNS geometry, does not yet lift the visible 360-degree trace into the complete native Möbius state, and selects no physical or consciousness interpretation. This paper may therefore treat it only as a candidate geometric input; no authority, empirical standing, or meaning transfers from UCNS.

## 17.3 Circle count as an outer arity signature

For this program, an \(n\)-circle Möbius construction represents an \(n\)-member direct scale set:

\[
\mathfrak M_n^{[r]}
\longleftrightarrow
\mathfrak C_n^{[r]}(\mathbb S_n).
\]

The circle count says which scale layers participate directly in the current pattern-recursion stabilization. It does not count every lower closure nested within those carriers. Circle count and recursion depth must therefore be reported together.

# 18. Prime-indexed relational primitives

The dyad is the exceptional base coupling. In standard number theory, \(2\) is prime. This geometry treats it separately because its sole nonzero modular step is self-inverse, whereas the odd-prime constructions below organize nonzero steps into distinct inverse pairs. Nothing in this paper changes the mathematical primality of two.

## 18.1 Exact modular structure

Label \(n\) positions by \(\mathbb Z_n\). A step \(k\) acts as

\[
j\mapsto j+k\pmod n.
\]

The cycle length is

\[
L(n,k)=\frac{n}{\gcd(n,k)}.
\]

Therefore, for \(n>1\),

\[
n\ \text{is prime}
\quad\Longleftrightarrow\quad
L(n,k)=n
\ \text{for every}\ 1\le k<n.
\]

For an odd prime \(p\), inverse steps pair as

\[
k\leftrightarrow p-k,
\]

so there are

\[
\frac{p-1}{2}
\]

unoriented generator classes.

## 18.2 Complete relation graph

Every unordered pair of positions occurs in exactly one inverse-paired step class, hence

\[
\bigcup_{k=1}^{(p-1)/2}C_{p,k}=K_p,
\]

with

\[
|E(K_p)|=\binom p2=\frac{p(p-1)}2.
\]

The minimum orientable genus is [20]

\[
g(K_p)
=
\min\left\{
m\in\mathbb Z_{\ge0}
\mid
12m\ge(p-3)(p-4)
\right\}.
\]

Thus

\[
g(K_3)=0,\quad g(K_5)=1,\quad g(K_7)=1,
\quad g(K_{11})=5,\quad g(K_{13})=8.
\]

Seven is the largest prime whose complete interaction graph embeds on one torus. Eleven enters a higher-genus regime.

## 18.3 Irreducible-complexity hypothesis

**H:** Each odd prime \(p\) may support a candidate relational primitive \(\mathcal P_p\) whose complete invariant package cannot be reconstructed from lower-arity primitives.

A candidate must provide:

1. \(p\) valid carriers;
2. all declared generator classes;
3. orientation-resolved lifts;
4. typed contacts, crossings, and abstract relations;
5. compatible phase and chirality;
6. framed return;
7. a global holonomy or obstruction invariant;
8. an irreducibility test;
9. projection independence.

The geometry is not a consciousness criterion. It is a possible implementation of causal relation structures whose irreducibility can be tested.

## 18.4 Falsifier

**F:** If prime and composite arities show no invariant difference beyond labels inserted by hand, or if every proposed \(\mathcal P_p\) decomposes without information loss, the prime-primitive hypothesis fails even if the modular graph facts remain true.

# 19. Warped toroidal filling and scale monodromy

## 19.1 Hypertorus and filling

**K:** The \(n\)-torus is

\[
T^n=(S^1)^n.
\]

A one-dimension-higher filling can be

\[
M^{n+1}=D^2\times T^{n-1},
\qquad
\partial M^{n+1}=T^n.
\]

A warped metric is

\[
ds^2
=
dr^2
+f_0(r)^2d\theta_0^2
+\sum_{j=1}^{n-1}f_j(r)^2d\theta_j^2.
\]

Smooth closure at the disk center requires regularity conditions such as

\[
f_0(0)=0,
\qquad
f_0'(0)=1,
\qquad
f_j(0)>0,
\qquad
f_j'(0)=0\ \ (j\ge1).
\]

These are representative local conditions; the remaining derivatives must be chosen so that the metric extends smoothly through \(r=0\). The boundary hyperarea at \(r=R\) is

\[
A_{\partial M}
=(2\pi)^n\prod_{j=0}^{n-1}f_j(R),
\]

while proper interior volume is

\[
V_M
=(2\pi)^n
\int_0^R
\prod_{j=0}^{n-1}f_j(r)\,dr.
\]

The boundary values can remain fixed while interior profiles vary. This is a legitimate Riemannian filling construction, not a claim that an ordinary shell in flat space violates isoperimetric constraints.

## 19.2 Scale fiber and monodromy

Introduce an effective scale coordinate \(\sigma\):

\[
T^n
\xrightarrow{\iota}
\mathcal B^{n+1}
\xrightarrow{\pi}
I_\sigma,
\]

with

\[
ds^2
=d\sigma^2+G_{ab}(\sigma)d\theta^ad\theta^b.
\]

Let \(A\in\mathrm{GL}(n,\mathbb Z)\) be a torus automorphism. If scale closes by

\[
(\theta,\sigma+L)\sim(A\theta,\sigma),
\]

then one circuit returns the fiber transformed by \(A\), and \(k\) circuits return it by

\[
A^k.
\]

If

\[
\det A=1
\]

and \(A\) has reciprocal eigenvalues \(\lambda,\lambda^{-1}\), then

\[
\lambda^k,
\qquad
\lambda^{-k}
\]

produce simultaneous expansion and contraction along different directions while preserving oriented fiber volume.

**H:** Such monodromy may model recurrence across organizational scale. A physical scale dimension is not established by the mathematics alone.

# 20. Heptadic human consciousness, eighths from seven, and recursion depth

## 20.1 The seven-to-one aggregate

Let seven outer carriers \(B_0,\ldots,B_6\) and their complete typed relation ledger define

\[
\mathcal A_8^{[r+1]}
=
\operatorname{Closure}_7
\left(
\{B_i^{[r]}\},
\mathcal I,
\mathcal R,
\chi,
\phi,
H
\right),
\]

where \(\mathcal I\) is incidence, \(\mathcal R\) is the relation ledger, \(\chi\) is chirality, \(\phi\) is phase, and \(H\) is holonomy.

The eighth is not an eighth peer carrier. It is the coherent, obstructed, or history-dependent global output of the seven:

\[
\mathcal A_8^{\mathrm{coherent}},
\qquad
\mathcal A_8^{\mathrm{obstruction}},
\qquad
\mathcal A_8^{\mathrm{history}}.
\]

The phrase *eighths from seven* is plural because every completed heptadic closure at every nested location can generate such a global aggregate. An aggregate at level \(r+1\) can then function as one carrier in a still higher closure.

## 20.2 Human-consciousness threshold

**H7:** Within this theory, human consciousness requires a heptadic outer closure of seven Möbius-described carriers. Each outer carrier must itself be a stabilized dyadic, triadic, or quintadic closure, so there is at least one nested recursion level beneath the outer seven.

Let

\[
a_i\in\{2,3,5\},
\qquad
B_i^{[1]}
=
\mathfrak C_{a_i,\boldsymbol\alpha_i}^{[1]}
\left(
\mathbb S_{a_i,\boldsymbol\alpha_i}^{[0]}
\right),
\]

so every outer circle has an explicit internal scale set \(\boldsymbol\alpha_i\). Let \(\boldsymbol\beta=(\beta_0,\ldots,\beta_6)\) name the seven outer layer-carriers, and define

\[
\mathcal H_{\mathrm{human},\boldsymbol\beta}^{[2]}
=
\operatorname{Cl}_7
\left(
B_0^{[1]},\ldots,B_6^{[1]};
\mathcal R_7,\chi_7,\phi_7,H_7
\right).
\]

Counting the outer closure as level one, the human requirement is

\[
n_{\mathrm{out}}=7,
\qquad
|\boldsymbol\beta|=7,
\qquad
d_{\mathrm{rec}}\ge2,
\qquad
a_i\in\{2,3,5\}.
\]

The seven entries in \(\boldsymbol\beta\) must be identified by a scale-set certificate rather than selected after the result is known.

The seven carriers need not have identical internal arities. A mixed signature such as

\[
(7;2,3,5,2,3,5,3)
\]

is allowed if its complete relation ledger closes and survives the irreducibility tests. The claim is about functional scale-set carriers, not seven localized brain regions.

The human I-event is proposed to be the self-awareness output of the coherent heptadic aggregate:

\[
\mathsf I_t
=
\mathcal E_{\mathrm{self}}
\left(
\mathcal A_8^{[2]}(t)
\right)
\]

when the coherence, viability, temporal-depth, self-location, and regulatory conditions are simultaneously satisfied.

## 20.3 Moving to organizational “four-dimensionality”

Adding a circle changes direct arity. Adding a recursion level changes dimensional organization. The proposed move to “4D” is an increase in recursion depth:

\[
\mathfrak C_n^{[r]}
\longrightarrow
\mathfrak C_m^{[r+1]}
\left(
\mathfrak C_{a_1}^{[r]},\ldots,
\mathfrak C_{a_m}^{[r]}
\right).
\]

It is not an increase in outer carrier count:

\[
\mathfrak C_7^{[r]}
\longrightarrow
\mathfrak C_8^{[r]}.
\]

At the added level, the system models and constrains the prior closure as a whole. If that added recursion is visualized as an additional dimension, the word *dimension* is organizational and representational unless a physical measurement establishes an additional spacetime or scale dimension.

## 20.4 Failure condition

The heptadic human-consciousness hypothesis fails or must be narrowed if conscious human states can be modeled and interventionally predicted without a seven-carrier outer closure, if the seven-carrier model gives no advantage over lower or arbitrary arities, or if recursion depth does not distinguish human conscious organization from matched nonconscious dynamics.

# 21. Neural implementation without reduction to one brain region

The heptadic hypothesis does not predict seven anatomical consciousness centers. Each outer carrier can be a distributed functional closure whose internal implementation mixes dyadic, triadic, and quintadic couplings across cellular, circuit, bodily, behavioral, and environmental scales. A neural test must therefore identify causal carrier boundaries and recursion signatures rather than count gross regions.

## 21.1 Recurrent neural dynamics

**K:** At the membrane scale, the Hodgkin-Huxley equations provide a standard biophysical description of action-potential generation [23]:

\[
C_m\frac{dV}{dt}
=
I_{\mathrm{ext}}
-\bar g_{\mathrm{Na}}m^3h(V-E_{\mathrm{Na}})
-\bar g_{\mathrm K}n^4(V-E_{\mathrm K})
-g_L(V-E_L),
\]

with gating variables \(x\in\{m,h,n\}\) satisfying

\[
\frac{dx}{dt}
=
\alpha_x(V)(1-x)-\beta_x(V)x.
\]

These equations connect chemical and electrical organization to neural signaling. They are not a consciousness criterion.

**M:** At a neural-population scale, a generic recurrent network can be written

\[
\tau\dot{\mathbf v}
=
-\mathbf v
+W\phi(\mathbf v)
+U\mathbf o
+B\mathbf a
+\boldsymbol\xi(t),
\]

where \(\mathbf v\) is neural state, \(W\) recurrent coupling, \(\mathbf o\) sensory input, \(\mathbf a\) modulatory or action-related input, and \(\boldsymbol\xi\) noise.

Candidate conscious content \(Z_t\) is a metastable, causally integrated mode of this larger body-brain-environment system, not merely a high firing rate in one location.

## 21.2 Prediction and broadcast

A hierarchical model can update latent expectations by prediction error:

\[
\varepsilon_l=o_l-g_l(\mu_l,\mu_{l+1}),
\]

\[
\dot\mu_l
=
F_l(\mu_l)
-K_l\varepsilon_l
+K_{l+1}\varepsilon_{l+1}.
\]

The precise update law is architecture-dependent. Conscious access requires that
the selected content affect memory, valuation, planning, and action above the
preregistered per-module threshold; \(G_{\mathrm c}>0\) by itself is not enough.

## 21.3 Relation to existing consciousness research

Global-workspace theories emphasize wide availability and recurrent amplification [12,14]. Integrated-information theories emphasize intrinsic causal structure [13,15]. Recurrent-processing and predictive approaches emphasize feedback and model-dependent perception. The present theory treats these as partially orthogonal constraints rather than mutually exclusive slogans. Information-decomposition analyses have also reported reduced synergistic workspace integration during anesthesia and disorders of consciousness, with restoration during recovery [17].

Current reviews emphasize that leading theories differ in their explananda, mechanisms, and empirical commitments [16]. Current evidence does not justify declaring a winner. A large preregistered adversarial collaboration published in 2025 [18] found results that aligned with some predictions of both Integrated Information Theory and Global Neuronal Workspace Theory while substantially challenging central predictions of both. A 2026 cross-species adversarial protocol adds preregistered causal manipulations in non-human primates and mice [33]; it is a protocol, not evidence for this paper's arity or heptadic claims. The appropriate response is not to average theories into vagueness, but to define measurable components and preregister divergent predictions.
