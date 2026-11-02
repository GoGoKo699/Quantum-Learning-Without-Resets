"""Finite diagnostics for the weight-one initial-negentropy obstruction.

Run from the repository root: python verification/verify_entropy.py
Uses only the repository's existing NumPy dependency. The independent
run_checks.py/results.json suite is not changed. This script writes
entropy_results.json beside itself and rejects non-finite quantities.

All logarithms in the density-matrix calculations are natural logarithms.
Initial trajectory states have an explicit 1e-7 maximally mixed admixture;
the actual resulting negentropy is charged. The spectral routines do not
silently add purity or regularize the reference state. Exact singular
endpoints are evaluated on their supports. These finite floating-point
checks do not replace the universal analytical proof.
"""

from itertools import combinations, product
import json
import math
from pathlib import Path

import numpy as np


SEED = 2026110202
RNG = np.random.default_rng(SEED)
TOLERANCE = 5e-10
SUPPORT_TOLERANCE = 1e-12
INITIAL_MIXED_WEIGHT = 1e-7
I2 = np.eye(2, dtype=complex)
AXES = (
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.diag([1, -1]).astype(complex),
)


def finite(label, *values):
    for value in values:
        if not np.all(np.isfinite(np.asarray(value))):
            raise AssertionError(f"{label}: non-finite value")


def assert_le(label, lhs, rhs, tolerance=TOLERANCE):
    finite(label, lhs, rhs)
    if lhs > rhs + tolerance:
        raise AssertionError((label, lhs, rhs, tolerance))


def assert_close(label, lhs, rhs, tolerance=TOLERANCE):
    finite(label, lhs, rhs)
    residual = float(np.max(np.abs(np.asarray(lhs) - np.asarray(rhs))))
    if residual > tolerance:
        raise AssertionError((label, residual, tolerance))
    return residual


def hermitian(matrix):
    finite("Hermitian input", matrix)
    return (matrix + matrix.conj().T) / 2


def spectrum(matrix):
    """Reject non-Hermitian or non-PSD input; remove only roundoff negatives."""
    finite("spectral input", matrix)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise AssertionError("spectral input must be square")
    assert_close("Hermiticity", matrix, matrix.conj().T)
    values, vectors = np.linalg.eigh(hermitian(matrix))
    finite("eigensystem", values, vectors)
    if values[0] < -SUPPORT_TOLERANCE:
        raise AssertionError(("nonpositive input", float(values[0])))
    return np.maximum(values, 0), vectors


def entropy(state):
    values, _ = spectrum(state)
    positive = values > 0
    return float(-np.dot(values[positive], np.log(values[positive])))


def relative_entropy(state, reference):
    """Finite quantum D(state||reference), with explicit support rejection.

    A reference eigenvalue <= 1e-12 is treated as numerical zero. A state
    with more than 1e-12 mass outside that support is rejected. The tested
    full-rank states have eigenvalues well above this threshold.
    """
    values, vectors = spectrum(reference)
    spectrum(state)
    diagonal = np.diag(vectors.conj().T @ state @ vectors).real
    support = values > SUPPORT_TOLERANCE
    if diagonal[~support].sum() > SUPPORT_TOLERANCE:
        raise ValueError("relative entropy is infinite: support mismatch")
    result = -entropy(state) - np.dot(diagonal[support], np.log(values[support]))
    finite("relative entropy result", result)
    return float(result)


def trace_distance(state, other):
    values = np.linalg.eigvalsh(hermitian(state - other))
    finite("trace-distance eigenvalues", values)
    return float(np.abs(values).sum() / 2)


def random_state(dimension):
    z = RNG.normal(size=(dimension, dimension))
    z = z + 1j * RNG.normal(size=(dimension, dimension))
    result = z @ z.conj().T
    return result / np.trace(result)


def random_unitary(dimension):
    z = RNG.normal(size=(dimension, dimension))
    z = z + 1j * RNG.normal(size=(dimension, dimension))
    q, r = np.linalg.qr(z)
    phase = np.diag(r) / np.abs(np.diag(r))
    result = q * phase.conj()
    assert_close("sampled unitary", result.conj().T @ result,
                 np.eye(dimension))
    return result


def side_marginal(state, n, side_dimension):
    d = 2**n
    return np.einsum("iaib->ab", state.reshape(d, side_dimension, d,
                                               side_dimension))


def q0(state, n, side_dimension):
    d = 2**n
    return np.kron(np.eye(d) / d, side_marginal(state, n, side_dimension))


