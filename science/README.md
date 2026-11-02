# Scientific reading route

The scientific question is whether unlimited ordinary channel time and unlimited mixed protected memory can compensate for a finite initial supply of purity. The answer is quantified for a hidden positive Pauli mode. Every theorem and algorithm uses the same [complete-processor model](model.md).

Read the pages in the order below. The two collision-purity converse proofs answer different decision questions; their trace-distance quantities must not be exchanged. A separate entropy proof strengthens the converse for the weight-one promise at $`\lambda=1/2`$.

| Page | Main result and role |
|---|---|
| [Model, resources and decision task](model.md) | The ordinary channel promise, fixed hidden label, global unital controls, normalized collision purity, and the exact definition of $\Delta_1$. |
| [A purity-potential bound](purity_bound.md) | A telescoping null-purity estimate bounds the average of individually optimized output distances. This introduces the Pauli-sector projections and explains the role of protected memory. |
| [A uniform bound for one final decision](decision_bound.md) | Forward and backward energy budgets yield a complementary mixture-distance bound, including the exact finite-query geometric factor. |
| [An entropy obstruction for weight-one Pauli spikes](entropy_bound.md) | The shared sister result: a reverse-relative-entropy coupling gives a linear initial-entropy requirement, with a fully charged side-width consequence. |
| [Finite algorithms and the one-clean-qubit optimum](protocols.md) | The exact Pauli-to-pointer gadget, a one-query small-strength protocol, a finite weak-rotation scan, and a separate near-unit fixed-error construction. All costs are charged. |
| [What the purity law changes](interpretation.md) | The time-versus-purity distinction, the conservation scale, a protected-memory counterexample to naive contraction, and the precise limits of the result. |

For $M=4^n-1$, the matched conclusion is

```math
\Delta_1(n,\lambda)
=\Theta\!\left(\min\left\{1,\frac{\lambda}{M(1-\lambda)}\right\}\right),
\qquad 0\le\lambda\lt1.
```

This is a statement about the best attainable common-decision signal over all finite query budgets. It is not a statement that every construction has constant success probability, or that its query count is optimal.

For the restricted weight-one task, [the entropy theorem](entropy_bound.md) separately gives $`C\ge4n/3`$ at error $`1/3`$, and $`k\ge n/3`$ when every protected register and retained record is charged to $`k`$ qubits. This is a necessary-condition theorem, not a matching linear-resource construction. The sister [Pauli Learning Memory Thresholds](https://github.com/GoGoKo699/Pauli-Learning-Memory-Thresholds) gives the fresh-experiment support–memory frontier and the learning interpretation.

The [related-work account](../references/RELATED_WORK.md) identifies the existing task, prior serial and weak-driving constructions, the noisy-oracle purity argument, and the operator-norm foundations. The [verification account](../verification/README.md) explains which finite identities are independently reconstructed in code and which statements depend on the written proofs.
