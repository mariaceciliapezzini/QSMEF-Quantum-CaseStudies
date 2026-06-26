# Quantum Phase Estimation (QPE)
El repositorio contiene la implementación del caso de estudio Quantum Phase Estimation (QPE) utilizado en el algoritmo de Shor para la evaluación del marco SMEF (Software Engineering Module Evaluation Framework).

Objetivo
Analizar la contribución funcional de los componentes de la etapa cuántica de Shor mediante teoría de juegos cooperativos y valores de Shapley.

Descripción
La implementación construye el circuito de estimación de fase utilizado para determinar el período r de la función:
f(x)=axmodN

Posteriormente, SMEF descompone la implementación en bloques funcionales:

B0: preparación del registro de trabajo.
B1: generación de superposición uniforme.
B2,k: aplicaciones controladas de U
Readout: transformada cuántica de Fourier inversa (QFT†).

Evaluación mediante SMEF
Para cada coalición de bloques:

Se preserva el orden original de ejecución.
Los bloques ausentes se reemplazan implícitamente por la identidad.
Se calcula una métrica funcional basada en un observable de periodicidad.
Se construye la función característica v(C).
Se obtienen los valores de Shapley de cada bloque.
Detección de anomalías

La implementación permite introducir perturbaciones controladas en los bloques de fase.
Esto permite analizar cómo las anomalías modifican las contribuciones funcionales identificadas por SMEF.