def qa(state, pauli, n, side_dimension):
    d = 2**n
    blocks = state.reshape(d, side_dimension, d, side_dimension)
    coefficient = np.einsum("ij,jaib->ab", pauli, blocks)
    return np.kron(pauli / d, coefficient)


def weight_one_labels(n):
    labels = []
    for site in range(n):
        for axis_name, axis in zip("XYZ", AXES):
            pauli = np.ones((1, 1), dtype=complex)
            for position in range(n):
                pauli = np.kron(pauli, axis if position == site else I2)
            labels.append((site, axis_name, pauli))
    return labels


def site_side_marginal(state, n, side_dimension, site):
    dimensions = [2] * n + [side_dimension]
    array = state.reshape(dimensions + dimensions)
    for position in reversed(range(n)):
        if position != site:
            array = np.trace(array, axis1=position,
                             axis2=position + len(dimensions))
            del dimensions[position]
    return array.reshape(2 * side_dimension, 2 * side_dimension)


def dephase_local(state, axis, side_dimension):
    conjugation = np.kron(axis, np.eye(side_dimension))
    return hermitian((state + conjugation @ state @ conjugation) / 2)


def check_channel_implementation():
    """Compare sector formulas with their positive Pauli-error channels."""
    max_error = 0.0
    cases = 0
    for n, k in [(1, 0), (1, 1), (2, 0), (2, 1)]:
        d, side_dimension = 2**n, 2**k
        state = random_state(d * side_dimension)
        errors = []
        for local_indices in product(range(4), repeat=n):
            operator = np.ones((1, 1), dtype=complex)
            for index in local_indices:
                operator = np.kron(operator, ((I2,) + AXES)[index])
            errors.append(operator)
        null_by_errors = sum(np.kron(error, np.eye(side_dimension)) @ state
                             @ np.kron(error, np.eye(side_dimension)).conj().T
                             for error in errors) / d**2
        max_error = max(max_error, assert_close(
            "depolarizing Pauli-error representation", null_by_errors,
            q0(state, n, side_dimension)))
        for _, _, hidden in weight_one_labels(n):
            output = np.zeros_like(state)
            weights = []
            for error in errors:
                sign = float(np.trace(hidden @ error @ hidden @ error).real / d)
                assert_close("Pauli commutation sign squared", sign**2, 1)
                weight = (1 + .5 * sign) / d**2
                assert_le("positive Pauli-error weight", 0, weight)
                weights.append(weight)
                full_error = np.kron(error, np.eye(side_dimension))
                output += weight * full_error @ state @ full_error.conj().T
            assert_close("Pauli-error normalization", sum(weights), 1)
            expected = q0(state, n, side_dimension) + .5 * qa(
                state, hidden, n, side_dimension)
            max_error = max(max_error, assert_close(
                "attenuated Pauli-error representation", output, expected))
            cases += 1
    return {"cases": cases, "max_sector_vs_Pauli_error_residual": max_error}


def check_coupling():
    cases = 0
    min_slack = math.inf
    max_identity_error = 0.0
    max_noncommuting_block_norm = 0.0
    for n, k in [(1, 0), (1, 1), (2, 0), (2, 1)]:
        side_dimension = 2**k
        dimension = 2**n * side_dimension
        for _ in range(3):
            sigma, rho = random_state(dimension), random_state(dimension)
            omega = q0(sigma, n, side_dimension)
            zeta = q0(rho, n, side_dimension)
            input_divergence = relative_entropy(sigma, rho)
            for _, _, pauli in weight_one_labels(n):
                sigma_r = hermitian(omega + qa(sigma, pauli, n, side_dimension))
                rho_r = hermitian(zeta + qa(rho, pauli, n, side_dimension))
                flipped = hermitian(2 * omega - sigma_r)
                spectrum(flipped)
                source = relative_entropy(sigma_r, omega)
                lhs = relative_entropy(omega, (rho_r + zeta) / 2)
                convex_bound = (relative_entropy(sigma_r, rho_r)
                                + relative_entropy(flipped, zeta)) / 2
                rhs = input_divergence + source / 2
                assert_le("coupling joint convexity", lhs, convex_bound)
                assert_le("coupling input data processing", convex_bound, rhs)
                error = assert_close(
                    "flipped-state Pythagoras", relative_entropy(flipped, zeta),
                    source + relative_entropy(omega, zeta))
                max_identity_error = max(max_identity_error, error)
                min_slack = min(min_slack, rhs - lhs)
                cases += 1
            if k:
                # Z pinching leaves two A-valued blocks. Noncommutation
                # rules out accidentally testing classical side data only.
                local = site_side_marginal(sigma, n, side_dimension, 0)
                b0, b1 = local[:side_dimension, :side_dimension], local[side_dimension:, side_dimension:]
                commutator = b0 @ b1 - b1 @ b0
                max_noncommuting_block_norm = max(
                    max_noncommuting_block_norm,
                    float(np.linalg.norm(commutator)))
    if max_noncommuting_block_norm < 1e-5:
        raise AssertionError("noncommuting protected blocks were not exercised")
    return {"cases": cases, "min_amortized_slack": min_slack,
            "max_flipped_identity_residual": max_identity_error,
            "max_protected_block_commutator_norm": max_noncommuting_block_norm}


