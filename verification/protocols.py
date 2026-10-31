"""Bounds and exact reduced dynamics for reset-free hidden-Pauli detection.

Model: n >= 1 queried qubits, M = 4**n - 1 nonidentity Pauli labels,
known strength 0 <= strength <= 1, ordinary memoryless channel queries,
known unital controls, and a final label-independent POVM. The functions
use floating-point arithmetic to evaluate exact finite-dimensional model
formulas; they do not model gate synthesis errors.

Numerical scan-output evaluators are restricted to 1 <= n <= 5 and
2 <= block_length <= 100*(4**n-1). Analytic bound, parameter, and cost
APIs do not have this numerical-output restriction. Finite checks in this
domain are diagnostics, not absolute or interval accuracy certificates.

Bias convention: probability_gap is p(alternative decision | alternative)
minus p(alternative decision | null). Equal-prior success advantage over
one half is half this gap. All counts refer to one complete experiment.

NumPy 2.3.5 is the version used for the archived verification results.
"""

from dataclasses import dataclass
import math
from numbers import Integral

import numpy as np


MAX_NUMERICAL_SCAN_QUBITS = 5
MAX_NUMERICAL_BLOCK_MULTIPLIER = 100


def label_count(n: int) -> int:
    """Return M = 4**n - 1; n is a positive integer."""
    if not isinstance(n, Integral) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    return 4**int(n) - 1


def _strength(strength: float) -> float:
    strength = float(strength)
    if not math.isfinite(strength) or not 0 <= strength <= 1:
        raise ValueError("strength must lie in [0, 1]")
    return strength


def _purity(purity: float) -> float:
    purity = float(purity)
    if not math.isfinite(purity) or purity < 1:
        raise ValueError("collision purity must be finite and at least one")
    return purity


def _nonnegative_integer(value: int, name: str) -> int:
    if not isinstance(value, Integral) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return int(value)


def _check_scan_output_domain(n: int, block_length: int | None = None) -> None:
    """Reject scan evaluations beyond the finite floating-point study."""
    M = label_count(n)
    if n > MAX_NUMERICAL_SCAN_QUBITS:
        raise ValueError(
            "numerical scan outputs support only 1 <= n <= "
            f"{MAX_NUMERICAL_SCAN_QUBITS}; analytic parameter, bound, and "
            "cost APIs remain available outside this range"
        )
    if block_length is not None:
        L = _nonnegative_integer(block_length, "block_length")
        if not 2 <= L <= MAX_NUMERICAL_BLOCK_MULTIPLIER * M:
            raise ValueError(
                "numerical scan outputs require 2 <= block_length <= "
                f"{MAX_NUMERICAL_BLOCK_MULTIPLIER}*M, with M=4**n-1; "
                "the analytical protocol is not restricted by this guard"
            )


def _cosine_power(sin_squared_angle: float, exponent: int) -> float:
    """Evaluate cos(angle)**exponent stably for 0 <= angle <= pi/2."""
    if exponent == 0:
        return 1.0
    if sin_squared_angle == 1:
        return 0.0
    return math.exp(exponent * math.log1p(-sin_squared_angle) / 2)


def geometric_sum(strength: float, queries: int) -> float:
    """Return sum(strength**j for j in range(queries)), including endpoints.

    Uses expm1 for stability near strength=1 and does not loop over queries.
    Zero queries returns zero; strength=1 returns queries.
    """
    strength = _strength(strength)
    queries = _nonnegative_integer(queries, "queries")
    if queries == 0:
        return 0.0
    if strength == 1:
        return float(queries)
    if strength == 0:
        return 1.0
    return -math.expm1(queries * math.log(strength)) / (1 - strength)


