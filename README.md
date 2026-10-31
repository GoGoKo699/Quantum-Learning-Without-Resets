# Quantum Learning Without Resets

**How much can a quantum processor learn from one supply of initial purity, even if it can query an unknown channel indefinitely?** For a hidden Pauli mode, one initially pure qubit has an exact attainable-signal scale, up to universal constants. Arbitrarily large protected mixed memory cannot remove this restriction.

The channel is either complete depolarization or retains one unknown nonidentity Pauli component with known strength $\lambda$. The hidden component is fixed throughout the experiment. Between ordinary channel calls, the processor may use any known global unital quantum channel. Every accessible register belongs to the initial resource budget, and there is one final measurement.

## Main result

Let $n\ge1$ be the number of query qubits and $M=4^n-1$ the number of possible hidden modes. Start with one pure qubit and any finite number of maximally mixed qubits. Let $\Delta_1(n,\lambda)$ be the supremum, over all finite query budgets, of the trace distance between the final null state and the uniform mixture of alternative final states.

For $0\le\lambda\lt1$,

```math
\boxed{
\frac1{128}\min\!\left\{1,\frac{\lambda}{M(1-\lambda)}\right\}
\le \Delta_1(n,\lambda)
\le
\min\!\left\{1,\frac{\lambda}{2M(1-\lambda)}\right\}.
}
```

At $\lambda=0$ the value is zero. At $\lambda=1$ the supremum is one; no finite exact-discrimination claim is needed. The [finite algorithms](science/protocols.md) achieve the lower scaling using the same final pointer measurement for every hidden label.

Trace distance here means half the trace norm. Equal-prior success is $(1+\Delta_1)/2$, so the advantage above one half is $\Delta_1/2$. A small constant signal and a specified error such as $0.1$ are separate guarantees.

| Regime or resource | Established consequence |
|---|---|
| Fixed $0\lt\lambda\lt1$, one clean qubit | Optimal signal is of order $4^{-n}$, uniformly over the number of calls. |
| One clean qubit near conservation | Nonvanishing signal becomes possible at $1-\lambda$ of order $1/M$. A sufficiently small constant at this scale permits a specified fixed error. |
| Arbitrarily large mixed protected memory | Both converse bounds remain unchanged. |
| General initial collision purity $\mathcal P$ | Common-decision distance is at most $\lambda\sqrt{\mathcal P-1}/[2M(1-\lambda)]$, capped at one. Tightness for arbitrary purity is not established. |
| Finite query count $T$ | Replace $(1-\lambda)^{-1}$ by $\sum_{j=0}^{T-1}\lambda^j$ in the common-decision bound. |

The result identifies an information limit that persists as the query budget grows. A one-bit answer could fit in the pure pointer; the obstruction comes from finding an unknown direction among many Pauli sectors with a finite initial resource.

## Proof and algorithm

The proof follows two Hilbert–Schmidt energy budgets along the depolarizing null: the state propagated forward and one common measurement effect propagated backward. Their total exposure to the queried Pauli sectors is finite. A finite feedback expansion combines these budgets and yields the bound for every query count.

The algorithm surrounds each ordinary query with a controlled **known** Pauli gate and its inverse. This exactly converts the trial mode into a dephasing channel on a pointer, while returning the query register to its mixed state. A finite sequence of weak rotations and dephasings then reaches the predicted signal scale. The construction uses one query for $\lambda\le1/2$ and at most

```math
33M\min\{(1-\lambda)^{-1},M\}
```

queries for $\lambda>1/2$, with $O(n)$ known gates per query. These are sufficient costs, not optimal query bounds. A separate finite scan supplies an explicit worst-case error certificate near $\lambda=1$.

## Read the science

Start with the [scientific reading route](science/README.md) and the [model](science/model.md). The complete arguments are organized by question:

| Question | Authoritative account |
|---|---|
| What channel, purity budget, controls and error convention are assumed? | [Model and resources](science/model.md) |
| How does null-trajectory purity loss bound label-wise output distances? | [Purity-potential theorem](science/purity_bound.md) |
| Why does one final decision admit a complementary bound? | [Common-decision theorem](science/decision_bound.md) |
| Which finite algorithms match the one-clean-qubit signal law? | [Protocols and resource accounting](science/protocols.md) |
| Why do mixed memory and more query time fail to replace purity? | [Interpretation and limits](science/interpretation.md) |
| What is inherited from prior channel-learning and noisy-oracle work? | [Related work](references/RELATED_WORK.md) and [bibliography](references/references.bib) |
| What do the independent finite calculations check? | [Verification](verification/README.md) |

The [LLM reading guide](llms.txt) maps scientific questions to the same authoritative files.

## Learn the project

The single educational anchor is **John Watrous, *The Theory of Quantum Information* (2018)**, using the [author's available manuscript](https://cs.uwaterloo.ca/~watrous/TQI/). The [Watrous bridge](learning/WATROUS_BRIDGE.md) identifies the relevant sections, translates the notation and explains the additional steps needed for the purity bounds and finite protocols.

The [30-milestone map](learning/MILESTONES.md) gives a common route through the project: **10 background/preliminaries milestones** build the complete-processor and decision framework, and **20 narrative/innovation milestones** connect the two converse arguments, finite protocols and resource consequences. Each milestone specifies a central question, an understanding target, earlier dependencies, a conceptual connection and source pointers. Use the map alongside the bridge for self-directed study.

## Reproduce the checks

Use Python 3.12 and the pinned NumPy dependency:

```bash
python -m pip install -r verification/requirements.txt
python verification/run_checks.py
```

The deterministic suite reconstructs full channel circuits, checks the forward and backward feedback identities, compares scalar scan formulas with matrix powers, and exercises endpoint and resource conventions. It writes [results.json](verification/results.json). Finite numerical checks supplement the proofs; they cannot establish an asymptotic theorem.

## Scope

The [Pauli detection task and several algorithmic ingredients have established precedents](references/RELATED_WORK.md). The matched result concerns a single initialized experiment with a charged initial purity budget, ordinary memoryless channel access and unital controls. It does not grant an environment output, an inverse, a controlled unknown channel or fresh pure records.

Repeated experiments with newly prepared probes supply more purity. Existing small-memory learning protocols that permit resets therefore lie in a different resource model. The near-conservation construction has exponentially many queries in $n$; no efficient general learner, optimal runtime, full tomography result or thermodynamic heat law is claimed.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
