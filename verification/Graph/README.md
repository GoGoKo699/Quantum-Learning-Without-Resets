# Signal-bound figure

The [vector plot](signal_bounds.pdf) evaluates the proved one-clean-qubit signal envelopes as a function of the rescaled retention. For $`M=4^n-1`$ and $`0<\lambda<1`$, put

```math
z=\frac{\lambda}{M(1-\lambda)},\qquad
L(z)=\frac{\min\{1,z\}}{128},\qquad
U(z)=\min\{1,z/2\}.
```

The shaded region is the proved interval $`L(z)\le\Delta_1\le U(z)`$. Both axes are logarithmic. The lower envelope is attained up to the displayed universal constant by finite protocols; the upper envelope follows from the common-decision bound. The optimized signal ranges over all finite query budgets, and the curves do not assert a fixed-budget optimum. Exact conservation is treated separately in the [finite protocols](../../science/protocols.md).

## Reproduce

From the repository root:

```bash
python3 -m pip install -r verification/Graph/requirements.txt
python3 verification/Graph/generate_signal_bounds.py
```

The default output is `verification/Graph/signal_bounds.pdf`, independent of the working directory. An explicit output can be selected with `--output PATH`. The generator uses Python with NumPy 2.3.5 and Matplotlib 3.10.8, pinned in [requirements.txt](requirements.txt). It evaluates 1,203 rescaled-retention points, includes the two breakpoints $`z=1,2`$ exactly, and fixes the PDF creation/modification metadata for reproducible output.

## Scientific sources and checks

- [Access model](../../science/model.md): ordinary fixed-label queries, one initialized processor and the collision-purity resource.
- [Common decision](../../science/decision_bound.md): the inverse-label-count upper bound and its finite-query version.
- [Finite protocols](../../science/protocols.md): the attainable signal scale, its query cost and endpoint treatment.
- [Finite diagnostics](../README.md): physical gadget, feedback, scan and entropy checks.

The plotting values can be compared with `verification/protocols.py`: `mixture_distance_bound(n, strength)` is $`U(z)`$ for collision purity two, while `one_clean_bias_scale(n, strength)/128` is $`L(z)`$. The API's `strength` denotes $`\lambda`$ and `queries` denotes $`T`$. The plot contains analytical bounds rather than fitted or simulated optimal data.