def mixture_distance_bound(
    n: int, strength: float, purity: float = 2.0, queries: int | None = None
) -> float:
    """Upper-bound trace distance between the protocol's mixture and null.

    The collision purity is P = D Tr(rho_in**2); one clean qubit gives P=2.
    If queries is given, the bound is
        min(1, strength * sqrt(P-1) * sum_{j<T} strength**j / (2M)).
    If queries is None, use the query-independent resolvent bound. At
    strength=1 that unlimited-query bound is the trivial one (unless P=1).
    This is not an average of label-dependent optimal trace distances.
    """
    M, strength, purity = label_count(n), _strength(strength), _purity(purity)
    if queries is not None:
        queries = _nonnegative_integer(queries, "queries")
    if purity == 1 or strength == 0 or queries == 0:
        return 0.0
    if queries is None:
        if strength == 1:
            return 1.0
        multiplier = 1 / (1 - strength)
    else:
        multiplier = geometric_sum(strength, queries)
    return min(1.0, strength * math.sqrt(purity - 1) * multiplier / (2 * M))


def individual_distance_bound(
    n: int, strength: float, purity: float = 2.0
) -> float:
    """Upper-bound the mean of the individual final-state trace distances.

    Returns min(1, strength * sqrt((P-1)/(M*(1-strength**2))) / 2).
    At strength=1 only the trivial bound is returned. This separate bound
    permits each label's trace distance to have its own optimizing POVM.
    """
    M, strength, purity = label_count(n), _strength(strength), _purity(purity)
    if purity == 1 or strength == 0:
        return 0.0
    if strength == 1:
        return 1.0
    return min(
        1.0,
        strength * math.sqrt((purity - 1) / (M * (1 - strength**2))) / 2,
    )


def one_clean_bias_scale(n: int, strength: float) -> float:
    """Return min(1, strength/[M*(1-strength)]), with endpoint values 0,1."""
    M, strength = label_count(n), _strength(strength)
    if strength == 1:
        return 1.0
    return min(1.0, strength / (M * (1 - strength)))


def bloch_block(eta: float, angle: float, length: int) -> np.ndarray:
    """Exact finite Bloch matrix (dephase_eta after R_y(angle))**length.

    Coordinates are the pointer's (x,z) Bloch components. This is a
    two-by-two floating-point evaluation, not a channel approximation.
    length=0 returns the identity. This low-level matrix helper carries
    no uniform accuracy guarantee for arbitrary length or tiny angle;
    the public scan-output evaluators enforce their finite study domain.
    """
    eta = _strength(eta)
    length = _nonnegative_integer(length, "length")
    if not math.isfinite(angle):
        raise ValueError("angle must be finite")
    c, s = math.cos(angle), math.sin(angle)
    return np.linalg.matrix_power(np.array([[eta * c, eta * s], [-s, c]]), length)


@dataclass(frozen=True)
class PointerOutput:
    """A fixed two-outcome pointer test and its exact-model probabilities."""

    axis: str
    null_expectation: float
    alternative_expectation: float
    alternative_outcome: int

    @property
    def null_alternative_probability(self) -> float:
        """Probability of declaring alternative under the null."""
        return (1 + self.alternative_outcome * self.null_expectation) / 2

    @property
    def alternative_probability(self) -> float:
        """Probability of declaring alternative under the hidden alternative."""
        return (1 + self.alternative_outcome * self.alternative_expectation) / 2

    @property
    def probability_gap(self) -> float:
        return self.alternative_outcome * (
            self.alternative_expectation - self.null_expectation
        ) / 2

    @property
    def equal_prior_success(self) -> float:
        return (1 + self.probability_gap) / 2

    @property
    def null_error(self) -> float:
        return self.null_alternative_probability

    @property
    def alternative_error(self) -> float:
        return 1 - self.alternative_probability


