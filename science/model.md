# Model, resources and decision task

A small quantum memory can remain coherent through many calls to a channel. That does not imply that its initial purity can be used indefinitely to turn a weak, unknown correlation into a readable bit. We study this distinction in the positive Pauli-spike detection problem introduced by [Chen and Gong](../references/RELATED_WORK.md#chen-and-gong).

The unknown channel is fixed throughout a run. The learner has ordinary channel access, known controls and a final measurement. The resource restriction is imposed on the **entire initialized processor**, including its protected workspace. This prevents an inaccessible purification or a fresh measurement register from silently supplying additional purity.

## 1. The channel promise

Let $n\ge1$, $d=2^n$, and $M=d^2-1$. Use Hermitian Pauli representatives $P_e$ indexed by $e\in\mathbb F_2^{2n}$, with $P_0=I$ and

```math
\mathrm{Tr}(P_eP_f)=d\,\mathbf1_{e=f}.
```

The null is complete depolarization. An alternative retains one nonidentity Pauli coefficient:

```math
\begin{aligned}
\mathcal D(X)&=\frac{I}{d}\mathrm{Tr}X,\\
\mathcal E_{e,\lambda}(X)
&=\frac{I\mathrm{Tr}X+
\lambda P_e\mathrm{Tr}(P_eX)}{d},
\qquad e\in\mathbb F_2^{2n}\setminus\{0\},\quad 0\le\lambda\le1.
\end{aligned}
\tag{M1}
```

Sums over hidden labels range over $e\ne0$ unless another set is specified. The label $e$ is unknown and is never supplied during the computation. It is fixed across all calls, rather than independently redrawn at each call. The strength $\lambda$ is known to the explicit constructive algorithms. The converses hold for each $\lambda$ even if it is known.

These maps are completely positive, trace preserving and unital. One direct check is their Pauli-error representation. For symplectic Pauli labels $e,v$,

```math
\begin{aligned}
p_0(v)=\frac1{d^2},\qquad
p_{e,\lambda}(v)=
\frac{1+\lambda(-1)^{[e,v]}}{d^2}.
\end{aligned}
\tag{M2}
```

The probabilities are nonnegative and sum to one. Their Pauli eigenvalues are one at the identity, $\lambda$ at $P_e$ and zero elsewhere. Thus (M1) is an ordinary noisy channel, not a nonphysical linear oracle. The channel can also measure the two eigenspaces of $P_e$ and prepare $(I\pm\lambda P_e)/d$ according to the outcome. It is entanglement breaking, including at $\lambda=1$.

A second promise used in the [shared entropy theorem](entropy_bound.md) restricts $`e`$ to the $`3n`$ weight-one labels and fixes $`\lambda=1/2`$. Its channel is exactly (M1), with fewer possible labels. Its uniform alternative mixture averages over those $`3n`$ labels, rather than over all $`M=4^n-1`$ labels. This restriction does not change the complete-processor or no-reset assumptions. The full-family definition of $`\Delta_1(n,\lambda)`$ below remains unchanged.

An implementation of (M2) can use a classical hidden label and random local Pauli errors. The learner receives neither that description nor the sampled error. An environment output, dilation isometry, inverse, controlled call to the unknown map or reusable random seed is not part of the oracle interface. Controlled **known** Pauli gates are ordinary learner operations.

## 2. The complete processor

Write the queried register as $S$ and the protected workspace as $A$, of dimensions $d$ and $K$. The total dimension is $D=dK$. The initial state $\rho_{\mathrm{in}}$ on $SA$ is known and independent of the hypothesis.

There are $T$ ordinary calls. A known channel $\mathcal C_t$ acts on all of $SA$ before call $t$:

```math
\begin{aligned}
\rho_t^0&=(\mathcal D\otimes\mathrm{id}_A)
              \mathcal C_t(\rho_{t-1}^0),\\
\rho_t^e&=(\mathcal E_{e,\lambda}\otimes\mathrm{id}_A)
              \mathcal C_t(\rho_{t-1}^e),\\
\rho_0^e&=\rho_0^0=\rho_{\mathrm{in}}.
\end{aligned}
\tag{M3}
```

Every $\mathcal C_t$ is completely positive, trace preserving and **unital**:

```math
\begin{aligned}
\mathcal C_t(I)=I.
\end{aligned}
\tag{M4}
```

The same map is used under every hypothesis. It may coherently process whatever information has already entered the state. This includes arbitrary known global unitaries, swaps into protected memory, dephasing and more general unital processing. The assumption does not require a product state at query cuts, commuting controls, independent probes or short memory.

A final known channel can be absorbed into the final measurement effect, so it does not enlarge the discrimination power being bounded. Input-independent classical randomization is also harmless: condition on its seed, apply the same uniform bound, and average. A seed correlated with the unknown label is not allowed.

All retained records are part of $SA$. A nonselective measurement that is unital is allowed. A free record initialized in a standard pure state, repeated preparation of a polarized probe, or a conditional pure reset is an extra resource. Saying that an algorithm has “no intermediate measurements” does not establish (M4): measurement-free nonunital reset channels can still replenish purity.

The fixed dimension presents no restriction on how much mixed memory is available. Any finite collection of maximally mixed ancillary registers can be included initially. The universal bounds are uniform in its size. They do not grant access to a purification of those registers.

## 3. Initial collision purity

Define the dimension-normalized collision purity

```math
\begin{aligned}
\mathcal P=D\,\mathrm{Tr}(\rho_{\mathrm{in}}^2),
\qquad 1\le\mathcal P\le D.
\end{aligned}
\tag{M5}
```

Its excess above one has the useful geometric form

```math
\begin{aligned}
\mathcal P-1=
D\left\|\rho_{\mathrm{in}}-\frac{I}{D}\right\|_2^2.
\end{aligned}
\tag{M6}
```

The subscript 2 denotes the Hilbert–Schmidt norm. A product of $c$ pure qubits and otherwise maximally mixed qubits has $\mathcal P=2^c$. Appending an independent maximally mixed register does not change $\mathcal P$. Unital processing cannot increase it.

The **one-clean-qubit class** starts from one pure qubit tensored with any number of maximally mixed qubits, and then uses the allowed controls. Its initial purity is two. The converse also covers the larger class of states with $\mathcal P\le2$; the matching algorithms need only the product initialization just described. We do not identify every state of collision purity at most two with a state preparable from that product by the allowed operations.

For the weight-one promise, the [entropy theorem](entropy_bound.md) uses the additional resource

```math
C=\log_2D-H(\rho_{\mathrm{in}}),\qquad
0\le C\le\log_2\mathcal P,
```

where $`H`$ is von Neumann entropy in bits. This is an entropy deficit, distinct from collision purity. A product of $`c`$ clean qubits and otherwise maximally mixed qubits has both $`C=c`$ and $`\mathcal P=2^c`$. If all protected memory has at most $`k_{\mathrm{phys}}`$ qubits, $`C\le n+k_{\mathrm{phys}}`$. Any retained classical records must be included for that dimension bound; a coherent-only width convention with free classical history supplies a different resource. Appending independent maximally mixed memory leaves $`C`$ unchanged.

Collision purity is a resource parameter for this theorem. It is not a measured heat expenditure or the von Neumann entropy removed by an implementation. We make no universal thermodynamic conversion claim.

## 4. Decision statistics and error conventions

For a fixed terminal effect $0\le F\le I$, let outcome one occur with probability $p_e=\mathrm{Tr}(F\rho_T^e)$ and let $p_0=\mathrm{Tr}(F\rho_T^0)$. The same effect must handle every hidden label.

We use the halved trace norm

```math
\begin{aligned}
D_{\mathrm{tr}}(\rho,\sigma)
=\frac12\|\rho-\sigma\|_1.
\end{aligned}
\tag{M7}
```

The uniform-mixture output is $\bar\rho_T=M^{-1}\sum_{e\ne0}\rho_T^e$. Its trace distance from the null equals the largest absolute difference in the probability of one event:

```math
\begin{aligned}
D_{\mathrm{tr}}(\bar\rho_T,\rho_T^0)
=\max_{0\le F\le I}
\left|\frac1M\sum_{e\ne0} p_e-p_0\right|.
\end{aligned}
\tag{M8}
```

For equal prior probabilities of the null and this alternative mixture, optimal success is $(1+D_{\mathrm{tr}})/2$. The success advantage over one half is therefore half the trace distance. These conventions are kept separate throughout.

A worst-case error guarantee $\delta\lt1/2$ requires one decision rule with

```math
\begin{aligned}
p_0\le\delta,\qquad p_e\ge1-\delta
\quad\text{for every }e.
\end{aligned}
\tag{M9}
```

Consequently its mixture trace distance is at least $1-2\delta$. A mixture converse therefore rules out a worst-case algorithm. A mixture lower bound by itself need not supply a worst-case algorithm; the constructions below have identical final pointer statistics for all labels, or directly prove (M9).

For the optimal-bias result, define

```math
\begin{aligned}
\Delta_1(n,\lambda)=
\sup_{\substack{T\text{ finite}\\
\text{one-clean-qubit protocols}}}
D_{\mathrm{tr}}(\bar\rho_T,\rho_T^0).
\end{aligned}
\tag{M10}
```

The supremum includes any finite maximally mixed workspace. It concerns an unrestricted finite query budget, rather than an efficient-time class. At $\lambda=1$ the supremum is one; no finite protocol is claimed to attain perfect discrimination.

## 5. What is charged

Every invocation of (M1) counts as one query. The constructions count their known controlled-Pauli gates separately and state their mixed-workspace requirements. The algorithms do not assume QRAM, an amplitude encoding of a classical dataset or a free inverse oracle.

The bounds concern one initialized run. Starting another run with a clean pointer is a new supply of purity. Repeating many such experiments and retaining their classical results is not an operation on the same fixed-purity initialized processor. The converse cannot be read as a ban on ordinary tomography with repeated fresh preparation.

See [the energy bound](purity_bound.md) for label-wise output distances, [the decision bound](decision_bound.md) for a common final measurement, and [the explicit algorithms](protocols.md) for full-family one-clean-qubit attainability. The [shared entropy theorem](entropy_bound.md) gives the separate, stronger initial-entropy obstruction for weight one at $`\lambda=1/2`$.
