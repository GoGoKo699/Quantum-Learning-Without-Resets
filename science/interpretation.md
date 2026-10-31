# What the purity law changes

The main result concerns how much one final decision can learn about a hidden Pauli mode when the processor receives a fixed supply of purity. It separates this resource from the number of queries and the size of protected mixed memory.

For one clean qubit, write $M=4^n-1$. The [matched law](protocols.md) is

```math
\Delta_1(n,\lambda)
=\Theta\!\left(
\min\left\{1,\frac{\lambda}{M(1-\lambda)}\right\}
\right)
\qquad (0\le\lambda\lt1).
\tag{I1}
```

The constants are universal. At exactly $\lambda=1$, the supremum is one. $\Delta_1$ is trace-distance distinguishability; the equal-prior success advantage is half of it.

## 1. Time cannot supply missing initial purity

At any fixed $0\lt\lambda\lt1$, the optimal decision signal is of order $4^{-n}$. The upper bound applies to every finite sequence of known unital controls and ordinary queries. Running longer cannot eventually turn this into a constant signal.

This is stronger than a large query lower bound. A query lower bound says that success requires waiting long enough. Here a fixed initialized resource limits the success achievable after any amount of query time.

That conclusion does not follow just from monotonicity of purity. A one-bit answer could fit in the initially pure pointer. The additional obstruction is that the relevant direction is unknown among $M$ orthogonal Pauli sectors. Along the null evolution, the total forward state exposure to those sectors is finite. A common final effect has a finite backward exposure as well. Their product bounds the readable signal.

## 2. Near-conservation opens the possibility of detection

When $\lambda$ is close to one, the characteristic decay time of a repeatedly retained mode is of order $(1-\lambda)^{-1}$ calls. Equation (I1) compares that scale with the number $M$ of possible hidden modes.

This is an interpretation of the proven formula, not a separate dynamical assumption. The actual protocol actively controls the register and does not simply wait for a passive signal. The weak-rotation construction uses the long coherence lifetime of the matching trial, while incompatible trials strongly dephase the pointer.

For a sequence of systems, a nonvanishing decision bias is possible precisely when $\lambda/[M(1-\lambda)]$ stays bounded away from zero, subject to the usual asymptotic interpretation of a uniform lower bound. For a prescribed error such as $0.1$, the explicit high-accuracy scan requires a sufficiently small constant in $1-\lambda\le c/M$. The exact best constant is not determined.

The result therefore contains both an impossibility away from conservation and a finite mechanism that reaches the conservation scale.

## 3. Protected memory survives, but mixed width alone does not help

The null channel is $Q_0=\mathcal D_S\otimes\mathrm{id}_A$. It leaves every operator $I_S/d\otimes X_A$ untouched. A proof that all traceless processor operators decay at every call would fail.

For example, take one query qubit in $|0\rangle$ and one protected qubit maximally mixed. Query the channel with hidden mode $Z$, swap the two qubits, and then make arbitrarily many further calls on the query register without coupling the stored output back. A signal of trace distance $\lambda/2$ remains in the protected qubit. This uses one initial pure qubit and demonstrates the failure of a blanket per-call contraction claim. It does not violate the hidden-label theorem: this example privileges the known trial direction $Z$ rather than detecting every unknown Pauli with that signal.

The normalized initial purity $D\operatorname{Tr}\rho^2$ stays unchanged when independent maximally mixed memory is appended. Both converse bounds are independent of its amount. Mixed memory can implement useful control schedules and retain correlations, but cannot evade the theorem by increasing width.

## 4. What resets supply to existing learning algorithms

The [closest Pauli-learning protocols](../references/RELATED_WORK.md#chen-and-gong) count memory width, queries and final measurements while allowing preparation or reset channels. Those are internally consistent resource models. A processor may have few qubits at any moment and still receive fresh purity many times.

The present model charges that supply through the initial state and unital controls. It therefore explains why removing reset capability from a small-memory algorithm can change its achievable information, even if the number of calls is unbounded. It does not contradict the earlier algorithms or prove that their particular amount of resetting is optimal.

Repeated independent experiments also supply fresh initialized pointers. The theorem concerns one initialized run and cannot be multiplied into a universal measurement lower bound without analyzing the resource used across runs.

## 5. Several clean qubits and decision conventions

The general common-decision bound scales as $\sqrt{\mathcal P-1}/M$. If purity is supplied as $c$ pure qubits with all other qubits mixed, $\mathcal P=2^c$. At fixed strength and fixed nontrivial error, the necessary condition gives $c\ge4n-O(1)$.

This is a lower bound, not a complete tradeoff for arbitrary $c$. The matching construction established here concerns one pure qubit. It would be incorrect to extrapolate its optimality in $\lambda$ into tightness in every initial spectrum or purity value.

The [individual-distance theorem](purity_bound.md) answers a different question: it allows a separately optimized terminal measurement for each hidden label. The complementary [mixture theorem](decision_bound.md) uses one common decision and improves the scaling away from conservation. Neither gives the hidden label itself or estimates all channel eigenvalues.

## 6. Scope of the algorithmic conclusion

The finite construction has exponentially many calls in the near-conserved regime. This work establishes the optimal scale of attainable decision bias over all finite query budgets. It does not provide an efficient general learning algorithm, the optimal number of calls, or a practical advantage over ordinary fresh-probe tomography.

All bounds refer to ordinary memoryless channels. Access to a unitary dilation, its environment or an inverse changes the model. Likewise, known nonunital cooling or resetting changes the resource budget. One should not transfer the conclusion to those interfaces without a new argument.

The role of purity here is operational and mathematical. No temperature, work reservoir or heat-flow model has been specified, so the result is not a thermodynamic work theorem. A finite-purity information obstruction can be physically meaningful without identifying collision purity with a particular energetic cost.

The open questions left by the result are concrete: optimal finite query complexity, tight dependence on several clean qubits, and extensions to other hidden channel families. None is needed for the matched one-clean-qubit bias law proved here.