def scan_costs(n: int, block_length: int) -> dict[str, int]:
    """Exact query and specified-native-gate counts for a complete scan.

    Each of M candidates has L steps; each step has one query, two known
    controlled Pauli-string gates, and one pointer R_y rotation.
    Decomposing each string into controlled single-qubit X/Y/Z gates gives
    exactly 2L * sum_b weight(P_b) = 6n*4**(n-1)*L such two-qubit gates.
    This does not assign a platform-specific synthesis cost to those gates
    or to arbitrary one-qubit rotations. Dephasing maps are counted by
    the particular protocol separately.
    """
    M = label_count(n)
    L = _nonnegative_integer(block_length, "block_length")
    if L == 0:
        raise ValueError("block_length must be positive")
    Q = M * L
    return {
        "queries": Q,
        "controlled_pauli_string_calls": 2 * Q,
        "controlled_single_pauli_gates": 6 * n * 4**(n - 1) * L,
        "pointer_y_rotations": Q,
    }


def small_strength_output(n: int, strength: float) -> PointerOutput:
    """One-query mixed-label gadget; valid at every strength.

    The one clean pointer starts in |+>. A maximally mixed 2n-qubit label
    register covers all 4**n Paulis, including identity; the query system
    has n mixed qubits. The final X=+1 outcome declares alternative.
    The output is identical for every hidden nonidentity label and its
    probability gap is strength/[2*(M+1)]. This is the crossover
    construction's branch for strength <= 1/2.
    """
    M, strength = label_count(n), _strength(strength)
    return PointerOutput("X", 1 / (M + 1), (1 + strength) / (M + 1), 1)


def small_strength_costs(n: int) -> dict[str, int]:
    """Exact costs in a declared gate set for the one-query mixed-label test.

    Encode each Pauli as P(x,z)=i**(xz) X**x Z**z. Each local multiplexed
    controlled Pauli uses one CCZ on the query bit, one CCX on the query
    bit, and one controlled-controlled-S phase on the pointer. The two
    multiplexers therefore use 6n three-qubit native gates in this gate
    set, plus one Hadamard to prepare |+>. Inverse gates are included in
    this count. A compilation into any selected one/two-qubit universal
    gate set has O(n) cost, with a convention-dependent exact constant.
    """
    label_count(n)
    return {
        "queries": 1,
        "clean_qubits": 1,
        "mixed_query_qubits": n,
        "mixed_label_qubits": 2 * n,
        "total_qubits": 3 * n + 1,
        "controlled_pauli_multiplexers": 2,
        "native_three_qubit_gates": 6 * n,
        "pointer_hadamards": 1,
    }


@dataclass(frozen=True)
class WeakScanParameters:
    """Finite weak-scan parameters; strength is supplied to the algorithm."""

    n: int
    strength: float
    labels: int
    gamma: float
    effective_strength: float
    h: float
    block_length: int
    t: float
    sin_squared_angle: float
    angle: float
    clipping_factor: float

    @property
    def query_count(self) -> int:
        return self.labels * self.block_length

    @property
    def costs(self) -> dict[str, int]:
        """Admitted unital-control costs; optional mixed-coin dilation noted."""
        result = scan_costs(self.n, self.block_length)
        clipping = self.query_count if self.clipping_factor < 1 else 0
        result.update({
            "clean_qubits": 1,
            "mixed_query_qubits": self.n,
            "total_qubits_with_free_unital_controls": self.n + 1,
            "clipping_dephasing_maps": clipping,
            "boundary_dephasing_maps": self.labels,
            "extra_mixed_coins_for_unitary_dilation": clipping + self.labels,
        })
        return result


