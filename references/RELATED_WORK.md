# Related work and attribution

The contribution studied here is a limit on the information obtainable from a fixed supply of initialized purity in a known Pauli-channel detection task. Memory size, query count, measurement count, and the ability to reprepare registers are distinct resources. The [model](../science/model.md) includes every accessible register in one processor and allows arbitrary global unital controls between ordinary channel calls.

For $M=4^n-1$ hidden nonidentity Pauli modes and initial collision purity $\mathcal P=D\mathrm{Tr}(\rho_{\mathrm{in}}^2)$, the [common-decision theorem](../science/decision_bound.md) proves, for every query count $T$ and $0\le\lambda<1$,

```math
D_{\mathrm{tr}}\!\left(\frac1M\sum_a\rho_T^a,\rho_T^0\right)
\le
\min\!\left\{1,
\frac{\lambda\sqrt{\mathcal P-1}}{2M(1-\lambda)}
\right\}.
```

Here $D_{\mathrm{tr}}=\tfrac12\lVert\cdot\rVert_1$. This bounds the distance of the **uniform mixture of final states** from the null. It concerns one measurement common to every hidden label. The average of the individually optimized distances, $M^{-1}\sum_aD_{\mathrm{tr}}(\rho_T^a,\rho_T^0)$, satisfies a [separate bound](../science/purity_bound.md) and is not interchangeable with this quantity.

The [finite protocols](../science/protocols.md), with known $\lambda$ and one initially pure qubit, establish the matching scaling

```math
\Delta_1(n,\lambda)
=\Theta\!\left(
\min\!\left\{1,\frac{\lambda}{M(1-\lambda)}\right\}
\right),
\qquad 0<\lambda<1,
```

where $\Delta_1$ is the supremum of this mixture distinguishability over finite query budgets and finite maximally mixed workspaces. At the endpoints, $\Delta_1(n,0)=0$ and $\Delta_1(n,1)=1$. This is an attainable-distinguishability characterization; it does not determine the optimal query count or the optimum for arbitrary $\mathcal P$.

## Chen and Gong

