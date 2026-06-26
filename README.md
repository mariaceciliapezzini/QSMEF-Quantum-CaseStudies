# SMEF

SMEF (*Software Engineering Module Evaluation Framework*) es un marco metodológico para el análisis funcional de implementaciones cuánticas.

Este repositorio contiene las implementaciones experimentales utilizadas para evaluar SMEF mediante estudios de caso basados en SKW y QPE/Shor.

Las implementaciones fueron desarrolladas con fines de evaluación metodológica. Cada caso de estudio modela los componentes funcionales necesarios para aplicar SMEF y analizar su contribución al comportamiento global de la implementación mediante observables hermitianos y valores de Shapley.


## Estudios de caso

### SKW

Modelo funcional basado en el algoritmo de búsqueda cuántica sobre hipercubos de Shenvi, Kempe y Whaley.

La implementación representa explícitamente los operadores funcionales utilizados por SMEF:

* Oráculo
* Moneda de Grover
* Desplazamiento flip-flop

### QPE/Shor

Modelo funcional basado en la etapa de Estimación de Fase Cuántica (QPE)
utilizada en el algoritmo de Shor.

Los componentes funcionales considerados por SMEF son:

- B0: preparación inicial.
- B1: generación de superposición mediante compuertas Hadamard.
- B2,k: aplicaciones controladas del operador U^(2^k).

La QFT inversa y la medición se utilizan como mecanismo de lectura
de resultados y no se incluyen dentro de los componentes atribuibles
analizados mediante valores de Shapley.

## Objetivo

El objetivo de estas implementaciones es servir como casos de estudio para evaluar SMEF, permitiendo:

* construir configuraciones parciales;
* calcular funciones características;
* obtener valores de Shapley;
* analizar el impacto funcional de anomalías introducidas en los componentes.

## Publicación asociada

SMEF: Un marco metodológico para el análisis funcional de implementaciones cuánticas.