def weak_scan_parameters(n: int, strength: float) -> WeakScanParameters:
    """Construct the proved finite weak scan for 1/2 < strength <= 1.

    gamma=max(1-strength,1/M), ell=1-gamma,
    h=(1+ell)/gamma, L=ceil(32/gamma), t=1/[16(M+h)],
    sin(angle)**2=2t/L. A known dephasing ell/strength follows every
    gadget, and full Z dephasing follows every candidate block.
    The scan uses Q=M*L <= 33M*min(1/(1-strength),M) queries.
    This parameter API is not restricted to the numerical output domain;
    floating-point parameters alone are not an accuracy certificate.
    """
    M, strength = label_count(n), _strength(strength)
    if strength <= 0.5:
        raise ValueError("weak scan is the branch for strength > 1/2")
    gamma = max(1 - strength, 1 / M)
    ell = 1 - gamma
    h = (1 + ell) / gamma
    L = math.ceil(32 / gamma)
    t = 1 / (16 * (M + h))
    x = 2 * t / L
    return WeakScanParameters(
        n, strength, M, gamma, ell, h, L, t, x, math.asin(math.sqrt(x)),
        min(1.0, ell / strength),
    )


def weak_scan_output(n: int, strength: float) -> PointerOutput:
    """Numerically evaluate the finite weak scan, identical for every label.

    Returns z_null=k0**M and z_alt=k0**(M-1)*kell, with
    k0=cos(angle)**L and kell=(A_ell**L)[1,1]. The fixed Z=-1 outcome
    declares alternative. Uses complete dephasing at block boundaries.
    Evaluation is restricted to 1 <= n <= 5 and 2 <= L <= 100M.
    Scalar survival powers use the exact parameter u=sin(angle)**2 in
    exp(exponent*log1p(-u)/2); the active block uses floating-point
    matrix powers. The finite diagnostics are not interval certificates.
    """
    _check_scan_output_domain(n)
    p = weak_scan_parameters(n, strength)
    _check_scan_output_domain(n, p.block_length)
    kell = float(bloch_block(p.effective_strength, p.angle, p.block_length)[1, 1])
    null = _cosine_power(p.sin_squared_angle, p.block_length * p.labels)
    inactive = _cosine_power(
        p.sin_squared_angle, p.block_length * (p.labels - 1)
    )
    return PointerOutput("Z", null, inactive * kell, -1)


def weak_scan_gap_lower_bound(n: int, strength: float) -> float:
    """Proved finite gap ell/[32*(M*gamma+1+ell)], without asymptotic limits."""
    p = weak_scan_parameters(n, strength)
    return p.effective_strength / (
        32 * (p.labels * p.gamma + 1 + p.effective_strength)
    )


def one_clean_output(n: int, strength: float) -> PointerOutput:
    """Choose the one-query or weak-scan branch of the finite bias protocol.

    The weak-scan branch inherits weak_scan_output's finite numerical
    domain. The one-query branch evaluates its elementary scalar formula.
    """
    strength = _strength(strength)
    if strength <= 0.5:
        return small_strength_output(n, strength)
    return weak_scan_output(n, strength)


def near_unit_scan_output(
    n: int, strength: float, block_length: int | None = None
) -> PointerOutput:
    """Canonical finite pi scan, with mandatory block-boundary dephasing.

    Each candidate has L steps of R_y(pi/L) followed by its exact pointer
    gadget. Complete Z dephasing follows every candidate block. The
    default L=50M gives the conservative fixed-error construction.
    There is no clipping. For every hidden label the output is exactly
        z_null=k0**M, z_alt=k0**(M-1)*k_strength,
    where k0=cos(pi/L)**L and k_strength=(A_strength**L)[1,1].
    At strength=1, k_strength=-1. Unlike the explicitly separate
    coherent_scan_output function, this canonical protocol has identical
    outputs for all hidden positions even when strength<1.
    Numerical evaluation is restricted to 1 <= n <= 5 and
    2 <= block_length <= 100M. Scalar powers use log1p(-sin(angle)**2)/2.
    Active matrix powers remain floating-point finite diagnostics.
    """
    M, strength = label_count(n), _strength(strength)
    L = 50 * M if block_length is None else _nonnegative_integer(
        block_length, "block_length"
    )
    _check_scan_output_domain(n, L)
    angle = math.pi / L
    u = math.sin(angle)**2
    active_factor = float(bloch_block(strength, angle, L)[1, 1])
    null = _cosine_power(u, M * L)
    inactive = _cosine_power(u, (M - 1) * L)
    return PointerOutput("Z", null, inactive * active_factor, -1)


