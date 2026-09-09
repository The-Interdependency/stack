
# 5. Nonlinearity, pattern formation, and topological memory

## 5.1 Why nonlinearity matters

Linear waves pass through one another. Persistent localized structures generally require interactions or constraints that make the state influence its own future evolution.

A standard effective equation for a complex order parameter near an oscillatory instability is the complex Ginzburg-Landau equation [6]:

\[
\partial_t\Psi
=
(r+i\omega_0)\Psi
+(c_1+ic_2)\nabla^2\Psi
-(u+iv)|\Psi|^2\Psi
+\xi(x,t).
\]

Here the cubic term can saturate growth, spatial coupling can organize phase, and \(\xi\) represents noise. This equation is not asserted to govern photons in vacuum. It represents a mathematically known route by which a phase-bearing medium can form persistent patterns.

## 5.2 Reaction-diffusion organization

**K:** Another route is reaction-diffusion [5]:

\[
\frac{\partial u}{\partial t}
=D_u\nabla^2u+f(u,v),
\qquad
\frac{\partial v}{\partial t}
=D_v\nabla^2v+g(u,v).
\]

A homogeneous fixed point can be stable without diffusion and unstable with differential diffusion, producing spatial structure. Pattern formation therefore needs neither a miniature designer nor a conscious field; ordinary nonlinear dynamics can amplify relational differences.

## 5.3 Chemical networks

At a chemical scale, concentrations \(\mathbf c\) evolve as

\[
\dot{\mathbf c}=\mathbf S\mathbf v(\mathbf c),
\]

where \(\mathbf S\) is the stoichiometric matrix and \(\mathbf v\) is the vector of reaction rates. Autocatalysis, inhibition, compartmentalization, and resource flow can produce self-maintaining reaction networks.

## 5.4 Topological invariants

For an order parameter \(\Psi=|\Psi|e^{i\phi}\), phase winding around a closed loop \(\gamma\) is

\[
\nu_\gamma
=
\frac{1}{2\pi}
\oint_\gamma\nabla\phi\cdot d\ell
\in\mathbb Z.
\]

A nonzero integer cannot change continuously without the order parameter passing through a singular or vanishing state. This is a precise sense in which a relation can be protected by topology.

# 6. Dynamical stability and identity through change

## 6.1 Attractors and Lyapunov stability

Let a system obey

\[
\dot x=f(x,u,w),
\]

where \(u\) is control and \(w\) is disturbance. A fixed point \(x_{\mathrm{eq}}\) is locally stable if there exists a Lyapunov function \(V(x)\) satisfying

\[
V(x_{\mathrm{eq}})=0,
\qquad
V(x)>0\ \text{for}\ x\ne x_{\mathrm{eq}},
\qquad
\dot V=\nabla V\cdot f\le0.
\]

Conscious organisms are not fixed points. Their relevant identity is a stable set, trajectory family, or metastable regime.

## 6.2 Identity as an equivalence class

**M:** Let \(I_k:X_k\rightarrow\mathcal Q_k\) be a declared coarse identity map at scale \(k\). Define

\[
x\sim_{I_k}y
\quad\Longleftrightarrow\quad
I_k(x)=I_k(y).
\]

Equality of the coarse labels is reflexive, symmetric, and transitive, so it defines the genuine equivalence class

\[
[x]_{I_k}
=
\{y\in X_k:I_k(y)=I_k(x)\}.
\]

For noisy measurements, a separate feature map \(\widetilde I_k:X_k\rightarrow\mathbb R^m\) may supply the empirical neighborhood test

\[
d_k\!\left(\widetilde I_k(x),\widetilde I_k(y)\right)\le\varepsilon_k.
\]

That tolerance relation is evidence for common class membership; it is not itself assumed to be transitive. A body can replace molecules while remaining within the same identity class. A belief can change while the agent remains the same agent. Exact microstate preservation is neither required nor biologically possible.

## 6.3 Robust persistence

