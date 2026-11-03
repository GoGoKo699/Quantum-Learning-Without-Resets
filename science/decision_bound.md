# A uniform bound for one final decision

A common final measurement permits a complementary bound, with stronger scaling away from conservation. We exploit the common effect by following both the state entering the null process and the effect propagated backward through that process.

The proof is a finite-dimensional linear-algebra argument on Hilbert–Schmidt operator space. Its auxiliary port variables are mathematical objects; the algorithm is not supplied with environment outputs or additional channels.

## 1. Statement

Let $h_T(\lambda)=\sum_{j=0}^{T-1}\lambda^j$, with $h_0(\lambda)=0$. Under [the complete-processor model](model.md),

```math
\begin{aligned}
\boxed{
D_{\mathrm{tr}}(\bar\rho_T,\rho_T^0)
\le
\min\!\left\{1,
\frac{\lambda h_T(\lambda)\sqrt{\mathcal P-1}}{2M}
\right\},
\qquad 0\le\lambda\le1.
}
\end{aligned}
\tag{D1}
```

For $0\le\lambda\lt1$, this implies the query-independent bound

```math
\begin{aligned}
\boxed{
D_{\mathrm{tr}}(\bar\rho_T,\rho_T^0)
\le
\min\!\left\{1,
\frac{\lambda\sqrt{\mathcal P-1}}{2M(1-\lambda)}
\right\}.
}
\end{aligned}
\tag{D2}
```

At $\lambda=1$, (D1) reads $D_{\mathrm{tr}}\le \min\lbrace1,T\sqrt{\mathcal P-1}/(2M)\rbrace$. This is a necessary query bound, not a query-optimality claim.

Equation (D2) is a **mixture** trace-distance bound. It does not assert the same bound for $M^{-1}\sum_{e\ne0}D_{\mathrm{tr}}(\rho_T^e,\rho_T^0)$. For that quantity use [the separate purity theorem](purity_bound.md). Convexity makes that individual-distance estimate a valid mixture bound too, so one may take the smaller of the two. Before capping at one, (D2) is stronger precisely when $M(1-\lambda)\ge1+\lambda$, for nonzero strength and excess purity.

## 2. Open the signal sector

Use the orthogonal projections $Q_0,Q_e$ from (P1). Fix a label $e$. For arbitrary operator $x_0$ and port inputs $v_t\in\mathrm{ran}Q_e$, define

```math
\begin{aligned}
u_t=Q_e\mathcal C_t(x_{t-1}),
\qquad
x_t=Q_0\mathcal C_t(x_{t-1})+v_t,
\qquad 1\le t\le T.
\end{aligned}
\tag{D3}
```

Because $Q_0$ and $Q_e$ have orthogonal ranges,

```math
\begin{aligned}
\|x_t\|_2^2+\|u_t\|_2^2
&=\|Q_0\mathcal C_t(x_{t-1})\|_2^2
+\|v_t\|_2^2+\|Q_e\mathcal C_t(x_{t-1})\|_2^2\\
&\le\|x_{t-1}\|_2^2+\|v_t\|_2^2.
\end{aligned}
\tag{D4}
```

The last step uses Hilbert–Schmidt contraction of the unital CPTP control. Summing in time proves that the map

```math
\begin{aligned}
(x_0,v_1,\ldots,v_T)
\longmapsto (x_T,u_1,\ldots,u_T)
\end{aligned}
\tag{D5}
```

is a contraction between Hilbert-space direct sums. Write its blocks as

```math
\begin{aligned}
x_T=\mathcal N x_0+B_e v,\qquad
u=F_e x_0+G_e v.
\end{aligned}
\tag{D6}
```

Here $\mathcal N=Q_0\mathcal C_T\cdots Q_0\mathcal C_1$ is the null evolution and does not depend on $e$. The matrix $G_e$ is strictly lower triangular in the time index, because $u_t$ depends only on $v_1,\ldots,v_{t-1}$. Therefore $G_e^T=0$, where the superscript $T$ here denotes the integer power equal to the number of calls. Every block of a contraction has operator norm at most one, so $\lVert G_e\rVert_{2\to2}\le1$.

