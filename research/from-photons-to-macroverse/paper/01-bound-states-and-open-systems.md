# 3. From field quanta to atomic bound states

## 3.1 “Photon scale” is not one spatial size

**K:** A photon has no fixed universal diameter or wavelength. In vacuum,

\[
E=\hbar\omega=\frac{hc}{\lambda},
\qquad
p=\frac{h}{\lambda}.
\]

High-energy photons have short wavelengths; low-energy photons have long wavelengths. The phrase *photon scale to atomic scale* therefore names a change of physical organization: from propagating quanta of a field to stable bound states of several interacting fields. It is not a zoom from one fixed photon-sized object to an atom-sized object.

The characteristic atomic length will arise below from a balance between quantum localization energy and electromagnetic attraction.

## 3.2 Quantum dynamics and bound states

**K:** A closed quantum state evolves under

\[
i\hbar\frac{\partial}{\partial t}|\psi(t)\rangle
=
\widehat H|\psi(t)\rangle.
\]

Bound structures are associated with normalizable eigenstates or resonances satisfying

\[
\widehat H|\psi_n\rangle=E_n|\psi_n\rangle.
\]

A bound state exists when the interacting Hamiltonian has a state below the relevant dissociation threshold. Persistence therefore depends on the complete interaction law and conserved quantities, not on superposition alone.

## 3.3 Quantum electrodynamics: radiation and charged fields

**K:** Electromagnetic radiation interacts with charged matter through quantum electrodynamics. In rationalized natural units \((\hbar=c=1)\),

\[
\mathcal L_{\mathrm{QED}}
=
-\frac14F_{\mu\nu}F^{\mu\nu}
+
\bar\psi(i\gamma^\mu D_\mu-m)\psi,
\]

with

\[
D_\mu=\partial_\mu+iqA_\mu.
\]

The Dirac field and electromagnetic field can exchange energy, momentum, and charge-compatible excitations. Let \(e_{\mathrm p}\) denote a positron. The Breit-Wheeler process is

\[
\gamma+\gamma\rightarrow e^{-}+e_{\mathrm p}
\]

For incoming photon four-momenta \(k_1^\mu,k_2^\mu\),

\[
s=(k_1+k_2)^2
=2E_1E_2(1-\cos\vartheta)
\ge4m_e^2.
\]

For a head-on collision,

\[
E_1E_2\ge m_e^2.
\]

A single free photon cannot produce a free electron-positron pair in empty vacuum while conserving four-momentum; a second photon, a nucleus, or another participant must absorb recoil. Pair production establishes a lawful conversion between field energy and charged excitations. It still does not produce a proton, a nucleus, or an atom.

## 3.4 Quantum chromodynamics: quarks, gluons, and hadrons

**K:** Ordinary nuclei require protons and neutrons, which are hadrons governed by quantum chromodynamics [24]. In natural units,

\[
\mathcal L_{\mathrm{QCD}}
=
-\frac14G^a_{\mu\nu}G^{a\mu\nu}
+
\sum_f
\bar q_f(i\gamma^\mu D_\mu-m_f)q_f,
\]

where

\[
G^a_{\mu\nu}
=
\partial_\mu A^a_\nu
-
\partial_\nu A^a_\mu
+
g_s f^{abc}A^b_\mu A^c_\nu.
\]

The final term makes the gluon field self-interacting. At low energies, quarks and gluons are confined into color-neutral hadrons. A proton or neutron is represented schematically by a QCD bound-state equation

\[
\widehat H_{\mathrm{QCD}}|h\rangle
=M_hc^2|h\rangle.
\]

There is no simple closed-form proton wavefunction analogous to the nonrelativistic hydrogen orbital. Low-energy QCD is strongly coupled and is treated through lattice calculations, effective field theories, and experiment. Most nucleon mass is dynamical field and binding energy rather than the arithmetic sum of the light quark rest masses [24].

This stage corrects a crucial misconception: atoms do not arise from electron-positron pair production alone. The known physical baseline contains electromagnetic, quark, gluon, weak, and Higgs fields. Photons are the opening example, not the exclusive ancestor.

## 3.5 Nuclear binding: hadrons become nuclei

**K:** Protons and neutrons interact through the residual strong force, with electromagnetic repulsion between protons. A schematic nuclear Hamiltonian is

\[
H_{\mathrm{nuc}}
=
\sum_i\frac{\mathbf p_i^2}{2m_i}
+
\sum_{i<j}V_{ij}^{\mathrm{strong}}
+
V_{\mathrm C}
+
H_{\mathrm{many\mbox{-}body}}.
\]

