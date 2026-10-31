# Finite algorithms and the one-clean-qubit optimum

The upper bounds concern a single initialized processor. The constructions below use exactly one initially pure pointer and otherwise maximally mixed registers. The strength $\lambda$ is known. Every call is an ordinary use of the unknown channel.

The first construction attains the whole decision-bias scaling. A second, coherent scan gives a specified worst-case error near an exactly conserved mode. These are different guarantees: a small nonzero bias is not automatically success probability $2/3$.

## 1. Optimal distinguishability over finite query budgets

For $M=4^n-1$ and $0\le\lambda\lt1$, let

```math
s=\frac{\lambda}{M(1-\lambda)}.
```

The quantity $\Delta_1(n,\lambda)$ is defined in (M10). The [decision converse](decision_bound.md) and the algorithms below establish

```math
\begin{aligned}
\boxed{
\frac1{128}\min\{1,s\}
\le\Delta_1(n,\lambda)
\le\min\{1,s/2\}.
}
\end{aligned}
\tag{A1}
```

At $\lambda=0$, the value is zero. At $\lambda=1$, its supremum is one. Every algorithm used for the lower bounds has a finite number of calls; perfect finite-query discrimination is not asserted at the endpoint.

The two constructive branches use

```math
\begin{aligned}
Q&=
\begin{cases}
1,&0\lt\lambda\le1/2,\\
M\left\lceil 32/g\right\rceil
\le33M\min\{(1-\lambda)^{-1},M\},
&1/2\lt\lambda\le1,
\end{cases}\\
g&=\max\{1-\lambda,1/M\}.
\end{aligned}
\tag{A2}
```

At $\lambda=1$, the minimum on the right is $M$. These are sufficient query counts. No matching query-complexity theorem is claimed.

## 2. Extracting a known trial mode onto a pointer

Initialize $S$ in $I/d$ and let the pointer state be $\sigma$. For a known nonidentity Pauli $P_b$, use

```math
\begin{aligned}
V_b=I_S\otimes|0\rangle\langle0|
+P_b\otimes|1\rangle\langle1|.
\end{aligned}
\tag{A3}
```

Apply $V_b$, query the unknown channel on $S$, and apply $V_b$ again. The exact effect is

```math
\begin{aligned}
\frac Id\otimes\sigma
\longmapsto
\frac Id\otimes\mathcal Z_{\eta_b}(\sigma),
\end{aligned}
\tag{A4}
```

where $\mathcal Z_\eta$ keeps the pointer's diagonal entries and multiplies its off-diagonal entries by $\eta$. Under the null $\eta_b=0$. Under alternative $a$, $\eta_b=\lambda$ if $b=a$, and zero otherwise.

To verify this, expand $\sigma$ into its two-by-two pointer blocks. The diagonal query blocks are $I/d$. After the first $V_b$, each off-diagonal block is proportional to $P_b/d$. The unknown channel maps that Pauli to $\eta_bP_b$, and the final $V_b$ restores the block to $\eta_bI/d$. Thus $S$ returns exactly to its initial mixed state, uncorrelated with the pointer. The statement remains true when the pointer is correlated with other protected registers, by linearity on its operator-valued blocks.

This is a controlled **known** gate surrounding an ordinary unknown-channel call. It does not assume controlled-channel or dilation access. For $b=0$, the identity Pauli, the gadget leaves the pointer unchanged under either hypothesis.

## 3. One-query construction for small strength

For $0\lt\lambda\le1/2$, put the clean pointer in $|+\rangle$. Supply a $2n$-qubit maximally mixed label register covering all $d^2=M+1$ Pauli strings, including the identity. Condition the known gates in (A3) on this label and make one intervening query. Ignore the label in the final pointer $X$ measurement.

The pointer's $X$ expectations are

```math
\begin{aligned}
x_0=\frac1{M+1},\qquad
x_a=\frac{1+\lambda}{M+1}.
\end{aligned}
\tag{A5}
```

The identity trial contributes in both cases; exactly one additional trial contributes under every alternative. The fixed measurement has probability gap

```math
\begin{aligned}
\Delta_{\mathrm{small}}=\frac{\lambda}{2(M+1)}
=\frac{M(1-\lambda)}{2(M+1)}s
\ge\frac3{16}s.
\end{aligned}
\tag{A6}
```

Here $M\ge3$ and $s\le1/3$. This proves more than the lower constant required in (A1) in this regime.

The implementation uses $n$ mixed query qubits, $2n$ mixed label qubits and one pure pointer. Its collision purity is exactly two. Conditional Pauli synthesis costs $O(n)$ known gates, with no uniformly sampled non-power-of-two classical seed required.

