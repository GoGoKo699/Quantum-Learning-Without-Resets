# Detecting a weight-one Pauli spike with linear initial purity

A channel either depolarizes an $n$-qubit register or preserves one unknown single-qubit Pauli coefficient with attenuation $\lambda=1/2$. The processor is initialized once, uses ordinary calls and known unital controls, and makes one terminal measurement. The [entropy obstruction](entropy_bound.md) shows that constant-error detection needs linear initial purity even with arbitrarily many queries. Linear purity also suffices at the optimal leading query count. The same construction identifies the hidden site and axis.

## Finite resource statement

Use the weight-one promise and the initialized processor of the [model](model.md) and [entropy theorem](entropy_bound.md). Set $m=3n$ and fix a worst-case error tolerance $0\lt\delta\lt 1/2$. The Bernoulli relative entropy in nats is

```math
D=\frac34\ln\frac32+\frac14\ln\frac12
 =\frac34\ln 3-\ln 2.
```

Write $j(\delta)=(1-2\delta)\log_2[(1-\delta)/\delta]$. The entropy theorem gives $C\geq 4n j(\delta)$ bits of initial entropy deficit for detection, with no dependence on the finite query count. For product clean and maximally mixed initialization, $C$ is the number of initially clean qubits. If all protected qubits and records fit in $k_{\mathrm{phys}}$ qubits, then $k_{\mathrm{phys}}\geq \max\{0,4n j(\delta)-n\}$. In particular, at error $1/3$ these lower bounds are $4n/3$ on clean qubits and $n/3$ on protected width.

For a finite attaining protocol, choose likelihood boundaries $a=\delta/4$ and $A=4m/\delta$. Define $h=\ln(3)\sqrt{\ln(4/\delta)/2}$ and use the fixed number of calls

```math
T=\left\lceil
  \left(\frac{h+\sqrt{h^2+4D\ln A}}{2D}\right)^2
\right\rceil .
\tag{L1}
```

For round $t=1,\ldots,T$, define a capacity $b_t$ in Bell-pair slots:

```math
\begin{aligned}
q&=\frac{\sqrt{3/2}+\sqrt{1/2}}{2}\lt 1,\\
\mu_t&=n\min\{1,3a^{-1/2}q^{t-1}\},\\
b_t&=\min\!\left\{n,\left\lceil 2\mu_t+\log_2(4T/\delta)+1\right\rceil\right\}.
\end{aligned}
\tag{L2}
```

The protocol uses $2\sum_t b_t$ clean qubits for the Bell-pair slots. A reversible implementation described below uses at most another $6\sum_t b_t+T$ clean flag qubits and $O(T\log(n+T+2))$ clean working qubits. Their sum bounds the entire protected width and initial entropy deficit when the query register starts maximally mixed. For each fixed $\delta$, $T=\ln(m)/D+O_\delta(\sqrt{\ln(m+1)})$ and the clean-qubit count is $O_\delta(n)$. The error bound holds under the null and separately under every alternative. Under an alternative, success means returning its actual Pauli label.

Consequently, at constant error the optimal initial entropy deficit has order $n$. The unrestricted optimal ordinary call count has leading term $\ln(m)/D$, and the linear-purity protocol attains that same term. These statements concern the specified attenuation and weight-one family.

## The Bell outcome law

