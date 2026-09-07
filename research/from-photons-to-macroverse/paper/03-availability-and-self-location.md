# 12. Global availability and temporal depth

## 12.1 Candidate conscious content

Let \(Z_t\) denote a candidate content-bearing state or metastable complex. Let \(Y_t^j\) denote specialized systems for memory, valuation, planning, action, language, and perceptual interpretation.

An observational global-availability measure is

\[
G_{\mathrm{obs}}(Z_t)
=
\frac1m
\sum_{j=1}^m
I(Z_t;Y_{t+\Delta}^j\mid Y_t^j).
\]

Let \(\rho_Z(z)\) be a preregistered intervention distribution and \(z_0\) a declared reference content state. An interventional form is stronger:

\[
G_{\mathrm c}(Z_t;\rho_Z,z_0)
=
\frac1m
\sum_{j=1}^m
\mathbb E_{z\sim\rho_Z}
D_{\mathrm{KL}}
\left[
P(Y_{t+\Delta}^j\mid\operatorname{do}(Z_t=z))
\,\|\,
P(Y_{t+\Delta}^j\mid\operatorname{do}(Z_t=z_0))
\right].
\]

The mean alone is not sufficient. Define the per-module effect \(g_j\) as the
summand inside \(G_{\mathrm c}\), and define
\[
S_G=\{j:g_j>\tau_G\}.
\]
Conscious access, under this model, requires \(G_{\mathrm c}>0\), per-module
effects above \(\tau_G\) for the preregistered memory, valuation, planning, and
action modules, and \(|S_G|\ge k_G\). The module set, \(\tau_G\), \(k_G\),
reference state, intervention distribution, horizon, and estimator must be
frozen before comparison.

## 12.2 Temporal depth

The temporal model is not an unindexed clock. It is the retention and projection of a self-located relational state. Section 13.3 makes the bridge from \(\mathrm{other}(\mathrm{self})\mathrm{environment}\) to \(\mathrm{past}(\mathrm{present})\mathrm{future}\) explicit.

A content that exists only at an instantaneous boundary has no modeled past and constrains no modeled future. Let \(X_t^{-Z}\) denote the current state with the candidate content variable excluded. Define retained-past depth by

\[
\Theta_{\mathrm{ret}}(Z_t)
=
\int_0^{T_{\mathrm{past}}}
w_{\mathrm{past}}(\tau)
I(Z_t;X_{t-\tau})\,d\tau.
\]

For each intervention value \(z\), let

\[
P_z^{\tau}(\cdot\mid X_t^{-Z})
=
P(X_{t+\tau}\in\cdot\mid\operatorname{do}(Z_t=z),X_t^{-Z}).
\]

Define the pairwise prospective effect