def check_entropy_charge():
    cases = 0
    min_pair_slack = math.inf
    min_tensorization_slack = math.inf
    max_local_full_error = 0.0
    min_three_axis_slack = math.inf
    for n, k in [(1, 0), (1, 1), (2, 0), (2, 1)]:
        side_dimension = 2**k
        for _ in range(3):
            sigma = random_state(2**n * side_dimension)
            omega = q0(sigma, n, side_dimension)
            global_deficit = relative_entropy(sigma, omega)
            assert_close("null entropy identity", global_deficit,
                         entropy(omega) - entropy(sigma))
            sum_local_deficits = 0.0
            sum_axis_deficits = 0.0
            for site in range(n):
                local = site_side_marginal(sigma, n, side_dimension, site)
                local_null = np.kron(I2 / 2, side_marginal(sigma, n,
                                                          side_dimension))
                deficit = relative_entropy(local, local_null)
                axis_deficits = []
                for axis_index, axis in enumerate(AXES):
                    pinched = dephase_local(local, axis, side_dimension)
                    source = relative_entropy(pinched, local_null)
                    pauli = weight_one_labels(n)[3 * site + axis_index][2]
                    full_source = relative_entropy(
                        hermitian(omega + qa(sigma, pauli, n, side_dimension)), omega)
                    max_local_full_error = max(max_local_full_error, assert_close(
                        "local/full source identity", source, full_source))
                    axis_deficits.append(source)
                for first, second in combinations(range(3), 2):
                    assert_le("two-axis complementarity",
                              axis_deficits[first] + axis_deficits[second], deficit)
                    min_pair_slack = min(min_pair_slack,
                                         deficit - axis_deficits[first] - axis_deficits[second])
                assert_le("three-axis charge", sum(axis_deficits), 1.5 * deficit)
                min_three_axis_slack = min(min_three_axis_slack,
                                           1.5 * deficit - sum(axis_deficits))
                sum_local_deficits += deficit
                sum_axis_deficits += sum(axis_deficits)
                cases += 1
            assert_le("conditional entropy tensorization", sum_local_deficits,
                      global_deficit)
            min_tensorization_slack = min(min_tensorization_slack,
                                          global_deficit - sum_local_deficits)
            assert_le("aggregate Pauli entropy charge", sum_axis_deficits,
                      1.5 * global_deficit)

    bell_vector = np.array([1, 0, 0, 1], dtype=complex) / math.sqrt(2)
    bell = np.outer(bell_vector, bell_vector.conj())
    bell_null = np.eye(4) / 4
    bell_global = relative_entropy(bell, bell_null)
    bell_axes = [relative_entropy(dephase_local(bell, axis, 2), bell_null)
                 for axis in AXES]
    bell_error = assert_close("Bell global deficit", bell_global, 2 * math.log(2))
    bell_error = max(bell_error, assert_close("Bell axis deficits", bell_axes,
                                            [math.log(2)] * 3))
    bell_error = max(bell_error, assert_close("Bell 3/2 saturation",
                                            sum(bell_axes), 1.5 * bell_global))
    return {"site_cases": cases, "min_pairwise_slack": min_pair_slack,
            "min_three_axis_slack": min_three_axis_slack,
            "min_tensorization_slack": min_tensorization_slack,
            "max_local_full_source_residual": max_local_full_error,
            "bell_axis_sum_over_global_deficit": sum(bell_axes) / bell_global,
            "max_bell_saturation_residual": bell_error}


def clean_product_state(qubits, clean_qubits, mixed_weight):
    state = np.ones((1, 1), dtype=complex)
    for position in range(qubits):
        factor = np.diag([1.0, 0.0]) if position < clean_qubits else I2 / 2
        state = np.kron(state, factor)
    return (1 - mixed_weight) * state + mixed_weight * np.eye(2**qubits) / 2**qubits


