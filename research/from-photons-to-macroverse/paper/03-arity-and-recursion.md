
# 11. Scale-invariant coupling and arity-specific recursive closure

## 11.1 Effective layer-carriers and direct scale sets

An *effective layer-carrier* is a stabilized process treated as one participant at the current recursion level. It has a declared identity map, characteristic update law, and causal channel to at least one other layer-carrier. It can correspond to a spatial, temporal, energetic, biological, cognitive, or social organization scale. Calling it a layer does not require a new fundamental spatial dimension.

Write

\[
L_{\alpha_i}^{[r]}
\]

for layer-carrier \(i\) at recursion level \(r\), where \(\alpha_i\) names its physical or organizational scale. The ordered direct scale set of an \(n\)-adic closure is

\[
\mathbb S_{n,\boldsymbol\alpha}^{[r]}
=
\left(
L_{\alpha_1}^{[r]},\ldots,L_{\alpha_n}^{[r]}
\right),
\qquad
\boldsymbol\alpha=(\alpha_1,\ldots,\alpha_n).
\]

Every actual closure therefore has a *specific* direct scale set. The integer \(n\) identifies its arity class; the label vector \(\boldsymbol\alpha\) identifies which scales participate. A layer-carrier can be elementary relative to the current description or can already be the stabilized output of a lower closure.

Let \(S_0\) be lower-level dynamics, \(S_1\) the embodied aggregate at which selected lower variables become externally legible, and \(S_2\) a larger relational context capable of constraining \(S_1\). This is the first triadic scale set used in the paper:

\[
\mathbb S_{3,(0,1,2)}=(S_0,S_1,S_2).
\]

The upward path is

\[
v_0=P_0(x_0),
\]

\[
x_1=E_0(v_0),
\]

\[
x_2=E_1(P_1(x_1),R_1).
\]

The downward path is

\[
c_1=D_2(x_2),
\]

\[
c_0=D_1(x_1,c_1),
\]

\[
x_0(t+\Delta t)
=
F_0(x_0(t),c_0(t)).
\]

The triadic loop is

\[
S_0\rightarrow S_1\rightarrow S_2\rightarrow S_1\rightarrow S_0.
\]

## 11.2 One coupling schema, different scale-dependent results

**H:** The coupling that produces a closure is invariant in relational form across scale, but its realized state is scale-dependent.

Let

\[
\mathcal K_{n,\boldsymbol\alpha}^{[r]}:
X_{\alpha_1}^{[r]}\times\cdots\times X_{\alpha_n}^{[r]}
\longrightarrow
Y_{n,\boldsymbol\alpha}^{[r+1]}
\]

be the realized \(n\)-ary coupling. The invariant is the coupling *schema*: direct arity, recurrence, orientation, constraint return, retention, projection, and closure test. Numerical parameters, materials, amplitudes, time constants, observables, and the identity of the resulting aggregate remain scale-dependent.

If \(C_{\boldsymbol\alpha\to\boldsymbol\beta}\) translates one realization to another scale set, approximate scale-form consistency requires

\[
d\!\left(
C_{\boldsymbol\alpha\to\boldsymbol\beta}
\mathcal K_{n,\boldsymbol\alpha}^{[r]}(\mathbf x),
\mathcal K_{n,\boldsymbol\beta}^{[r]}
\big(C_{\boldsymbol\alpha\to\boldsymbol\beta}^{\times n}\mathbf x\big)
\right)
\le \varepsilon_{n,\boldsymbol\alpha\boldsymbol\beta}.
\]

The same relational law can therefore recur at photon, atomic, cellular, neural, bodily, interpersonal, or larger organizational scales without producing the same object. Scale invariance of coupling does not imply scale invariance of result.

## 11.3 The dyadic, triadic, quintadic, and heptadic scale-set classes

Define