**Sitan Chen and Weiyuan Gong, [*Efficient Pauli Channel Estimation with Logarithmic Quantum Memory*](https://doi.org/10.1103/PRXQuantum.6.020323), PRX Quantum 6, 020323 (2025).** The precise locations below refer to [arXiv:2309.14326v5](https://arxiv.org/html/2309.14326v5).

Problem 3 and Section 4 give the depolarizing-versus-uniform-Pauli-spike task at $\lambda=1$; Section 5.1 treats smaller positive components. This work supplies the task, spike family, serial testing of candidate Paulis, and concatenation setting used here.

Their controls explicitly permit reinitialization. Algorithm 1, step 7, Eq. (11), replaces the working register by $(I+P_t)/d$. Step 10 applies

```math
X\longmapsto
\left[\frac{I+P_{t+1}}d\otimes|0\rangle\langle0|\right]
\mathrm{Tr}X
```

to the working register and first ancilla. Algorithm 3, Eqs. (21)–(22), similarly reprepares clean auxiliaries. These are nonunital channels. Consequently, small memory and a small number of measurements in their model do not imply a bounded total purity supply. The present converse adds that resource constraint and therefore does not contradict their upper bounds.

## Weak driving, resets and interaction-free discrimination

**Yuan-Zhuo Wang, Yi-Ran Xiao, Ming-Yang Li, Shengjun Wu, and Zeng-Bing Chen, [*Weakly-Driven Quantum Walks for Memory-Constrained Pauli Channel Learning*](https://arxiv.org/html/2509.07702v1), arXiv:2509.07702 (2025).** Section II explicitly grants deterministic qubit reset and independently prepared query inputs. Section III.2 describes serial overwriting, resetting, and entropy export to an external bath. This is a direct comparison for the distinction between measurement count and purity supply. Weak pointer driving and accumulation of a small signal are established ingredients. The present constructions use a charged initial pointer and unital dephasing, without repeated pure-state replacement.

**Markus Hasenöhrl and Michael M. Wolf, [*“Interaction-Free” Channel Discrimination*](https://doi.org/10.1007/s00023-022-01175-z), Annales Henri Poincaré 23, 3331–3390 (2022).** Their [open manuscript](https://arxiv.org/pdf/2010.00623), including Theorem 5.7, develops channel discrimination using Zeno mechanisms and at most one ancillary qubit, with error-versus-interaction tradeoffs. The general mechanism behind a rotation that is suppressed by repeated channel action is prior art. Here it is implemented through the Pauli-to-pointer dephasing gadget and analyzed across an unknown family of $M$ modes under one initialized purity budget. Interaction probability and total initialized collision purity are different resource measures.

## Noisy oracles and purity loss

**Simon Buchholz, Jonas M. Kübler, and Bernhard Schölkopf, [*Multi-Armed Bandits and Quantum Channel Oracles*](https://quantum-journal.org/papers/q-2025-03-25-1672/), Quantum 9, 1672 (2025).** Section 3.1 and Appendix D of [arXiv:2301.08544v4](https://arxiv.org/html/2301.08544v4) supply a close proof antecedent. Equation (34) bounds fidelity progress by a query-exposure factor times the square root of purity loss. Summing gives a query lower bound of order $N(1-p)/p$ at constant error, where $p$ is the oracle's firing probability. Thus charging discrimination progress to purity loss is an established idea. Their unitary null permits persistent query exposure. Our depolarizing null instead supplies finite forward and backward Hilbert–Schmidt budgets across hidden sectors, yielding a bound uniform in $T$.

**Oded Regev and Liron Schiff, [*Impossibility of a Quantum Speed-up with a Faulty Oracle*](https://cims.nyu.edu/~regev/papers/faultygrover.pdf), ICALP 2008.** Their faulty-search oracle applies the intended unitary with probability $1-p$ and does nothing with probability $p$. Theorem 1 gives $T>pN/[10(1-p)]$. This bounds queries with an identity null oracle; it does not assert finite-purity saturation as the query budget grows. Their $p$ is a failure probability, opposite to the firing-probability convention above.

The feedback decomposition and geometric-series estimate used in the common-decision proof are standard linear algebra. The result here comes from combining those estimates with the two finite hidden-sector budgets and a single terminal effect. It should not be read as a new general principle that noise or purity loss limits quantum computation.

## Unital processing and protected memory

**Omar Fawzi, Aadil Oufkir, and Daniel Stilck França, [*Lower Bounds on Learning Pauli Channels with Individual Measurements*](https://doi.org/10.1109/TIT.2025.3527902), IEEE Transactions on Information Theory 71(4) (2025).** Theorem 3.2 and Lemma 3.6 of the [open manuscript](https://arxiv.org/pdf/2301.09192) treat Pauli-channel learning with ancilla-free individual measurements, permitting arbitrarily many within-round queries interspersed with unital operations. Their contraction argument is relevant prior art. With protected memory, however, the lifted depolarizing null preserves every operator $I/d\otimes X_A$; it is not strictly contractive on the full traceless processor space. The present bounds handle this surviving memory through the initialized purity of the complete processor and remain uniform in the memory dimension. Their diamond-norm tomography task also differs from the binary spike decision considered here.

## Operator norm foundations

**David Pérez-García, Michael M. Wolf, Dénes Petz, and Mary Beth Ruskai, [*Contractivity of positive and trace preserving maps under Lₚ norms*](https://doi.org/10.1063/1.2218675), Journal of Mathematical Physics 47, 083506 (2006).** Theorem II.4 in the [primary manuscript](https://arxiv.org/pdf/math-ph/0601063) gives the unital Schatten-norm contractivity used in both energy estimates. A unital CPTP map and its adjoint are Hilbert–Schmidt contractions. This does not hold for arbitrary nonunital CPTP maps. Theorems II.2–II.3 also give the standard interpolation/Russo–Dye route to $\lVert\mathcal C\rVert_{2\to2}^2\le\lVert\mathcal C(I)\rVert_\infty$ for a CPTP map. These norm facts are established foundations, not new results of this work.

**Yu Luo and Yongming Li, [*Robustness of purity: an operational approach to resource theory of purity*](https://doi.org/10.1140/epjd/e2019-90693-y), European Physical Journal D 73, 89 (2019).** The publisher's abstract connects purity robustness to optimal advantage in mixed-unitary discrimination games. Operational discrimination value for purity is therefore prior work. Only the abstract and bibliographic material were accessible for this comparison; no theorem-level comparison with its full text is asserted. The concrete resource used here is dimension-normalized collision purity in a fixed sequential experiment.

## Shared weight-one entropy obstruction

[Pauli Learning Memory Thresholds](https://github.com/GoGoKo699/Pauli-Learning-Memory-Thresholds), [pinned model at revision a58e7e5](https://github.com/GoGoKo699/Pauli-Learning-Memory-Thresholds/blob/a58e7e563d8688e6e09c29a8ec78b8fbb3378d07/science/model.md), evaluates the support–memory frontier when experiments may prepare fresh probes and retain their outcomes. Its low-weight upper protocol is not a no-reset construction. Its weak identity-mixture parameter is also distinct from an attenuated spike eigenvalue: mixing the identity with an exactly preserving spike leaves the hidden mode exactly preserved.

The [weight-one entropy theorem](../science/entropy_bound.md) is a shared contribution of the two projects, with its complete proof owned by this repository and its width/learning consequences in the sister's [no-reset frontier](https://github.com/GoGoKo699/Pauli-Learning-Memory-Thresholds/blob/main/science/no_reset_frontier.md). For $`\lambda=1/2`$, it proves

```math
\sum_{a:\,|a|=1}D_2(\rho_T^0\Vert\rho_T^a)\le\frac34C,
```

where $`D_2`$ is quantum relative entropy in bits and $`C`$ is the initial von Neumann entropy deficit. Error at most $`1/3`$ requires $`C\ge4n/3`$. If all side registers and retained records occupy $`k`$ qubits, then $`C\le n+k`$ and $`k\ge n/3`$ is necessary. A matching linear-resource protocol, sharp constants and the full joint frontier are not claimed.

The [restricted-label collision-purity estimate](../science/decision_bound.md#7-restricted-labels-the-immediate-purity-corollary) is an immediate consequence of the pre-existing energy argument, also visible at [revision 690dbd3](https://github.com/GoGoKo699/Quantum-Learning-Without-Resets/blob/690dbd3f98c466d535fa531785ac64217380603d/science/decision_bound.md). It gives $`c\ge\log_2(1+4n^2)`$ at the same error. That logarithmic necessity is credited as inherited; it is not the new entropy obstruction.

The proof uses established joint convexity, data processing, pinching identities and strong subadditivity, as developed in [Watrous, Chapter 5](https://cs.uwaterloo.ca/~watrous/TQI/TQI.5.pdf). **Mario Berta, Matthias Christandl, Roger Colbeck, Joseph M. Renes and Renato Renner, [*The uncertainty principle in the presence of quantum memory*](https://doi.org/10.1038/nphys1734), Nature Physics 6, 659–662 (2010), [arXiv:0909.0950](https://arxiv.org/abs/0909.0950)** is a primary antecedent for complementary-basis entropy bounds with quantum memory. The particular Pauli inequality needed here is derived directly by pinching and data processing. These entropy foundations are not new claims. The query-specific contribution is the reverse-relative-entropy increment, its charge to the shared null trajectory, and the resulting no-reset obstruction.

This strengthens the present restricted promise rather than characterizing every initial spectrum. The comparison does not assert that this is a new general entropy-loss principle or an optimal theorem for all strengths and weights.

## Educational anchor: Watrous

**John Watrous, *The Theory of Quantum Information*, Cambridge University Press (2018)** is the educational anchor for this project. The [author's book page](https://cs.uwaterloo.ca/~watrous/TQI/) provides the [complete manuscript](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf), individual chapters and [errata](https://cs.uwaterloo.ca/~watrous/TQI/TQI.errata.pdf). The locators below were checked against the author's **standard-layout chapter PDFs** and use their printed page numbers.

| Project ingredient | Verified Watrous locator | Application here |
|---|---|---|
| Operator-space geometry | [Chapter 1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf), §1.1.2, Eq. (1.112), pp. 21–22; Eqs. (1.127)–(1.134), pp. 23–24 | Adjoint maps and the operator-vector correspondence used by the [decision proof](../science/decision_bound.md). |
| Partial trace | Chapter 1, §1.1.2, Eqs. (1.120)–(1.121), p. 22 | The protected-workspace projection $Q_0$ in [the sector decomposition](../science/purity_bound.md). |
| Operator norms | Chapter 1, §1.1.3, Eqs. (1.165)–(1.181), pp. 32–34 | Trace norm, Frobenius norm and the conversion from squared signal energy to distinguishability. |
| Physical channels | [Chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf), §2.2.1, Definition 2.13, p. 73; §2.2.2, Theorem 2.22, p. 82, and Corollary 2.27, p. 89 | Complete positivity and normalized Kraus representations for [the oracle and controls](../science/model.md). Theorem 2.22 alone characterizes complete positivity; Corollary 2.27 includes trace preservation. |
| Adjoint controls | Chapter 2, Proposition 2.18 and its following remark, p. 76; Theorem 2.26, p. 87 | A unital CPTP control has a unital CPTP adjoint, as required by the backward budget. |
| Final binary decision | [Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf), §3.1, Theorem 3.4, pp. 128–129 | The Holevo–Helstrom relation between a common final effect, trace distance and success probability. |
| Channel perturbations | Chapter 3, §3.3.2, Definition 3.43, p. 170; Theorem 3.46, p. 173; Proposition 3.48(2), p. 174 | The diamond norm and the composition estimate underlying the [protocol's hybrid error bound](../science/protocols.md). |
| Entropy and relative entropy | [Chapter 5](https://cs.uwaterloo.ca/~watrous/TQI/TQI.5.pdf), especially the joint-convexity, data-processing and strong-subadditivity results | Foundations for the [shared entropy obstruction](../science/entropy_bound.md); its particular Pauli complementarity step is proved directly. |
| Hilbert–Schmidt contraction | [Chapter 4](https://cs.uwaterloo.ca/~watrous/TQI/TQI.4.pdf), §4.2.2, Theorem 4.27, p. 231; natural representation in Chapter 2, Eqs. (2.60)–(2.63), p. 77 | The operator norm of $K(\Phi)$ is the induced Hilbert–Schmidt norm of $\Phi$. A positive trace-preserving endomorphism is unital exactly when this norm is one. |

Watrous calls $\lVert X\rVert_2$ the **Frobenius norm**, which is the Hilbert–Schmidt norm used here. On p. 34 he uses the full $\lVert\rho-\sigma\rVert_1$ as trace distance; this repository uses $D_{\mathrm{tr}}=\tfrac12\lVert\rho-\sigma\rVert_1$. Thus equal-prior success is $(1+D_{\mathrm{tr}})/2$. The prior denoted $\lambda$ in his Theorem 3.4 is a different parameter from this project's spike strength.

The book supplies these prerequisites. The hidden-sector budgets, their combination in the feedback argument, and the finite Pauli-pointer constructions are developed in this repository's science files. The [source-to-project bridge](../learning/WATROUS_BRIDGE.md) and [milestone map](../learning/MILESTONES.md) organize that connection.

## Scope of the contribution

The task family, serial testing, weak driving, Zeno discrimination, and the use of purity loss in noisy-oracle bounds all have precedents above. The full-family result established here is the uniform-query bound with arbitrary protected workspace, together with the matching one-clean-qubit decision-bias crossover under explicitly charged preparation and ordinary channel access. It characterizes one initialized experiment. Repeating experiments with freshly initialized pointers supplies additional purity and lies outside that fixed-budget experiment.

The shared weight-one result additionally replaces the restricted-label collision resource by a von Neumann entropy budget at $`\lambda=1/2`$. Its necessary conditions and model transfer are stated separately above.

Machine-readable citations for the sources discussed here are in [references.bib](references.bib).
