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

The implementation represents the quantum phase estimation process used
in the order-finding stage of Shor's algorithm.

The exploratory decomposition considered the following attributable
components:

- work-register initialization;
- uniform superposition generation using Hadamard gates;
- controlled applications of the modular multiplication operators
  \(U^{2^k}\).

The inverse Quantum Fourier Transform (QFT†) was kept outside the set of
attributable components and applied as a fixed readout operation to every
coalition. The experiment did not perform an explicit measurement
operation; instead, it obtained the relevant probabilities directly from
the resulting statevector.

These operations define structurally identifiable stages of the
implementation. However, structural identification alone is not
sufficient to define valid QSMEF functional components.

## Applicability Analysis

QSMEF evaluates coalitions by neutralizing absent components while
preserving the operational order of the components that remain.

For a decomposition to support a valid QSMEF analysis, the induced
coalitions must remain functionally comparable with respect to the
property represented by the selected observable.

In the QPE implementation considered here, neutralizing components
involved in state preparation, superposition generation, or controlled
modular evolution changes the functional conditions under which phase
information is generated. The fixed QFT† readout therefore acts on states
produced under different functional contexts across coalitions.

As a consequence, the resulting coalition configurations cannot, in
general, be interpreted as functionally comparable partial realizations
of the same phase-estimation process.

Therefore, the original decomposition used for the QPE experiment does
not satisfy the applicability conditions required by QSMEF.

## Observable Considerations

The use of a Hermitian observable is necessary for defining a QSMEF
functional metric, but Hermiticity alone is not sufficient.

The observable must also:

- act on the Hilbert space shared by the evaluated configurations; and
- preserve the same functional interpretation across all coalitions.

For the QPE decomposition considered here, the neutralization of
functionally interdependent components prevents guaranteeing this common
semantic interpretation across coalitions.

Although the same QFT† readout and the same observable are applied to
every coalition, the states entering the readout arise from different
functional contexts. The resulting expectation values therefore remain
mathematically well defined but do not necessarily represent the same
functional property under comparable computational conditions.

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
QPE implementation, the exploratory numerical results, and the
methodological issues identified during the applicability assessment.

Any QPE coalition results or Shapley values reported in this directory
should be interpreted only as outputs of the exploratory cooperative game
and not as validated QSMEF functional-attribution results.
