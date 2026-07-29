# QSMEF Case Study: SKW Quantum Search Algorithm

This repository contains the implementation of the Shenvi–Kempe–Whaley (SKW) quantum search algorithm used as a case study for the Quantum Software Engineering Module Evaluation Framework (QSMEF).

The program implements a simulation of the SKW quantum search algorithm on an *n*-dimensional hypercube using a state-vector representation.

Unlike circuit-based implementations, the simulation does not rely on quantum gates or physical quantum circuits. Instead, it directly applies the functional operators of the algorithm to the coin–position Hilbert space.

The functional operators are:

- **O:** Oracle
- **G:** Grover coin
- **S:** Flip-flop shift operator

Each quantum state is represented as a vector of complex amplitudes, and the system evolves through the successive application of the SKW functional operators.

## QSMEF Evaluation

QSMEF (*Quantum Software Engineering Module Evaluation Framework*) is applied to the implementation by considering the following functional components:

\[
B=\{O,G,S\}
\]

For each system state, QSMEF constructs partial configurations that preserve the original execution order. Missing components are implicitly replaced by identity operators.

From these configurations, QSMEF computes:

1. the Hermitian observable \(H_{ener}\);
2. the functional metric \(M_H\);
3. the characteristic function \(v(C)\);
4. the Shapley value of each functional component.

## Objective

The objective of this implementation is to quantify the functional contribution of the Oracle, the Grover coin, and the flip-flop shift operator to the overall behavior of the SKW algorithm, as well as to analyze the effect of anomalies introduced into the implementation.