def near_unit_scan_costs(n: int, block_length: int | None = None) -> dict[str, int]:
    """Counts for the canonical pi scan, including M boundary dephasings.

    There is one clean pointer and n mixed query qubits with admitted
    unital controls. If every known control is instead dilated into a
    unitary, the M complete dephasings can use M initially mixed coins
    that are each used once and retained/ignored.
    """
    M = label_count(n)
    L = 50 * M if block_length is None else _nonnegative_integer(
        block_length, "block_length"
    )
    if L < 2:
        raise ValueError("near-unit scan requires block_length >= 2")
    result = scan_costs(n, L)
    result.update({
        "clean_qubits": 1,
        "mixed_query_qubits": n,
        "total_qubits_with_free_unital_controls": n + 1,
        "boundary_dephasing_maps": M,
        "extra_mixed_coins_for_unitary_dilation": M,
    })
    return result


def coherent_scan_output(
    n: int,
    strength: float,
    block_length: int | None = None,
    hidden_position: int = 0,
) -> PointerOutput:
    """Explicit no-boundary-dephasing variant of the pi-rotation scan.

    Enumerate M nonidentity labels; apply L steps of R_y(pi/L) followed
    by that candidate's pointer gadget. There is no boundary dephasing
    and no clipping. hidden_position is zero based. The default
    L=50M is the conservative fixed-error construction. At strength=1,
    z_null=cos(pi/L)**(ML) and z_alt=-cos(pi/L)**((M-1)L), independent
    of the hidden position. Away from that endpoint the position can
    affect the output, so it is an explicit argument.
    Numerical evaluation is restricted to 1 <= n <= 5 and
    2 <= block_length <= 100M. The inactive powers are evaluated with
    stable scalar logarithms; active matrix powers remain floating point.
    """
    M, strength = label_count(n), _strength(strength)
    L = 50 * M if block_length is None else _nonnegative_integer(
        block_length, "block_length"
    )
    _check_scan_output_domain(n, L)
    hidden_position = _nonnegative_integer(hidden_position, "hidden_position")
    if hidden_position >= M:
        raise ValueError("hidden_position must be less than M")
    angle = math.pi / L
    s = math.sin(angle)
    u = s * s
    active = bloch_block(strength, angle, L)
    null = _cosine_power(u, M * L)
    alternative = _cosine_power(u, (M - 1) * L) * float(active[1, 1])
    if hidden_position < M - 1:
        alternative -= (
            s * _cosine_power(u, (M - 1) * L - 1) * float(active[0, 1])
        )
    return PointerOutput("Z", null, alternative, -1)


def near_unit_scan_error_bound(
    n: int, strength: float, block_length: int | None = None
) -> float:
    """Upper-bound both errors of the canonical near-unit scan Z decision.

    The analytic bound, uniform in hidden position, is
        pi**2*M/(4L) + L*(1-strength)/2.
    It is capped at one because it can be uninformative away from
    strength=1. The default L=50M and 1-strength <= 0.001/M give
    error at most pi**2/200 + 0.025 < 0.075.
    """
    M, strength = label_count(n), _strength(strength)
    L = 50 * M if block_length is None else _nonnegative_integer(
        block_length, "block_length"
    )
    if L < 2:
        raise ValueError("coherent scan requires block_length >= 2")
    return min(1.0, math.pi**2 * M / (4 * L) + L * (1 - strength) / 2)


def coherent_scan_error_bound(
    n: int, strength: float, block_length: int | None = None
) -> float:
    """The same robust bound also applies to the explicit coherent variant."""
    return near_unit_scan_error_bound(n, strength, block_length)
