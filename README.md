# Quantum Learning Without Resets

**How much can a quantum processor learn from one supply of initial purity, even if it can query an unknown channel indefinitely?** For a hidden Pauli mode, one initially pure qubit has an exact attainable-signal scale, up to universal constants. Arbitrarily large protected mixed memory cannot remove this restriction. For one attenuated weight-one mode, a linear supply of clean qubits suffices at the optimal logarithmic query rate.

**Companion repository: [Pauli Learning Memory Thresholds](https://github.com/GoGoKo699/Pauli-Learning-Memory-Thresholds).** It studies the coherent width needed for learning with fresh experiments. The shared [weight-one entropy obstruction](science/entropy_bound.md) proves that logarithmic initial purity cannot support the attenuated task at $`\lambda=1/2`$ without resets or free fresh records. This repository owns the complete proof; the companion's [no-reset frontier](https://github.com/GoGoKo699/Pauli-Learning-Memory-Thresholds/blob/main/science/no_reset_frontier.md) explains its width and learning consequences.

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

## Weight one: matching purity bounds and the optimal query rate

Restrict the hidden label to the $`3n`$ weight-one Paulis and set $`\lambda=1/2`$. Let $`C=\log_2\dim(SA)-H(\rho_{\mathrm{in}})`$ be the complete processor's initial entropy deficit in bits. It equals $`c`$ for $`c`$ clean qubits and otherwise maximally mixed registers. The [entropy theorem](science/entropy_bound.md) proves, for every finite number of queries,

```math
\sum_{e:\,|e|=1}D_{\mathrm{bits}}(\rho_T^0\Vert\rho_T^e)\le\frac34C.
```

Here $`D_{\mathrm{bits}}`$ is ordinary quantum relative entropy with base-two logarithms. Worst-case error at most $`1/3`$ requires **$`C\ge4n/3`$**. If every protected register and retained record fits in $`k_{\mathrm{phys}}`$ qubits, then $`C\le n+k_{\mathrm{phys}}`$, so **$`k_{\mathrm{phys}}\ge n/3`$** is necessary as well. In particular, $`O(\log n)`$ initially clean qubits and $`O(\log n)`$ fully charged side memory cannot solve this task, regardless of query count.

The [linear-purity protocol](science/linear-purity-protocol.md) attains the order of both lower bounds. It prepares parallel Bell probes from a fixed supply of $O(n)$ clean qubits, stores the readout in that same workspace, and stops probing sites as their candidate axes are ruled out. One terminal measurement reports the null or the hidden site and axis. At fixed worst-case error $\delta\lt 1/2$, the optimal query count satisfies

```math
T_{\min}
=\frac{\ln(3n)}{D(3/4\Vert1/2)}+O_\delta(\sqrt{\ln n}),
\qquad
D(3/4\Vert1/2)=\tfrac34\ln(3/2)+\tfrac14\ln(1/2).
```

Here $D$ is the relative entropy in nats between two Bernoulli distributions. The query lower bound already holds for binary detection with unrestricted purity and workspace. The exact optimal purity constant remains open.

## Proof and algorithm

The full-family one-clean-qubit proof follows two Hilbert–Schmidt energy budgets along the depolarizing null: the state propagated forward and one common measurement effect propagated backward. Their total exposure to the queried Pauli sectors is finite. A finite feedback expansion combines these budgets and yields the bound for every query count.

The algorithm surrounds each ordinary query with a controlled **known** Pauli gate and its inverse. This exactly converts the trial mode into a dephasing channel on a pointer, while returning the query register to its mixed state. A finite sequence of weak rotations and dephasings then reaches the predicted signal scale. The construction uses one query for $\lambda\le1/2$ and at most

```math
33M\min\{(1-\lambda)^{-1},M\}
```

queries for $\lambda>1/2$, with $O(n)$ known gates per query. These are sufficient costs, not optimal query bounds. A separate finite scan supplies an explicit worst-case error certificate near $\lambda=1$.

## Run the weight-one characterization

1. **Initialize the fixed processor.** Use the [call budget, likelihood bounds, and tape capacities](science/linear-purity-protocol.md#finite-resource-statement) for the desired error. The device is promised to be fully depolarizing or to retain one single-site Pauli component at half strength. Start the query register maximally mixed and allocate every clean Bell-pair slot, flag, and work register at initialization.
2. **Probe active sites with Bell pairs.** Prepare assigned Bell pairs with Hadamards and CNOTs. Swap one half into each active query site, make one ordinary call on the full query register, then swap the halves back. Undo Bell preparation and dephase the slots in the computational basis. Use the three Pauli signs from each Bell label to [update the likelihood tests on the same tape](science/linear-purity-protocol.md#compile-the-experiment-into-one-initialized-processor). Multiply each active ratio by three halves for a positive sign or one half for a negative sign. Freeze a test when it first crosses either boundary.
3. **Read the device diagnosis.** If a round exceeds its initialized capacity, record overflow and finish the fixed schedule with calls on the mixed query register. At the terminal measurement, return the first accepted site and axis in the fixed order if one exists and there was no overflow. Otherwise return the null.

The [one-clean-qubit pointer circuit](science/protocols.md#2-extracting-a-known-trial-mode-onto-a-pointer) applies a controlled known Pauli and its inverse around an ordinary device call. Its full-family tests return a binary decision. The weight-one site-and-axis procedure charges its entire fixed purity budget, all device calls, and the reversible processing.

## Explanatory report

The [explanatory report at the November 3 source revision](https://github.com/GoGoKo699/Quantum-Learning-Without-Resets/blob/ba797e1f5aba82d1a9c0dbe5879c9994ec39a8d9/learning/report/Quantum_Learning_Without_Resets_Report.pdf) develops the one-clean-qubit analysis and shared weight-one converse. The current [weight-one protocol and query converse](science/linear-purity-protocol.md) resolve the linear-resource attainability question raised in that report.

## Read the science

Start with the [scientific reading route](science/README.md) and the [model](science/model.md). The complete arguments are organized by question:

| Question | Authoritative account |
|---|---|
| What channel, purity budget, controls and error convention are assumed? | [Model and resources](science/model.md) |
| How does null-trajectory purity loss bound label-wise output distances? | [Purity-potential theorem](science/purity_bound.md) |
| Why does one final decision admit a complementary bound? | [Common-decision theorem](science/decision_bound.md) |
| Why does the weight-one attenuated task need linear initial entropy? | [Shared entropy obstruction](science/entropy_bound.md) |
| How can one fixed linear supply of purity attain the optimal query rate? | [Weight-one protocol and query converse](science/linear-purity-protocol.md) |
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
python verification/verify_entropy.py
python verification/verify_linear_purity.py
```

The [analytical signal envelopes](verification/Graph/signal_bounds.pdf) are generated directly by [Python](verification/Graph/generate_signal_bounds.py), using [pinned plotting dependencies](verification/Graph/requirements.txt). The curves evaluate the proved lower and upper envelopes, with no fitted or simulated optimum. Technical reproduction commands are in [verification](verification/README.md).

The original deterministic suite reconstructs full channel circuits, checks the forward and backward feedback identities, compares scalar scan formulas with matrix powers, and exercises endpoint and resource conventions. It writes [results.json](verification/results.json). The separate entropy verifier checks the reverse-relative-entropy coupling, Pauli complementarity and complete small no-reset trajectories; it writes [entropy_results.json](verification/entropy_results.json). The [linear-purity verifier](verification/verify_linear_purity.py) checks the Bell readout, tape budget and likelihood calculations on finite instances. These checks supplement the analytical proofs.

## Scope

The shared entropy obstruction concerns the separate weight-one promise at $`\lambda=1/2`$. Its complete proof is here; the companion repository owns the fresh-experiment support–memory frontier. The full-family one-clean-qubit optimum uses all $`M=4^n-1`$ labels, as stated above.

The [Pauli detection task and several algorithmic ingredients have established precedents](references/RELATED_WORK.md). The matched result concerns a single initialized experiment with a charged initial purity budget, ordinary memoryless channel access and unital controls. It does not grant an environment output, an inverse, a controlled unknown channel or fresh pure records.

Repeated experiments with newly prepared probes supply more purity. Existing small-memory learning protocols that permit resets therefore lie in a different resource model. The near-conservation construction for the full family has exponentially many queries in $n$. The sharp leading query count concerns only the weight-one promise with attenuation one half. The proof counts calls and initialized qubits under known global unital controls.

## Purpose and contact

The project is currently under collaboration, and the manuscript is being written. For questions, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
