# A purity budget for individual output distances

The channel can repeatedly transfer a signal into protected memory. The proof must account for that transfer; a claim that every traceless operator contracts at each query would be false on the complete processor.

We first bound the average distance between each alternative output and the null. This also applies when the final measurement is chosen after the hidden label is revealed. The complementary [decision theorem](decision_bound.md) uses the additional requirement that one common measurement handles the unknown label. It gives stronger scaling away from conservation; neither displayed estimate is numerically stronger throughout the entire parameter range.

All notation and resources follow [the model](model.md).

## 1. Orthogonal Pauli sectors

On operators of $SA$, define

```math
\begin{aligned}
Q_0(X)&=\frac{I}{d}\otimes\operatorname{Tr}_S X,\\
Q_a(X)&=\frac{P_a}{d}\otimes
\operatorname{Tr}_S[(P_a\otimes I_A)X],
\qquad 1\le a\le M.
\end{aligned}
\tag{P1}
```

These are orthogonal projections for the Hilbert–Schmidt inner product, and

```math
Q_a^\dagger=Q_a,\quad Q_aQ_b=\delta_{ab}Q_a,
\quad \sum_{a=0}^{M}Q_a=\mathrm{id}.
\tag{P2}
```

Only $Q_0$ must itself be a channel. The individual nonidentity sector projections need not be positive; they are mathematical components of the physical map

```math
\mathcal E_{a,\lambda}\otimes\mathrm{id}_A=Q_0+\lambda Q_a.
\tag{P3}
```

The null retains the whole protected-workspace algebra. In particular, $Q_0$ is not full depolarization on $SA$.

A unital CPTP map contracts the Hilbert–Schmidt norm. For any operator $X$, the Kadison–Schwarz inequality and trace preservation give

```math
\|\mathcal C(X)\|_2^2
\le\operatorname{Tr}\mathcal C(X^\dagger X)
=\|X\|_2^2.
\tag{P4}
```

This standard fact is attributed to [Pérez-García et al. and Watrous](../references/RELATED_WORK.md#operator-norm-foundations). General CPTP maps need not satisfy it.

## 2. The theorem

For $0\le\lambda\lt1$ and every finite $T$,

```math
\frac1M\sum_{a=1}^{M}
\|\rho_T^a-\rho_T^0\|_2^2
\le
\frac{\lambda^2}{M(1-\lambda^2)}
\left[
\operatorname{Tr}(\rho_{\mathrm{in}}^2)
-\operatorname{Tr}((\rho_T^0)^2)
\right].
\tag{P5}
```

Consequently,

```math
\boxed{
\frac1M\sum_{a=1}^{M}
D_{\mathrm{tr}}(\rho_T^a,\rho_T^0)
\le
\min\!\left\{1,
\frac{\lambda}{2\sqrt{1-\lambda^2}}
\sqrt{\frac{\mathcal P-1}{M}}
\right\}.
}
\tag{P6}
```

The bound has no factor depending on the number of calls. The dimension of protected workspace appears only through the initial collision purity.

## 3. One-step signal growth

Let $\sigma=\rho_{t-1}^0$ and $\delta_a=\rho_{t-1}^a-\rho_{t-1}^0$. At the next call, with $\mathcal C=\mathcal C_t$,

```math
\delta'_a
=Q_0\mathcal C(\delta_a)
+\lambda Q_a\mathcal C(\delta_a+\sigma).
\tag{P7}
```

Put $x=Q_a\mathcal C(\delta_a)$ and $y=Q_a\mathcal C(\sigma)$. Orthogonality and (P4) imply

```math
\begin{aligned}
\|\delta'_a\|_2^2
&=\|Q_0\mathcal C(\delta_a)\|_2^2
+\lambda^2\|x+y\|_2^2\\
&\le\|\delta_a\|_2^2-\|x\|_2^2
+\lambda^2\|x+y\|_2^2.
\end{aligned}
\tag{P8}
```

Completing the square gives

```math
-\|x\|_2^2+\lambda^2\|x+y\|_2^2
=
-(1-\lambda^2)
\left\|x-\frac{\lambda^2}{1-\lambda^2}y\right\|_2^2
+\frac{\lambda^2}{1-\lambda^2}\|y\|_2^2.
\tag{P9}
```

This controls any signal that comes back from protected memory. No assumption that $x$ vanishes is made.

## 4. The null trajectory pays for all directions

The null state after this step is $\sigma'=Q_0\mathcal C(\sigma)$. Summing the source terms over all nonidentity Paulis yields

```math
\begin{aligned}
\sum_{a=1}^{M}\|Q_a\mathcal C(\sigma)\|_2^2
&=\|\mathcal C(\sigma)\|_2^2-\|\sigma'\|_2^2\\
&\le\|\sigma\|_2^2-\|\sigma'\|_2^2.
\end{aligned}
\tag{P10}
```

Every alternative uses the same null trajectory. Thus one can sum (P8)–(P10) over time without conditioning on an unknown-label-dependent state. Since every initial difference is zero, the right side telescopes and proves (P5).

Finally, $\|X\|_1\le\sqrt D\|X\|_2$, Cauchy–Schwarz over labels, and $\operatorname{Tr}((\rho_T^0)^2)\ge1/D$ give

```math
\begin{aligned}
\frac1M\sum_a D_{\mathrm{tr}}(\rho_T^a,\rho_T^0)
&\le\frac{\sqrt D}{2}
\sqrt{\frac1M\sum_a\|\rho_T^a-\rho_T^0\|_2^2}\\
&\le
\frac{\lambda}{2\sqrt{1-\lambda^2}}
\sqrt{\frac{D\operatorname{Tr}(\rho_{\mathrm{in}}^2)-1}{M}}.
\end{aligned}
```

This proves (P6).

## 5. Meaning and limits

If $\mathcal P=1$, the entire processor starts maximally mixed and remains so under every allowed operation. Both the theorem and the actual signal are exactly zero.

If the processor starts with one pure qubit and all other qubits maximally mixed, then $\mathcal P=2$. Equation (P6) already makes constant-error detection impossible unless $1-\lambda=O(M^{-1})$.

The denominator $1-\lambda^2$ is not controlled at $\lambda=1$. This is a physical boundary of this estimate: an exactly preserved mode admits an arbitrarily accurate single-pointer scan as query time increases. The finite-time decision bound remains meaningful at that endpoint.

This theorem bounds the **average of the individual trace distances**. It allows a different optimal effect for each alternative. The [next theorem](decision_bound.md) improves the hidden-label decision scaling away from conservation by controlling a common effect in both forward and backward time.

The broad idea of charging noisy-oracle information gain to purity loss has prior antecedents in [Regev–Schiff and Buchholz–Kübler–Schölkopf](../references/RELATED_WORK.md#noisy-oracles-and-purity-loss). Here the completely depolarizing null and orthogonal hidden Pauli sectors make the total source energy finite even with protected memory and unlimited query time.
