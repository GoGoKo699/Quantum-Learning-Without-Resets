"""Reproducible finite diagnostics for the mathematical claims.

Run: python verification/run_checks.py
Requires NumPy 2.3.5. A deterministic seed is used. The output results.json
contains concise summary statistics, not per-case logs. These numerical
checks do not certify the analytic proofs.
Comparisons reject non-finite operands before computing maxima, minima,
or tolerance tests. The finite diagnostics are not interval certificates.
"""

from itertools import product
import json
import math
from pathlib import Path

import numpy as np

import protocols


OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(2026103102)
SINGLE = [
    np.eye(2, dtype=complex),
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.diag([1, -1]).astype(complex),
]


def require_finite(label, *values):
    """Fail explicitly on NaN or infinity before a comparison can mask it."""
    for value in values:
        array = np.asarray(value)
        if not np.all(np.isfinite(array)):
            raise AssertionError(f"{label}: non-finite numeric value")


def finite_max(*values):
    require_finite("maximum operands", *values)
    return max(*values)


def finite_min(*values):
    require_finite("minimum operands", *values)
    return min(*values)


def max_abs(matrix):
    require_finite("max-absolute-value matrix", matrix)
    value = float(np.max(np.abs(matrix)))
    require_finite("max-absolute-value result", value)
    return value


def trace_norm(matrix):
    require_finite("trace-norm matrix", matrix)
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    require_finite("trace-norm singular values", singular_values)
    value = float(singular_values.sum())
    require_finite("trace norm", value)
    return value


def require_finite_pointer(label, output):
    require_finite(
        label,
        output.null_expectation,
        output.alternative_expectation,
        output.null_alternative_probability,
        output.alternative_probability,
        output.probability_gap,
        output.equal_prior_success,
        output.null_error,
        output.alternative_error,
    )


def require_finite_report(report, path="results"):
    """Final backstop for every numeric field serialized into the report."""
    if isinstance(report, dict):
        for key, value in report.items():
            require_finite_report(value, f"{path}.{key}")
    elif isinstance(report, (list, tuple)):
        for index, value in enumerate(report):
            require_finite_report(value, f"{path}[{index}]")
    elif isinstance(report, (int, float, complex, np.number)):
        require_finite(path, report)


def paulis(n):
    answer = []
    for indices in product(range(4), repeat=n):
        p = np.ones((1, 1), dtype=complex)
        for index in indices:
            p = np.kron(p, SINGLE[index])
        answer.append(p)
    return answer


def unitary(dim):
    z = RNG.normal(size=(dim, dim)) + 1j * RNG.normal(size=(dim, dim))
    q, r = np.linalg.qr(z)
    require_finite("unitary QR factors", q, r)
    result = q * (np.diag(r) / abs(np.diag(r))).conj()
    require_finite("sampled unitary", result)
    return result


def min_eigenvalue(matrix):
    require_finite("eigenvalue input matrix", matrix)
    values = np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)
    require_finite("eigenvalues", values)
    return float(values[0])


def norm2(matrix):
    require_finite("operator-norm matrix", matrix)
    values = np.linalg.svd(matrix, compute_uv=False)
    require_finite("operator-norm singular values", values)
    return float(values[0])


def superoperator(basis, u):
    require_finite("superoperator inputs", basis, u)
    transformed = np.array([u @ b @ u.conj().T for b in basis])
    result = np.einsum("aij,bij->ab", basis.conj(), transformed)
    require_finite("superoperator matrix", result)
    return result