Given a perturbation \(\delta\), let \(x_t^\delta\) be the perturbed trajectory and \(\mathcal Q_{\mathrm{target}}\) the target identity class. Let \(Q_{\mathrm{target}}\subset\mathbb R^m\) be the feature-space image of the target identity class and define distance to that set by

\[
d(y,Q_{\mathrm{target}})
=
\inf_{q\in Q_{\mathrm{target}}}d(y,q).
\]

Using this declared dimensionless distance, define recovery over horizon \(T\) as

\[
\mathcal R_T(\delta)
=
\exp\left[
-\frac1T
\int_0^T
 d\bigl(\widetilde I(x_t^\delta),Q_{\mathrm{target}}\bigr)\,dt
\right].
\]

A stable entity has high expected recovery under an admitted perturbation distribution:

\[
\overline{\mathcal R}_T
=
\mathbb E_{\delta\sim q(\delta)}[\mathcal R_T(\delta)].
\]

**H:** The first transition toward objecthood occurs when relations are not merely present but contribute to \(\overline{\mathcal R}_T\).

# 7. Coarse-graining and the rise of macroscopic entities

## 7.1 Scale maps

Let

\[
C_k:X_k\rightarrow X_{k+1}
\]

be a coarse-graining map from a finer description to a coarser one. A compatible scale tower is

\[
\mathfrak X
=
\left\{
(x_0,x_1,\ldots,x_N):x_{k+1}=C_k(x_k)
\right\}.
\]

The macrostate is not an extra substance. It is a quotient description that preserves selected invariants while discarding microdetail.

## 7.2 Cross-scale consistency

Let \(I_k\) and \(I_{k+1}\) be scale-specific invariants, and let \(T_k\) translate the fine-scale invariant into the coarse description. Cross-scale identity requires

\[
d_{k+1}
\left(
I_{k+1}(C_kx),
T_kI_k(x)
\right)
\le\varepsilon_k.
\]

When this relation remains stable under perturbation, the same entity is legible at several scales.

## 7.3 Evolutionary selection

Once self-maintaining variants reproduce with heritable differences, selection changes their frequencies. A standard replicator equation is [9]

\[
\dot p_i
=
p_i\bigl(f_i(\mathbf p)-\bar f(\mathbf p)\bigr),
\qquad
\bar f=\sum_jp_jf_j.
\]

Evolution does not aim at consciousness. It can nevertheless select regulatory architectures that predict, act, integrate information, and preserve themselves in variable environments.

# 8. Information, relation, and causal irreducibility

## 8.1 Shannon information [7]

For a discrete variable \(X\),

\[
H(X)=-\sum_xp(x)\log p(x).
\]

Mutual information is

\[
I(X;Y)
=
\sum_{x,y}
p(x,y)
\log\frac{p(x,y)}{p(x)p(y)}.
\]

Conditional mutual information is

\[
I(X;Y\mid Z)
=
\sum_{x,y,z}
p(x,y,z)
\log
\frac{p(x,y\mid z)}{p(x\mid z)p(y\mid z)}.
\]

Unless another base is stated, logarithms are natural and the resulting information quantities are measured in nats.

These quantities measure statistical dependence. They do not by themselves establish causal influence or consciousness.

## 8.2 Directional information

Transfer entropy is

\[
T_{X\rightarrow Y}
=
I(X_t;Y_{t+1}\mid Y_t).
\]

It is useful for detecting predictive directionality, but confounding can make predictive influence differ from intervention-level causation [10].

## 8.3 Interventional causal irreducibility

**M:** Let \(X=(X^1,\ldots,X^n)\) have an interventional transition kernel