def check_trajectories():
    checkpoints = 0
    min_slacks = {"amortization": math.inf, "complementarity": math.inf,
                  "initial_entropy_budget": math.inf, "overall": math.inf}
    max_trace_defect = 0.0
    max_control_entropy_decrease = 0.0
    max_zero_clean_change = 0.0
    max_mixture_bound_excess = 0.0
    max_individual_squared_bound_excess = 0.0
    max_purity_conversion_excess = 0.0
    min_eigenvalue = math.inf
    configurations = []
    for n, k in [(1, 0), (1, 1), (2, 0), (2, 1)]:
        side_dimension = 2**k
        dimension = 2**(n + k)
        labels = weight_one_labels(n)
        for clean in sorted({0, 1, n + k}):
            for control_kind in ["unitary", "random_unitary_mixture"]:
                configurations.append([n, k, clean, control_kind])
                initial = clean_product_state(n + k, clean, INITIAL_MIXED_WEIGHT)
                negentropy = math.log(dimension) - entropy(initial)
                assert_le("initial c-clean entropy budget", negentropy,
                          clean * math.log(2))
                max_purity_conversion_excess = max(
                    max_purity_conversion_excess, negentropy - clean * math.log(2))
                null = initial.copy()
                alternatives = [initial.copy() for _ in labels]
                accumulated_source = 0.0
                accumulated_entropy_gain = 0.0
                for queries in range(1, 5):
                    first = random_unitary(dimension)
                    second = random_unitary(dimension)
                    def control(state):
                        output = first @ state @ first.conj().T
                        if control_kind == "random_unitary_mixture":
                            output = .7 * output + .3 * (second @ state @ second.conj().T)
                        return hermitian(output)
                    assert_close("control unitality", control(np.eye(dimension)),
                                 np.eye(dimension))
                    sigma = control(null)
                    max_control_entropy_decrease = max(
                        max_control_entropy_decrease, entropy(null) - entropy(sigma))
                    assert_le("unital control entropy increase", entropy(null),
                              entropy(sigma))
                    next_null = hermitian(q0(sigma, n, side_dimension))
                    accumulated_entropy_gain += entropy(next_null) - entropy(sigma)
                    for label_index, (_, _, pauli) in enumerate(labels):
                        retained = hermitian(q0(sigma, n, side_dimension)
                                             + qa(sigma, pauli, n, side_dimension))
                        accumulated_source += relative_entropy(retained, next_null)
                        tau = control(alternatives[label_index])
                        alternatives[label_index] = hermitian(
                            q0(tau, n, side_dimension)
                            + .5 * qa(tau, pauli, n, side_dimension))
                    null = next_null
                    for state in [null] + alternatives:
                        values, _ = spectrum(state)
                        min_eigenvalue = min(min_eigenvalue, float(values[0]))
                        max_trace_defect = max(max_trace_defect,
                                               abs(float(np.trace(state).real) - 1))
                    if clean == 0:
                        for state in [null] + alternatives:
                            max_zero_clean_change = max(max_zero_clean_change,
                                float(np.linalg.norm(state - np.eye(dimension) / dimension)))
                    if queries not in [1, 2, 4]:
                        continue
                    reverse_sum = sum(relative_entropy(null, alternative)
                                      for alternative in alternatives)
                    half_source = accumulated_source / 2
                    entropy_charge = .75 * accumulated_entropy_gain
                    total_budget = .75 * negentropy
                    assert_le("trajectory amortization", reverse_sum, half_source)
                    assert_le("trajectory complementarity", half_source, entropy_charge)
                    assert_le("trajectory initial budget", entropy_charge, total_budget)
                    assert_le("trajectory theorem", reverse_sum, total_budget)
                    for key, slack in [("amortization", half_source - reverse_sum),
                                       ("complementarity", entropy_charge - half_source),
                                       ("initial_entropy_budget", total_budget - entropy_charge),
                                       ("overall", total_budget - reverse_sum)]:
                        min_slacks[key] = min(min_slacks[key], slack)
                    mixture = sum(alternatives) / len(alternatives)
                    mixture_distance = trace_distance(null, mixture)
                    individual_squared = sum(trace_distance(null, alternative)**2
                                             for alternative in alternatives) / len(alternatives)
                    squared_bound = max(negentropy, 0) / (8 * n)
                    assert_le("mixture trace-distance consequence", mixture_distance,
                              math.sqrt(squared_bound))
                    assert_le("individual squared-distance consequence",
                              individual_squared, squared_bound)
                    assert_le("reverse-mixture relative entropy consequence",
                              relative_entropy(null, mixture),
                              max(negentropy, 0) / (4 * n))
                    max_mixture_bound_excess = max(max_mixture_bound_excess,
                        mixture_distance - math.sqrt(squared_bound))
                    max_individual_squared_bound_excess = max(
                        max_individual_squared_bound_excess, individual_squared - squared_bound)
                    checkpoints += 1
    return {"initial_regularization_mixed_weight": INITIAL_MIXED_WEIGHT,
            "configuration_count": len(configurations),
            "queried_qubits": [1, 2], "side_qubits": [0, 1],
            "clean_qubits": "distinct values among 0, 1, n+k",
            "control_kinds": ["unitary", "random_unitary_mixture"],
            "checkpoints": checkpoints,
            "query_prefixes": [1, 2, 4], "min_slacks": min_slacks,
            "max_trace_defect": max_trace_defect,
            "max_unital_control_entropy_decrease": max_control_entropy_decrease,
            "max_zero_clean_state_change": max_zero_clean_change,
            "max_mixture_bound_excess": max_mixture_bound_excess,
            "max_individual_squared_bound_excess": max_individual_squared_bound_excess,
            "max_initial_c_clean_entropy_conversion_excess": max_purity_conversion_excess,
            "min_output_eigenvalue": min_eigenvalue}