For a nucleus with \(Z\) protons and \(N\) neutrons, the binding energy is

\[
B(Z,N)
=
\left[Zm_p+Nm_n-M(Z,N)\right]c^2.
\]

A positive binding energy means the nucleus has lower mass-energy than its separated constituents. A common empirical nuclear-radius scale is

\[
R_A\approx r_0A^{1/3},
\qquad
A=Z+N,
\qquad
r_0\approx1.2\ \mathrm{fm}.
\]

Hydrogen begins with the simplest nucleus: one proton. Heavier atomic nuclei add nuclear structure before any electron is bound.

## 3.6 The atomic length emerges from kinetic energy versus attraction

**K:** For a hydrogenic atom, separate center-of-mass motion and use the electron-nucleus reduced mass

\[
\mu=\frac{m_em_N}{m_e+m_N}.
\]

The nonrelativistic relative Hamiltonian is

\[
H_Z
=
-\frac{\hbar^2}{2\mu}\nabla^2
-
\frac{Ze^2}{4\pi\varepsilon_0r}.
\]

The scale of the atom can be seen without solving the full differential equation. Localizing the electron to a radius \(r\) gives a characteristic energy

\[
E(r)
\sim
\frac{\hbar^2}{2\mu r^2}
-
\frac{Ze^2}{4\pi\varepsilon_0r}.
\]

The first term rises as localization becomes tighter; the second favors attraction. Minimizing gives

\[
\frac{dE}{dr}=0
\quad\Longrightarrow\quad
r\sim a_Z,
\]

with

\[
a_Z
=
\frac{4\pi\varepsilon_0\hbar^2}{\mu Ze^2}
=
\frac{\hbar}{\mu cZ\alpha}.
\]

For ordinary hydrogen, \(a_Z\) is essentially the Bohr radius,

\[
a_0\approx5.29\times10^{-11}\ \mathrm m.
\]

The nucleus is of order femtometres while the electron distribution is of order tens of picometres: atomic size is roughly \(10^5\) times the proton charge-radius scale. The atom is not a tiny solar system; \(|\psi(\mathbf r)|^2\) is a probability density for a quantum bound state.

The hydrogenic spectrum is

\[
E_n
=
-\frac{\mu Z^2e^4}
{2(4\pi\varepsilon_0)^2\hbar^2n^2}
=
-\frac{\mu c^2(Z\alpha)^2}{2n^2},
\qquad
n=1,2,\ldots
\]

before fine structure, Lamb shift, hyperfine structure, and finite-nuclear-size corrections. For neutral hydrogen the measured ionization energy is approximately \(13.5984\ \mathrm{eV}\) [25].

## 3.7 Binding requires somewhere for excess energy to go

Two particles approaching under attraction do not automatically remain bound. Energy and momentum must be redistributed. Radiative recombination provides a direct route:

\[
p+e^{-}\rightarrow H+\gamma
\]

More generally, let \(X_q\) denote an ion in charge state \(q\). Then

\[
X_q+e^{-}
\rightarrow
X_{q-1,n}+\gamma
\]

For capture into level \(n\), energy conservation gives schematically

\[
\hbar\omega
=
K_{\mathrm{in}}
+|E_n|
-E_{\mathrm{recoil}}.
\]

Light therefore plays two different roles. It can supply energy to ionize or create excitations, and it can carry away energy when a lower-energy bound state forms. Atomic transitions obey

\[
\hbar\omega_{if}=E_i-E_f.
\]

The discrete spectral lines tabulated by NIST are the empirical signature of this bound-state structure [25].

In thermal equilibrium, ionization balance is approximated by the Saha equation [28]:

\[
\frac{n_en_{q+1}}{n_q}
=
\frac{2g_{q+1}}{g_q}
\left(
\frac{2\pi m_ek_BT}{h^2}
\right)^{3/2}
\exp\left(-\frac{\chi_q}{k_BT}\right).
\]

As a plasma cools, the exponential favors bound atoms. Cosmological recombination is a nonequilibrium expanding-universe problem, so the Saha equation is a baseline rather than the final kinetic description.

## 3.8 Multi-electron atoms and the beginning of chemistry

For \(N\) electrons around a nucleus of charge \(Z\), a nonrelativistic Hamiltonian is

