# Project understanding map: 30 milestones

This map organizes quantum learning without renewed initialization into exactly **30 milestones**. The targets follow the scientific problem and its proof dependencies. They form a common route through the work, independent of any particular reader's background.

The allocation is **10 background/preliminaries milestones** and **20 narrative/innovation milestones**. The background builds a compact finite-dimensional quantum-information toolkit and ends with the complete operational model. The narrative receives more space because the two converse bounds answer different measurement questions, and the finite constructions provide two different guarantees: a matched bias law and a prescribed error near conservation. Their mechanisms, assumptions, and resource costs must be understood before the final synthesis.

The sole educational anchor is **John Watrous, *The Theory of Quantum Information* (2018)**. The [Watrous bridge](WATROUS_BRIDGE.md) identifies the free author manuscript, exact source locations, notation translations, and locally supplied steps. The [science pages](../science/README.md) own the exact statements and full proofs. Research citations support attribution; they do not add educational-anchor requirements.

Each milestone contains a central question, an understanding target, dependencies and a story role, a conceptual connection, and source pointers. The map supports global understanding without claiming to enumerate every technical calculation.

## Route through the project

| Phase | Milestones | Scientific connection |
|---|---|---|
| Background/preliminaries | M01–M04 | States, complete processors, channel access, and the allowed controls |
| Background/preliminaries | M05–M09 | Operator geometry, purity, readable decisions, and pointer dynamics |
| Background/preliminaries | M10 | Synthesis of one fully specified experiment |
| Narrative/innovation | M11–M15 | Hidden Pauli sectors and the individual-distance purity budget |
| Narrative/innovation | M16–M21 | One common effect, finite feedback, and the decision converse |
| Narrative/innovation | M22–M26 | Exact gadget, finite crossover construction, and prescribed error |
| Narrative/innovation | M27–M29 | Resource accounting, the matched law, attribution, and evidence |
| Narrative/innovation | M30 | Synthesis of the complete contribution and its limits |

## Phase I: background/preliminaries

### M01 States and observable probabilities

**Central question.** What mathematical object describes the information present in a quantum register?

**Understanding target.** Interpret a density operator as a positive matrix of trace one, with pure and maximally mixed states as different spectra. Relate a measured probability to the trace of a state against a positive effect. Keep a state, a vector representing a pure state, and a classical outcome distinct.

**Dependencies and story role.** No earlier milestone is required. Introduces the local objects from which the full experiment is built.

**Conceptual connection.** A readable output probability depends on both the prepared state and the chosen measurement; neither the number of matrix entries nor purity alone specifies that probability.

