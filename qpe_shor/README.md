# QSMEF Applicability Analysis: Quantum Phase Estimation (QPE) in Shor's Algorithm

This directory contains an applicability analysis of the Quantum Software
Engineering Module Evaluation Framework (QSMEF) to the Quantum Phase
Estimation (QPE) stage used in Shor's algorithm.

Unlike the SKW quantum search case study, this analysis is not presented
as a valid QSMEF application. Instead, it documents a methodological
boundary identified when applying coalition-based component
neutralization to the QPE implementation.

## Objective

The objective of this analysis is to examine whether the functional
components of the QPE stage can be evaluated through QSMEF while
preserving the structural and semantic conditions required for meaningful
comparison between coalitions.

The analysis shows that the considered decomposition does not satisfy
these conditions. Consequently, Shapley values obtained from this
decomposition should not be interpreted as valid QSMEF functional
contributions.

## QPE Implementation

The implementation constructs the quantum phase estimation circuit used
in the order-finding stage of Shor's algorithm.

The analyzed implementation contains operations associated with:

- work-register initialization;
- uniform superposition generation using Hadamard gates;
- controlled applications of the modular multiplication operators
  \(U^{2^k}\);
- inverse Quantum Fourier Transform (QFT†);
- measurement of the counting register.

These operations are structurally identifiable in the implementation.
However, structural identification alone is not sufficient to define
valid QSMEF functional components.

## Applicability Analysis

QSMEF evaluates coalitions by neutralizing absent components while
preserving the operational context required to compare the resulting
configurations.

For a decomposition to support a valid QSMEF analysis, the induced
coalitions must remain functionally comparable with respect to the
property represented by the selected observable.

In the QPE implementation considered here, neutralizing operations
involved in state preparation, controlled modular evolution, or phase
readout changes the functional conditions under which the phase
information is generated and interpreted.

As a consequence, the resulting coalition configurations cannot, in
general, be interpreted as partial realizations of the same functional
process with a common semantic meaning.

Therefore, the original decomposition used for the QPE experiment does
not satisfy the applicability conditions required by QSMEF.

## Observable Considerations

The use of a Hermitian observable is necessary for defining a QSMEF
functional metric, but Hermiticity alone is not sufficient.

The observable must also:

- act on the Hilbert space shared by the evaluated configurations; and
- preserve the same functional interpretation across all coalitions.

For the QPE decomposition considered here, the neutralization of
functionally interdependent stages prevents guaranteeing this common
semantic interpretation across coalitions.

## Methodological Conclusion

The QPE/Shor experiment is retained as an applicability analysis rather
than as a validation case for QSMEF.

Its role is to illustrate an important methodological boundary of the
framework: not every structurally decomposable quantum implementation
admits a functionally meaningful coalition-based evaluation.

Accordingly, numerical Shapley values previously obtained from this
decomposition are not used as evidence for the validation of QSMEF.

The reproducible SKW quantum search implementation on the hypercube is
the valid QSMEF application case included in this repository.

## Supplementary Material

The supplementary material associated with this analysis documents the
QPE implementation and the methodological issues identified during the
applicability assessment.

Any previously reported QPE coalition results or Shapley values should
be interpreted only as outputs of the exploratory implementation and not
as valid functional-attribution results of QSMEF.