\[
K_{\tau}(z,z')
=
D_{\mathrm{KL}}
\left(
P_z^{\tau}
\,\|\,
P_{z'}^{\tau}
\right).
\]

Prospective interventional depth is

\[
\Theta_{\mathrm{pros}}(Z_t)
=
\int_0^{T_{\mathrm{future}}}
w_{\mathrm{future}}(\tau)
\mathbb E_{z,z'}[K_{\tau}(z,z')]\,d\tau.
\]

Then

\[
\Theta(Z_t)
=
\Theta_{\mathrm{ret}}(Z_t)
+
\Theta_{\mathrm{pros}}(Z_t).
\]

The first term measures retained past. The second measures how alternate content states change future-state distributions beyond the rest of the current state. The weights and intervention distribution must be declared before estimation.

## 12.3 Metastability

Conscious content is neither completely fixed nor unconstrained noise. Let \(\mathcal Z\) be a candidate content manifold and \(Z_t\) a trajectory on it. A metastable episode remains within a coherent region for a finite duration and then transitions:

\[
\Pr[Z_{t+\tau}\in\Omega_Z\mid Z_t\in\Omega_Z]
\gg
\Pr[Z_{t+\tau}\in\Omega_Z]
\]

for \(0<\tau<T_Z\). If \(\tau_{\mathrm{exit}}\) is the first exit time from \(\Omega_Z\), metastability additionally requires

\[
0<\mathbb E[\tau_{\mathrm{exit}}]<\infty,
\]

so the state is persistent but not permanently frozen.

# 13. Self-location: other, self, and environment

## 13.1 Indexical model

A world model can be sophisticated without representing the model-bearing system as a distinct causal center. Let the latent model factor as

\[
z_t
=
\left(
z_t^{\mathrm{self}},
z_t^{\mathrm{other}},
z_t^{\mathrm{environment}}
\right).
\]

The self component predicts body state, action consequences, and ownership of sensory changes. Define the relationally indexed state

\[
\mathcal R_t
=
\mathrm{other}(\mathrm{self})\mathrm{environment}_t
\equiv
(O_t,S_t,E_t).
\]

The parenthesized notation marks the self as the active index through which other and environment are distinguished, not as an isolated substance placed between two external objects.

## 13.2 Self-model efficacy

Let \(q_{\mathrm{self}}\) be a generative model with an explicit self-index and \(q_{\mathrm{flat}}\) a matched model without that distinction. Let \(\rho_{\Sigma}\) be a preregistered distribution over matched tasks, perturbations, and initial conditions. Define

\[
\Sigma_T(\rho_{\Sigma})
=
\mathbb E_{\rho_{\Sigma}}
\left[
\mathcal L(q_{\mathrm{flat}})
-
\mathcal L(q_{\mathrm{self}})
\right].
\]

A positive \(\Sigma_T\) under that declared comparison shows that self-location contributes to prediction and regulation. It does not prove phenomenal selfhood, but it makes the concept operational.

## 13.3 From other(self)environment to past(present)future

The bridge is not a jump from one vocabulary to another. It is a nested sequence of closures over declared scale sets.

### Dyadic prerequisites

A dyad can preserve a distinction and a return relation:

\[
\mathfrak D_{OS}=\operatorname{Cl}_2(O,S),
\qquad
\mathfrak D_{SE}=\operatorname{Cl}_2(S,E),
\]

\[
\mathfrak D_{PN}=\operatorname{Cl}_2(P,N),
\qquad
\mathfrak D_{NF}=\operatorname{Cl}_2(N,F).
\]

These dyads can distinguish other from self, self from environment, retained from current, or current from projected. No one dyad yet supplies complete self-location or a complete temporal horizon.

### Triadic relational and temporal closure

The relational triad is

\[
\mathcal R_{3,t}
=
\operatorname{Cl}_3(O_t,S_t,E_t)
=
\mathrm{other}(\mathrm{self})\mathrm{environment}_t.
\]

It makes the self an active index within a relation to both another center or process and a surrounding field of constraint. The temporal triad is

\[
\mathcal T_{3,t}
=
\operatorname{Cl}_3(P_t,N_t,F_t)
=
\mathrm{past}(\mathrm{present})\mathrm{future}_t.
\]

It makes the present the active update within retained history and reachable projection. Each can be implemented as a triadically coupled set of dyads, but the completed triad has relations not supplied by any pair alone.

### Quintadic gluing of relation and time

The temporal model becomes *subject-relative* only when the self-index in \(\mathcal R_{3,t}\) is coupled to the present update in \(\mathcal T_{3,t}\). Let

\[
\iota_t:S_t\leftrightarrow N_t
\]

be the gluing relation that says: this modeled self is the center whose retained relations are being updated now. Define the present-self event

\[
J_t=\operatorname{Upd}(S_t,N_t;\iota_t).
\]

The candidate quintadic bridge is the amalgamated closure

\[
\mathcal Q_{5,t}
=
\mathcal R_{3,t}\sqcup_{\iota_t}\mathcal T_{3,t}
=
\operatorname{Cl}_5
\left(
O_t,E_t,P_t,J_t,F_t
\right).
\]

The five roles are other, environment, past, future, and the present self-locating update that joins the two triads. The notation does **not** say that the self-system and the temporal present are identical in every respect. It says they must refer to the same update event for memory and prospection to be *mine* rather than merely stored data and simulated possibilities.

For an arbitrary \(n\)-adic carrier at scale set \(\boldsymbol\alpha\), write

\[
\mathcal R_{n,\boldsymbol\alpha,t}
=(O_{n,t},S_{n,t},E_{n,t}).
\]

Its temporalization is

\[
\mathcal T_{n,\boldsymbol\alpha,t}
=
\left(
\operatorname{Ret}_n(\mathcal R_{n,<t}),
\mathcal R_{n,t},
q_n\!\left(
\mathcal R_{n,>t}
\mid
\mathcal R_{n,\le t},a_t
\right)
\right).
\]

The update loop is

\[
\mathcal R_{n,t-1}
\xrightarrow{\operatorname{retain}}
\mathcal T_{n,t}
\xrightarrow{\operatorname{infer/act}}
\widehat{\mathcal R}_{n,t+1}
\xrightarrow{\operatorname{compare}}
\mathcal R_{n,t+1}.
\]

The present is therefore not a dimensionless instant. It is the coherent update event in which retained self-located relations constrain inference and projected self-located relations constrain action.

### Heptadic global alignment

Dyadic, triadic, and quintadic closures can recur at different scales with the same coupling schema and different contents. In the human case, seven such nested layer-carriers are proposed to close heptadically:

\[
\mathcal A_{8,t}
=
\operatorname{Cl}_7
\left(
B_{1,t},\ldots,B_{7,t}
\right),
\qquad
B_i\in\{\mathfrak D_2,\mathfrak T_3,\mathfrak Q_5\}
\]

at their immediate internal level. The heptadic aggregate aligns their scale-specific relational and temporal models into one globally available present-self event. This is the explicit bridge from pairwise distinctions, through relational and temporal triads, through quintadic subject-relative temporalization, to the nested heptad described in Section 20.
