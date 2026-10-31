# A uniform bound for one final decision

A common final measurement permits a complementary bound, with stronger scaling away from conservation. We exploit the common effect by following both the state entering the null process and the effect propagated backward through that process.

The proof is a finite-dimensional linear-algebra argument on Hilbert–Schmidt operator space. Its auxiliary port variables are mathematical objects; the algorithm is not supplied with environment outputs or additional channels.

## 1. Statement

Let $h_T(\lambda)=\sum_{j=0}^{T-1}\lambda^j$, with $h_0(\lambda)=0$. Under [the complete-processor model](model.md),

```math
\boxed{
D_{\mathrm{tr}}(\bar\rho_T,\rho_T^0)
\le
\min\!\left\{1,
\frac{\lambda h_T(\lambda)\sqrt{\mathcal P-1}}{2M}
\right\},
\qquad 0\le\lambda\le1.
}
\tag{D1}
```

For $0\le\lambda\lt1$, this implies the query-independent bound

```math
\boxed{
D_{\mathrm{tr}}(\bar\rho_T,\rho_T^0)
\le
\min\!\left\{1,
\frac{\lambda\sqrt{\mathcal P-1}}{2M(1-\lambda)}
\right\}.
}
\tag{D2}
```

At $\lambda=1$, (D1) reads $D_{\mathrm{tr}}\le
\min\{1,T\sqrt{\mathcal P-1}/(2M)\}$. This is a necessary query bound, not a query-optimality claim.

Equation (D2) is a **mixture** trace-distance bound. It does not assert the same bound for $M^{-1}\sum_aD_{\mathrm{tr}}(\rho_T^a,\rho_T^0)$. For that quantity use [the separate purity theorem](purity_bound.md). Convexity makes that individual-distance estimate a valid mixture bound too, so one may take the smaller of the two. Before capping at one, (D2) is stronger precisely when $M(1-\lambda)\ge1+\lambda$, for nonzero strength and excess purity.

## 2. Open the signal sector

Use the orthogonal projections $Q_0,Q_a$ from (P1). Fix a label $a$. For arbitrary operator $x_0$ and port inputs $v_t\in\operatorname{ran}Q_a$, define

```math
u_t=Q_a\mathcal C_t(x_{t-1}),
\qquad
x_t=Q_0\mathcal C_t(x_{t-1})+v_t,
\qquad 1\le t\le T.
\tag{D3}
```

Because $Q_0$ and $Q_a$ have orthogonal ranges,

```math
\begin{aligned}
\|x_t\|_2^2+\|u_t\|_2^2
&=\|Q_0\mathcal C_t(x_{t-1})\|_2^2
+\|v_t\|_2^2+\|Q_a\mathcal C_t(x_{t-1})\|_2^2\\
&\le\|x_{t-1}\|_2^2+\|v_t\|_2^2.
\end{aligned}
\tag{D4}
```

The last step uses Hilbert–Schmidt contraction of the unital CPTP control. Summing in time proves that the map

```math
(x_0,v_1,\ldots,v_T)
\longmapsto (x_T,u_1,\ldots,u_T)
\tag{D5}
```

is a contraction between Hilbert-space direct sums. Write its blocks as

```math
x_T=A x_0+B_a v,\qquad
u=F_a x_0+G_a v.
\tag{D6}
```

Here $A=Q_0\mathcal C_T\cdots Q_0\mathcal C_1$ is the null evolution and does not depend on $a$. The matrix $G_a$ is strictly lower triangular in the time index, because $u_t$ depends only on $v_1,\ldots,v_{t-1}$. Therefore $G_a^T=0$, where the superscript $T$ here denotes the integer power equal to the number of calls. Every block of a contraction has operator norm at most one, so $\|G_a\|_{2\to2}\le1$.

Close the ports with $v=\lambda u$. Equations (D3) then reproduce the alternative evolution exactly. Nilpotence gives

```math
R_a(\lambda):=(I-\lambda G_a)^{-1}
=\sum_{j=0}^{T-1}\lambda^jG_a^j,
\qquad
\|R_a(\lambda)\|_{2\to2}\le h_T(\lambda).
\tag{D7}
```

In particular, no convergence limit or infinite-time inverse is needed at $\lambda=1$. The difference from the null output is

```math
\rho_T^a-\rho_T^0
=\lambda B_aR_a(\lambda)F_a(\rho_{\mathrm{in}}).
\tag{D8}
```

## 3. One forward budget for every hidden label

With all ports zero, set $x_t^0=Q_0\mathcal C_t(x_{t-1}^0)$. Then the time-$t$ component of $F_a x_0$ is $Q_a\mathcal C_t(x_{t-1}^0)$. Orthogonality gives