Close the ports with $v=\lambda u$. Equations (D3) then reproduce the alternative evolution exactly. Nilpotence gives

```math
\begin{aligned}
\mathcal R_e(\lambda):=(I-\lambda G_e)^{-1}
=\sum_{j=0}^{T-1}\lambda^jG_e^j,
\qquad
\|\mathcal R_e(\lambda)\|_{2\to2}\le h_T(\lambda).
\end{aligned}
\tag{D7}
```

In particular, no convergence limit or infinite-time inverse is needed at $\lambda=1$. The difference from the null output is

```math
\begin{aligned}
\rho_T^e-\rho_T^0
=\lambda B_e\mathcal R_e(\lambda)F_e(\rho_{\mathrm{in}}).
\end{aligned}
\tag{D8}
```

## 3. One forward budget for every hidden label

With all ports zero, set $x_t^0=Q_0\mathcal C_t(x_{t-1}^0)$. Then the component at time $t$ of $F_e x_0$ is $Q_e\mathcal C_t(x_{t-1}^0)$. Orthogonality gives

```math
\begin{aligned}
\sum_{e\ne0}\|F_e x_0\|_2^2
&=\sum_{t=1}^T
\left[
\|\mathcal C_t(x_{t-1}^0)\|_2^2-\|x_t^0\|_2^2
\right]\\
&\le\|x_0\|_2^2-\|\mathcal N x_0\|_2^2
\le\|x_0\|_2^2.
\end{aligned}
\tag{D9}
```

This statement holds for arbitrary operators, not just density matrices. The same null trajectory supplies all labels.

## 4. A backward budget for the effect

Fix an arbitrary terminal operator $F$ and set $y_T=F$,

```math
\begin{aligned}
y_{t-1}=\mathcal C_t^\dagger Q_0(y_t),
\qquad t=T,\ldots,1.
\end{aligned}
\tag{D10}
```

The adjoint of a unital trace-preserving CP map is again unital and trace preserving, and hence also contracts the Hilbert–Schmidt norm. The response of the final effect to an inserted port input at time $t$ is

```math
\begin{aligned}
(B_e^\dagger F)_t=Q_e(y_t).
\end{aligned}
\tag{D11}
```

For example, the terminal component is $Q_eF$, while the preceding component is $Q_e\mathcal C_T^\dagger Q_0F$. This checks the time ordering and includes the last port.

Thus

```math
\begin{aligned}
\sum_{e\ne0}\|B_e^\dagger F\|_2^2
&=\sum_{t=1}^T\|(I-Q_0)y_t\|_2^2\\
&\le\sum_{t=1}^T
\left(\|y_t\|_2^2-\|y_{t-1}\|_2^2\right)
\le\|F\|_2^2.
\end{aligned}
\tag{D12}
```

A protected memory can preserve both signals and effects. The estimate does not ask that every vector contract strictly; it bounds the total energy that can enter the queried Pauli sectors.

## 5. Center, average and optimize

Unitality and trace preservation allow us to replace the input and effect by

```math
\begin{aligned}
x_0=\rho_{\mathrm{in}}-\frac{I}{D},
\qquad
F_0=F-\frac{\mathrm{Tr}F}{D}I
\end{aligned}
\tag{D13}
```

without changing any signal. This also follows directly from $F_e(I)=0$ and $B_e^\dagger(I)=0$.

Apply (D7)–(D12), first for each label and then Cauchy–Schwarz across labels:

```math
\begin{aligned}
\left|
\mathrm{Tr}F(\bar\rho_T-\rho_T^0)
\right|
&\le\frac{\lambda h_T(\lambda)}M
\sum_{e\ne0}\|B_e^\dagger F_0\|_2\|F_e x_0\|_2\\
&\le\frac{\lambda h_T(\lambda)}M
\|F_0\|_2\|x_0\|_2.
\end{aligned}
\tag{D14}
```