def check_feedback():
    max_feedback_error = 0.0
    max_contraction_excess = 0.0
    max_forward_violation = 0.0
    max_backward_violation = 0.0
    max_nilpotence_error = 0.0
    max_trace_bound_violation = 0.0
    port_cases = 0
    state_cases = 0
    for n, k in [(1, 0), (1, 1), (2, 1)]:
        d, K = 2**n, 2**k
        D, memory_operators = d * K, K * K
        system_ps, memory_ps = paulis(n), paulis(k)
        basis = np.array([
            np.kron(p, q) / math.sqrt(D)
            for p in system_ps for q in memory_ps
        ])
        H = D * D
        identity = np.eye(H, dtype=complex)
        selectors = [
            identity[:, a * memory_operators:(a + 1) * memory_operators]
            for a in range(d * d)
        ]
        Q0 = selectors[0] @ selectors[0].conj().T
        for T in [1, 2, 4]:
            for mixture_weight in [1.0, 0.37]:
                controls = []
                for _ in range(T):
                    C = mixture_weight * superoperator(basis, unitary(D))
                    if mixture_weight < 1:
                        C += (1 - mixture_weight) * superoperator(
                            basis, unitary(D)
                        )
                    controls.append(C)
                R = [Q0 @ C for C in controls]
                prefix = [identity]
                for Rt in R:
                    prefix.append(Rt @ prefix[-1])
                suffix = [None] * (T + 1)
                suffix[T] = identity
                for t in range(T - 1, -1, -1):
                    suffix[t] = suffix[t + 1] @ R[t]
                A = prefix[T]
                sum_FF = np.zeros((H, H), dtype=complex)
                sum_BB = np.zeros((H, H), dtype=complex)
                ports = []
                for a, J in enumerate(selectors[1:], start=1):
                    F = np.vstack([
                        J.conj().T @ controls[t] @ prefix[t]
                        for t in range(T)
                    ])
                    B = np.hstack([
                        suffix[t + 1] @ J for t in range(T)
                    ])
                    G = np.zeros(
                        (T * memory_operators, T * memory_operators),
                        dtype=complex,
                    )
                    for s in range(T):
                        propagated = J.copy()
                        for t in range(s + 1, T):
                            row = slice(t * memory_operators,
                                        (t + 1) * memory_operators)
                            col = slice(s * memory_operators,
                                        (s + 1) * memory_operators)
                            G[row, col] = J.conj().T @ controls[t] @ propagated
                            propagated = R[t] @ propagated
                    whole_map = np.block([[A, B], [F, G]])
                    max_contraction_excess = finite_max(
                        max_contraction_excess, norm2(whole_map) - 1
                    )
                    max_nilpotence_error = finite_max(
                        max_nilpotence_error, norm2(np.linalg.matrix_power(G, T))
                    )
                    sum_FF += F.conj().T @ F
                    sum_BB += B @ B.conj().T
                    ports.append((J @ J.conj().T, B, F, G))
                    port_cases += 1
                max_forward_violation = finite_max(
                    max_forward_violation,
                    -min_eigenvalue(identity - A.conj().T @ A - sum_FF),
                )
                max_backward_violation = finite_max(
                    max_backward_violation,
                    -min_eigenvalue(identity - A @ A.conj().T - sum_BB),
                )
                diagonal = np.diag([1] * (D // 2) + [-1] * (D // 2))
                U = unitary(D)
                traceless = U @ diagonal @ U.conj().T
                for lam in [0.0, 0.2, 0.7, 0.99, 1.0]:
                    direct_maps = []
                    for Qa, B, F, G in ports:
                        direct = identity
                        for C in controls:
                            direct = (Q0 + lam * Qa) @ C @ direct
                        feedback = A + lam * B @ np.linalg.solve(
                            np.eye(len(G)) - lam * G, F
                        )
                        max_feedback_error = finite_max(
                            max_feedback_error, norm2(direct - feedback)
                        )
                        direct_maps.append(direct)
                    average_map = sum(direct_maps) / len(direct_maps)
                    for q in [0.2, 0.6, 1.0]:
                        rho = (np.eye(D) + q * traceless) / D
                        coefficients = np.einsum("bij,ij->b", basis.conj(), rho)
                        delta_coeff = (average_map - A) @ coefficients
                        delta = np.einsum("b,bij->ij", delta_coeff, basis)
                        actual = trace_norm(delta) / 2
                        P = D * float(np.trace(rho @ rho).real)
                        bound = protocols.mixture_distance_bound(n, lam, P, T)
                        require_finite("mixture comparison", rho, actual, P, bound)
                        max_trace_bound_violation = finite_max(
                            max_trace_bound_violation, float(actual - bound)
                        )
                        state_cases += 1
    # The constant at T=1 is exactly attained for the mixture objective.
    saturation_errors = []
    for n in [1, 2, 3]:
        d, M, lam = 2**n, 4**n - 1, 0.73
        delta = lam * paulis(n)[1] / (M * d)
        actual = trace_norm(delta) / 2
        saturation_errors.append(abs(float(actual) - lam / (2 * M)))
    report = {
        "open_port_cases": port_cases,
        "state_bound_cases": state_cases,
        "max_feedback_operator_norm_error": max_feedback_error,
        "max_block_contraction_excess": max_contraction_excess,
        "max_forward_budget_psd_violation": max_forward_violation,
        "max_backward_budget_psd_violation": max_backward_violation,
        "max_nilpotence_operator_norm_error": max_nilpotence_error,
        "max_trace_bound_violation": max_trace_bound_violation,
        "max_T1_saturation_error": finite_max(saturation_errors),
    }
    for key, value in report.items():
        require_finite(f"feedback diagnostic {key}", value)
        if "cases" not in key and value > 1e-10:
            raise AssertionError((key, value))
    return report


def parameters(M, lam):
    n = int(round(math.log(M + 1, 4)))
    p = protocols.weak_scan_parameters(n, lam)
    g, ell, h, L, t, x = (p.gamma, p.effective_strength, p.h,
                          p.block_length, p.t, p.sin_squared_angle)
    require_finite("weak-scan parameters", g, ell, h, L, t, x)
    c, s = math.sqrt(1 - x), math.sqrt(x)
    active = np.array([[ell * c, ell * s], [-s, c]])
    log_c = math.log1p(-x) / 2
    k0 = math.exp(L * log_c)
    kell = float(np.linalg.matrix_power(active, L)[1, 1])
    gap = math.exp((M - 1) * L * log_c) * (k0 - kell) / 2
    require_finite("independent weak-scan evaluation",
                   c, s, active, k0, kell, gap)
    return g, ell, h, L, t, x, c, s, k0, kell, gap


def check_finite_scan():
    rows = []
    max_root_formula_error = 0.0
    min_ratio = None
    max_api_output_error = 0.0
    for M in [3, 15, 63, 255, 1023]:
        lambdas = {0.500001, 0.6, 0.8, 0.95, 0.9999, 1.0}
        lambdas.update(1 - r / M for r in [0.25, 0.75, 1, 2, 8])
        for lam in sorted(l for l in lambdas if l > 0.5):
            g, ell, h, L, t, x, c, s, k0, kell, gap = parameters(M, lam)
            discriminant_root = math.sqrt(1 - h * h * x)
            rp = ((1 + ell) * c + g * discriminant_root) / 2
            rm = ((1 + ell) * c - g * discriminant_root) / 2
            b = (c / discriminant_root - 1) / 2
            root_formula = (1 + b) * rp**L - b * rm**L
            require_finite("characteristic-root formula",
                           discriminant_root, rp, rm, b, root_formula)
            max_root_formula_error = finite_max(
                max_root_formula_error, abs(kell - root_formula)
            )
            tau = (h - 1) * t
            scale = 1.0 if lam == 1 else finite_min(1.0, lam / (M * (1 - lam)))
            ratio = gap / scale
            require_finite("crossover scale and ratio", tau, scale, ratio)
            min_ratio = ratio if min_ratio is None else finite_min(min_ratio, ratio)
            n = int(round(math.log(M + 1, 4)))
            api_gap = protocols.weak_scan_output(n, lam).probability_gap
            require_finite("weak scan API probability gap", api_gap)
            max_api_output_error = finite_max(max_api_output_error, abs(gap - api_gap))
            decision_bound = protocols.mixture_distance_bound(n, lam, 2.0, M * L)
            require_finite("finite-query decision bound", decision_bound)
            if api_gap > decision_bound + 1e-9:
                raise AssertionError(("scan_vs_finite_query_bound", n, lam, api_gap))
            inequalities = {
                "discriminant_margin": 1 / 128 - h * h * x,
                "root_upper_bound": 1 - h * x / 2 - rp,
                "coefficient_upper_bound": h * h * x - b,
                "block_gap_bound": k0 - kell - 49 * tau / 64,
                "null_survival_bound": k0**(M - 1) - 15 / 16,
                "finite_analytic_bound": gap - ell / (32 * (M * g + 1 + ell)),
                "uniform_bias_bound": gap - scale / 128,
            }
            for label, margin in inequalities.items():
                require_finite(f"crossover inequality {label}", margin)
                if margin < -1e-9:
                    raise AssertionError((M, lam, label, margin))
            if M * L > 33 * M / g + 1e-8:
                raise AssertionError(("query_count", M, lam, L))
            rows.append({
                "M": M, "lambda": lam, "effective_lambda": ell,
                "L": L, "queries": M * L, "exact_pointer_gap": gap,
                "min_scale": scale, "gap_over_scale": ratio,
            })
    if finite_max(max_root_formula_error, max_api_output_error) > 1e-8:
        raise AssertionError(("root_formula", max_root_formula_error))
    return {
        "cases": len(rows),
        "max_root_formula_error": max_root_formula_error,
        "max_API_output_error": max_api_output_error,
        "min_gap_over_predicted_scale": min_ratio,
        "required_universal_constant": 1 / 128,
    }


def partial_system(x, d, K):
    require_finite("partial-trace matrix", x)
    result = np.einsum("iaib->ab", x.reshape(d, K, d, K))
    require_finite("partial trace", result)
    return result


def sector(x, p, K):
    d = len(p)
    require_finite("sector inputs", x, p)
    result = np.kron(
        p / d, partial_system(np.kron(p, np.eye(K)) @ x, d, K)
    )
    require_finite("sector matrix", result)
    return result


def check_density_circuits():
    ps = paulis(1)
    d, M = 2, 3
    max_scan_error = 0.0
    scan_cases = 0
    ket0, ket1 = np.diag([1, 0]), np.diag([0, 1])
    for lam in [0.55, 0.8, 1.0]:
        g, ell, h, L, t, x, c, s, k0, kell, gap = parameters(M, lam)
        theta = math.asin(s)
        ry = np.array([[math.cos(theta / 2), -math.sin(theta / 2)],
                       [math.sin(theta / 2), math.cos(theta / 2)]])
        rotation = np.kron(np.eye(d), ry)
        z = np.kron(np.eye(d), SINGLE[3])
        q = ell / lam
        for hidden in [0, 1, 2, 3]:
            rho = np.kron(np.eye(d) / d, ket0).astype(complex)
            for candidate in [1, 2, 3]:
                V = np.kron(np.eye(d), ket0) + np.kron(ps[candidate], ket1)
                for _ in range(L):
                    rho = rotation @ rho @ rotation.conj().T
                    rho = V @ rho @ V.conj().T
                    queried = sector(rho, np.eye(d), 2)
                    if hidden:
                        queried += lam * sector(rho, ps[hidden], 2)
                    rho = V @ queried @ V.conj().T
                    rho = (1 + q) * rho / 2 + (1 - q) * z @ rho @ z / 2
                rho = (rho + z @ rho @ z) / 2
            actual = float(np.trace(z @ rho).real)
            expected = k0**M if hidden == 0 else k0**(M - 1) * kell
            require_finite("full-density scan comparison", rho, actual, expected)
            max_scan_error = finite_max(max_scan_error, abs(actual - expected))
            scan_cases += 1
    B = M + 1
    V = np.zeros((d * B * 2, d * B * 2), dtype=complex)
    for b in range(B):
        label = np.zeros((B, B))
        label[b, b] = 1
        V += np.kron(np.eye(d), np.kron(label, ket0))
        V += np.kron(ps[b], np.kron(label, ket1))
    pointer_plus = np.array([[1, 1], [1, 1]], dtype=complex) / 2
    initial = np.kron(np.eye(d) / d, np.kron(np.eye(B) / B, pointer_plus))
    pointer_X = np.kron(np.eye(d * B), SINGLE[1])
    max_label_error = 0.0
    label_cases = 0
    for lam in [0.0, 0.1, 0.5, 1.0]:
        for hidden in [0, 1, 2, 3]:
            rho = V @ initial @ V.conj().T
            queried = sector(rho, np.eye(d), B * 2)
            if hidden:
                queried += lam * sector(rho, ps[hidden], B * 2)
            rho = V @ queried @ V.conj().T
            actual = float(np.trace(pointer_X @ rho).real)
            expected = (1 + (lam if hidden else 0)) / B
            require_finite("mixed-label density comparison", rho, actual, expected)
            max_label_error = finite_max(max_label_error, abs(actual - expected))
            label_cases += 1
    if finite_max(max_scan_error, max_label_error) > 1e-10:
        raise AssertionError(("density_circuit", max_scan_error, max_label_error))
    return {
        "scan_cases": scan_cases,
        "max_scan_bloch_formula_error": max_scan_error,
        "mixed_label_cases": label_cases,
        "max_mixed_label_formula_error": max_label_error,
    }


def hs2(x):
    require_finite("Hilbert-Schmidt input", x)
    value = float(np.vdot(x, x).real)
    require_finite("squared Hilbert-Schmidt norm", value)
    return value


def oracle(x, p, lam, k):
    return sector(x, np.eye(len(p)), k) + lam * sector(x, p, k)


def random_state(dim, pure):
    a = RNG.normal(size=(dim, 1 if pure else dim)) + 1j * RNG.normal(size=(dim, 1 if pure else dim))
    rho = a @ a.conj().T
    result = rho/np.trace(rho)
    require_finite("sampled state", result)
    return result


def check_purity_potential():
    rows=[]
    largest_violation=0.
    for n, k in [(1, 1), (1, 2), (2, 1), (2, 2), (3, 2)]:
        d=2**n
        ps=paulis(n)[1:]
        for lam in [0.2, 0.7, 0.98]:
            for pure in [False, True]:
                initial=random_state(d*k, pure)
                null=initial.copy()
                alternatives=[initial.copy() for _ in ps]
                for t in range(1, 13):
                    u,v=unitary(d*k),unitary(d*k)
                    def control(x):
                        return .6*(u@x@u.conj().T)+.4*(v@x@v.conj().T)
                    null=sector(control(null), np.eye(d), k)
                    alternatives=[oracle(control(r),p,lam,k) for r,p in zip(alternatives,ps)]
                    actual=sum(hs2(r-null) for r in alternatives)/len(ps)
                    bound=lam**2/(1-lam**2)*(hs2(initial)-hs2(null))/len(ps)
                    require_finite("purity-potential comparison", actual, bound)
                    largest_violation=finite_max(largest_violation,actual-bound)
                    if actual > bound + 1e-11:
                        raise AssertionError((n,k,lam,pure,t,actual,bound))
                rows.append({'n':n,'K':k,'lambda':lam,'pure':pure,'T':12,'mean_HS_squared':actual,'bound':bound})
    return {'instances':len(rows)*12,'largest_positive_violation':largest_violation}


def check_exact_gadget():
    max_error=0.
    cases=0
    for n in [1,2]:
        d=2**n
        ps=paulis(n)[1:]
        rho=random_state(2,False)
        initial=np.kron(np.eye(d)/d,rho)
        for a,p in enumerate(ps):
            for b,q in enumerate(ps):
                v=np.kron(np.eye(d),np.diag([1,0]))+np.kron(q,np.diag([0,1]))
                for lam in [0.,.4,1.]:
                    actual=v@oracle(v@initial@v.conj().T,p,lam,2)@v.conj().T
                    eta=lam if a==b else 0.
                    target=rho.copy()
                    target[0,1]*=eta
                    target[1,0]*=eta
                    target=np.kron(np.eye(d)/d,target)
                    err=max_abs(actual - target)
                    max_error=finite_max(max_error,err)
                    cases+=1
                    if err>1e-12:
                        raise AssertionError((n,a,b,lam,err))
    return {'cases':cases,'max_entry_error':max_error}


def check_near_unit_scan():
    """Check the canonical scan with mandatory boundary dephasing."""
    cases = 0
    max_ideal_error = 0.0
    max_position_formula_error = 0.0
    max_near_unit_error = 0.0
    max_near_unit_certificate = 0.0
    for n in [1, 2, 3, 4, 5]:
        M = protocols.label_count(n)
        L = 50 * M
        log_c = math.log1p(-math.sin(math.pi / L)**2) / 2
        for gamma_M in [0.0, 1e-3, 1e-2, 1e-1, 1.0, 10.0]:
            gamma = gamma_M / M
            if gamma >= 1:
                continue
            lam = 1 - gamma
            output = protocols.near_unit_scan_output(n, lam, L)
            require_finite_pointer("near-unit output", output)
            dephase = np.diag([0.0, 1.0])
            inactive = dephase @ protocols.bloch_block(0.0, math.pi / L, L)
            active = dephase @ protocols.bloch_block(lam, math.pi / L, L)
            require_finite("near-unit block matrices", inactive, active)
            for position in sorted({0, M // 2, M - 1}):
                explicit = (
                    np.linalg.matrix_power(inactive, M - position - 1)
                    @ active
                    @ np.linalg.matrix_power(inactive, position)
                    @ np.array([0.0, 1.0])
                )
                require_finite("near-unit explicit hidden-position output", explicit)
                max_position_formula_error = finite_max(
                    max_position_formula_error,
                    abs(float(explicit[1]) - output.alternative_expectation),
                )
                if gamma_M == 0:
                    max_ideal_error = finite_max(
                        max_ideal_error,
                        abs(output.null_expectation - math.exp(M * L * log_c)),
                        abs(output.alternative_expectation
                            + math.exp((M - 1) * L * log_c)),
                    )
                if gamma_M == 1e-3:
                    observed = finite_max(output.null_error, output.alternative_error)
                    certificate = protocols.near_unit_scan_error_bound(n, lam, L)
                    require_finite("near-unit error comparison", observed, certificate)
                    max_near_unit_error = finite_max(max_near_unit_error, observed)
                    max_near_unit_certificate = finite_max(
                        max_near_unit_certificate, certificate
                    )
                    if observed > certificate + 1e-9 or certificate >= 0.075:
                        raise AssertionError(("near_unit_error", n, position,
                                              observed, certificate))
                cases += 1
    if finite_max(max_ideal_error, max_position_formula_error) > 1e-8:
        raise AssertionError(("near_unit_formula",
                              max_ideal_error, max_position_formula_error))
    return {
        "cases": cases,
        "boundary_dephasing": True,
        "max_ideal_formula_error": max_ideal_error,
        "max_hidden_position_formula_error": max_position_formula_error,
        "max_observed_error_at_gamma_M_0.001": max_near_unit_error,
        "max_certified_error_at_gamma_M_0.001": max_near_unit_certificate,
    }


def check_endpoint_and_gate_conventions():
    """Check endpoint limits and the phase-sensitive local multiplexer."""
    endpoint_cases = 0
    for n in [1, 3, 5]:
        M = protocols.label_count(n)
        for T in [0, 1, 4]:
            for lam in [0.0, 0.3, 0.99, 1.0]:
                expected_sum = sum(lam**j for j in range(T))
                actual_sum = protocols.geometric_sum(lam, T)
                require_finite("geometric-sum comparison", actual_sum, expected_sum)
                if abs(actual_sum - expected_sum) > 1e-12:
                    raise AssertionError(("geometric_sum", n, T, lam))
                mixed_bound = protocols.mixture_distance_bound(n, lam, 1.0, T)
                require_finite("maximally-mixed bound", mixed_bound)
                if mixed_bound != 0:
                    raise AssertionError(("maximally_mixed", n, T, lam))
                if T == 0 or lam == 0:
                    expected = 0.0
                elif lam == 1:
                    expected = finite_min(1.0, T / (2 * M))
                else:
                    expected = finite_min(1.0, lam * expected_sum / (2 * M))
                actual = protocols.mixture_distance_bound(n, lam, 2.0, T)
                require_finite("endpoint bound comparison", actual, expected)
                if abs(actual - expected) > 1e-12:
                    raise AssertionError(("finite_bound_endpoint", n, T, lam))
                endpoint_cases += 1
        zero_output = protocols.one_clean_output(n, 0.0)
        unit_output = protocols.one_clean_output(n, 1.0)
        require_finite_pointer("zero-strength output", zero_output)
        require_finite_pointer("unit-strength output", unit_output)
        if zero_output.probability_gap != 0:
            raise AssertionError(("zero_signal_protocol", n))
        if unit_output.probability_gap < 1 / 128:
            raise AssertionError(("unit_signal_protocol", n))
    # Four-qubit ordering is query, label-x, label-z, pointer.
    CCZ = np.eye(16, dtype=complex)
    CCX = np.zeros((16, 16), dtype=complex)
    CCS = np.eye(16, dtype=complex)
    for index, (query, x, z, pointer) in enumerate(product(range(2), repeat=4)):
        CCZ[index, index] = (-1)**(query * z * pointer)
        CCS[index, index] = 1j**(x * z * pointer)
        output_query = query ^ (x * pointer)
        out_index = 8 * output_query + 4 * x + 2 * z + pointer
        CCX[out_index, index] = 1
    implemented = CCS @ CCX @ CCZ
    expected = np.zeros((16, 16), dtype=complex)
    label_paulis = [SINGLE[0], SINGLE[3], SINGLE[1], SINGLE[2]]
    for b, p in enumerate(label_paulis):
        label = np.zeros((4, 4))
        label[b, b] = 1
        expected += np.kron(np.eye(2), np.kron(label, np.diag([1, 0])))
        expected += np.kron(p, np.kron(label, np.diag([0, 1])))
    gate_error = max_abs(implemented - expected)
    if gate_error > 1e-12:
        raise AssertionError(("local_multiplexer_native_gates", gate_error))
    return {
        "endpoint_cases": endpoint_cases,
        "local_multiplexer_max_entry_error": gate_error,
    }


def expect_rejection(label, callback, exception_type, message_fragment):
    """A negative control passes only for the intended explicit rejection."""
    try:
        callback()
    except exception_type as error:
        if message_fragment not in str(error):
            raise AssertionError(f"{label}: unexpected rejection: {error}") from error
    else:
        raise AssertionError(f"{label}: invalid input was not rejected")


def check_numerical_guards():
    """Regressions for tiny-angle extrapolation and masked non-finite values."""
    nonfinite_controls = [
        ("NaN maximum", lambda: finite_max(0.0, math.nan)),
        ("infinite minimum", lambda: finite_min(0.0, math.inf)),
        ("NaN matrix norm", lambda: norm2(np.array([[1.0, math.nan], [0.0, 1.0]]))),
    ]
    for label, callback in nonfinite_controls:
        expect_rejection(label, callback, AssertionError, "non-finite")

    # Reproduce the reviewer's failure injection at the actual comparison site.
    original_output = protocols.weak_scan_output

    class NaNOutput:
        probability_gap = math.nan

    try:
        protocols.weak_scan_output = lambda n, strength: NaNOutput()
        expect_rejection(
            "NaN weak-scan API gap", check_finite_scan,
            AssertionError, "weak scan API probability gap: non-finite",
        )
    finally:
        protocols.weak_scan_output = original_output

    domain_rejections = 0
    for output_function in [
        protocols.weak_scan_output,
        protocols.near_unit_scan_output,
        protocols.coherent_scan_output,
        protocols.one_clean_output,
    ]:
        expect_rejection(
            f"{output_function.__name__} n=12",
            lambda function=output_function: function(12, 1.0),
            ValueError, "numerical scan outputs support only",
        )
        domain_rejections += 1
    for output_function in [
        protocols.near_unit_scan_output, protocols.coherent_scan_output
    ]:
        for L in [1, 100 * protocols.label_count(5) + 1]:
            expect_rejection(
                f"{output_function.__name__} L={L}",
                lambda function=output_function, length=L: function(5, 1.0, length),
                ValueError, "numerical scan outputs require",
            )
            domain_rejections += 1

    # The artificial output guard must not restrict analytical APIs.
    general_parameters = protocols.weak_scan_parameters(12, 1.0)
    require_finite(
        "general parameter and analytical bound APIs",
        general_parameters.gamma,
        general_parameters.effective_strength,
        general_parameters.angle,
        protocols.weak_scan_gap_lower_bound(12, 1.0),
        protocols.mixture_distance_bound(12, 0.7, 2.0, 100),
        protocols.near_unit_scan_error_bound(12, 1.0),
    )
    require_finite_report(protocols.near_unit_scan_costs(12))
    require_finite_report(general_parameters.costs)

    # Exercise both supported length boundaries against stable endpoint formulas.
    boundary_cases = 0
    max_endpoint_formula_error = 0.0
    for n in [1, 5]:
        M = protocols.label_count(n)
        for L in [2, 100 * M]:
            u = math.sin(math.pi / L)**2
            null_reference = 0.0 if u == 1 else math.exp(
                M * L * math.log1p(-u) / 2
            )
            ideal_alt_reference = 0.0 if u == 1 else -math.exp(
                (M - 1) * L * math.log1p(-u) / 2
            )
            for strength in [0.0, 0.6, 1.0]:
                outputs = [
                    protocols.near_unit_scan_output(n, strength, L),
                    protocols.coherent_scan_output(n, strength, L, 0),
                    protocols.coherent_scan_output(n, strength, L, M - 1),
                ]
                for output in outputs:
                    require_finite_pointer("supported numerical boundary", output)
                    for probability in [
                        output.null_alternative_probability,
                        output.alternative_probability,
                    ]:
                        if not -1e-12 <= probability <= 1 + 1e-12:
                            raise AssertionError(("nonphysical boundary probability",
                                                  n, L, strength, probability))
                    errors = [abs(output.null_expectation - null_reference)]
                    if strength == 0:
                        errors.append(abs(output.alternative_expectation
                                          - null_reference))
                    elif strength == 1:
                        errors.append(abs(output.alternative_expectation
                                          - ideal_alt_reference))
                    max_endpoint_formula_error = finite_max(
                        max_endpoint_formula_error, finite_max(errors)
                    )
                    boundary_cases += 1
    if max_endpoint_formula_error > 1e-8:
        raise AssertionError(("numerical-domain endpoint discrepancy",
                              max_endpoint_formula_error))
    return {
        "nonfinite_negative_controls_passed": len(nonfinite_controls) + 1,
        "NaN_probability_gap_injection_rejected": True,
        "out_of_domain_rejections": domain_rejections,
        "n12_analytic_apis_still_available": True,
        "supported_boundary_cases": boundary_cases,
        "max_boundary_endpoint_formula_error": max_endpoint_formula_error,
    }


def main():
    results = {
        "numpy_version": np.__version__,
        "seed": 2026103102,
        "purity_potential": check_purity_potential(),
        "exact_pointer_gadget": check_exact_gadget(),
        "feedback": check_feedback(),
        "finite_crossover": check_finite_scan(),
        "full_density_circuits": check_density_circuits(),
        "near_unit_scan": check_near_unit_scan(),
        "endpoint_and_gate_conventions": check_endpoint_and_gate_conventions(),
        "numerical_guard_regressions": check_numerical_guards(),
        "scan_output_domain": {
            "n_min": 1,
            "n_max": protocols.MAX_NUMERICAL_SCAN_QUBITS,
            "block_length_min": 2,
            "block_length_max_multiple_of_M":
                protocols.MAX_NUMERICAL_BLOCK_MULTIPLIER,
        },
        "scope": (
            "Finite floating-point diagnostics, not absolute or interval "
            "certificates; analytical proofs are separate."
        ),
    }
    require_finite_report(results)
    output = json.dumps(results, indent=2, allow_nan=False) + "\n"
    (OUT / "results.json").write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
