# QSMEF

QSMEF (*Quantum Software Engineering Module Evaluation Framework*) is a
methodological framework for analyzing the functional contribution of
components in quantum software implementations.

This repository contains the experimental material associated with the
evaluation and applicability analysis of QSMEF. It includes two quantum
implementations that serve different methodological purposes:

- the Shenvi–Kempe–Whaley (SKW) quantum search on the hypercube, used as
  a QSMEF application case;
- the Quantum Phase Estimation (QPE) subroutine of Shor's algorithm,
  retained as an applicability analysis that identifies a methodological
  boundary of the framework.

## SKW Application Case

The SKW implementation defines three functional components:

- Oracle
- Grover coin
- Flip-flop shift operator

QSMEF constructs partial configurations by neutralizing absent components
while preserving the operational order of the components that remain.

In this case, the selected functional decomposition and Hermitian observable
preserve functional comparability across coalitions. QSMEF can therefore use
the resulting characteristic function and Shapley values to analyze the
functional contribution of the selected components.

## QPE Applicability Analysis

The QPE experiment initially explored the following decomposition:

- **B0:** Initial state preparation.
- **B1:** Superposition generation using Hadamard gates.
- **B2,k:** Controlled applications of the operator \(U^{2^k}\).

The experiment evaluated the cooperative game defined by these components.
The inverse Quantum Fourier Transform (QFT†) remained outside the set of
attributable components and was applied as a fixed readout operation to every
coalition. The experiment did not perform an explicit measurement operation;
instead, it obtained the relevant probabilities directly from the resulting
statevector.

Further methodological analysis showed that this decomposition does not
preserve functional comparability across all coalitions. In QPE, the
functional role of each stage depends on the computational context established
by the other stages. Neutralizing some components therefore changes the
conditions under which the remaining operations perform their intended
function.

For this reason, the QPE experiment does not constitute a valid QSMEF
application case. The repository retains the implementation and its numerical
Shapley results for reproducibility and to document the applicability analysis.
These values characterize the exploratory cooperative game defined for the
experiment, but they should not be interpreted as validated QSMEF functional
contributions.

The file `qpe_shor/QPE_Supplementary.pdf` provides the complete applicability
analysis.

## Applicability Considerations

The QPE analysis shows that a QSMEF evaluation requires more than identifying
functional blocks and defining a Hermitian observable.

The analysis must ensure that:

- all evaluated configurations remain structurally compatible;
- component neutralization preserves functional comparability across
  coalitions;
- the selected observable retains the same functional meaning across
  those coalitions.

These conditions determine whether QSMEF can interpret the resulting Shapley
values as functional contributions.

## Reproducibility

The repository preserves the implementations and numerical experiments
associated with both analyses.

The QPE code remains available to reproduce the exploratory cooperative game
and the numerical results documented in the supplementary material.

## Requirements

The implementations require Python 3.10 or later.

Install the required dependencies using:

```bash
pip install -r requirements.txt
