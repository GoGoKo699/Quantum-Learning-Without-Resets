# From Watrous to quantum learning without resets

An unknown noisy device is available for repeated use. A learner can keep a protected quantum memory, apply known controls, and finally read one decision bit. This project asks whether an arbitrarily long experiment can replace a missing supply of fresh initialization.

The question is made precise for a channel that either erases every nonidentity Pauli coefficient or retains one unknown coefficient. The processor begins with a fixed amount of purity. All known controls are unital quantum channels, so a reset to a pure state is an additional resource. The result bounds the information in the final decision for every finite number of ordinary channel calls and gives finite protocols that attain the one-clean-qubit scaling.

The sole educational anchor is **John Watrous, *The Theory of Quantum Information*, Cambridge University Press (2018)**. Source locations below refer to the author's 2018 prepublication manuscript, available through the [author's book page](https://cs.uwaterloo.ca/~watrous/TQI/) and [free complete PDF](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf). The book is linked, not reproduced here. The [30-milestone map](MILESTONES.md) organizes the understanding route; [science/model.md](../science/model.md) owns the assumptions and [the scientific reading route](../science/README.md) locates the complete proofs.

Watrous supplies states, channels, measurements, operator norms, and channel-distance tools. The Pauli exposure budgets, finite feedback argument, and matched construction are additional steps developed in this project. They are explained below rather than attributed to a textbook theorem.

## Targeted reading from Watrous

These are focused lookups within one source.

| Project use | Exact source location | Role |
|---|---|---|
| States and complete registers | [Chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf), §§2.1.2–2.1.3; [Chapter 1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf), §1.1.2, Eqs. (1.120)–(1.121) | Density operators, reduced states, and partial trace |
| Physical channels | Chapter 2, Definition 2.13; Theorem 2.22; Corollary 2.27, Eq. (2.129) | Complete positivity, channel representations, and trace-preserving Kraus normalization |
| Adjoints | Chapter 1, Eq. (1.112); Chapter 2, Proposition 2.18 and Theorem 2.26 | Adjoint positivity and trace preservation versus unitality |
| Operator geometry | Chapter 1, §1.1.2, Eqs. (1.127)–(1.134), printed pp. 23–24, and §1.1.3, Eqs. (1.165)–(1.181), pp. 32–34; Chapter 2, Eqs. (2.60)–(2.63) | Vectorization, Schatten norms, and the natural representation |
| Unital contraction | [Chapter 4](https://cs.uwaterloo.ca/~watrous/TQI/TQI.4.pdf), §4.2.2, Theorem 4.27, printed p. 231 | Induced Hilbert–Schmidt contractivity |
| Dephasing | Chapter 2, §2.2.3, Eqs. (2.162)–(2.169) | A physical unital operation |
| Final decisions | Chapter 2, §2.3.1, Definition 2.34 and Eqs. (2.199)–(2.201), printed pp. 100–101; [Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf), §3.1.1, Theorem 3.4, pp. 128–129 | Effects and optimal binary discrimination |
| Accumulated implementation error | Chapter 3, §3.3.2: Definition 3.43, Theorem 3.46, Proposition 3.48(2), Eq. (3.273), printed pp. 170–174 | Diamond norm, protected auxiliaries, and composition bounds |

The pointer's elementary Bloch and rotation formulas below are locally derived applications of the channel framework. No additional textbook is needed for them.

## Notation and operational assumptions

| Source convention | Project convention | Interpretation |
|---|---|---|
| Hilbert spaces $\mathcal X,\mathcal Y$ | Registers $S,A$ | Query register and protected workspace |
| Vector $u$, adjoint $u^*$, projector $uu^*$ | $\lvert\psi\rangle$, $\langle\psi\rvert$, $\lvert\psi\rangle\langle\psi\rvert$ | Pure-state notation |
| Superoperator adjoint $\Phi^*$ | $\mathcal C^\dagger$ | Adjoint for the Hilbert–Schmidt inner product |
| Frobenius norm $\lVert X\rVert_2$ | Hilbert–Schmidt norm $\lVert X\rVert_2$ | The same operator-space norm |
| Natural matrix representation $\mathrm K(\Phi)$ | A matrix representing $\mathcal C$ on operator space | Its spectral norm is the induced Hilbert–Schmidt norm, not the diamond norm |
| Full norm $\lVert\rho-\sigma\rVert_1$ called trace distance | $D_{\mathrm{tr}}(\rho,\sigma)=\lVert\rho-\sigma\rVert_1/2$ | An explicit factor-of-two translation |
| Prior parameter $\lambda$ in Theorem 3.4 | Prior $p$ in this bridge | The project's $\lambda$ is reserved for channel strength |

Watrous explicitly calls the full trace norm “trace distance” immediately after Eq. (1.181), printed p. 34. Every distance and success conversion below uses the project's halved convention.

Here $d=2^n$, with $n\ge1$, is the query dimension, $K$ the finite protected-workspace dimension, and $D=dK$ the processor dimension. This scalar $K$ is unrelated to the natural representation $\mathrm K(\Phi)$. There are $M=d^2-1$ nonidentity Pauli labels. The hidden label $a$ is fixed throughout the finite run.

A call implements $\mathcal E_{a,\lambda}\otimes\mathrm{id}_A$ on the current joint state. A Stinespring representation proves that a channel is physically realizable; it does not give the learner its environment or inverse. The constructive circuits control known Pauli gates before and after an ordinary call. Their strength $\lambda$ is known. The converses apply even with that knowledge.

## Preparation and purity accounting

A qubit reset has the form
```math
\mathcal R(X)=|0\rangle\langle0|\mathrm{Tr}X.
```
It preserves trace, but $\mathcal R(I_2)=2|0\rangle\langle0|\ne I_2$. Therefore it is not a free unital control. By contrast, complete dephasing,
```math
\mathcal Z_0(X)=\frac12(X+ZXZ),
```
fixes the identity and retains the diagonal populations. Removing phase information and replacing a state by a pure state have different effects on the resource budget.

The [model's collision purity](../science/model.md) is
```math
\mathcal P=D\mathrm{Tr}(\rho_{\mathrm{in}}^2),
\qquad
\mathcal P-1
=D\left\|\rho_{\mathrm{in}}-\frac ID\right\|_2^2.
```
For a state $\rho$ on dimension $D$, appending an independent maximally mixed register of dimension $r$ gives
```math
Dr\,\mathrm{Tr}\left[
\left(\rho\otimes\frac{I_r}{r}\right)^2
\right]
=D\mathrm{Tr}(\rho^2).
```
Thus mixed workspace can grow without adding initial purity. One pure qubit with otherwise maximally mixed registers has $\mathcal P=2$; $c$ pure qubits give $\mathcal P=2^c$.

All accessible records belong to the processor. Deferring an intermediate measurement into a record register does not make that register's pure initialization free. Nonselective unital dephasing is allowed. Starting another experiment with a fresh clean pointer supplies new purity and is a different resource account.

The one-clean-qubit constructions use a particular product initialization. The converse covers every initial state with the stated $\mathcal P$, a potentially larger class. Collision purity is not identified with a temperature, energy, or thermodynamic work cost.

## One common effect and two distances

An effect $F$ satisfies $0\le F\le I$. Its expectation is one event probability. For two states,
```math
\max_{0\le F\le I}
\left|\mathrm{Tr}F(\rho-\sigma)\right|
=D_{\mathrm{tr}}(\rho,\sigma).
```
For equal priors, Watrous's Theorem 3.4 therefore gives optimal success
```math
p_{\mathrm{succ}}
=\frac12+\frac14\|\rho-\sigma\|_1
=\frac{1+D_{\mathrm{tr}}(\rho,\sigma)}2.
```
A probability gap $\Delta$ is twice the success advantage above one half.

When $a$ is hidden, the same effect must be used for every alternative. The relevant state is $\bar\rho=M^{-1}\sum_a\rho^a$, so the decision objective is $D_{\mathrm{tr}}(\bar\rho,\rho^0)$. In contrast, $M^{-1}\sum_aD_{\mathrm{tr}}(\rho^a,\rho^0)$ optimizes a different effect for each label.

A simple state example makes the distinction visible. Let $\rho^0=I/2$ and $\rho^\pm=(I\pm rZ)/2$, with $0\le r\le1$. Each individual distance is $r/2$, but their equal mixture is exactly $\rho^0$. No common decision distinguishes that mixture from the null. This illustrates the optimization issue; the project itself uses the [positive Pauli-spike promise](../science/model.md), not this two-state ensemble.

A worst-case decision with error at most $\delta\lt1/2$ must have null acceptance at most $\delta$ and every alternative acceptance at least $1-\delta$. Its mixture gap is therefore at least $1-2\delta$. Conversely, a mixture signal alone need not guarantee uniform performance. The constructive protocols here establish identical pointer statistics across hidden labels or directly bound both errors.

## A complete one-query example

Take $n=1$, so the candidate nonidentity Paulis are $X,Y,Z$ and $M=3$. The null channel sends every qubit state to $I/2$. Alternative $a$ retains only its Bloch component:
```math
\frac12(I+r_xX+r_yY+r_zZ)
\longmapsto
\frac12(I+\lambda r_aP_a).
```
The label remains unknown.

Prepare a mixed query qubit $S$, a two-qubit maximally mixed label register $L$ covering $I,X,Y,Z$, and a pure pointer $B$ in $|+\rangle$:
```math
\rho_{\mathrm{in}}
=\frac{I_S}{2}\otimes\frac{I_L}{4}
\otimes|+\rangle\langle+|_B.
```
There are four qubits in total, exactly one pure. The total dimension is $16$, the state purity is $1/8$, and $\mathcal P=2$.

For each label value $b$, the known controlled gate is
```math
V_b=I_S\otimes|0\rangle\langle0|_B
+P_b\otimes|1\rangle\langle1|_B.
```
Apply the label-controlled choice of $V_b$, make one ordinary query on $S$, and apply the same known gate again. No measurement or pure-state preparation occurs between these operations.

For a nonidentity candidate, the pointer off-diagonal block of the query state becomes proportional to $P_b/2$. The channel kills it unless $b=a$, in which case it multiplies it by $\lambda$. The second controlled gate returns the query register to $I/2$. The identity candidate leaves the pointer unchanged under either hypothesis.

Consequently, after ignoring the label, the pointer states are
```math
\sigma_0=\frac12\left(I+\frac14X\right),
\qquad
\sigma_a=\frac12\left(I+\frac{1+\lambda}{4}X\right).
```
The final event $X=+1$ has probabilities
```math
p_0=\frac58,\qquad
p_a=\frac{5+\lambda}{8},\qquad
p_a-p_0=\frac{\lambda}{8}.
```
They are the same for every hidden $a$. At $\lambda=1/2$, the gap is $1/16$ and equal-prior success is $17/32$. This is a complete small-bias protocol, not a $2/3$-success protocol.

Its gap is compatible with the finite-query converse: for $T=1$, $M=3$, and $\mathcal P=2$, the mixture-distance upper bound is $\lambda/6$. The [general one-query construction](../science/protocols.md), (A5)–(A6), gives $\lambda/[2(M+1)]$ and accounts for the mixed label register explicitly.

## Pauli sectors and protected memory

The book's tensor and partial-trace rules turn the Pauli basis into an operator-space decomposition. For an operator $X$ on $SA$, put
```math
X_a=\mathrm{Tr}_S[(P_a\otimes I_A)X],
\qquad
X=\frac1d\sum_{a=0}^{M}P_a\otimes X_a.
```
The factor is $1/d$, not $1/D$: only the query basis is being expanded. Orthogonality gives
```math
\|X\|_2^2=\frac1d\sum_{a=0}^{M}\|X_a\|_2^2.
```
The maps $Q_a(X)=P_a\otimes X_a/d$ are mutually orthogonal Hilbert–Schmidt projections. In particular,
```math
Q_0(X)=\frac{I_S}{d}\otimes\mathrm{Tr}_S X,
\qquad
\mathcal E_{a,\lambda}\otimes\mathrm{id}_A=Q_0+\lambda Q_a.
```
Only the complete sum is the alternative channel. A nonidentity $Q_a$ is a mathematical projection and need not preserve positivity. Physicality of the full channel has a direct measure-and-prepare explanation: measure the two effects $(I\pm P_a)/2$, then prepare $(I\pm\lambda P_a)/d$ with the corresponding sign. These are valid output states for $0\le\lambda\le1$, and the resulting channel is exactly $\mathcal E_{a,\lambda}$. This is one physical representation; the learner receives the ordinary channel, not its internal measurement outcome.

The null leaves every $I_S/d\otimes X_A$ unchanged. Therefore, it does not strictly contract every traceless processor operator. The [query-and-swap example](../science/interpretation.md) makes this operational: a $Z$ signal obtained from a pure query qubit can be swapped into protected memory and remain there while later calls act on a mixed query register.

The converse must account for **total exposure to queried sectors**, including any later feedback from memory. It cannot assume that stored information decays automatically.

## Adjoints and Hilbert–Schmidt contraction

The adjoint is defined by
```math
\langle Y,\mathcal C(X)\rangle
=\langle\mathcal C^\dagger(Y),X\rangle,
\qquad
\langle Y,X\rangle=\mathrm{Tr}(Y^\dagger X).
```
Watrous's Theorem 2.26 relates trace preservation of $\mathcal C$ to unitality of $\mathcal C^\dagger$. Applying the same relation to the adjoint relates unitality of $\mathcal C$ to trace preservation of $\mathcal C^\dagger$. Complete positivity also passes to the adjoint.

Hence a unital CPTP control and its adjoint satisfy the hypotheses of Theorem 4.27. Vectorization identifies the spectral norm of the natural representation with the induced Hilbert–Schmidt norm. The conclusion used here is
```math
\|\mathcal C(X)\|_2\le\|X\|_2,
\qquad
\|\mathcal C^\dagger(Y)\|_2\le\|Y\|_2.
```
This holds for arbitrary operators, which matters because centered states, propagated effects, and the later auxiliary port variables need not be density matrices. It supplies a norm inequality, not strict decay in every direction.

The [purity proof](../science/purity_bound.md), (P4), also gives the short Kadison–Schwarz route to the first inequality. The forward/backward application is possible because both unitality and trace preservation are imposed on the complete processor controls.

## The individual-distance purity budget

Let $\sigma$ be the null state before a step and $\delta_a$ the alternative-minus-null deviation. The [one-step update](../science/purity_bound.md) is
```math
\delta'_a
=Q_0\mathcal C(\delta_a)
+\lambda Q_a\mathcal C(\delta_a+\sigma).
```
Write $x=Q_a\mathcal C(\delta_a)$ for returning signal and $y=Q_a\mathcal C(\sigma)$ for the source. Orthogonality and contraction imply
```math
\|\delta'_a\|_2^2-\|\delta_a\|_2^2
\le-\|x\|_2^2+\lambda^2\|x+y\|_2^2
\le\frac{\lambda^2}{1-\lambda^2}\|y\|_2^2,
\qquad \lambda\lt1.
```
The final step completes a square in $x$. Returning information is allowed; its maximal contribution is controlled by the source term.

Summing the source energy over all hidden directions gives
```math
\sum_{a=1}^{M}\|Q_a\mathcal C(\sigma)\|_2^2
\le\|\sigma\|_2^2-\|Q_0\mathcal C(\sigma)\|_2^2.
```
This is a drop along one common null trajectory. Summing over time cancels all intermediate terms. The trace-norm conversion $\|X\|_1\le\sqrt D\|X\|_2$, followed by Cauchy–Schwarz across labels, yields
```math
\frac1M\sum_aD_{\mathrm{tr}}(\rho_T^a,\rho_T^0)
\le
\min\left\{1,
\frac{\lambda}{2\sqrt{1-\lambda^2}}
\sqrt{\frac{\mathcal P-1}{M}}
\right\}.
```
The initial purity and the minimal final purity $1/D$ absorb the full processor dimension. The complete argument is [science/purity_bound.md](../science/purity_bound.md). This is the individual-distance theorem, including its $\lambda\lt1$ restriction.

## The common-decision feedback bound

The common-decision argument additionally budgets one final effect. Its auxiliary construction is linear algebra on operator space, not a new physical oracle interface.

For one hidden sector, temporarily replace its return by arbitrary inputs $v_t\in\mathrm{ran}(Q_a)$ and collect outputs $u_t\in\mathrm{ran}(Q_a)$:
```math
u_t=Q_a\mathcal C_t(x_{t-1}),
\qquad
x_t=Q_0\mathcal C_t(x_{t-1})+v_t.
```
Because the retained and injected sectors are orthogonal,
```math
\|x_t\|_2^2+\|u_t\|_2^2
\le\|x_{t-1}\|_2^2+\|v_t\|_2^2.
```
Summing makes the entire input-output map a contraction. Write its blocks as $x_T=A x_0+B_av$ and $u=F_ax_0+G_av$. Closing $v=\lambda u$ reproduces the actual alternative.

Time ordering is essential: a port output depends only on earlier injections. Therefore $G_a^T=0$, where the superscript is the integer power equal to the number of calls. For $T\ge1$ the feedback inverse is a finite sum:
```math
(I-\lambda G_a)^{-1}
=\sum_{j=0}^{T-1}\lambda^jG_a^j,
\qquad
\|(I-\lambda G_a)^{-1}\|_{2\to2}
\le h_T(\lambda):=\sum_{j=0}^{T-1}\lambda^j.
```
This gives
```math
\rho_T^a-\rho_T^0
=\lambda B_a(I-\lambda G_a)^{-1}F_a(\rho_{\mathrm{in}}).
```

Along the null evolution, sector orthogonality supplies the forward bound
```math
\sum_a\|F_ax_0\|_2^2\le\|x_0\|_2^2.
```
Propagating the same final effect backward through adjoint null controls supplies
```math
\sum_a\|B_a^\dagger F\|_2^2\le\|F\|_2^2.
```
The backward trajectory includes the final sector insertion $Q_aF$. Omitting this endpoint would change the budget. The protected-memory algebra may survive in both directions; the bounds concern the total energy that enters nonidentity query sectors.

Center both ends:
```math
x_0=\rho_{\mathrm{in}}-\frac ID,\qquad
F_0=F-\frac{\mathrm{Tr}F}{D}I.
```
Unitality and trace preservation ensure that this leaves the signal unchanged. If $\mu=\mathrm{Tr}F/D$, the eigenvalues of an effect lie in $[0,1]$, so
```math
\|F_0\|_2^2
=\mathrm{Tr}(F^2)-D\mu^2
\le D\mu(1-\mu)\le\frac D4.
```
Meanwhile $\|x_0\|_2^2=(\mathcal P-1)/D$. Apply Cauchy–Schwarz across hidden labels to the product of the two exposure histories. Optimizing the common effect gives
```math
D_{\mathrm{tr}}(\bar\rho_T,\rho_T^0)
\le
\min\left\{1,
\frac{\lambda h_T(\lambda)\sqrt{\mathcal P-1}}{2M}
\right\}.
```
For $T=0$, define $h_0=0$ and the states coincide. For $\lambda\lt1$, $h_T\le(1-\lambda)^{-1}$ gives a bound uniform in query time. At $\lambda=1$, $h_T=T$ remains meaningful.

This application of the forward and backward budgets, including their centering constants, is the project-specific step beyond the textbook foundations. [Science/decision_bound.md](../science/decision_bound.md) gives the full time-indexed proof. It bounds the mixture distance, not the average of individual distances.

## Pointer dynamics and boundary dephasing

The exact gadget in the one-query example works for arbitrary pointer inputs. For a known nonidentity trial $b$, it implements $\mathcal Z_{\lambda}$ if $b=a$ and $\mathcal Z_0$ otherwise, while returning $S$ to $I/d$. Reusing that system is possible because of the gadget identity, not because a reset is supplied.

The scans start the pointer in $|0\rangle$, with $z=1$. For the real pointer states encountered during the scan, write
```math
\sigma=\frac12(I+xX+zZ).
```
A known rotation $R_y(\theta)=\exp(-i\theta Y/2)$ sends $(x,z)$ to $(cx+vz,-vx+cz)$, where $c=\cos\theta$ and $v=\sin\theta$. Following it by $\mathcal Z_\eta$ therefore gives
```math
A_\eta=
\begin{pmatrix}
\eta c&\eta v\\
-v&c
\end{pmatrix}.
```
The parameterized dephasing is physical because
```math
\mathcal Z_\eta
=\frac{1+\eta}{2}\,\mathrm{id}
+\frac{1-\eta}{2}\,\mathrm{Ad}_Z,
\qquad 0\le\eta\le1.
```

At each candidate-block boundary the canonical protocols apply complete $Z$ dephasing. Every block then begins with $x=0$, while its $z$ value retains the accumulated signal. For block length $L$, set $k_0=c^L$ and $k_\eta=(A_\eta^L)_{22}$. With one active block among $M$,
```math
z_0=k_0^M,\qquad
z_a=k_0^{M-1}k_\eta.
```
These are independent of the active block's position. The common final event $Z=-1$ has gap $k_0^{M-1}(k_0-k_\eta)/2$.

Without the boundary operation, residual $x$ from the active block can affect the next block. That is a different, position-dependent variant. Boundary dephasing is part of both canonical scans in [science/protocols.md](../science/protocols.md).

## Finite bias and prescribed error

For $\lambda\gt1/2$, the weak scan deliberately replaces the active multiplier by $\ell\le\lambda$ using a known dephasing. Its finite parameters are
```math
g=\max\{1-\lambda,1/M\},\qquad
\ell=1-g,\qquad h=\frac{1+\ell}{g},
```
```math
L=\left\lceil\frac{32}{g}\right\rceil,\qquad
t=\frac1{16(M+h)},\qquad
u=\frac{2t}{L},\qquad
\theta=\arcsin\sqrt u.
```
The extra multiplier $\ell/\lambda$ is in $[0,1]$. Clipping caps the effective coherence lifetime at order $M$ and avoids singular algorithm parameters at $\lambda=1$.

The finite proof does more than take a small-angle limit. It shows that the two characteristic roots of $A_\ell$ are positive and distinct, with discriminant parameter $h^2u\le1/128$. It bounds the root coefficients and remainder terms, while retaining a null survival factor at least $15/16$. This produces the explicit gap
```math
\Delta_{\mathrm{scan}}
\ge\frac{\ell}{32(Mg+1+\ell)}
\ge\frac1{128}
\min\left\{1,\frac{\lambda}{M(1-\lambda)}\right\},
```
with the final minimum interpreted as one at $\lambda=1$. The query count is
```math
Q=ML\le33M\min\{(1-\lambda)^{-1},M\}.
```
At the endpoint the right side is $33M^2$. The [characteristic-root estimates](../science/protocols.md), (A11)–(A19), explain why these constants hold for a finite algorithm.

A prescribed error needs a separate guarantee. Use the gadget without clipping, take $\theta=\pi/L$, and retain the same boundary dephasing. At $\lambda=1$, the active block rotates the pointer by $\pi$ while inactive blocks suppress its rotation:
```math
z_0=c^{ML},\qquad
z_a=-c^{(M-1)L},
\qquad c=\cos(\pi/L).
```
Writing $\gamma=1-\lambda$, the noisy active dephasing differs from the identity in diamond norm by exactly $\gamma$. This follows from its random-$Z$ representation and the orthogonal outputs of identity and $Z$ on $|+\rangle$. Only $L$ calls in the active block change. The composition bound in Watrous Proposition 3.48 therefore changes any final probability by at most $L\gamma/2$.

For a target error $0\lt\delta\lt1/2$, choose
```math
L=\left\lceil\frac{\pi^2M}{2\delta}\right\rceil,
\qquad
\gamma\le\frac{\delta}{L}.
```
The ideal scan error and the perturbation contribution are each at most $\delta/2$. Both errors are at most $\delta$. The canonical example $L=100M$ and $\gamma\le10^{-3}/M$ has worst-case error below $0.097$. The [complete bound](../science/protocols.md), (A21), retains the exact survival factors.

At exact conservation, taking larger and larger finite $L$ makes the error approach zero. This establishes a supremum of one for distinguishability; it does not assert a perfect finite-query optimizer. The weak scan's universal small-bias constant alone is not a $2/3$-success theorem.

## Resources and numerical boundaries

The one-query branch uses one pure pointer and $3n$ mixed qubits: $n$ query qubits and $2n$ label qubits. The scans use one pure pointer and $n$ mixed query qubits when unital dephasing is admitted directly.

Known dephasing can alternatively be realized using a fresh maximally mixed coin that selects opposite known $Z$ rotations. Preallocating these coins, retaining them, and never interacting with a used coin again reproduces the reduced dynamics. This increases mixed width by $O(Q)$ while leaving $\mathcal P=2$. It supplies no fresh pure state.

Each scan step uses one ordinary call, two controlled known Pauli-string gates, and one pointer rotation, with any clipping and boundary maps counted separately. A string has at most $n$ nonidentity local factors, giving $O(nQ)$ known-gate cost in the stated primitive model. This is not a platform-specific fault-tolerant runtime.

If $N_g$ known gates each have diamond error at most $\varepsilon_g$, the final probability error is at most $N_g\varepsilon_g/2$. Maintaining a small signal requires choosing this error relative to that signal. The claim does not treat fixed gate precision as sufficient for arbitrarily small bias.

The [verification implementation](../verification/README.md) evaluates finite formulas in floating-point arithmetic. Its scan-output evaluators are deliberately restricted to $1\le n\le5$ and $2\le L\le100M$. The one-query scalar branch is separate. Analytical bounds, parameter and cost APIs are not assigned this scan-output restriction, although floating-point parameter values are not numerical accuracy certificates.

Those limits concern the implementation, not the mathematical theorem. Finite diagnostics, nonfinite-value rejection, and stable scalar powers support reproducibility within their stated scope; they do not certify every arbitrarily small positive gap or replace the analytic proof.

## The result and its limits

For one pure qubit with otherwise maximally mixed workspace, define $\Delta_1(n,\lambda)$ as the supremum of common-decision mixture distinguishability over all finite query budgets and finite workspaces. The converse and constructions give, for $0\le\lambda\lt1$,
```math
\frac1{128}\min\{1,s\}
\le\Delta_1(n,\lambda)
\le\min\{1,s/2\},
\qquad
s=\frac{\lambda}{M(1-\lambda)}.
```
At $\lambda=0$ the value is zero; at $\lambda=1$ the supremum is one.

At fixed nonzero strength below one, the best signal is of order $1/M$. More time and more maximally mixed protected memory cannot turn it into a constant signal. Near conservation, the lifetime scale $(1-\lambda)^{-1}$ becomes comparable to the number of hidden directions, and a finite scan attains nonvanishing bias. A chosen worst-case error requires the stronger, error-dependent condition supplied by the separate $\pi$ scan.

The result concerns the best attainable bias, not optimal query complexity, hidden-label identification, or complete channel tomography. Its general-purity converse does not establish a matching tradeoff for every number of clean qubits or every initial spectrum. Reinitialization, nonunital cooling, and environment or inverse access change the model.

The [related-work account](../references/RELATED_WORK.md) credits the Pauli task, serial tests, weak driving, Zeno discrimination, noisy-oracle purity arguments, and norm foundations. The additional connection is the finite total exposure of both the initial state and one final effect to the hidden sectors, together with a construction under the same preparation budget. [M10](MILESTONES.md#m10-the-complete-operational-question) integrates the model, and [M30](MILESTONES.md#m30-the-complete-scientific-story) integrates this full resource conclusion.