\[
\mathfrak D_{2,\boldsymbol\alpha}
=
\operatorname{Cl}_2(\mathbb S_{2,\boldsymbol\alpha}),
\qquad
\mathfrak T_{3,\boldsymbol\alpha}
=
\operatorname{Cl}_3(\mathbb S_{3,\boldsymbol\alpha}),
\]

\[
\mathfrak Q_{5,\boldsymbol\alpha}
=
\operatorname{Cl}_5(\mathbb S_{5,\boldsymbol\alpha}),
\qquad
\mathfrak H_{7,\boldsymbol\alpha}
=
\operatorname{Cl}_7(\mathbb S_{7,\boldsymbol\alpha}).
\]

The following is the canonical research mapping used in this paper. It assigns a different organizational problem to each arity rather than treating the sequence as one object with extra circles.

| Closure class | Specific direct scale set in an application | Candidate role in the relational-temporal bridge |
|---|---|---|
| Dyadic \(\mathfrak D_2\) | \((L_{\alpha_1},L_{\alpha_2})\) | establishes a retained distinction or reciprocal return channel, such as other/self, self/environment, past/present, or present/future |
| Triadic \(\mathfrak T_3\) | \((L_{\alpha_1},L_{\alpha_2},L_{\alpha_3})\) | supplies irreducible mediation and the minimum closed loop; the canonical semantic instances are other(self)environment and past(present)future |
| Quintadic \(\mathfrak Q_5\) | five declared layer-carriers | binds the relational and temporal triads through a shared present-self update, producing a five-role bridge rather than two disconnected triads |
| Heptadic \(\mathfrak H_7\) | seven declared outer layer-carriers | closes seven nested carrier histories into the global aggregate hypothesized to be required for human consciousness |

The exact physical labels in \(\boldsymbol\alpha\) are part of the model certificate and cannot be inferred from the numeral alone. The numeral identifies the direct scale-set class. Section 13 gives the candidate dyadic-to-quintadic bridge; Section 20 gives the human heptad.

## 11.4 A triad is not a dyad plus one circle

For a genuine arity-specific closure,

\[
\mathfrak C_{n+1}(B_1,\ldots,B_{n+1})
\not\simeq
\mathfrak C_n(B_1,\ldots,B_n)\oplus B_{n+1}
\]

unless the added carrier is causally separable and the higher-order partition loss vanishes. Define

