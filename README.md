# QSMEF

QSMEF (*Quantum Software Engineering Module Evaluation Framework*) is a methodological framework for analyzing the functional contributions of components in quantum software implementations.

This repository contains the experimental material associated with the evaluation and applicability analysis of QSMEF. It includes three quantum studies that serve different methodological purposes:

* the Shenvi–Kempe–Whaley (SKW) coined quantum-walk search algorithm on the hypercube, used as the main QSMEF application case;
* the Quantum Approximate Optimization Algorithm (QAOA) applied to MaxCut, used as an additional QSMEF application case;
* the Quantum Phase Estimation (QPE) subroutine of Shor's algorithm, retained as an applicability analysis that identifies a methodological boundary of the framework.

## SKW Application Case

The SKW implementation defines three functional components:

* Oracle
* Grover coin operator
* Flip-flop shift operator

QSMEF constructs partial configurations by replacing absent components with the identity operator while preserving their original operational positions.

For this case, the selected functional decomposition and Hermitian observable preserve functional comparability across all coalitions. QSMEF can therefore use the resulting characteristic function and Shapley values to analyze the functional contributions of the selected components.

The `SKW` directory contains the implementation and experimental material associated with this application case.

## QAOA–MaxCut Application Case

The QAOA–MaxCut experiment considers a six-vertex cycle and a QAOA circuit with $p=2$. The functional decomposition defines four attributable components:

* $C_1$: first cost block;
* $M_1$: first mixer block;
* $C_2$: second cost block;
* $M_2$: second mixer block.

For every coalition, QSMEF preserves the original circuit order and replaces each absent functional block with the identity operator at its original position. The six-vertex cycle, initial state, parameter values, and selected Hermitian observable remain fixed across all 16 coalitions.

The complete circuit reproduces the reference QAOA behavior documented in the supplementary material. QSMEF then uses Shapley values to attribute the total change in the expected value of the selected observable among the four functional blocks.

The resulting contributions represent average marginal effects across coalition contexts rather than isolated effects of individual circuit blocks. They depend on the six-vertex cycle, parameter values, functional decomposition, selected observable, and baseline. Therefore, they should not be interpreted as absolute measures of component importance.

The file `qaoa_maxcut/MaxCut_Supplementary.pdf` provides the complete description, numerical results, and verification procedures for this application case.

## QPE Applicability Analysis

The QPE experiment initially explored the following decomposition:

* **B0:** initial-state preparation;
* **B1:** superposition generation using Hadamard gates;
* **B2,k:** controlled applications of the operator $U^{2^k}$.

The experiment evaluated the cooperative game defined by these components. The inverse Quantum Fourier Transform (QFT$^\dagger$) remained outside the set of attributable components and was applied as a fixed readout operation to every coalition. The experiment did not perform an explicit measurement operation; instead, it obtained the relevant probabilities directly from the resulting statevector.

Further methodological analysis showed that this decomposition does not preserve functional comparability across all coalitions. In QPE, the functional role of each stage depends on the computational context established by the other stages. Replacing some components with the identity operator therefore changes the conditions under which the remaining operations perform their intended functions.

For this reason, the QPE experiment does not constitute a valid QSMEF application case. The repository retains the implementation and its numerical Shapley results for reproducibility and to document the applicability analysis. These values characterize the exploratory cooperative game defined for the experiment, but they should not be interpreted as validated QSMEF functional contributions.

The file `qpe_shor/QPE_Supplementary.pdf` provides the complete applicability analysis.

## Applicability Considerations

The QPE analysis shows that a QSMEF evaluation requires more than identifying functional blocks and defining a Hermitian observable.

The analysis must ensure that:

* all evaluated configurations remain structurally compatible;
* replacing absent components with the identity operator preserves functional comparability across coalitions;
* the selected observable retains the same functional meaning across those coalitions.

These conditions determine whether QSMEF can interpret the resulting Shapley values as functional contributions.

## Repository Structure

```text
.
├── SKW/
├── qaoa_maxcut/
│   └── MaxCut_Supplementary.pdf
├── qpe_shor/
│   └── QPE_Supplementary.pdf
├── README.md
└── requirements.txt
```

## Reproducibility

The repository preserves the implementations and experimental material associated with the QSMEF evaluation and applicability analyses.

The SKW and QAOA–MaxCut application cases document valid functional-attribution analyses under their selected decompositions, observables, and baselines.

The QPE material reproduces the exploratory cooperative game and numerical results considered during the applicability analysis. Its Shapley values remain available for transparency and reproducibility but do not constitute validated QSMEF functional contributions.

## Requirements

The implementations require Python 3.10 or later.

Install the required dependencies using:

```bash
pip install -r requirements.txt
```
