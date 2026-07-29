# QSMEF Case Study: Quantum Phase Estimation (QPE) in Shor's Algorithm

This repository contains the implementation of the Quantum Phase Estimation (QPE) case study used in Shor's algorithm for evaluating the Quantum Software Engineering Module Evaluation Framework (QSMEF).

## Objective

The objective of this implementation is to analyze the functional contribution of the components of the quantum phase estimation stage of Shor's algorithm using cooperative game theory and Shapley values.

## Description

The implementation constructs the quantum phase estimation circuit used to estimate the period \(r\) of the function

\[
f(x)=a^x \bmod N.
\]

SMEF decomposes the implementation into the following functional components:

- **B0:** Work-register initialization.
- **B1:** Uniform superposition generation using Hadamard gates.
- **B2,k:** Controlled applications of the operator \(U^{2^k}\).

The inverse Quantum Fourier Transform (QFT†) followed by measurement constitutes the readout stage. This stage is used exclusively to obtain the measurement outcomes and is therefore not included among the functional components evaluated through Shapley values.

## QSMEF Evaluation

For each coalition of functional components:

- the original execution order is preserved;
- absent components are implicitly replaced by the identity operator;
- a functional metric based on a Hermitian periodicity observable is computed;
- the characteristic function \(v(C)\) is constructed;
- the Shapley value of each functional component is calculated.

## Anomaly Detection

The implementation supports the introduction of controlled perturbations into the phase blocks. These perturbations enable the analysis of how anomalies modify the functional contributions of the individual components identified by QSMEF.