```math
\begin{aligned}
\sum_a\|F_a x_0\|_2^2
&=\sum_{t=1}^T
\left[
\|\mathcal C_t(x_{t-1}^0)\|_2^2-\|x_t^0\|_2^2
\right]\\
&\le\|x_0\|_2^2-\|A x_0\|_2^2
\le\|x_0\|_2^2.
\end{aligned}
\tag{D9}
```

This statement holds for arbitrary operators, not just density matrices. The same null trajectory supplies all labels.

## 4. A backward budget for the effect

Fix an arbitrary terminal operator $E$ and set $y_T=E$,

```math
y_{t-1}=\mathcal C_t^\dagger Q_0(y_t),
\qquad t=T,\ldots,1.
\tag{D10}
```

The adjoint of a unital trace-preserving CP map is again unital and trace preserving, and hence also contracts the Hilbert–Schmidt norm. The response of the final effect to an inserted port input at time $t$ is

```math
(B_a^\dagger E)_t=Q_a(y_t).
\tag{D11}
```

For example, the terminal component is $Q_aE$, while the preceding component is $Q_a\mathcal C_T^\dagger Q_0E$. This checks the time ordering and includes the last port.

Thus

```math
\begin{aligned}
\sum_a\|B_a^\dagger E\|_2^2
&=\sum_{t=1}^T\|(I-Q_0)y_t\|_2^2\\
&\le\sum_{t=1}^T
\left(\|y_t\|_2^2-\|y_{t-1}\|_2^2\right)
\le\|E\|_2^2.
\end{aligned}
\tag{D12}
```

A protected memory can preserve both signals and effects. The estimate does not ask that every vector contract strictly; it bounds the total energy that can enter the queried Pauli sectors.

## 5. Center, average and optimize

Unitality and trace preservation allow us to replace the input and effect by

```math
x_0=\rho_{\mathrm{in}}-\frac{I}{D},
\qquad
E_0=E-\frac{\operatorname{Tr}E}{D}I
\tag{D13}
```

without changing any signal. This also follows directly from $F_a(I)=0$ and $B_a^\dagger(I)=0$.

Apply (D7)–(D12), first for each label and then Cauchy–Schwarz across labels:

```math
\begin{aligned}
\left|
\operatorname{Tr}E(\bar\rho_T-\rho_T^0)
\right|
&\le\frac{\lambda h_T(\lambda)}M
\sum_a\|B_a^\dagger E_0\|_2\|F_a x_0\|_2\\
&\le\frac{\lambda h_T(\lambda)}M
\|E_0\|_2\|x_0\|_2.
\end{aligned}
\tag{D14}
```

For an effect $0\le E\le I$, its eigenvalues lie in $[0,1]$. Their variance is at most $1/4$. Therefore

```math
\|E_0\|_2\le\frac{\sqrt D}{2},
\qquad
\|x_0\|_2=\sqrt{\frac{\mathcal P-1}{D}}.
\tag{D15}
```

Taking the optimal effect proves (D1). Bounding the finite geometric sum by $(1-\lambda)^{-1}$ proves (D2).

## 6. Consequences with explicit error conventions

If a single decision rule has error at most $\delta\lt1/2$ under the null and every alternative, then (M9) and (D2) require

```math
1-2\delta
\le
\frac{\lambda\sqrt{\mathcal P-1}}{2M(1-\lambda)}.
\tag{D16}
```

For one clean qubit, constant error below one half is therefore impossible along any sequence with $M(1-\lambda)/\lambda\to\infty$. At fixed $0\lt\lambda\lt1$, its equal-prior success advantage above one half is at most $\lambda/[4M(1-\lambda)]$ for any number of calls.

For an initialization of $c$ pure qubits and otherwise mixed qubits, the same necessary condition is

```math
2^c-1\ge
4M^2(1-2\delta)^2\frac{(1-\lambda)^2}{\lambda^2}.
\tag{D17}
```

When $\lambda$ and $\delta$ are fixed away from their trivial endpoints, this gives $c\ge4n-O(1)$. It is a converse for initial purity, not a matching clean-qubit complexity theorem.

For $\lambda=1$, (D1) instead requires $T\sqrt{\mathcal P-1}\ge2M(1-2\delta)$. The [constructive scan](protocols.md) meets the one-clean-qubit **feasibility threshold** near this endpoint. Its query count is larger than this necessary lower bound.

The full one-clean-qubit optimum over finite query budgets is determined up to universal constants in [the protocol theorem](protocols.md). Its matching quantity is the common-decision mixture distinguishability, not label identification or complete tomography.
