# An entropy obstruction for weight-one Pauli spikes

Low Pauli weight makes learning possible with few reference qubits when each experiment can prepare a fresh probe. It does not make the same experiment possible from a logarithmic initial purity supply. For a hidden weight-one Pauli coefficient attenuated by $`\lambda=1/2`$, we prove a linear entropy requirement that holds for every finite number of queries.

This is a **shared result with [Pauli Learning Memory Thresholds](https://github.com/GoGoKo699/Pauli-Learning-Memory-Thresholds)**. This page owns its complete theorem and proof; the sister's [no-reset frontier](https://github.com/GoGoKo699/Pauli-Learning-Memory-Thresholds/blob/main/science/no_reset_frontier.md) gives the implications for the width convention and learning task. The [pinned sister model](https://github.com/GoGoKo699/Pauli-Learning-Memory-Thresholds/blob/a58e7e563d8688e6e09c29a8ec78b8fbb3378d07/science/model.md) and [pinned no-reset model](https://github.com/GoGoKo699/Quantum-Learning-Without-Resets/blob/690dbd3f98c466d535fa531785ac64217380603d/science/model.md) specify the two original resource contracts. The theorem below uses the complete-processor contract stated here.

## 1. Model and entropy resource

The queried register $`S`$ contains $`n\ge1`$ qubits. Every accessible protected register and every retained record belongs to a finite-dimensional register $`A`$. The initial state $`\rho_{\mathrm{in}}`$ on $`SA`$ is known and independent of the hypothesis. Between ordinary channel calls, the complete processor undergoes arbitrary known unital CPTP maps $`\mathcal C_t`$. There are no resets or free fresh records. An inaccessible purification, environment output, inverse or controlled use of the unknown channel is not supplied. These are the assumptions of [the complete-processor model](model.md#2-the-complete-processor).

Write $`d=2^n`$ and let $`a=(i,\alpha)`$ range over all $`3n`$ weight-one Pauli labels, where $`\alpha\in\{X,Y,Z\}`$. The corresponding Pauli is $`P_a=I\otimes\cdots\otimes\alpha_i\otimes\cdots\otimes I`$. On operators of the complete processor, define

```math
\begin{aligned}
Q_0(X)&=\frac{I_S}{d}\otimes\operatorname{Tr}_S X,\\
Q_a(X)&=\frac{P_a}{d}\otimes
\operatorname{Tr}_S[(P_a\otimes I_A)X],\\
R_a&=Q_0+Q_a,\qquad
E_a=Q_0+\frac12Q_a.
\end{aligned}
\tag{E1}
```

The null query is $`Q_0`$; the alternative is $`E_a`$ for one unknown label fixed throughout the run. Both are ordinary memoryless channels on $`S`$ tensored with the identity on $`A`$. The map $`R_a`$ is also a channel: it retains the binary Pauli eigenspace information and the protected memory. None of these definitions grants the learner the hidden label.

Use base-two von Neumann entropy $`H`$ and base-two quantum relative entropy,

```math
\begin{aligned}
D_2(\rho\Vert\sigma)
&=\operatorname{Tr}\rho(\log_2\rho-\log_2\sigma),\\
C&=\log_2\dim(SA)-H(\rho_{\mathrm{in}}).
\end{aligned}
\tag{E2}
```

The subscript in $`D_2`$ specifies the logarithm base; it does **not** denote a Rényi divergence of order two. The usual support convention assigns infinite relative entropy when the support of the first state is not contained in that of the second.

The entropy deficit $`C`$ is measured in bits. For $`c`$ initially clean qubits and all other qubits maximally mixed, $`C=c`$. With the collision purity $`\mathcal P`$ from (M5),

```math
0\le C\le\log_2\mathcal P.
\tag{E3}
```

Appending independent maximally mixed memory leaves both $`C`$ and $`\mathcal P`$ unchanged. If all protected registers fit in $`k`$ qubits, then $`C\le n+k`$. This last dimension bound charges classical records as well as coherent workspace; it does not apply to a convention that leaves an unlimited classical history outside the processor.

## 2. The all-time entropy theorem

Let $`\rho_T^0`$ and $`\rho_T^a`$ be the complete states after any finite $`T`$ queries, with the same initial state and known controls under every hypothesis. Then

```math
\boxed{
\sum_{a:\,|a|=1}D_2(\rho_T^0\Vert\rho_T^a)
\le\frac34 C.
}
\tag{E4}
```

The direction of relative entropy is part of the statement: the null state is its first argument. The bound allows arbitrary protected memory and arbitrary return of previously acquired signal from that memory. It has no factor depending on $`T`$.

Suppose one final decision accepts the alternative with probabilities $`p_0\le\delta`$ under the null and $`p_a\ge1-\delta`$ under every alternative, where $`0<\delta<1/2`$. Define

```math
j_2(\delta)=(1-2\delta)\log_2\frac{1-\delta}{\delta}.
```

The theorem implies

```math
\boxed{C\ge4n\,j_2(\delta).}
\tag{E5}
```

In particular, error at most $`1/3`$ requires

```math
\boxed{C\ge\frac43n.}
\tag{E6}
```

Therefore $`c=O(\log n)`$ clean qubits cannot attain this error, even with unrestricted additional mixed memory and an arbitrarily large finite query budget. If the entire protected register has at most $`k`$ qubits, (E6) and $`C\le n+k`$ also require

```math
\boxed{k\ge\frac13n.}
\tag{E7}
```

These are necessary conditions. They do not assert an attaining protocol at linear resources, sharp constants, or a complete frontier in $`(k,c,T)`$.

## 3. One query charges reverse relative entropy to a null source

For arbitrary prequery states $`\sigma,\rho`$, set

```math
\sigma'=R_a\sigma,\quad \rho'=R_a\rho,\quad
\omega=Q_0\sigma,\quad\zeta=Q_0\rho.
```

Choose a Pauli unitary on $`S`$ that anticommutes with $`P_a`$. Conjugating $`\sigma'`$ by this unitary gives a state $`\sigma_{\mathrm{flip}}=2\omega-\sigma'`$. It swaps the two positive, possibly noncommuting, $`A`$-valued blocks. The flipped state is positive, has the same $`A`$ marginal, and has the same entropy as $`\sigma'`$. This unitary is a mathematical proof device; it is not an unknown-label operation available to the protocol.

The two output states have decompositions

```math
\omega=\frac{\sigma'+\sigma_{\mathrm{flip}}}{2},
\qquad
E_a\rho=\frac{\rho'+\zeta}{2}.
\tag{E8}
```

Joint convexity of quantum relative entropy gives

```math
D_2(\omega\Vert E_a\rho)
\le\frac12D_2(\sigma'\Vert\rho')
+\frac12D_2(\sigma_{\mathrm{flip}}\Vert\zeta).
\tag{E9}
```

Because $`\omega=I_S/d\otimes\sigma_A`$ and $`\zeta=I_S/d\otimes\rho_A`$, the conditional-expectation identity is

```math
D_2(\sigma_{\mathrm{flip}}\Vert\zeta)
=D_2(\sigma'\Vert\omega)+D_2(\omega\Vert\zeta).
\tag{E10}
```

One can check (E10) directly by expanding the logarithms: the first term is the entropy deficit of $`\sigma'`$ relative to $`I_S/d\otimes\sigma_A`$; the second is $`D_2(\sigma_A\Vert\rho_A)`$. The sign flip preserves the first entropy and the memory marginal. Data processing bounds both $`D_2(\sigma'\Vert\rho')`$ and $`D_2(\omega\Vert\zeta)`$ by $`D_2(\sigma\Vert\rho)`$. Thus

```math
\boxed{
D_2(Q_0\sigma\Vert E_a\rho)
\le D_2(\sigma\Vert\rho)
+\frac12D_2(R_a\sigma\Vert Q_0\sigma).
}
\tag{E11}
```

This inequality compares different alternative and null prequery states. It therefore includes feedback through protected memory; it does not assume those states remain equal. Finite input divergence ensures the needed support inclusions by data processing. The formulas also follow from full-rank regularization and continuity on the relevant supports. Starting from identical initial states, (E11) keeps every divergence used below finite.

## 4. Complementary axes share one local entropy budget

Fix one null prequery state $`\sigma`$. For site $`i`$, write

```math
\begin{aligned}
\tau_i&=\sigma_{S_iA},\qquad
\omega_i=\frac{I_i}{2}\otimes\sigma_A,\\
g_i&=D_2(\tau_i\Vert\omega_i)=1-H(S_i|A)_\sigma,\\
d_{i,\alpha}&=D_2(\Delta_\alpha\tau_i\Vert\omega_i).
\end{aligned}
\tag{E12}
```

Here $`\Delta_\alpha`$ is dephasing of qubit $`i`$ in Pauli basis $`\alpha`$, with $`A`$ untouched. Depolarizing all other query qubits shows that the source term in (E11) for $`a=(i,\alpha)`$ is exactly $`d_{i,\alpha}`$.

For different axes $`\alpha,\beta`$, the composition $`\Delta_\beta\Delta_\alpha`$ depolarizes qubit $`i`$. The pinching identity and data processing give

```math
\begin{aligned}
g_i-d_{i,\alpha}
&=D_2(\tau_i\Vert\Delta_\alpha\tau_i)\\
&\ge D_2(\Delta_\beta\tau_i\Vert\omega_i)
=d_{i,\beta}.
\end{aligned}
\tag{E13}
```

Sum the three pairwise inequalities. Each $`d_{i,\alpha}`$ appears twice, so

```math
\sum_{\alpha\in\{X,Y,Z\}}d_{i,\alpha}\le\frac32g_i.
\tag{E14}
```

This is the complementary-basis entropy inequality with quantum side information, derived directly here. The memory blocks need not commute. Strong subadditivity implies conditional subadditivity, $`\sum_i H(S_i|A)\ge H(S|A)`$. Consequently

```math
\begin{aligned}
\sum_{a:\,|a|=1}D_2(R_a\sigma\Vert Q_0\sigma)
&\le\frac32\sum_i g_i\\
&\le\frac32[n-H(S|A)_\sigma]\\
&=\frac32[H(Q_0\sigma)-H(\sigma)].
\end{aligned}
\tag{E15}
```

Thus all $`3n`$ local directions are charged to the entropy created by one null query.

## 5. Telescope along the common null trajectory

Let $`\sigma_t=\mathcal C_t(\rho_{t-1}^0)`$. Apply (E11) with null input $`\sigma_t`$ and alternative input $`\mathcal C_t(\rho_{t-1}^a)`$. Data processing through the known control and identical initial states give

```math
D_2(\rho_T^0\Vert\rho_T^a)
\le\frac12\sum_{t=1}^T
D_2(R_a\sigma_t\Vert Q_0\sigma_t).
\tag{E16}
```

Sum over all weight-one labels and use (E15):

```math
\sum_{a:\,|a|=1}D_2(\rho_T^0\Vert\rho_T^a)
\le\frac34\sum_{t=1}^T
[H(\rho_t^0)-H(\sigma_t)].
\tag{E17}
```

A unital control cannot decrease von Neumann entropy. Therefore the entropy gains at null queries satisfy

```math
\begin{aligned}
\sum_{t=1}^T[H(\rho_t^0)-H(\sigma_t)]
&\le H(\rho_T^0)-H(\rho_{\mathrm{in}})\\
&\le\log_2\dim(SA)-H(\rho_{\mathrm{in}})=C.
\end{aligned}
\tag{E18}
```

Equations (E17)–(E18) prove (E4). Protected memory may preserve state components indefinitely; the proof only charges their cumulative exposure to the noisy query sectors. It makes no assertion of strict contraction on every traceless processor operator.

## 6. Decision error and trace-distance consequences

Measurement data processing and $`p_0\le\delta<1-\delta\le p_a`$ imply

```math
\begin{aligned}
D_2(\rho_T^0\Vert\rho_T^a)
&\ge d_2(p_0\Vert p_a)\\
&\ge d_2(\delta\Vert1-\delta)
=j_2(\delta),
\end{aligned}
\tag{E19}
```

where $`d_2`$ is binary relative entropy in bits. Sum (E19) over the $`3n`$ alternatives and combine with (E4) to obtain (E5). At $`\delta=1/3`$, $`j_2(1/3)=1/3`$, giving (E6)–(E7).

For the uniform final alternative mixture $`\bar\rho_T=(3n)^{-1}\sum_a\rho_T^a`$, convexity in the second relative-entropy argument and Pinsker's inequality yield

```math
\begin{aligned}
D_2(\rho_T^0\Vert\bar\rho_T)&\le\frac{C}{4n},\\
D_{\mathrm{tr}}(\bar\rho_T,\rho_T^0)
&\le\min\left\{1,\sqrt{\frac{C\ln2}{8n}}\right\}.
\end{aligned}
\tag{E20}
```

Here $`D_{\mathrm{tr}}`$ is half the trace norm, as throughout this repository. Averaging the individual Pinsker inequalities and applying Cauchy–Schwarz gives the same upper bound on $`(3n)^{-1}\sum_a D_{\mathrm{tr}}(\rho_T^a,\rho_T^0)`$. Equation (E4) therefore also applies when the terminal measurement may depend on a later-revealed label. For the stated worst-case error, the exact binary-relative-entropy inequality (E19) gives the sharper constant in (E6).

## 7. What the existing collision bound already implies

The [common-decision proof](decision_bound.md) restricts immediately to any set of $`m`$ nonidentity Pauli labels: the forward and backward sums become inequalities rather than equalities. For the present $`m=3n`$ and $`\lambda=1/2`$, its inherited corollary is

```math
D_{\mathrm{tr}}(\bar\rho_T,\rho_T^0)
\le\min\left\{1,\frac{\sqrt{\mathcal P-1}}{6n}\right\}.
\tag{E21}
```

For a clean/mixed product initialization, error at most $`1/3`$ therefore already requires $`c\ge\log_2(1+4n^2)`$. This logarithmic necessity is not the entropy theorem. Equations (E4)–(E6) replace it by a linear requirement in the regime where collision purity alone allows a polynomial value of $`\mathcal P`$. For small fixed purity, the collision bound can remain numerically stronger; both bounds may be used. No tight arbitrary-purity characterization follows from either converse.

The learning consequences follow by reduction. Suppose an acquisition procedure, independent of the requested label, later estimates any requested weight-one coefficient with additive error strictly below $`1/4`$ and success at least $`2/3`$ under both the null and every promised alternative. When the request is $`a`$, thresholding its estimate at $`1/4`$ distinguishes the null from alternative $`a`$. Equation (E19) applies separately to these possibly different final effects, so the same $`C\ge4n/3`$ requirement holds even for per-target confidence. If the estimates are simultaneously accurate, their maximum additionally yields one common detector for the unknown-label promise. This is a transfer of the entropy converse, not a new tomography theorem. The sister account states its exact learning and width conventions.

## 8. Attribution and limits

Joint convexity, data processing, pinching identities and strong subadditivity are standard quantum-information tools; see [Watrous, Chapter 5](https://cs.uwaterloo.ca/~watrous/TQI/TQI.5.pdf). Entropic uncertainty with quantum memory has established antecedents, including [Berta et al.](https://arxiv.org/abs/0909.0950). Equation (E13) supplies the special Pauli version needed here without importing a stronger general uncertainty theorem. The shared contribution is the query coupling (E11), its combination with the finite null entropy budget, and the resulting attenuated-spike obstruction. Broader purity-loss and noisy-oracle antecedents retain their [separate attribution](../references/RELATED_WORK.md).

The result is specifically proved for weight one and $`\lambda=1/2`$. It establishes necessary initial-entropy and fully charged width conditions, not a matching linear-resource protocol, sharp constants, a full $`(k,c,T)`$ frontier, or a theorem for $`\lambda>1/2`$. Independent finite checks in [verification](../verification/README.md) test the coupling, complementarity charge and complete small trajectories; the all-time statement is analytical.

Fresh preparation, nonunital reset and free external records change the resource contract. The [partial-Bell protocol in the pinned sister account](https://github.com/GoGoKo699/Pauli-Learning-Memory-Thresholds/blob/a58e7e563d8688e6e09c29a8ec78b8fbb3378d07/science/partial_bell.md) uses independently prepared experiments and stored outcomes. Its [identity-mixture parameter](https://github.com/GoGoKo699/Pauli-Learning-Memory-Thresholds/blob/a58e7e563d8688e6e09c29a8ec78b8fbb3378d07/science/weak_noise.md) is also different from this attenuation parameter: an identity mixture with an exactly preserved spike still preserves that spike. Setting its mixture strength to $`1/2`$ does not create the present $`\lambda=1/2`$ channel. The theorem therefore does not contradict those protocols or the [exact-conservation scan](protocols.md#5-specified-worst-case-error-near-conservation).