\[
P(X_{t+1}=x'\mid\operatorname{do}(X_t=x)).
\]

For a nontrivial partition \(\pi=\{B_1,\ldots,B_m\}\), choose a declared reference intervention distribution \(r(x)\). Randomize the inputs arriving from outside each block and define the cut block kernel

\[
P^{\mathrm{cut}}_{B,r}(x'_B\mid\operatorname{do}(x_B))
=
\sum_{\widetilde x_{\overline B}}
r_{\overline B}(\widetilde x_{\overline B})
P\!\left(x'_B\mid\operatorname{do}(x_B,\widetilde x_{\overline B})\right).
\]

The partitioned transition kernel is

\[
P_{\pi,r}(x'\mid\operatorname{do}(x))
=
\prod_{B\in\pi}
P^{\mathrm{cut}}_{B,r}(x'_B\mid\operatorname{do}(x_B)).
\]

Define causal irreducibility by

\[
\Phi_{\mathrm c}(X;r)
=
\min_{\pi\in\Pi_{\mathrm{proper}}(X)}
\mathbb E_{x\sim r}
\left[
D_{\mathrm{KL}}
\left(
P(\cdot\mid\operatorname{do}(x))
\,\|\,
P_{\pi,r}(\cdot\mid\operatorname{do}(x))
\right)
\right].
\]

The comparison assumes absolute continuity or an explicitly declared smoothing rule so that the divergence is finite.

Here

\[
D_{\mathrm{KL}}(P\|Q)
=
\sum_zP(z)\log\frac{P(z)}{Q(z)}.
\]

If \(\Phi_{\mathrm c}(X;r)=0\), at least one partition reproduces the full transition law under the chosen intervention distribution. If \(\Phi_{\mathrm c}(X;r)>0\), every admissible partition loses causal constraint.

This measure is related in spirit to integrated-information approaches [13,15] but is not presented as a restatement of any current Integrated Information Theory quantity. It is an explicit candidate tailored to falsifiable system identification.

## 8.4 Differentiation

Integration without a differentiated repertoire can describe a rigid synchronized block. For a finite candidate repertoire \(\mathcal Z\) with \(|\mathcal Z|>1\), define normalized differentiation

\[
\mathcal D(Z)
=
\frac{H(Z)}{\log|\mathcal Z|}
\in[0,1].
\]

A rich conscious system requires both causal unity and a differentiated repertoire.

## 8.5 Six forms of irreducibility

The phrase **irreducible complexity** is used here in a technical rather than theological sense. The theory distinguishes:

| Form | Criterion |
|---|---|
| Dynamical | no lower-order linear superposition reproduces the nonlinear trajectory family |
| Topological | an integer or holonomy invariant cannot change continuously without a singular event |
| Causal | \(\Phi_{\mathrm c}>0\) under the declared intervention family |
| Regulatory | ablating the internal model reduces prediction, control, or viability: \(\mathcal M>0\) |
| Scale-relational | cutting an upward or downward scale map reduces recovery: \(\Gamma>0\) |
| Perspectival | removing self-location worsens the generative and control model: \(\Sigma>0\) |

No one form entails the others. Consciousness, under the present hypothesis, requires several to coincide in one temporally extended embodied process.

# 9. Boundaries, viability, and the first agent

## 9.1 Conditional boundary

Partition states into internal \(\mu\), external \(\eta\), and blanket states \(b=(s,a)\), with sensory states \(s\) and active states \(a\). A Markov blanket satisfies

\[
p(\mu,\eta\mid b)
=
p(\mu\mid b)p(\eta\mid b),
\]

or equivalently

\[
I(\mu;\eta\mid b)=0.
\]

For empirical systems the independence is approximate. Let

\[
H_b=H(\mu,\eta\mid b)
\]

and preregister a minimum supported conditional entropy \(\tau_H>0\). For finite discrete or explicitly discretized variables, define normalized boundary integrity by

\[
\mathcal B_{\mathrm{bdry}}
=
\begin{cases}
1-\dfrac{I(\mu;\eta\mid b)}{H_b},
& H_b\ge\tau_H,\\[6pt]
\text{undefined},
& H_b<\tau_H.
\end{cases}
\]

The support threshold prevents a constant or nearly constant system from receiving a perfect boundary score merely because both the conditional mutual information and conditional entropy vanish. An undefined value remains missing evidence; it is not replaced by \(1\), \(0\), or an arbitrarily smoothed number. Continuous-state applications require a declared estimator or replacement divergence and their own preregistered support test.

## 9.2 Viability

Let \(K\subset X\) be the set of states compatible with continued organization. Viability over horizon \(T\) is

\[
\mathcal V_T
=
\Pr\left[X_t\in K\ \text{for all}\ t\in[0,T]\right].
\]

A rock may be stable, but it does not ordinarily regulate itself to remain in a viability set. An agent changes its actions as a function of sensed conditions so as to preserve \(\mathcal V_T\).

## 9.3 Bayesian inference and variational free energy

For latent causes \(z\) and observations \(o\), Bayes' rule is

\[
p(z\mid o)
=
\frac{p(o\mid z)p(z)}{p(o)}.
\]

For an approximate posterior \(q(z)\), variational free energy is [11]

\[
F[q]
=
\mathbb E_q[\ln q(z)-\ln p(o,z)],
\]

Equivalently,

\[
F[q]
=
D_{\mathrm{KL}}\bigl(q(z)\|p(z\mid o)\bigr)
-
\ln p(o)
\ge
-\ln p(o).
\]

Minimizing \(F\) improves posterior approximation. The use of this formalism as a universal theory of life or consciousness is a hypothesis, not a consequence of the inequality.

# 10. Internal models and causal self-preservation

## 10.1 Minimal model criterion

**M:** An internal state \(m_t\) counts as a model only if it satisfies four conditions:

1. it covaries with survival-relevant hidden or future states;
2. it generates predictions or action policies;
3. changing it changes regulation;
4. ablating it worsens prediction or recovery under matched conditions.

Write

\[
m_t=M(\mu_t),
\]

\[
\widehat o_{t+1:T}
=P(m_t,a_{t:t+T-1}),
\]

and predictive error

\[
e_{t+1}=o_{t+1}-\widehat o_{t+1}.
\]

## 10.2 Model efficacy

The good-regulator principle motivates the requirement that successful regulation embody a model [8]. Let \(\mathcal L\) combine prediction error, control cost, and viability loss. Define causal model efficacy as

\[
\mathcal M_T
=
\mathbb E
\left[
\mathcal L_{\mathrm{ablated}}
-
\mathcal L_{\mathrm{intact}}
\right].
\]

If \(\mathcal M_T\le0\), the alleged model is not shown to contribute to regulation. Correlation is insufficient.

## 10.3 Agency

Let \(A_t\) be an action variable. Let \(\rho_T(x,a,a')\) be a preregistered reference distribution over matched contexts and ordered action interventions. Define the action's causal reach by

\[
\mathcal A_T(\rho_T)
=
\mathbb E_{(x,a,a')\sim\rho_T}
D_{\mathrm{KL}}
\left[
P(X_{t+1:t+T}\mid\operatorname{do}(A_t=a),x)
\,\|\,
P(X_{t+1:t+T}\mid\operatorname{do}(A_t=a'),x)
\right].
\]

A thermostat can have nonzero causal reach. Conscious agency additionally requires that actions depend on an integrated self/world model. The observational condition

\[
I(M_t;A_t\mid O_{\le t})>0
\]

is only a screening test. Let \(\rho_M(o,m,m')\) be a preregistered distribution over matched observations and ordered model-state interventions. A stronger causal model-to-action measure is

\[
\mathcal A_M(\rho_M)
=
\mathbb E_{(o,m,m')\sim\rho_M}
D_{\mathrm{KL}}
\left[
P(A_t\mid\operatorname{do}(M_t=m),o)
\,\|\,
P(A_t\mid\operatorname{do}(M_t=m'),o)
\right].
\]

Neither quantity is numerically defined until its support, matching rule, horizon, intervention semantics, estimator, and uncertainty procedure are declared. Control is necessary in this theory but not sufficient.
