"""Finite checks for the linear-purity, logarithmic-query spike detector.

Run from the repository root: python verification/verify_linear_purity.py
Only Python's standard library is required. Exact arithmetic is used for
the Bell readout, small stopping processes and truncated likelihoods.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
import json
import math
from pathlib import Path


AXES = range(1, 4)
ERRORS = range(4)
DRIFT = (3 * math.log(1.5) + math.log(0.5)) / 4
AFFINITY = (math.sqrt(1.5) + math.sqrt(0.5)) / 2


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def sign(axis, error):
    """Pauli conjugation signs in order I, X, Y, Z."""
    return -1 if axis and error and axis != error else 1


def bell_readout(input_bit, error):
    """Direct three-qubit circuit on a computational input and two clean slots."""
    state = [0j] * 8
    state[4 * input_bit] = 1
    # Wires, high bit first: query, probe tape, reference tape.
    state[4 * input_bit + 2] = 1
    state = [state[index ^ (1 if index & 2 else 0)] for index in range(8)]

    def swap_query_and_probe(index):
        return index ^ (6 if bool(index & 4) != bool(index & 2) else 0)

    state = [state[swap_query_and_probe(index)] for index in range(8)]
    phases = (1, 1, 1j, 1)
    flipped = error in (1, 2)
    transformed = [0j] * 8
    for index, amplitude in enumerate(state):
        phase = -phases[error] if error in (2, 3) and index & 4 else phases[error]
        transformed[index ^ (4 if flipped else 0)] = phase * amplitude
    state = [transformed[swap_query_and_probe(index)] for index in range(8)]
    state = [state[index ^ (1 if index & 2 else 0)] for index in range(8)]
    decoded = [state[index & ~2] + (-1 if index & 2 else 1) * state[index | 2]
               for index in range(8)]

    # Both H normalization factors were suppressed. The nonzero amplitude
    # therefore has magnitude two even for Y, where its phase is imaginary.
    output, = [index for index, amplitude in enumerate(decoded) if amplitude]
    require(abs(decoded[output]) == 2, "incorrect probability in Bell decoder")
    return output >> 2, output & 3


def check_bell_readout():
    """Compare physical outcome bits and the sign statistics read from them."""
    code = (0, 1, 3, 2)
    for input_bit, error in product(range(2), ERRORS):
        require(bell_readout(input_bit, error) == (input_bit, code[error]),
                "Bell decoding or restoration of the untouched query bit failed")

    # Output bits are the X⊗X and Z⊗Z sign bits. The Y character is
    # their product, corresponding to the transposed Y on the reference.
    for hidden in ERRORS:
        weights = [Fraction(2 + sign(hidden, error), 8)
                   if hidden else Fraction(1, 4) for error in ERRORS]
        require(sum(weights) == 1, "Pauli-error law is not normalized")
        for axis in AXES:
            read_mask = (0, 2, 3, 1)[axis]
            plus = Fraction(0)
            for error, weight in enumerate(weights):
                bits = bell_readout(0, error)[1]
                decoded_sign = (-1) ** ((bits & read_mask).bit_count())
                require(decoded_sign == sign(axis, error), "wrong Bell sign")
                if decoded_sign == 1:
                    plus += weight
            require(plus == (Fraction(3, 4) if axis == hidden else Fraction(1, 2)),
                    "the target and inactive axes do not have the stated biases")
    return {"circuit_basis_cases": 8, "axis_marginal_cases": 12}


def exact_site_process(deadline, hidden, low, high):
    """Nonterminal likelihood vectors and their exact local probabilities."""
    states = {(Fraction(1),) * 3: Fraction(1)}
    weights = [Fraction(2 + sign(hidden, error), 8)
               if hidden else Fraction(1, 4) for error in ERRORS]
    active_probabilities = []
    crossing_probabilities = [Fraction(0)] * 3
    for _ in range(deadline):
        active_probabilities.append(sum(states.values()))
        following = defaultdict(Fraction)
        for likelihoods, mass in states.items():
            for error, weight in enumerate(weights):
                next_state = []
                branch_mass = mass * weight
                for index, likelihood in enumerate(likelihoods):
                    if likelihood:
                        likelihood *= Fraction(2 + sign(index + 1, error), 2)
                        if likelihood >= high:
                            crossing_probabilities[index] += branch_mass
                    next_state.append(likelihood if low < likelihood < high else 0)
                if any(next_state):
                    following[tuple(next_state)] += branch_mass
        states = following
    return active_probabilities, crossing_probabilities


def binomial_tail(trials, rate, cutoff):
    """Probability that more than cutoff independent sites are live."""
    return sum(math.comb(trials, count) * rate**count * (1 - rate)**(trials - count)
               for count in range(max(0, cutoff + 1), trials + 1))


def check_stopping_and_caps():
    """Evaluate exact toy stopping laws and the overflow tail they imply."""
    deadline, low, high = 144, Fraction(1, 4), Fraction(4)
    null_active, null_crossing = exact_site_process(deadline, 0, low, high)
    live_cases = 0
    for hidden in AXES:
        active, crossing = exact_site_process(deadline, hidden, low, high)
        require(crossing[hidden - 1] > null_crossing[hidden - 1],
                "sequential test failed to distinguish the biased target axis")
        for axis in AXES:
            if axis != hidden:
                require(crossing[axis - 1] == null_crossing[axis - 1],
                        "a neighboring axis changed its stopping law")
        require(active[0] == 1 and all(a >= b for a, b in zip(active, active[1:])),
                "a stopped site became active again")

    n = 19
    error_allowance = Fraction(1, 3)
    for t, active in enumerate(null_active):
        mean_bound = n * min(1.0, 3 * float(low) ** (-0.5) * AFFINITY**t)
        require(n * float(active) <= mean_bound + 1e-12,
                "the affinity estimate missed a finite live-site probability")
        budget = min(n, math.ceil(2 * mean_bound + math.log2(4 * deadline /
                                                             float(error_allowance)) + 1))
        if budget < n:
            overflow = binomial_tail(n - 1, active, budget - 1)
            require(overflow <= error_allowance / (4 * deadline),
                    "the cap did not bound the tail including a distinguished site")
            live_cases += 1
    require(live_cases, "the finite cap checks never reached a nontrivial cap")

    # Exercise actual overflow, including round slots that cannot borrow
    # capacity from one another. The given potential paths are independent
    # probes, so ignoring unselected terms cannot change earlier records.
    first_two_errors = ((0, 0), (0, 1))
    tiny_deadline, tiny_low, tiny_high = 3, Fraction(1, 3), Fraction(9, 4)
    branches = set()
    for caps in ((2, 2, 2), (2, 1, 2), (2, 2, 0)):
        likelihoods = [[Fraction(1)] * 3 for _ in range(2)]
        slot_counts = []
        accepted = False
        overflowed = False
        for t, cap in enumerate(caps):
            active_sites = [site for site, values in enumerate(likelihoods) if any(values)]
            if len(active_sites) > cap:
                overflowed = True
                slot_counts.extend([0] * (tiny_deadline - t))
                break
            slot_counts.append(len(active_sites))
            for site in active_sites:
                error = first_two_errors[site][t] if t < 2 else 2
                for index, value in enumerate(likelihoods[site]):
                    value *= Fraction(2 + sign(index + 1, error), 2)
                    accepted |= value >= tiny_high
                    likelihoods[site][index] = value if tiny_low < value < tiny_high else 0
        if overflowed:
            branches.add("overflow")
        elif accepted:
            branches.add("acceptance")
        require(len(slot_counts) == tiny_deadline and
                all(used <= reserved for used, reserved in zip(slot_counts, caps)),
                "the fixed slate of slots was breached")
    require(branches == {"overflow", "acceptance"}, "cap fixtures missed a control branch")
    return {"exact_site_rounds_per_law": deadline, "cap_fixture_schedules": 3,
            "null_crossing_probability": float(null_crossing[0]),
            "finite_capped_tail_cases": live_cases}


def check_finite_parameters():
    """Check the deadline and deterministic tape bounds against their formulas."""
    cases = 0
    for n, delta in product((1, 19, 300, 10_000, 1_000_000), (1/3, 1/10, 1/100)):
        low, high = delta / 4, 12 * n / delta
        concentration = math.log(3) * math.sqrt(math.log(4 / delta) / 2)
        root = (concentration + math.sqrt(concentration**2 + 4 * DRIFT * math.log(high))
                ) / (2 * DRIFT)
        deadline = math.ceil(root**2)
        require(DRIFT * deadline - math.log(high) + 1e-12 >=
                concentration * math.sqrt(deadline), "query deadline misses concentration")
        log_budget = math.log2(4 * deadline / delta)
        slots = 0
        for t in range(deadline):
            mean_bound = n * min(1.0, 3 * low ** (-0.5) * AFFINITY**t)
            budget = min(n, math.ceil(2 * mean_bound + log_budget + 1))
            if budget < n:
                require(mean_bound - (budget - 1) * math.log(2) <=
                        math.log(delta / (4 * deadline)) + 1e-12,
                        "the per-round union bound lost the distinguished site")
            slots += budget
        require(slots <= 6 * n / (math.sqrt(low) * (1 - AFFINITY)) +
                deadline * (log_budget + 2), "invalid fixed-tape upper bound")
        cases += 1
    return {"system_sizes_and_errors": cases}


def check_likelihood_converse():
    """Enumerate small Pauli-error streams without using the Fourier lemma."""
    checked_pairs = 0
    maximum_tv = 0.0
    for n, deadline in ((1, 1), (1, 4), (2, 2), (2, 3)):
        labels = tuple(product(range(n), AXES))
        outcomes = list(product(ERRORS, repeat=n * deadline))
        null_mass = Fraction(1, len(outcomes))
        likelihoods = []
        for path in outcomes:
            likelihoods.append(tuple(Fraction(math.prod(
                2 + sign(axis, path[t * n + site]) for t in range(deadline)), 2**deadline)
                for site, axis in labels))
        for first, second in combinations(range(len(labels)), 2):
            joint = Counter((row[first], row[second]) for row in likelihoods)
            left = Counter(row[first] for row in likelihoods)
            right = Counter(row[second] for row in likelihoods)
            require(all(joint[x, y] * len(outcomes) == count_x * count_y
                        for x, count_x in left.items() for y, count_y in right.items()),
                    "the distinct Pauli likelihood paths are not pairwise independent")
            checked_pairs += 1

        mixture = [sum(row) / len(labels) for row in likelihoods]
        tv = null_mass * sum(abs(value - 1) for value in mixture) / 2
        maximum_tv = max(maximum_tv, float(tv))
        require(null_mass * sum(mixture) == 1, "mixture is not normalized")
        for threshold in (Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(3)):
            truncated = [sum((value for value in row if value <= threshold), Fraction(0))
                         / len(labels)
                         for row in likelihoods]
            mean = null_mass * sum(truncated)
            variance = null_mass * sum((value - mean)**2 for value in truncated)
            require(variance <= threshold / len(labels), "truncated variance is too large")
            tail = null_mass * sum(row[0] for row in likelihoods if row[0] > threshold)
            require(mean == 1 - tail, "truncation mass is not the active-tail probability")
            require(float(tv) <= float(tail) + 0.5 * math.sqrt(float(variance)) + 1e-12,
                    "finite binary-mixture distance exceeded its truncation bound")
    return {"transcript_families": 4, "pairwise_independence_cases": checked_pairs,
            "largest_exact_mixture_tv": maximum_tv}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="also write the JSON summary to this path")
    args = parser.parse_args()
    result = {
        "bell_readout": check_bell_readout(),
        "stopping_and_tape": check_stopping_and_caps(),
        "finite_parameters": check_finite_parameters(),
        "likelihood_converse": check_likelihood_converse(),
    }
    rendered = json.dumps(result, indent=2, allow_nan=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
