# Related work and attribution

The contribution studied here is a limit on the information obtainable from a fixed supply of initialized purity in a known Pauli-channel detection task. Memory size, query count, measurement count, and the ability to reprepare registers are distinct resources. The [model](../science/model.md) includes every accessible register in one processor and allows arbitrary global unital controls between ordinary channel calls.

For $M=4^n-1$ hidden nonidentity Pauli modes and initial collision purity $\mathcal P=D\operatorname{Tr}(\rho_{\mathrm{in}}^2)$, the [common-decision theorem](../science/decision_bound.md) proves, for every query count $T$ and $0\le\lambda<1$,

```math
D_{\mathrm{tr}}\!\left(\frac1M\sum_a\rho_T^a,\rho_T^0\right)
\le
\min\!\left\{1,
\frac{\lambda\sqrt{\mathcal P-1}}{2M(1-\lambda)}
\right\}.
```

Here $D_{\mathrm{tr}}=\tfrac12\|\cdot\|_1$. This bounds the distance of the **uniform mixture of final states** from the null. It concerns one measurement common to every hidden label. The average of the individually optimized distances, $M^{-1}\sum_aD_{\mathrm{tr}}(\rho_T^a,\rho_T^0)$, satisfies a [separate bound](../science/purity_bound.md) and is not interchangeable with this quantity.

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
\operatorname{Tr}X
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

**David Pérez-García, Michael M. Wolf, Dénes Petz, and Mary Beth Ruskai, [*Contractivity of positive and trace preserving maps under $L_p$ norms*](https://doi.org/10.1063/1.2218675), Journal of Mathematical Physics 47, 083506 (2006).** Theorem II.4 in the [primary manuscript](https://arxiv.org/pdf/math-ph/0601063) gives the unital Schatten-norm contractivity used in both energy estimates. A unital CPTP map and its adjoint are Hilbert–Schmidt contractions. This does not hold for arbitrary nonunital CPTP maps. Theorems II.2–II.3 also give the standard interpolation/Russo–Dye route to $\|\mathcal C\|_{2\to2}^2\le\|\mathcal C(I)\|_\infty$ for a CPTP map. These norm facts are established foundations, not new results of this work.

**Yu Luo and Yongming Li, [*Robustness of purity: an operational approach to resource theory of purity*](https://doi.org/10.1140/epjd/e2019-90693-y), European Physical Journal D 73, 89 (2019).** The publisher's abstract connects purity robustness to optimal advantage in mixed-unitary discrimination games. Operational discrimination value for purity is therefore prior work. Only the abstract and bibliographic material were accessible for this comparison; no theorem-level comparison with its full text is asserted. The concrete resource used here is dimension-normalized collision purity in a fixed sequential experiment.

## Three educational anchors

These three references support the channel model and proof prerequisites. **Watrous is the recommended starting point** because it directly covers all the required operator-space and decision-theoretic ingredients.

### 1. Watrous — recommended

**John Watrous, *The Theory of Quantum Information*, Cambridge University Press (2018).** [Author's book page](https://cs.uwaterloo.ca/~watrous/TQI/) and [free prepublication PDF](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf).

Section 1.1.3 develops Schatten norms. Sections 2.2.1–2.2.2 and Theorem 2.22 cover channel representations. Theorem 2.26 relates trace preservation to unitality of the adjoint. Theorem 3.4 is the Holevo–Helstrom discrimination theorem. Section 4.2.2, Theorem 4.27 (printed p. 231), gives the induced Hilbert–Schmidt contraction characterization through the natural matrix representation. These locations provide a short path from complete-processor channels to both directions of the energy proof.

### 2. Nielsen and Chuang

**Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition, Cambridge University Press (2010).** The [official frontmatter and detailed contents](https://assets.cambridge.org/97811070/02173/frontmatter/9781107002173_frontmatter.pdf) are freely accessible; the full chapters may require purchased or institutional access.

Sections 8.2.2–8.2.4 introduce environments, operator-sum representations, and axiomatic quantum operations. Section 8.3.1 covers partial trace; Sections 8.3.3–8.3.4 cover phase-flip and depolarizing channels. Section 9.2.1 introduces trace distance. These section locations were checked against the publisher's contents. For the precise Hilbert–Schmidt contraction theorem, use Watrous or Pérez-García et al.

### 3. Wilde

**Mark M. Wilde, *Quantum Information Theory*, second edition, Cambridge University Press (2017).** [Publisher record](https://doi.org/10.1017/9781316809976), [author's open draft](https://www.markwilde.com/qit-notes.pdf), and [arXiv book record](https://arxiv.org/abs/1106.1445).

The following locations refer to the author draft titled *From Classical to Quantum Shannon Theory*, dated December 5, 2021: Sections 4.6.1–4.6.2 cover preparation and discarding, Section 4.6.6 covers measurement channels, and Section 5.3 treats coherent instruments. Sections 9.1.3–9.1.5 develop probability differences, discrimination, and monotonicity. Definition 9.1.2 uses the full trace norm as “trace distance”; translate to the factor-$1/2$ convention used here.

## Scope of the contribution

The task family, serial testing, weak driving, Zeno discrimination, and the use of purity loss in noisy-oracle bounds all have precedents above. The specific result established here is the uniform-query bound with arbitrary protected workspace, together with the matching one-clean-qubit decision-bias crossover under explicitly charged preparation and ordinary channel access. It characterizes one initialized experiment. Repeating experiments with freshly initialized pointers supplies additional purity and lies outside that fixed-budget experiment.

Machine-readable citations for the sources discussed here are in [references.bib](references.bib).
