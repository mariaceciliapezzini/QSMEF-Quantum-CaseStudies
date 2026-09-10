# QAOA–MaxCut Application Case

This directory contains the supplementary material for the application of QSMEF to the Quantum Approximate Optimization Algorithm (QAOA) for MaxCut.

## Problem Instance

The experiment considers MaxCut on a six-vertex cycle and a QAOA circuit with $p=2$. The analysis uses a fixed parameterization based on the formulation reported by Wang et al.

The complete circuit reproduces the reference QAOA behavior before QSMEF performs the functional-attribution analysis.

## Functional Decomposition

QSMEF decomposes the parameterized circuit into four functional blocks:

* $C_1$: first cost block;
* $M_1$: first mixer block;
* $C_2$: second cost block;
* $M_2$: second mixer block.

For every coalition, QSMEF preserves the original circuit order and replaces each absent functional block with the identity operator at its original position.

The six-vertex cycle, initial state, parameter values, and selected Hermitian observable remain fixed across all 16 coalitions.

## Functional Attribution

QSMEF defines the characteristic function from the change in the expected value of the selected Hermitian observable relative to the empty-coalition baseline.

The framework evaluates all $2^4=16$ coalitions and uses Shapley values to attribute the total change among the four functional blocks.

The resulting contributions represent average marginal effects across coalition contexts rather than isolated effects of individual blocks. They depend on the problem instance, parameter values, functional decomposition, selected observable, and baseline. Therefore, they should not be interpreted as absolute measures of component importance.

## Supplementary Document

The file [`MaxCut_Supplementary.pdf`](MaxCut_Supplementary.pdf) provides:

* the complete QAOA–MaxCut problem definition;
* the selected Hermitian observable and functional metric;
* the functional decomposition used by QSMEF;
* the reproduction of the reference QAOA behavior;
* the characteristic function and Shapley values;
* the results for all 16 coalitions;
* the numerical verification procedures;
* the discussion, limitations, and conclusions.

## Scope

This experiment provides an additional QSMEF application case in a computational structure distinct from the SKW coined quantum-walk search analyzed in the companion paper.

The results apply to the selected six-vertex cycle, QAOA parameterization, functional decomposition, observable, and baseline. The experiment does not establish a general attribution pattern for other QAOA configurations.