Use binary symplectic labels and write $\chi_e(v)=(-1)^{[e,v]}$. The [Pauli channel representation](model.md#1-the-channel-promise) expresses one unknown call as a Pauli error $P_v$ drawn with probability

```math
p_0(v)=4^{-n},\qquad
p_e(v)=4^{-n}(1+\chi_e(v)/2).
\tag{L3}
```

Under the null, the two-bit local error labels are independent and uniform. Under alternative $e=(i,\alpha)$, only site $i$ has a different distribution. There it has probability $[1+\chi_{i,\alpha}(v)/2]/4$ for each local Pauli label. The site labels remain independent, and new labels are drawn at each call.

When one half of a clean Bell pair enters the query at a chosen site, the Bell basis at the output reads its local error label exactly. One such label gives the three character values for that site's $X,Y,Z$ candidates. Under the matching alternative the true axis has probability $3/4$ for character value $+1$. Each other axis has probability $1/2$, because distinct nonzero Pauli characters are orthogonal. Within one site the proof uses these marginal laws. The capacity calculation uses independence across sites.

## Stop probing rejected sites

Give each of the $m$ candidates a likelihood ratio initialized to one. The ratio compares the matching character law $\Pr(+1)=3/4$ to the fair law $\Pr(+1)=1/2$. Each new character multiplies its ratio by $3/2$ for $+1$ and by $1/2$ for $-1$. A candidate rejects when its ratio first reaches $a$ or below, and accepts when it first reaches $A$ or above. Either crossing ends that candidate's test. A site remains active while at least one of its three candidates is still being tested.

At the start of round $t$, compare the number of active sites to $b_t$. If it fits, probe those sites in parallel with Bell pairs from this round's segment. The same channel invocation serves all of them. If it exceeds the capacity, record overflow and stop acquiring data. Finish the fixed schedule with ordinary padding calls on the maximally mixed query register. At the terminal measurement report the first accepted candidate in a fixed order, if one exists and there was no overflow. Otherwise report the null.

### Error in the ideal experiment without capacity limits

For the analysis, draw a potential local error label at every site for each round, with the product law (L3). Reveal labels only where the experiment probes. A candidate that remains active through round $s$ receives one new sample per round up to $s$. It therefore follows its own potential sample sequence until stopping.

For any false candidate its likelihood ratio along the full potential sequence is a nonnegative martingale starting at one. The probability that it ever reaches $A$ is at most $1/A$, by the maximal inequality for nonnegative martingales. This bound holds under every hypothesis where that candidate is false. A union bound over candidates makes the probability of any false acceptance at most $m/A=\delta/4$.

For the true candidate, the reciprocal likelihood ratio is a nonnegative martingale under its own law. The probability of ever reaching the lower boundary on the likelihood ratio is at most $a=\delta/4$. If this candidate never crosses the lower boundary and its unconstrained $T$-sample ratio reaches or exceeds $A$ by round $T$, it is accepted. The log-likelihood after $T$ potential samples is a sum with mean $TD$ whose increments lie in an interval of length $\ln 3$. Hoeffding's inequality gives

```math
\Pr_e\{\ln L_{e,T}\lt\ln A\}
\leq \exp\!\left[-\frac{2(TD-\ln A)^2}{T(\ln 3)^2}\right]
\leq\delta/4 .
\tag{L4}
```

Here (L1) ensures $TD-\ln A\geq h\sqrt T$. Along a path where the true candidate accepts and every false candidate fails to accept, the terminal rule returns the true label.

### The initialized capacity is sufficient

For a fair comparator that is still active at the start of round $t$, its $t-1$ sample likelihood ratio exceeds $a$. Under the fair law, $\mathbb E_0\sqrt{L_{t-1}}=q^{t-1}$. Markov's inequality and a union bound over three axes give the probability of an off-target site being active at most $\min\{1,3a^{-1/2}q^{t-1}\}$.

In the ideal experiment, the indicators of off-target site activity are independent across sites. Each is a function only of that site's potential error sequence. Their sum $X_t$ has mean at most $\mu_t$. Under the null every site is off-target. Under any alternative the actual active count is at most $X_t+1$. The bound on the moment generating function at base two is

```math
\mathbb E[2^{X_t}]
  =\prod_i[1+\Pr\{\text{site }i\text{ active}}]
  \leq e^{\mu_t}.
```

Overflow is impossible when $b_t=n$. Otherwise, (L2) and Markov's inequality give

```math
\Pr\{X_t+1\gt b_t\}
\leq e^{\mu_t}2^{1-b_t}
\leq\frac{\delta}{4T},
```

using $2\ln 2\gt 1$. The capped and ideal experiments agree until their first overflow when coupled with the same potential labels. A union bound makes the total overflow probability at most $\delta/4$ under every hypothesis. The false acceptance, true rejection, timeout and overflow probabilities give a worst-case error of at most $\delta$. Under the null only false acceptance can cause an error.

Finally,

```math
\sum_{t=1}^T b_t
\leq \frac{6na^{-1/2}}{1-q}
 + T[\log_2(4T/\delta)+2]
= O_\delta(n).
\tag{L5}
```

This is a bound on the fixed tape capacity supplied at initialization, including enough spare slots to control the overflow probability.

## Compile the experiment into one initialized processor

Initialize the query register in $I/2^n$. Every Bell-pair slot is two protected qubits initialized in $|00\rangle$. Order sites by index. Within each round use their ranks among active sites to assign slots. With older outcome and flag segments as controls, prepare the assigned Bell pairs by a Hadamard and CNOT and swap one half of each pair into its query site. Apply the ordinary unknown channel once to the full query register. Undo the swaps using the same older controls, invert the Bell-basis preparation on the two physical slot qubits, and dephase the outcome segment in its computational basis.

The previous contents of each active query site stayed in the swapped-out half and are returned by the second swap. Inactive sites were maximally mixed and remain so. This follows directly by conditioning on the old tape and on the Pauli error in (L3), which is a product of local unitaries. After the swaps the query register is maximally mixed and independent of the new tape record. In an overflow or padding round, the controls leave the query register maximally mixed. Thus the same invariant holds every round, and the computational-basis state of the outcome tape has exactly the ideal readout distribution up to the first overflow.

The activity tests and overflow choice can be implemented by controlled unitaries and reversible Boolean logic. They use old segments as read-only controls. A reversible exclusive-or writes each derived continuation flag, upper-crossing flag and round-overflow flag into its own initially clean location. Two outcome bits and six flags per used slot suffice. Flags for unused slots remain zero. Dephasing is nonselective pinching of the initialized outcome qubits, which hold the classical record. All known operations on the complete processor are unital. The one terminal measurement is the computational-basis decision rule on the stored record, with outcomes coarse-grained to the null or a single Pauli label.

An explicit implementation can recover a site's rank in any round by traversing earlier continuation segments. To move from one round to the next, read the current site's flags and count the preceding slots with at least one continuing comparator. A comparator still active in round $t$ has received one sample per round. Count its positive signs along the recovered path. With $s$ positive signs in its first $t$ samples, its likelihood ratio is $3^s/2^t$, so the boundaries can be precompiled into integer comparisons on $s$ for each $t$. Reversible scans of the flags and outcomes use bounded counters. They can retain intermediate ranks and counts for at most $T$ steps and run the scans backwards after copying the required output to clear scratch. This uses $O(T\log(n+T+2))$ working qubits and polynomially many known gates in $n$ and $T$. The gate count and all workspace are additional resources to the ordinary query count.

## The query constant is optimal

For any $T$-query protocol, give a simulator $T$ independently sampled full Pauli error labels instead of channel access. At each query the simulator applies the corresponding Pauli conjugation to the query register. This reproduces all output statistics even with adaptive controls, general memory and arbitrary initial purity. Hence total variation distance in the classical label experiment upper-bounds the achievable distance of terminal decision laws. The simulator is used only in the converse.

Under the null all $T$ labels are uniform. Let $L_{e,T}$ be the likelihood ratio for alternative $e$ on the full record. By (L3) it is the product of the same factors used in the protocol. Under the null, the full likelihood ratios $L_{e,T},L_{f,T}$ are independent for every distinct pair $e,f$. The two distinct nonzero binary linear functionals $v\mapsto[e,v],v\mapsto[f,v]$ give two independent fair bits on a uniform $v$, and the calls are independent.

The alternative mixture has likelihood ratio $\overline L=m^{-1}\sum_e L_{e,T}$. The exact untruncated second moment gives a simple finite query bound:

```math
\mathrm{TV}(P_0,\overline P)
\leq\frac12\sqrt{\frac{(5/4)^T-1}{m}}.
\tag{L6}
```

Indeed, $\mathbb E_0L_{e,T}^2=(5/4)^T$ and the cross terms have mean one. To reach the sharp leading constant, truncate at any $B\gt0$. Put $Z_e=L_{e,T}\mathbf1\{L_{e,T}\leq B\}$ and $p_B=P_e(L_{e,T}\gt B)$, whose value is the same for all $e$. Change of measure gives $\mathbb E_0Z_e=1-p_B$, and $\mathbb E_0Z_e^2\leq B$. Pairwise independence then bounds the variance of the average of the $Z_e$ by $B/m$. The triangle inequality yields the finite bound

```math
\mathrm{TV}(P_0,\overline P)
   =\frac12 \mathbb E_0|\overline L-1|
   \leq p_B+\frac12\sqrt{B/m}.
\tag{L7}
```

The discarded likelihood mass and the shift in mean each contribute $p_B/2$. Under $P_e$, the log-likelihood has mean $TD$ and increments spanning an interval of length $\ln 3$. For $T\geq1$ and $\ln B\geq TD$, Hoeffding gives

```math
p_B\leq \exp\!\left[-\frac{2(\ln B-TD)^2}{T(\ln 3)^2}\right].
\tag{L8}
```

To make the finite implication explicit, write $z=1-2\delta$ and choose $B=m(z/2)^2$. The square-root term in (L7) is then $z/4$. A successful binary test needs $\mathrm{TV}(P_0,\overline P)\geq z$. Thus $p_B\geq 3z/4$, and (L8) implies the following necessary condition:

```math
\ln m-2\ln(2/z)\leq
TD+(\ln 3)\sqrt{\frac{T}{2}\ln\frac{4}{3z}} .
```

If $\ln B\lt TD$, the same condition holds immediately. Zero queries give identical decision laws. For fixed error and $T\leq\ln(m)/D$, the square-root term is $O_\delta(\sqrt{\ln(m+1)})$. This proves the matching two-sided order around the leading term in (L1). A label estimator also solves binary detection, so the same unrestricted query lower bound applies.

Bell-label access and Pauli-channel simulation are established tools, as are sequential likelihood-ratio tests. The revision uses them to concentrate a fixed supply of initial purity on the sites still contributing evidence. The [related-work account](../references/RELATED_WORK.md) explains the comparison to fresh Bell probes and to reset-permitting channel-learning protocols.
