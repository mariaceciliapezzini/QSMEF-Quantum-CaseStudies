# SMEF

SMEF (*Software Engineering Module Evaluation Framework*) is a methodological framework for the functional analysis of quantum software implementations.

This repository contains the experimental implementations used to evaluate SMEF through case studies based on the Shenvi–Kempe–Whaley (SKW) quantum search algorithm and the Quantum Phase Estimation (QPE) subroutine of Shor's algorithm.

The implementations were developed for methodological evaluation purposes. Each case study explicitly models the functional components required by SMEF to analyze their contribution to the overall behavior of the implementation using Hermitian observables and Shapley values.

## Case Studies

### SKW

Functional model based on the Shenvi–Kempe–Whaley (SKW) quantum search algorithm on the hypercube.

The implementation explicitly represents the functional operators considered by SMEF:

- Oracle
- Grover coin
- Flip-flop shift operator

### QPE

Functional model based on the Quantum Phase Estimation (QPE) subroutine used in Shor's algorithm.

The functional components considered by SMEF are:

- **B0:** Initial state preparation.
- **B1:** Superposition generation using Hadamard gates.
- **B2,k:** Controlled applications of the operator \(U^{2^k}\).

The inverse Quantum Fourier Transform (QFT) and the measurement stage are used exclusively as the readout mechanism and are therefore not included among the functional components evaluated through Shapley values.

## Objective

The objective of these implementations is to provide reproducible case studies for evaluating SMEF by enabling:

- construction of partial configurations;
- computation of characteristic functions;
- calculation of Shapley values;
- analysis of the functional impact of anomalies introduced into individual components.

## Requirements

The implementations were developed in Python 3.10 or later.

Install the required dependencies using:

```bash
pip install -r requirements.txt
```
The required packages are:

- qiskit
- qiskit-aer
- numpy
- matplotlib
- pylatexenc

## Associated Publication

**SMEF: A Methodological Framework for the Functional Analysis of Quantum Software Implementations.**