def check_conventions_and_guards():
    delta = 1 / 3
    binary_relative = (1 - 2 * delta) * math.log((1 - delta) / delta)
    constant_error = assert_close("base2 clean-qubit coefficient",
                                 4 * binary_relative / math.log(2), 4 / 3)
    max_eigenvalue_error = 0.0
    for n in [1, 2]:
        hidden, other = weight_one_labels(n)[0][2], weight_one_labels(n)[1][2]
        for operator, attenuated_eigenvalue, identity_mixture_eigenvalue in [
            (hidden, .5, 1.0), (other, 0.0, .5)]:
            null = q0(operator, n, 1)
            retained = null + qa(operator, hidden, n, 1)
            attenuated = null + .5 * qa(operator, hidden, n, 1)
            identity_mixture = .5 * operator + .5 * retained
            max_eigenvalue_error = max(max_eigenvalue_error, assert_close(
                "attenuated spike eigenvalue", attenuated,
                attenuated_eigenvalue * operator))
            max_eigenvalue_error = max(max_eigenvalue_error, assert_close(
                "identity mixture eigenvalue", identity_mixture,
                identity_mixture_eigenvalue * operator))
    pure = np.diag([1.0, 0.0]).astype(complex)
    assert_close("singular self relative entropy", relative_entropy(pure, pure), 0)
    assert_close("singular-to-mixed relative entropy",
                 relative_entropy(pure, I2 / 2), math.log(2))
    guard_cases = 0
    for action in [lambda: entropy(np.array([[np.nan, 0], [0, 1.0]])),
                   lambda: entropy(np.diag([1.1, -.1])),
                   lambda: relative_entropy(pure, np.diag([0.0, 1.0]))]:
        try:
            action()
        except (AssertionError, ValueError):
            guard_cases += 1
        else:
            raise AssertionError("invalid numeric/support input was accepted")
    return {"delta": delta, "delta_binary_relative_entropy_nats": binary_relative,
            "required_clean_qubits_per_n_at_delta_one_third":
                4 * binary_relative / math.log(2),
            "max_base2_constant_residual": constant_error,
            "max_channel_eigenvalue_residual": max_eigenvalue_error,
            "attenuation_lambda_half_hidden_other_eigenvalues": [.5, 0],
            "identity_mixture_tau_half_hidden_other_eigenvalues": [1, .5],
            "singular_support_cases": 2, "invalid_input_guards_passed": guard_cases,
            "width_corollary_condition":
                "k >= n/3 uses c <= n+k and counts every protected record in the fixed processor"}


def main():
    result = {"numpy_version": np.__version__, "seed": SEED,
              "absolute_tolerance": TOLERANCE,
              "support_tolerance": SUPPORT_TOLERANCE,
              "logarithm_base": "natural; clean-qubit conversion divides by ln(2)",
              "channel_implementation": check_channel_implementation(),
              "coupling": check_coupling(),
              "complementarity_and_tensorization": check_entropy_charge(),
              "full_trajectories": check_trajectories(),
              "conventions_and_guards": check_conventions_and_guards(),
              "scope": "Finite floating-point diagnostics only; universal claims are analytical. "
                       "No matching full purity-width frontier or unrestricted-lambda extension is certified."}
    output = json.dumps(result, indent=2, allow_nan=False) + "\n"
    destination = Path(__file__).resolve().with_name("entropy_results.json")
    destination.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