For an effect $0\le F\le I$, its eigenvalues lie in $[0,1]$. Their variance is at most $1/4$. Therefore

```math
\begin{aligned}
\|F_0\|_2\le\frac{\sqrt D}{2},
\qquad
\|x_0\|_2=\frac{\sqrt{\mathcal P-1}}{\sqrt D}.
\end{aligned}
\tag{D15}
```

Taking the optimal effect proves (D1). Bounding the finite geometric sum by $(1-\lambda)^{-1}$ proves (D2).

## 6. Consequences with explicit error conventions

If a single decision rule has error at most $\delta\lt1/2$ under the null and every alternative, then (M9) and (D2) require

```math
\begin{aligned}
1-2\delta
\le
\frac{\lambda\sqrt{\mathcal P-1}}{2M(1-\lambda)}.
\end{aligned}
\tag{D16}
```

For one clean qubit, constant error below one half is therefore impossible along any sequence with $M(1-\lambda)/\lambda\to\infty$. At fixed $0\lt\lambda\lt1$, its equal-prior success advantage above one half is at most $\lambda/[4M(1-\lambda)]$ for any number of calls.

For an initialization of $c$ pure qubits and otherwise mixed qubits, the same necessary condition is

```math
\begin{aligned}
2^c-1\ge
4M^2(1-2\delta)^2\frac{(1-\lambda)^2}{\lambda^2}.
\end{aligned}
\tag{D17}
```

When $\lambda$ and $\delta$ are fixed away from their trivial endpoints, this gives $c\ge4n-O(1)$ for the full $M=4^n-1$ family. Restricted label sets are treated below. It is a converse for initial purity, not a matching clean-qubit complexity theorem.

For $\lambda=1$, (D1) instead requires $T\sqrt{\mathcal P-1}\ge2M(1-2\delta)$. The [constructive scan](protocols.md) meets the one-clean-qubit **feasibility threshold** near this endpoint. Its query count is larger than this necessary lower bound.

The full one-clean-qubit optimum over finite query budgets is determined up to universal constants in [the protocol theorem](protocols.md). Its matching quantity is the common-decision mixture distinguishability, not label identification or complete tomography.

## 7. Restricted labels: the immediate purity corollary

The same proof applies to any specified set $`\mathcal L`$ of $`m`$ nonidentity Pauli labels. In (D9) and (D12), the source sums over $`\mathcal L`$ are bounded by the corresponding full-sector sums. For $`\bar\rho_T^{\mathcal L}=m^{-1}\sum_{e\in\mathcal L}\rho_T^e`$,

```math
\begin{aligned}
D_{\mathrm{tr}}(\bar\rho_T^{\mathcal L},\rho_T^0)
\le\min\left\{1,
\frac{\lambda h_T(\lambda)\sqrt{\mathcal P-1}}{2m}\right\}.
\end{aligned}
\tag{D18}
```

For all $`3n`$ weight-one labels and $`\lambda=1/2`$, the query-independent version is

```math
\begin{aligned}
D_{\mathrm{tr}}(\bar\rho_T^{\mathcal L},\rho_T^0)
\le\min\left\{1,\frac{\sqrt{\mathcal P-1}}{6n}\right\}.
\end{aligned}
\tag{D19}
```

Thus error at most $`1/3`$ requires $`c\ge\log_2(1+4n^2)`$ for clean/mixed product initialization. This is an immediate restriction of the existing theorem, not the stronger entropy result. The [shared entropy proof](entropy_bound.md) instead gives $`C\ge4n/3`$, where $`C`$ is the initial von Neumann entropy deficit in bits. It uses a reverse-relative-entropy query coupling and complementary local axes. Both bounds remain valid; neither is uniformly sharper at every purity. No matching arbitrary-purity upper protocol is asserted.
