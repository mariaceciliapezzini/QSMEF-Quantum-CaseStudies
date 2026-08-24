# QSMEF

QSMEF (*Quantum Software Engineering Module Evaluation Framework*) is a
methodological framework for the functional analysis of quantum software
implementations.

This repository contains the experimental material associated with the
evaluation and applicability analysis of QSMEF. It includes two quantum
implementations with different methodological roles:

- the Shenvi–Kempe–Whaley (SKW) quantum search on the hypercube, used as
  a QSMEF application case;
- the Quantum Phase Estimation (QPE) subroutine of Shor's algorithm,
  retained as an applicability analysis that identifies a methodological
  boundary of the framework.

## SKW Application Case

The SKW implementation models three functional components:

- Oracle
- Grover coin
- Flip-flop shift operator

QSMEF constructs partial configurations by neutralizing absent components
while preserving the operational order of the components that remain.

The selected decomposition and Hermitian observable support functional
comparison across coalitions. The resulting characteristic function and
Shapley values therefore provide the functional-attribution analysis
reported for this case.

## QPE Applicability Analysis

The QPE experiment initially explored the following decomposition:

- **B0:** Initial state preparation.
- **B1:** Superposition generation using Hadamard gates.
- **B2,k:** Controlled applications of the operator \(U^{2^k}\).

The initial construction also used the inverse Quantum Fourier Transform
(QFT) and measurement as part of the readout context.

Subsequent methodological analysis showed that this decomposition does
not preserve functional comparability across all coalitions. Neutralizing
some QPE stages changes the computational context and the functional role
of the remaining operations.

For this reason, the QPE experiment does not constitute a QSMEF
validation case. The repository retains its implementation and numerical
Shapley results for reproducibility and to document the applicability
analysis. These values describe the exploratory cooperative game and
should not be interpreted as validated QSMEF functional contributions.

The file `qpe_shor/QPE_Supplementary.pdf` provides the complete
applicability analysis.

## Applicability Considerations

The QPE analysis highlights that a QSMEF evaluation requires more than
a structural circuit decomposition and a Hermitian observable.

The analysis must ensure that:

- all evaluated configurations remain structurally compatible;
- component neutralization preserves functional comparability across
  coalitions;
- the selected observable retains the same functional meaning across
  those coalitions.

These conditions determine whether QSMEF can interpret the resulting
Shapley values as functional contributions.

## Reproducibility

The repository preserves the implementations and numerical experiments
associated with both analyses.

The QPE code remains available to reproduce the exploratory cooperative
game and the numerical results documented in the supplementary material.

## Requirements

The implementations were developed in Python 3.10 or later.

Install the required dependencies using:

```bash
pip install -r requirements.txt