**Source pointers.** [Watrous §§2.1.2 and 2.3.1](WATROUS_BRIDGE.md#targeted-reading-from-watrous); [state and decision conventions](../science/model.md), (M5)–(M8).

### M02 The complete processor and its marginals

**Central question.** Which registers remain available when the unknown channel acts?

**Understanding target.** Separate the queried register $S$ from protected workspace $A$, and distinguish their dimensions $d$ and $K$ from the total dimension $D=dK$. Use the partial trace to describe a marginal without assuming that the joint state is a product. Include every retained quantum or classical record in the processor.

**Dependencies and story role.** [M01](#m01-states-and-observable-probabilities). Expands one register into the physical system on which the resource constraint is imposed.

**Conceptual connection.** A channel can erase $S$ while leaving correlations or information in $A$. Tracking only the query marginal would miss both stored information and resources used to retain it.

**Source pointers.** [Watrous §1.1.2 and §2.1.3](WATROUS_BRIDGE.md#targeted-reading-from-watrous); [complete processor](../science/model.md), §2.

### M03 Channels and ordinary oracle access

**Central question.** What does one call to an unknown noisy device provide?

**Understanding target.** Understand complete positivity and trace preservation as conditions on an operation that may act on part of a larger state. Distinguish a channel from one of its unitary dilations: the existence of an environment representation does not grant access to that environment, its inverse, or a controlled version of the unknown map.

**Dependencies and story role.** [M01](#m01-states-and-observable-probabilities), [M02](#m02-the-complete-processor-and-its-marginals). Defines the allowed query before any algorithm or lower bound is considered.

**Conceptual connection.** The same input-output channel can have many environmental implementations. A result about ordinary channel calls must not silently use a more informative implementation.

**Source pointers.** [Watrous Definition 2.13, Theorem 2.22 and Corollary 2.27](WATROUS_BRIDGE.md#targeted-reading-from-watrous); [channel promise and access](../science/model.md), §1.

### M04 Unital processing and preparation

**Central question.** Which known operations preserve a fixed supply of initialization?

**Understanding target.** Distinguish trace preservation from unitality, the condition that the identity is fixed. Recognize unitary gates and complete dephasing as allowed controls. Explain why replacement by a pure state is nonunital, and why an unobserved reset can supply purity even without an intermediate recorded measurement.

**Dependencies and story role.** [M02](#m02-the-complete-processor-and-its-marginals), [M03](#m03-channels-and-ordinary-oracle-access). Identifies the operation class that makes preparation a charged resource.

**Conceptual connection.** Dephasing removes off-diagonal terms while keeping populations; resetting changes the populations to a prescribed pure state. This distinction later makes boundary dephasing compatible with the model.

**Source pointers.** [Watrous §§2.2.1–2.2.3](WATROUS_BRIDGE.md#targeted-reading-from-watrous); [preparation and purity accounting](WATROUS_BRIDGE.md#preparation-and-purity-accounting); [global controls](../science/model.md), (M3)–(M4).

### M05 Pauli coordinates for operators

**Central question.** How can an unknown direction in operator space be specified precisely?

**Understanding target.** Use the Hermitian Pauli strings, including the identity, as an orthogonal basis with trace normalization $\mathrm{Tr}(P_aP_b)=d\delta_{ab}$. Distinguish an operator coefficient from an eigenvalue of a state. Understand why $n$ qubits give $M=d^2-1=4^n-1$ nonidentity directions rather than $d-1$.

**Dependencies and story role.** [M01](#m01-states-and-observable-probabilities), [M02](#m02-the-complete-processor-and-its-marginals). Provides coordinates for the hidden mode and the later energy accounting.

**Conceptual connection.** The unknown label chooses an operator direction. The multiplicity of possible directions is an information constraint even though the final answer is only one bit.

**Source pointers.** [Pauli expansion and lifted sectors](WATROUS_BRIDGE.md#pauli-sectors-and-protected-memory); [basis and channel promise](../science/model.md), (M1); [sector projections](../science/purity_bound.md), (P1)–(P3).

### M06 Operator geometry and channel adjoints

**Central question.** Why can both a state and a final measurement be propagated through the same geometry?

**Understanding target.** Interpret the Hilbert–Schmidt inner product and norm as Euclidean geometry on operators. Distinguish this norm from trace and operator norms. Relate a channel adjoint to moving a map from the state to an effect inside a trace. Explain why a unital CPTP map and its adjoint both contract Hilbert–Schmidt norm.

**Dependencies and story role.** [M03](#m03-channels-and-ordinary-oracle-access), [M04](#m04-unital-processing-and-preparation), [M05](#m05-pauli-coordinates-for-operators). Supplies the common mathematical language of the forward and backward proofs.

**Conceptual connection.** Trace preservation makes the adjoint unital, while unitality makes the adjoint trace preserving. Both assumptions are needed to reuse the contraction argument backward.

**Source pointers.** [Watrous §1.1.3, Theorem 2.26 and Theorem 4.27](WATROUS_BRIDGE.md#targeted-reading-from-watrous); [adjoints and contraction](WATROUS_BRIDGE.md#adjoints-and-hilbertschmidt-contraction); [standard norm ingredient](../science/purity_bound.md), (P4).

### M07 Collision purity and mixed workspace

**Central question.** How is one clean qubit distinguished from a large amount of mixed memory?

**Understanding target.** Interpret the dimension-normalized collision purity $\mathcal P=D\mathrm{Tr}(\rho_{\mathrm{in}}^2)$ and its centered form $\mathcal P-1=D\|\rho_{\mathrm{in}}-I/D\|_2^2$. Derive $\mathcal P=2^c$ for $c$ pure qubits with otherwise maximally mixed registers. Explain why appending independent maximally mixed registers leaves $\mathcal P$ unchanged and why the theorem does not identify this number with heat or work.

**Dependencies and story role.** [M01](#m01-states-and-observable-probabilities), [M02](#m02-the-complete-processor-and-its-marginals), [M04](#m04-unital-processing-and-preparation), [M06](#m06-operator-geometry-and-channel-adjoints). Turns the control restriction into a quantitative input resource.

**Conceptual connection.** Increasing memory width can preserve and process correlations without increasing the initial deviation from the maximally mixed state in the normalized resource measure.

**Source pointers.** [Preparation and purity accounting](WATROUS_BRIDGE.md#preparation-and-purity-accounting); [collision purity](../science/model.md), (M5)–(M6); [resource interpretation](../science/interpretation.md), §§3 and 6.

### M08 One final decision and two distance questions

**Central question.** Which distinguishability quantity corresponds to a hidden-label decision?

**Understanding target.** Use halved trace distance as the largest probability difference of one event. Convert it to equal-prior success without losing a factor of two. Distinguish the distance between an averaged alternative state and the null from the average of individually optimized distances; the latter can use a different effect for each label.

**Dependencies and story role.** [M01](#m01-states-and-observable-probabilities), [M02](#m02-the-complete-processor-and-its-marginals), [M06](#m06-operator-geometry-and-channel-adjoints). Connects operator estimates to the actual output and fixes the two converse objectives.

**Conceptual connection.** A large signal for each known alternative does not guarantee that one measurement can read all those signals when the label is unknown. Averaging states and optimizing measurements are different operations.

**Source pointers.** [Watrous Theorem 3.4 and convention translation](WATROUS_BRIDGE.md#one-common-effect-and-two-distances); [decision statistics](../science/model.md), (M7)–(M10).

### M09 A pointer under rotation and dephasing

**Central question.** How can repeated noisy interactions change a single output qubit?

**Understanding target.** Represent a pointer state by its Bloch components and derive the real two-coordinate action of a rotation about $y$ followed by dephasing. Understand which component is preserved by $Z$ dephasing and which becomes a final measurement probability. Keep this elementary dynamics separate from any claim of successful learning.

**Dependencies and story role.** [M01](#m01-states-and-observable-probabilities), [M03](#m03-channels-and-ordinary-oracle-access), [M04](#m04-unital-processing-and-preparation). Introduces the local dynamical ingredients used by the constructive protocols.

**Conceptual connection.** A small rotation can accumulate when coherence survives but be suppressed when each step removes the off-diagonal component. Block-boundary dephasing can preserve the accumulated population difference.

**Source pointers.** [Locally derived pointer dynamics](WATROUS_BRIDGE.md#pointer-dynamics-and-boundary-dephasing); [Watrous complete dephasing, §2.2.3](WATROUS_BRIDGE.md#targeted-reading-from-watrous); [Bloch map](../science/protocols.md), (A8).

### M10 The complete operational question

**Central question.** What does the full experiment receive, do, and return?

**Understanding target.** Combine a fixed unknown channel label, a single initialized processor, known global unital controls, $T$ ordinary calls, and one terminal decision. State which resources may grow and which are fixed. Distinguish known signal strength in the constructions, arbitrary protected mixed workspace, and new purity supplied by restarting an experiment.

**Dependencies and story role.** [M01](#m01-states-and-observable-probabilities), [M02](#m02-the-complete-processor-and-its-marginals), [M03](#m03-channels-and-ordinary-oracle-access), [M04](#m04-unital-processing-and-preparation), [M05](#m05-pauli-coordinates-for-operators), [M06](#m06-operator-geometry-and-channel-adjoints), [M07](#m07-collision-purity-and-mixed-workspace), [M08](#m08-one-final-decision-and-two-distance-questions), [M09](#m09-a-pointer-under-rotation-and-dephasing). Synthesizes the background into the precise question addressed by the research phase.

**Conceptual connection.** The relevant comparison is attainable information at a fixed initialization budget, not merely how many queries a successful algorithm uses. An unrestricted finite running time remains compatible with a bounded output signal.

**Source pointers.** [Complete model](../science/model.md); [complete one-query example](WATROUS_BRIDGE.md#a-complete-one-query-example); [scientific reading route](../science/README.md).

## Phase II: narrative/innovation

### M11 A physical channel with one hidden Pauli mode

**Central question.** Why is the spike promise both physically valid and geometrically useful?

**Understanding target.** Explain how complete depolarization is modified to retain one nonidentity Pauli coefficient with strength $\lambda$. Use the Pauli-error or measure-and-prepare representation to establish that the full oracle is a channel. Lift it to $SA$ as $Q_0+\lambda Q_a$, while recognizing that a nonidentity sector projection $Q_a$ alone need not be positive.

**Dependencies and story role.** [M03](#m03-channels-and-ordinary-oracle-access), [M05](#m05-pauli-coordinates-for-operators), [M10](#m10-the-complete-operational-question). Starts the research argument with its particular physical family and mathematical decomposition.

**Conceptual connection.** A useful proof decomposition can contain nonphysical pieces while their prescribed sum is physical. Treating each sector as a separately available oracle would change the model.

**Source pointers.** [Physical promise](../science/model.md), (M1)–(M2); [orthogonal sectors](../science/purity_bound.md), (P1)–(P3); [Pauli sectors and protected memory](WATROUS_BRIDGE.md#pauli-sectors-and-protected-memory).

### M12 Why protected memory defeats naive contraction

**Central question.** Why does repeated depolarization not erase every useful signal?

**Understanding target.** Identify the invariant operator algebra $\{I_S\otimes X_A:X_A\in\mathsf L(A)\}$ of the null channel, whose density operators have the form $I_S/d\otimes\rho_A$. Follow the query-and-swap example in which a signal is stored in protected memory and survives later calls. Explain why this invalidates strict contraction on the full traceless processor space without violating a hidden-label average bound.

**Dependencies and story role.** [M02](#m02-the-complete-processor-and-its-marginals), [M06](#m06-operator-geometry-and-channel-adjoints), [M10](#m10-the-complete-operational-question), [M11](#m11-a-physical-channel-with-one-hidden-pauli-mode). Isolates the obstacle that the converse must actually overcome.

**Conceptual connection.** The proof must bound how much information can enter and leave the queried sectors over the whole run; it cannot assume that every stored deviation shrinks at every call.

**Source pointers.** [Protected-memory example](../science/interpretation.md), §3; [lifted null](../science/purity_bound.md), §1; [memory and sector geometry](WATROUS_BRIDGE.md#pauli-sectors-and-protected-memory).

### M13 Signal growth with returning memory

**Central question.** How can a previously stored deviation feed the signal again?

**Understanding target.** Write the alternative-minus-null update and separate the returning deviation from the new source supplied by the null state. Understand the completed-square inequality that charges growth to the source while retaining possible feedback from memory. Keep the restriction $\lambda\lt1$ visible in its coefficient.

**Dependencies and story role.** [M06](#m06-operator-geometry-and-channel-adjoints), [M11](#m11-a-physical-channel-with-one-hidden-pauli-mode), [M12](#m12-why-protected-memory-defeats-naive-contraction). Provides the local one-step estimate for the first converse.

**Conceptual connection.** A lower-bound proof can allow feedback rather than discard it: the negative quadratic term controls its best possible benefit instead of assuming the feedback component vanishes.

**Source pointers.** [One-step signal growth](../science/purity_bound.md), (P7)–(P9); [individual-distance proof bridge](WATROUS_BRIDGE.md#the-individual-distance-purity-budget).

### M14 One null trajectory pays for every direction

**Central question.** Why does summing over hidden modes remove the query-count dependence?

**Understanding target.** Apply Pauli-sector orthogonality to the common null state before a query. Relate the total nonidentity sector norm to the drop in null-state purity. Sum this identity over time so that intermediate terms cancel, giving one finite source budget shared across all alternatives.

**Dependencies and story role.** [M07](#m07-collision-purity-and-mixed-workspace), [M11](#m11-a-physical-channel-with-one-hidden-pauli-mode), [M13](#m13-signal-growth-with-returning-memory). Turns the local growth estimate into a global, query-independent potential argument.

**Conceptual connection.** All labels are compared with the same null trajectory. Replacing this common trajectory by separate alternative histories would lose the telescoping resource account.

**Source pointers.** [Null purity budget](../science/purity_bound.md), (P10) and (P5); [individual-distance proof bridge](WATROUS_BRIDGE.md#the-individual-distance-purity-budget).

### M15 From quadratic energy to individual distances

**Central question.** What operational conclusion follows from the first purity budget?

**Understanding target.** Combine the Hilbert–Schmidt estimate, the trace-norm conversion, and Cauchy–Schwarz over labels. Explain how total dimension cancels into the normalized purity $\mathcal P$. Interpret the resulting average individual-distance bound, the zero-signal case $\mathcal P=1$, and its near-conservation consequence for one clean qubit.

**Dependencies and story role.** [M06](#m06-operator-geometry-and-channel-adjoints), [M07](#m07-collision-purity-and-mixed-workspace), [M08](#m08-one-final-decision-and-two-distance-questions), [M14](#m14-one-null-trajectory-pays-for-every-direction). Completes the first converse and identifies the question it leaves open.

**Conceptual connection.** The estimate is independent of query time and memory width, but it still permits a label-dependent optimizing measurement. This motivates a second proof that accounts for the final decision as well as the state.

**Source pointers.** [Individual-distance theorem](../science/purity_bound.md), (P5)–(P6); [Watrous norm inequalities](WATROUS_BRIDGE.md#targeted-reading-from-watrous); [two decision objectives](../science/model.md), §4.

### M16 A common measurement as a second resource constraint

**Central question.** What extra structure becomes available when the hidden label is never revealed?

**Understanding target.** Express the decision probability as the pairing of one effect with the average alternative-minus-null output. Center the state and effect around the identity without changing this signal. Understand why the same effect can have a bounded backward exposure across all labels, whereas separately chosen effects need not share that budget.

**Dependencies and story role.** [M06](#m06-operator-geometry-and-channel-adjoints), [M08](#m08-one-final-decision-and-two-distance-questions), [M15](#m15-from-quadratic-energy-to-individual-distances). Introduces the additional ingredient of the common-decision converse.

**Conceptual connection.** The output restriction enters through a mathematical dual object: the final measurement propagated backward. Its role is more specific than a blanket statement that a processor can store only one bit.

**Source pointers.** [Centering and a common effect](../science/decision_bound.md), §§4–5; [two exposure budgets](WATROUS_BRIDGE.md#the-common-decision-feedback-bound).

### M17 Opening a mathematical signal port

**Central question.** How can channel feedback be represented without granting a new physical interface?

**Understanding target.** Replace the hidden-sector return temporarily by arbitrary operator inputs $v_t$ in $\mathrm{ran}(Q_a)$ and collect outgoing sector components $u_t$ in the same range. Derive the one-step direct-sum norm inequality and its telescoping block contraction. Identify $A$, $B_a$, $F_a$, and $G_a$ as linear response maps, not accessible environment registers or extra oracle calls.

**Dependencies and story role.** [M06](#m06-operator-geometry-and-channel-adjoints), [M11](#m11-a-physical-channel-with-one-hidden-pauli-mode), [M12](#m12-why-protected-memory-defeats-naive-contraction), [M16](#m16-a-common-measurement-as-a-second-resource-constraint). Builds a local-to-global linear system for one hidden sector.

**Conceptual connection.** An auxiliary mathematical system may permit unphysical operator inputs while still proving an inequality for the physical feedback obtained when the ports are closed.

**Source pointers.** [Open-port construction](../science/decision_bound.md), (D3)–(D6); [feedback bridge](WATROUS_BRIDGE.md#the-common-decision-feedback-bound).

### M18 Finite feedback and the geometric query factor

**Central question.** Why does the decision bound remain meaningful at exact conservation?

**Understanding target.** Explain strict time ordering of the feedback matrix and the resulting nilpotence $G_a^T=0$, where the superscript is an integer power. Close the port with $v=\lambda u$ and express the response using a finite geometric series. Interpret $h_T(\lambda)$, including $h_0=0$ and $h_T(1)=T$, without invoking an infinite-time inverse.

**Dependencies and story role.** [M17](#m17-opening-a-mathematical-signal-port). Converts the open system into the exact finite-query alternative map.

**Conceptual connection.** For $\lambda\lt1$ the geometric factor is bounded uniformly in time; at $\lambda=1$ it grows with $T$. This is the mathematical origin of the different endpoint behavior.

**Source pointers.** [Finite resolvent](../science/decision_bound.md), (D7)–(D8) and (D1)–(D2); [feedback bridge](WATROUS_BRIDGE.md#the-common-decision-feedback-bound).

### M19 The forward exposure budget

**Central question.** How much of the initial state can encounter all hidden sectors combined?

**Understanding target.** Interpret $F_ax_0$ as the history of one sector along the common null evolution. Sum its squared norms over labels and times, retaining the optional final-null remainder. Explain why protected information can survive while the total exposure to queried sectors is finite.

**Dependencies and story role.** [M14](#m14-one-null-trajectory-pays-for-every-direction), [M17](#m17-opening-a-mathematical-signal-port), [M18](#m18-finite-feedback-and-the-geometric-query-factor). Provides the state-side half of the common-decision converse.

**Conceptual connection.** The budget measures total sector exposure, not pointwise decay of the entire state. This is how the proof accommodates arbitrarily large protected memory.

**Source pointers.** [Forward budget](../science/decision_bound.md), (D9); [sector geometry](WATROUS_BRIDGE.md#pauli-sectors-and-protected-memory).

### M20 The backward exposure budget

**Central question.** How does one final effect acquire a matching finite budget?

**Understanding target.** Propagate the effect through adjoint null controls and identify the response at time $t$ to a sector injection. Include the last port explicitly. Use adjoint unital contractivity and orthogonality to telescope the sum over hidden sectors, obtaining a bound common to the same measurement.

**Dependencies and story role.** [M06](#m06-operator-geometry-and-channel-adjoints), [M16](#m16-a-common-measurement-as-a-second-resource-constraint), [M17](#m17-opening-a-mathematical-signal-port), [M19](#m19-the-forward-exposure-budget). Supplies the effect-side half and makes the common-decision restriction quantitative.

**Conceptual connection.** Forward and backward arguments use different trajectories but the same operator geometry. The adjoint preserves the required channel assumptions because the controls are both unital and trace preserving.

**Source pointers.** [Backward budget](../science/decision_bound.md), (D10)–(D12); [Watrous Theorems 2.26 and 4.27](WATROUS_BRIDGE.md#targeted-reading-from-watrous).

### M21 The finite-query common-decision theorem

**Central question.** How do the two exposure budgets yield a law for one readable decision?

**Understanding target.** Combine the finite resolvent with Cauchy–Schwarz across labels and the centered-effect variance bound. Recover the factor $\sqrt{\mathcal P-1}/(2M)$, both the finite-$T$ and uniform-$T$ inequalities, and the distinction from the individual-distance bound. Read the necessary clean-qubit condition as a converse rather than an optimal general-purity tradeoff.

**Dependencies and story role.** [M07](#m07-collision-purity-and-mixed-workspace), [M08](#m08-one-final-decision-and-two-distance-questions), [M18](#m18-finite-feedback-and-the-geometric-query-factor), [M19](#m19-the-forward-exposure-budget), [M20](#m20-the-backward-exposure-budget). Synthesizes the second converse before turning to attainability.

**Conceptual connection.** The factor $1/M$ comes from jointly budgeting state access and one final effect across hidden directions. The finite-$T$ endpoint gives a necessary query count, not a matching algorithm. The two converse bounds are numerically tighter in different parameter regimes.

**Source pointers.** [Decision theorem and consequences](../science/decision_bound.md), (D1)–(D2), (D14)–(D17); [feedback bridge](WATROUS_BRIDGE.md#the-common-decision-feedback-bound).

### M22 A trial Pauli becomes pointer dephasing

**Central question.** How can one ordinary call interrogate a candidate direction without a fresh probe?

**Understanding target.** Follow the controlled-known-Pauli sandwich on a maximally mixed query register and an arbitrary pointer. Track its off-diagonal blocks to obtain dephasing multiplier $\lambda$ for the matching candidate and zero for other nonidentity candidates. Explain why the query system returns to its mixed state, without a reset operation.

**Dependencies and story role.** [M03](#m03-channels-and-ordinary-oracle-access), [M05](#m05-pauli-coordinates-for-operators), [M09](#m09-a-pointer-under-rotation-and-dephasing), [M11](#m11-a-physical-channel-with-one-hidden-pauli-mode), [M21](#m21-the-finite-query-common-decision-theorem). Introduces the constructive primitive under exactly the converse's resource model.

**Conceptual connection.** Known controlled gates can surround an unconditional unknown-channel call. Reusing the returned mixed query state supplies no new purity, and the same reasoning extends to pointer correlations with other protected registers.

**Source pointers.** [Exact gadget](../science/protocols.md), (A3)–(A4); [one-query worked example](WATROUS_BRIDGE.md#a-complete-one-query-example).

### M23 A common one-query signal at small strength

**Central question.** How can a single trial procedure work uniformly over unknown labels?

**Understanding target.** Use a maximally mixed label register covering all Pauli strings, including identity, to control the gadget. Derive the two pointer $X$ expectations and the probability gap $\lambda/[2(M+1)]$. Account for the one pure pointer and $3n$ mixed qubits, and distinguish this small bias from a high-success decision.

**Dependencies and story role.** [M07](#m07-collision-purity-and-mixed-workspace), [M08](#m08-one-final-decision-and-two-distance-questions), [M22](#m22-a-trial-pauli-becomes-pointer-dephasing). Establishes the small-strength branch without a hidden preparation resource.

**Conceptual connection.** Uniformity can come from a mixed control register rather than a pure random-seed register. Ignoring the label leaves the same pointer statistics under every hidden alternative.

**Source pointers.** [One-query construction](../science/protocols.md), (A5)–(A6); [complete one-qubit example](WATROUS_BRIDGE.md#a-complete-one-query-example).

### M24 Weak rotations and block-boundary dephasing

**Central question.** How can a serial scan accumulate a position-independent signal?

**Understanding target.** Build each candidate block from small pointer rotations and the exact dephasing gadget. Derive the active and inactive block multipliers. Explain how complete $Z$ dephasing at every block boundary removes residual transverse coherence while preserving the population signal, making the final output independent of the active label's position.

**Dependencies and story role.** [M09](#m09-a-pointer-under-rotation-and-dephasing), [M22](#m22-a-trial-pauli-becomes-pointer-dephasing), [M23](#m23-a-common-one-query-signal-at-small-strength). Lifts the local gadget to a common serial decision for stronger signals.

**Conceptual connection.** The order of hidden labels can matter without boundary dephasing. The canonical construction deliberately removes that dependence without restoring the pointer to a pure state.

**Source pointers.** [Weak scan dynamics](../science/protocols.md), (A7)–(A10); [pointer dynamics and boundaries](WATROUS_BRIDGE.md#pointer-dynamics-and-boundary-dephasing).

### M25 A finite construction across the crossover

**Central question.** Why does the weak scan need neither an infinite-time limit nor an uncontrolled expansion?

**Understanding target.** Understand the deliberate clipping of the active multiplier, the finite choice of block length and rotation angle, and the resulting root estimates. Relate the active-versus-inactive population difference to the finite lower bound and the scale $\min\{1,\lambda/[M(1-\lambda)]\}$. Include $\lambda=1$ through clipping while keeping the construction finite.

**Dependencies and story role.** [M18](#m18-finite-feedback-and-the-geometric-query-factor), [M21](#m21-the-finite-query-common-decision-theorem), [M24](#m24-weak-rotations-and-block-boundary-dephasing). Provides the quantitative attainability argument and its explicit query budget.

**Conceptual connection.** Clipping prevents a singular parameter choice at exact conservation. The spectral calculation controls the remainder terms that a heuristic small-angle limit would leave unresolved.

**Source pointers.** [Finite weak-scan proof](../science/protocols.md), (A7), (A11)–(A19), (A2); [finite crossover bridge](WATROUS_BRIDGE.md#finite-bias-and-prescribed-error).

### M26 Prescribed error near a conserved mode

**Central question.** How does one obtain a chosen error probability rather than merely a nonzero bias?

**Understanding target.** Analyze the separate $\pi$-rotation scan with no clipping and mandatory block-boundary dephasing. At exact conservation identify the active pointer flip; away from it charge the $L$ altered calls using a channel-distance hybrid argument. Choose finite $L$ for a prescribed error and interpret perfect discrimination at $\lambda=1$ only as an unlimited-time supremum.

**Dependencies and story role.** [M03](#m03-channels-and-ordinary-oracle-access), [M08](#m08-one-final-decision-and-two-distance-questions), [M22](#m22-a-trial-pauli-becomes-pointer-dephasing), [M24](#m24-weak-rotations-and-block-boundary-dephasing), [M25](#m25-a-finite-construction-across-the-crossover). Separates a high-accuracy guarantee from the universal constant in the bias law.

**Conceptual connection.** A lower bound on a small probability gap does not establish success $2/3$. The robust scan supplies that stronger kind of guarantee only in its stated near-conserved regime.

**Source pointers.** [Specified-error construction](../science/protocols.md), (A20)–(A22); [Watrous Proposition 3.48](WATROUS_BRIDGE.md#targeted-reading-from-watrous); [finite bias and prescribed error](WATROUS_BRIDGE.md#finite-bias-and-prescribed-error).

### M27 Implementation resources and numerical scope

**Central question.** What must be counted when the finite protocols are realized?

**Understanding target.** Count ordinary calls, known controlled Pauli gates, pointer rotations, mixed label registers, and optional mixed coins for unital dephasing. Translate per-gate error into output error without claiming a hardware runtime. Distinguish the analytical all-dimension result from the restricted floating-point scan-output domain and finite diagnostic tolerances.

**Dependencies and story role.** [M04](#m04-unital-processing-and-preparation), [M07](#m07-collision-purity-and-mixed-workspace), [M23](#m23-a-common-one-query-signal-at-small-strength), [M24](#m24-weak-rotations-and-block-boundary-dephasing), [M25](#m25-a-finite-construction-across-the-crossover), [M26](#m26-prescribed-error-near-a-conserved-mode). Integrates the constructions with the resource and accuracy conventions of the model.

**Conceptual connection.** Mixed-coin dilation can replace admitted dephasing maps with known unitaries while retaining $\mathcal P=2$; it increases mixed width. Numerical domain guards protect an implementation, not the domain of the theorem.

**Source pointers.** [Implementation accounting](../science/protocols.md), §6; [verification scope](../verification/README.md); [resource and numerical boundaries](WATROUS_BRIDGE.md#resources-and-numerical-boundaries).

### M28 The matched one-clean-qubit law

**Central question.** What exactly is optimal once all finite query budgets are allowed?

**Understanding target.** Join the common-decision converse with the two constructive branches to obtain the upper and lower constants for $\Delta_1(n,\lambda)$. Interpret fixed strength, the crossover near $1-\lambda$ of order $1/M$, and both endpoints. Keep attainable bias, prescribed worst-case error, query complexity, and the dependence on several clean qubits separate.

**Dependencies and story role.** [M21](#m21-the-finite-query-common-decision-theorem), [M23](#m23-a-common-one-query-signal-at-small-strength), [M25](#m25-a-finite-construction-across-the-crossover), [M26](#m26-prescribed-error-near-a-conserved-mode), [M27](#m27-implementation-resources-and-numerical-scope). Assembles the principal theorem and its parameter-regime interpretation.

**Conceptual connection.** Time and mixed width cannot replace missing initial purity away from conservation. Near conservation they support a finite detection mechanism, but this does not establish an efficient general learning algorithm.

**Source pointers.** [Matched law](../science/protocols.md), (A1)–(A2); [interpretation](../science/interpretation.md), §§1–2 and 5–6; [result synthesis](WATROUS_BRIDGE.md#the-result-and-its-limits).

### M29 Attribution and the strength of the evidence

**Central question.** Which ingredients are imported, and what supports the contribution beyond them?

**Understanding target.** Locate the existing Pauli task, serial tests, weak driving, Zeno discrimination, and noisy-oracle purity-progress precedent. Identify the added role of finite forward and backward null exposure budgets under charged initialization. Separate written proofs, finite code diagnostics, and open questions about query optimality or general purity.

**Dependencies and story role.** [M15](#m15-from-quadratic-energy-to-individual-distances), [M21](#m21-the-finite-query-common-decision-theorem), [M25](#m25-a-finite-construction-across-the-crossover), [M27](#m27-implementation-resources-and-numerical-scope), [M28](#m28-the-matched-one-clean-qubit-law). Places the assembled result in its scientific context and identifies the limits of the evidence.

**Conceptual connection.** A new resource conclusion can use established mathematical and physical mechanisms. Accurate attribution clarifies which part of the claim requires the present argument.

**Source pointers.** [Related work](../references/RELATED_WORK.md); [verification account](../verification/README.md); [scientific scope](../science/interpretation.md), §§4–6.

### M30 The complete scientific story

**Central question.** How do the model, both converses, and the finite algorithms form one result?

**Understanding target.** Explain the path from one initialized processor and an unknown Pauli direction to finite null exposure, a common-measurement bound, and a matching one-clean-qubit bias law. Reconcile surviving protected memory with bounded readable signal, and relate the specified-error scan to the same conservation scale. State the operational assumptions and the principal unresolved extensions together.

**Dependencies and story role.** [M10](#m10-the-complete-operational-question), [M15](#m15-from-quadratic-energy-to-individual-distances), [M21](#m21-the-finite-query-common-decision-theorem), [M26](#m26-prescribed-error-near-a-conserved-mode), [M27](#m27-implementation-resources-and-numerical-scope), [M28](#m28-the-matched-one-clean-qubit-law), [M29](#m29-attribution-and-the-strength-of-the-evidence). Synthesizes the narrative phase and the complete project.

**Conceptual connection.** The result compares resources within a precise interface: a decision at fixed error can remain unattainable despite unlimited query time, while a sufficiently persistent hidden mode becomes readable without new initialization.

**Source pointers.** [Scientific reading route](../science/README.md); [model](../science/model.md); [interpretation](../science/interpretation.md); [bridge synthesis](WATROUS_BRIDGE.md#the-result-and-its-limits).