## 4. A finite weak-rotation scan for larger strength

For $1/2\lt\lambda\le1$, define

```math
\begin{aligned}
g&=\max\{1-\lambda,1/M\},&
\ell&=1-g,\\
h&=\frac{1+\ell}{g},&
L&=\left\lceil\frac{32}{g}\right\rceil,\\
t&=\frac1{16(M+h)},&
u&=\frac{2t}{L},\qquad
\theta=\arcsin\sqrt u.
\end{aligned}
\tag{A7}
```

After each gadget, apply the known pointer dephasing $\mathcal Z_{\ell/\lambda}$. It changes the active parameter from $\lambda$ to $\ell$ and leaves the inactive parameter zero. This deliberate clipping produces simple uniform finite constants.

Start the pointer in $|0\rangle$. Enumerate all $M$ nonidentity Pauli candidates. For each candidate, repeat $L$ times: rotate the pointer by $R_y(\theta)$, run its gadget, and apply the clipping dephasing. Completely dephase the pointer in the $Z$ basis at the end of each block. Measure $Z$ once after the final block.

Boundary dephasing preserves the populations carrying the accumulated signal; it does not reset the pointer. Under the admitted unital-control model, only the $n$ mixed query qubits and one pointer need persist.

For $c=\cos\theta$ and $v=\sin\theta$, the real Bloch vector transforms in one step as

```math
\begin{aligned}
\begin{pmatrix}x\\z\end{pmatrix}
\longmapsto
A_\eta
\begin{pmatrix}x\\z\end{pmatrix},
\qquad
A_\eta=
\begin{pmatrix}
\eta c&\eta v\\
-v&c
\end{pmatrix}.
\end{aligned}
\tag{A8}
```

Put $k_0=c^L$ and $k_\ell=(A_\ell^L)_{22}$. Every block begins with zero $x$ component. Therefore the exact final pointer values are

```math
\begin{aligned}
z_0=k_0^M,\qquad
z_a=k_0^{M-1}k_\ell,
\end{aligned}
\tag{A9}
```

independent of the active label's position. The final outcome one has probability gap

```math
\begin{aligned}
\Delta_{\mathrm{scan}}
=\frac{k_0^{M-1}}2(k_0-k_\ell).
\end{aligned}
\tag{A10}
```

### Finite lower bound

The characteristic roots of $A_\ell$ are

```math
\begin{aligned}
r_\pm=
\frac{(1+\ell)c\pm g\sqrt{1-h^2u}}2.
\end{aligned}
\tag{A11}
```

Because $h\ge3$, $h/L\le1/16$ and $t\le1/(16h)$,

```math
\begin{aligned}
h^2u=\frac{2h^2t}{L}\le\frac{h}{8L}\le\frac1{128}.
\end{aligned}
\tag{A12}
```

The roots are real, distinct and positive. Their product is $\ell$ and their sum is positive. The sequence $(A_\ell^j)_{22}$ starts at $1,c$, so

```math
\begin{aligned}
k_\ell=(1+b)r_+^L-b r_-^L,\qquad
b=\frac12\left(\frac{c}{\sqrt{1-h^2u}}-1\right).
\end{aligned}
\tag{A13}
```

Using $(1-y)^{-1/2}\le1+2y$ for $0\le y\le1/2$ gives $0\le b\le h^2u$. Also,

```math
\begin{aligned}
r_+\le1-\frac{hu}{2}=1-\frac{ht}{L}.
\end{aligned}
\tag{A14}
```

This follows by applying $\sqrt{1-y}\le1-y/2$ separately to the two square roots in (A11). It implies

```math
\begin{aligned}
k_\ell\le r_+^L+b
\le1-ht+\frac{(ht)^2}{2}+b.
\end{aligned}
\tag{A15}
```

Bernoulli's inequality gives $k_0=(1-u)^{L/2}\ge1-t$. Let $\tau=(h-1)t$. Then

```math
\begin{aligned}
\frac{(ht)^2}{2\tau}
\le\frac3{64},
\qquad
\frac b\tau
\le\frac{2h^2}{L(h-1)}
\le\frac3{16}.
\end{aligned}
\tag{A16}
```

Thus

```math
\begin{aligned}
k_0-k_\ell\ge\frac{49}{64}\tau,\qquad
k_0^{M-1}\ge1-(M-1)t\ge\frac{15}{16}.
\end{aligned}
\tag{A17}
```

Substitution in (A10) proves the explicit finite inequality

```math
\begin{aligned}
\Delta_{\mathrm{scan}}
\ge\frac{\tau}{4}
=\frac{\ell}{32(Mg+1+\ell)}.
\end{aligned}
\tag{A18}
```