\[
H
=
\sum_{i=1}^N
\left[
-\frac{\hbar^2}{2m_e}\nabla_i^2
-
\frac{Ze^2}{4\pi\varepsilon_0r_i}
\right]
+
\sum_{i<j}
\frac{e^2}{4\pi\varepsilon_0r_{ij}}
+
H_{\mathrm{rel}}+H_{\mathrm{spin}}.
\]

Electrons are fermions, so the many-electron state is antisymmetric:

\[
\Psi(\ldots,x_i,\ldots,x_j,\ldots)
=
-\Psi(\ldots,x_j,\ldots,x_i,\ldots).
\]

Coulomb interaction, antisymmetry, angular momentum, spin, and relativistic corrections generate shell structure and the periodic regularities of chemistry. Molecular binding then uses the full electron-nucleus Hamiltonian, often approximated by a Born-Oppenheimer factorization [27]:

\[
\Psi(\mathbf r,\mathbf R)
\approx
\psi_e(\mathbf r;\mathbf R)\chi_N(\mathbf R).
\]

The transition is therefore:

\[
\boxed{
\begin{aligned}
&\text{phase-bearing field quanta}\\
&\rightarrow\text{charged and colored quantum fields}\\
&\rightarrow\text{hadrons}\\
&\rightarrow\text{nuclei}\\
&\rightarrow\text{radiatively stabilized atoms}\\
&\rightarrow\text{multi-electron shells and chemistry}.
\end{aligned}
}
\]

This is established physics at the level stated. The consciousness-first interpretation enters elsewhere: these stages organize the physical expression of primitive presence; they do not create consciousness ex nihilo.

## 3.9 Current physical baseline

**K:** Taking \(x^0=ct\), a compact effective baseline for presently known nongravitational quantum fields coupled to classical gravitation is

\[
S_{\mathrm{known}}
=
\int d^4x\sqrt{-g}
\left[
\frac{c^3}{16\pi G}(R-2\Lambda)
+
\mathcal L_{\mathrm{SM}}
\right],
\]

where \(\mathcal L_{\mathrm{SM}}\) is the Standard Model Lagrangian and the gravitational term is the Einstein-Hilbert action. Variation of the metric gives

\[
G_{\mu\nu}+\Lambda g_{\mu\nu}
=
\frac{8\pi G}{c^4}T_{\mu\nu}.
\]

For a free relativistic excitation,

\[
E^2=p^2c^2+m^2c^4,
\]

which reduces to \(E=pc\) for a photon.

**H/P:** The physical substrate of organisms includes the full interacting field content of known physics. Consciousness is not assigned to photons alone, nor generated only when atoms or organisms appear. Physical complexity determines the form, boundary, memory, and agency through which primitive consciousness becomes a subject.

# 4. Open systems, decoherence, and persistence

## 4.1 Reduced states

No organism or brain is a perfectly closed quantum system. For a system \(S\) coupled to an environment \(E\), the reduced state is

\[
\rho_S=\operatorname{Tr}_E(\rho_{SE}).
\]

Measurement probabilities are given by the Born rule

\[
p(a)=\operatorname{Tr}(\rho E_a),
\]

where \(E_a\) is a positive operator-valued measurement element.

## 4.2 Markovian open-system dynamics

**K:** Under a standard time-homogeneous Markovian approximation, a completely positive trace-preserving quantum dynamical semigroup has Gorini-Kossakowski-Sudarshan-Lindblad form [4]:

\[
\frac{d\rho}{dt}
=
-\frac{i}{\hbar}[H,\rho]
+
\sum_k
\left(
L_k\rho L_k^\dagger
-
\frac12\{L_k^\dagger L_k,\rho\}
\right).
\]

The commutator describes unitary evolution. The remaining terms describe environmentally induced loss, gain, dephasing, and dissipation.

In a basis selected by the interaction, off-diagonal coherence often decays approximately as

\[
\rho_{ij}(t)
\approx
\rho_{ij}(0)e^{-\Gamma_{ij}t}.
\]

Decoherence helps explain why stable classical records can emerge from quantum dynamics, but it does not select consciousness.

## 4.3 Entropy and nonequilibrium maintenance

The von Neumann entropy is

\[
S(\rho)=-k_B\operatorname{Tr}(\rho\ln\rho).
\]

For a total closed system, unitary evolution preserves this entropy. For a thermodynamically consistent open-system description, entropy can increase or decrease locally through exchange while total entropy production satisfies

\[
\dot S_{\mathrm{prod}}\ge0.
\]

The precise entropy-production functional depends on the reservoirs and approximations used. A living system maintains local organization by exporting entropy and consuming free energy. It is therefore a dissipative process, not an exception to thermodynamics.
