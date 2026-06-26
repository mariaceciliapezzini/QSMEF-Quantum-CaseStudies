# SMEF #

Repositorio que contiene las implementaciones experimentales utilizadas para evaluar SMEF (*Software Engineering Module Evaluation Framework*).

Las implementaciones no tienen como objetivo reproducir de manera completa los algoritmos estudiados ni su ejecución sobre hardware cuántico. Su propósito es proporcionar modelos funcionales reproducibles que permitan aplicar SMEF y analizar la contribución de componentes internos mediante observables hermitianos y valores de Shapley.

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

