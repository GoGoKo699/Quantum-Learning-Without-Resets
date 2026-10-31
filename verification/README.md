# Verification and reproducible finite calculations

The analytical proofs are in [science/](../science/README.md). The code here reconstructs finite instances using independent representations, with deterministic random controls where appropriate. It checks the conventions and nontrivial identities on which those proofs depend.

## Run

From the repository root, with Python 3.12:

```bash
python -m pip install -r verification/requirements.txt
python verification/run_checks.py
```

The runner writes [results.json](results.json) and raises an assertion if a tested quantity is non-finite or an identity or inequality exceeds its stated tolerance. The committed run used NumPy 2.3.5 and seed 2026103102. Floating-point residuals may vary slightly with numerical libraries.

## What the checks reconstruct

| Check | Independent comparison | Committed cases |
|---|---|---:|
| Purity potential | Full density-matrix oracle trajectories and unital controls versus the telescoping Hilbert–Schmidt bound | 360 |
| Exact pointer gadget | Full controlled-Pauli/query/uncompute circuit versus the predicted product with a dephased pointer | 702 |
| Open-port proof | Direct oracle superoperator product versus the explicit feedback response; block contraction, nilpotence and both aggregate energy budgets | 126 port instances |
| Common-decision distance | Density outputs under the uniform fixed-label mixture versus the finite-query purity bound | 270 states |
| Finite crossover | Matrix powers, characteristic-root formula, proof inequalities and the implemented finite algorithm | 51 parameter points |
| Full scan circuits | Density-matrix circuit with boundary dephasing versus its reduced Bloch formula | 12 |
| One-query mixed-label circuit | Full label/system/pointer circuit versus the claimed fixed pointer expectations | 16 |
| Near-unit scan | Explicit block products at first, middle and last hidden positions versus scalar outputs and the robust error certificate | 87 |
| Endpoint and gate conventions | Zero/one strength, zero calls, one-call saturation and explicit local controlled-Pauli synthesis | 36 endpoint cases, plus local gate checks |
| Numerical guards | Injected non-finite values, out-of-domain calls and supported length-boundary evaluations | 4 non-finite controls, 8 rejected calls, 36 boundary cases |

The open-port identity residual is below $2\times10^{-16}$ in the archived run. The largest positive energy-budget deviation is below $3\times10^{-15}$. The finite crossover's smallest observed ratio of attained probability gap to the predicted scale is about $0.01458$, above the proved constant $1/128=0.0078125$. The largest scalar-versus-matrix scan discrepancy is below $1.5\times10^{-9}$.

These numbers describe the finite tested instances. They do not extrapolate numerical accuracy to arbitrarily large systems or replace the universal inequalities in the proof.

## Reusable API

[protocols.py](protocols.py) evaluates the exact finite-model formulas in floating-point arithmetic:

| Function | Meaning |
|---|---|
| `mixture_distance_bound(n, strength, purity=2, queries=None)` | Common-decision upper bound, with the finite geometric factor when a query count is supplied |
| `individual_distance_bound(n, strength, purity=2)` | Separate upper bound on the average of individually optimized trace distances |
| `small_strength_output(n, strength)` | One-query mixed-label pointer output |
| `weak_scan_parameters(n, strength)` | Finite clipped weak-scan parameters and resource counts, for strength above one half |
| `weak_scan_output(n, strength)` | Fixed final pointer statistics of that scan |
| `one_clean_output(n, strength)` | The matching finite construction, choosing its small- or large-strength branch |
| `near_unit_scan_output(n, strength, block_length)` | Canonical pi-rotation scan with complete dephasing at every block boundary |
| `near_unit_scan_error_bound(n, strength, block_length)` | Uniform analytical worst-case error certificate |
| `scan_costs`, `small_strength_costs`, `near_unit_scan_costs` | Counts in the explicitly documented known-gate primitives |

An output reports its measurement axis, both pointer expectations, the declared-alternative outcome, null and alternative errors, probability gap and equal-prior success. The probability gap is twice the success advantage above one half. It need not imply balanced errors.

The near-unit API defaults to $L=50M$, a valid conservative choice; the explicit example (A22) in the scientific account uses $L=100M$. Supply the block length when reproducing a particular formula. For example:

```python
import sys
sys.path.insert(0, "verification")
import protocols

n = 3
M = protocols.label_count(n)
strength = 1 - 0.001 / M
output = protocols.near_unit_scan_output(n, strength, block_length=100 * M)
certificate = protocols.near_unit_scan_error_bound(n, strength, 100 * M)
print(output.null_error, output.alternative_error, certificate)
```

The explicitly separate `coherent_scan_output` function omits boundary dephasing. Away from strength one, its output can depend on the hidden position; the argument makes that dependence explicit. It is not the canonical label-symmetric protocol.

## Resource and numerical limits

A query is one ordinary channel call. Each scan step uses two controlled known Pauli-string gates and one pointer rotation. Decomposing the strings into controlled single-qubit Pauli gates gives exactly $6n4^{n-1}L$ such gates for a full scan. Known dephasing maps and the optional mixed coins used to dilate them are counted separately. No fault-tolerant synthesis cost is implied.

The full-matrix checks cover small processors, and the feedback checks sample unitary and random-unitary controls. They do not enumerate all unital channels; the proof covers that larger class through Hilbert–Schmidt contraction. Scan checks include larger label counts using two-by-two matrices.

The numerical scan-output routines explicitly accept only $1\le n\le5$ and block lengths $2\le L\le100M$, the range of this finite study. Larger requests raise an informative error. Cumulative inactive-block powers use logarithmic formulas to avoid rounding a tiny-angle cosine to one. Active blocks still use floating-point matrix powers. The analytical bounds, parameter formulas and resource counts do not inherit this numerical-output restriction, and the scientific theorems remain universal. These routines are not interval-arithmetic certificates. Nor do they certify relative accuracy for arbitrarily tiny positive signals: subtracting nearly equal floating-point probabilities can erase such a gap, including in the one-query branch. Use the analytical gap formulas for that question.

Targeted negative controls require rejection of a non-finite scan output and of an out-of-range large-system numerical request. This prevents a small recorded residual from disguising an unevaluated or non-finite quantity.

The suite establishes no priority claim, journal assessment, optimal query complexity, exact arbitrary-purity frontier or hardware feasibility. It also does not inspect the hosted rendering of this Markdown. Those are different questions from the finite scientific calculations.