If no clipping occurred, then $\ell=\lambda$ and $g=1-\lambda$. For $\lambda\ge1/2$,

```math
\begin{aligned}
\frac{\lambda}{M(1-\lambda)+1+\lambda}
\ge\frac14\min\!\left\{1,\frac{\lambda}{M(1-\lambda)}\right\}.
\end{aligned}
\tag{A19}
```

Indeed, when $M(1-\lambda)\ge\lambda$, use $1+\lambda\le3\lambda\le3M(1-\lambda)$. Otherwise use $\lambda/(1+2\lambda)\ge1/4$.

If clipping occurred, $Mg=1$ and $\ell=1-1/M\ge2/3$, so (A18) is at least $1/128$. This proves the lower bound in (A1). Finally, $ML\le33M/g$ proves (A2).

## 5. Specified worst-case error near conservation

For a target error $0\lt\delta\lt1/2$, use the same gadget without clipping. In each candidate block, take $L$ rotations with angle $\theta=\pi/L$, and completely dephase in the $Z$ basis at the block boundary. Initialize the pointer in $|0\rangle$. This boundary operation makes the final populations independent of the active label's position, also when $\lambda\lt1$.

At $\lambda=1$, the active block is exactly $R_y(\pi)$ and flips the pointer. With $c=\cos(\pi/L)$,

```math
\begin{aligned}
z_0=c^{ML},\qquad z_a=-c^{(M-1)L}.
\end{aligned}
\tag{A20}
```

Later inactive blocks preserve the flipped sign. Both error probabilities are at most $M\pi^2/(4L)$, using $1-c^q\le q(1-c)\le q\pi^2/(2L^2)$.

For $\lambda=1-\gamma$, only the $L$ steps in the active block change. The diamond distance between $\mathcal Z_{1-\gamma}$ and the identity is $\gamma$. A hybrid argument therefore changes any final probability by at most $L\gamma/2$. Hence

```math
\begin{aligned}
p_{\mathrm{err,worst}}
\le
\max\left\{
\frac{1-c^{ML}}2,\,
\frac{1-c^{(M-1)L}}2+\frac{L\gamma}2
\right\}.
\end{aligned}
\tag{A21}
```

Take $L=\lceil\pi^2M/(2\delta)\rceil$ and $\gamma\le\delta/L$. Then both errors are at most $\delta$. In particular,

```math
\begin{aligned}
L=100M,\qquad 1-\lambda\le10^{-3}/M
\quad\Longrightarrow\quad
p_{\mathrm{err,worst}}\lt0.097.
\end{aligned}
\tag{A22}
```

The query count is $ML=O_\delta(M^2)$. The converse (D16) and this construction match the **scale** $1-\lambda\asymp M^{-1}$ for a specified fixed error, with different error-dependent constants. They do not determine the exact constant at the transition.

At $\lambda=1$, taking arbitrarily large finite $L$ in (A20) drives both errors to zero, establishing $\Delta_1(n,1)=1$ as a supremum.

## 6. Implementation and accuracy accounting

A known dephasing $\mathcal Z_q$ is unital. It can also be implemented using only known unitaries and an initially maximally mixed coin: condition opposite rotations $R_z(\phi)$ and $R_z(-\phi)$ on the coin, where $\cos\phi=q$, and ignore that coin thereafter. Preallocate one coin per use, retain all coins, and let the final POVM ignore them. This requires $O(Q)$ extra mixed qubits and still only one pure qubit. Correlations with used coins do not alter the analyzed reduced evolution because those coins are never used again.

The abstract unital-control implementation has $O(nQ)$ known controlled-Pauli and one-qubit gates. Counts treat parameterized rotations as primitives. For an implementation with $N_g$ imperfect known gates, if each gate has diamond error at most $\varepsilon_g$, a hybrid argument bounds the final probability error by $N_g\varepsilon_g/2$. Choosing this smaller than a fixed fraction of the desired probability gap preserves the claimed scaling. We do not claim an optimized fault-tolerant synthesis cost or hardware runtime.

For every construction, the pointer distributions are the same for all hidden labels. A gap $\Delta$ gives equal-prior success $(1+\Delta)/2$. If balanced errors are needed, final classical postprocessing can balance them while keeping at least half the gap, giving worst-case success at least $1/2+\Delta/4$. This is part of the final POVM, with no intermediate purity supply. The small constant in (A1) alone is not a $2/3$-success guarantee; use (A21) for a specified error.

The one-query trial, serial candidate scan, Zeno discrimination and weak driving have established antecedents. Their relationship to this construction is explained in [related work](../references/RELATED_WORK.md). The new matched statement is the finite-purity decision-bias law under the exact resource model.