\[
\Phi_n
=
\min_{\pi\in\operatorname{Part}_{\mathrm{proper}}([n])}
D_{\mathrm{KL}}
\left(
P_n(\mathbf x'\mid\mathbf x)
\,\|\,
P_n^{\pi}(\mathbf x'\mid\mathbf x)
\right).
\]

Here \(\operatorname{Part}_{\mathrm{proper}}([n])\) excludes the one-block
partition \(\{[n]\}\) and admits only partitions with at least two blocks. The
unpartitioned transition law is therefore not its own control.

When \(\Phi_n>0\), no admissible partition into lower-arity blocks reproduces the full transition law.

The difference is not merely philosophical. Let independent fair bits \(X,Y\) satisfy \(Z=X\oplus Y\). Then

\[
I(X;Y)=I(X;Z)=I(Y;Z)=0,
\qquad
H(Z\mid X,Y)=0.
\]

Every pair is uninformative while the triad is perfectly constrained. The three-way relation therefore cannot be recovered by “adding one item” to any dyadic description. Quintadic and heptadic closures must pass analogous partition tests rather than inherit irreducibility by name.

## 11.5 Nested closures: the tensor of tensors

Direct arity and recursion depth are different variables. Let \(r\) denote recursion level. A nested closure is

\[
\mathfrak C_{n,\boldsymbol\alpha}^{[r+1]}
=
\operatorname{Cl}_n
\left(
B_1^{[r]},\ldots,B_n^{[r]};
\mathcal R_n,\chi_n,\phi_n,H_n
\right),
\]

where each outer layer-carrier can itself be a closure,

\[
B_i^{[r]}
=
\mathfrak C_{a_i,\boldsymbol\alpha_i}^{[r]}(\cdots),
\qquad
a_i\in\{2,3,5,7\}.
\]

A triadically coupled set of dyads is therefore a literal nested case. For example,

\[
\mathfrak T_{\mathrm{OSE}}^{[2]}
=
\operatorname{Cl}_3
\left(
\mathfrak D_{OS}^{[1]},
\mathfrak D_{SE}^{[1]},
\mathfrak D_{EO}^{[1]}
\right),
\]

and a temporal triad can be written

\[
\mathfrak T_{\mathrm{PNF}}^{[2]}
=
\operatorname{Cl}_3
\left(
\mathfrak D_{PN}^{[1]},
\mathfrak D_{NF}^{[1]},
\mathfrak D_{FP}^{[1]}
\right).
\]

A triadically coupled set of dyads has first-level signature

\[
(3;2,2,2),
\]

while a triadically coupled set of triads has signature

\[
(3;3,3,3).
\]

They have the same outer arity and different internal structures. The complete recursive signature is therefore a rooted arity tree, not one integer.

When the carrier state spaces are linear, the phrase *tensor of tensors* can be used literally:

\[
V^{[r+1]}
=
\bigotimes_{i=1}^{n}V_i^{[r]},
\qquad
V_i^{[r]}
=
\bigotimes_{j=1}^{a_i}V_{ij}^{[r-1]},
\]

so

\[
V^{[r+1]}
=
\bigotimes_{i=1}^{n}
\left(
\bigotimes_{j=1}^{a_i}V_{ij}^{[r-1]}
\right).
\]

This notation records nested multilinear dependence. It does not, by itself, assert quantum entanglement or that every relevant state space is linear.

## 11.6 Möbius circle count and the scale-set certificate

**M/H:** In the Möbius descriptions used here, one circle denotes one directly participating outer layer-carrier at the displayed recursion level. Let

\[
\mu_i:C_i\longleftrightarrow L_{\alpha_i}^{[r]}.
\]

Then

\[
N_{\mathrm{circles}}
=
N_{\mathrm{direct\ layer\text{-}carriers}}
=n.
\]

Two circles identify a dyadic direct set, three a triadic set, five a quintadic set, and seven a heptadic set. The circle count identifies the arity class; the circle-to-layer map \(\mu\) identifies the actual scale set. A minimally adequate certificate is

\[
\operatorname{Cert}
\left(\mathfrak C_{n,\boldsymbol\alpha}^{[r]}\right)
=
\left(
n,\boldsymbol\alpha,r,\mathscr A,
\mathcal R_n,\chi_n,\phi_n,H_n,\mathcal F_n
\right),
\]

where \(\mathscr A\) is the rooted arity tree and \(\mathcal F_n\) is the declared closure or falsification test.

Nested structures inside a circle do not change the outer circle count; they change \(r\) and \(\mathscr A\). A seven-circle heptad whose immediate carriers have arities \((2,3,5,2,3,5,3)\) is not a twenty-three-circle direct closure. It is a heptadic closure with seven nested carrier histories.

## 11.7 Distributed identity and closure contribution

Let \(I_0(x_0)\) be the lower-scale identity variable. Preservation requires

\[
I_0(x_0(t+\Delta t))
\approx
I_0(x_0(t))
\]

within a declared tolerance and disturbance class. The identity is distributed across lower dynamics, embodied externalization, and higher constraint.

**M:** Compare recovery in a full loop with recovery after cutting one upward or downward map:

\[
\Gamma_T
=
\mathbb E_{\delta}
\left[
\mathcal R_T^{\mathrm{full}}(\delta)
-
\mathcal R_T^{\mathrm{cut}}(\delta)
\right].
\]

A positive \(\Gamma_T\) shows that cross-scale closure contributes causally to recovery.

**H:** Broad, context-sensitive self-preservation requires at least a triadic direct closure. Human consciousness adds the stronger heptadic and recursion-depth requirements stated in Section 20. The two thresholds must not be conflated.
