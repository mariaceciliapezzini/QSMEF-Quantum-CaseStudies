# SKW

Implementación de SMEF aplicada al algoritmo SKW.
Este programa implementa una simulación del algoritmo de
 búsqueda cuántica de Shenvi-Kempe-Whaley (SKW) sobre un
 hipercubo n-dimensional utilizando una representación a
 nivel de vector de estado.

 La implementación no se basa en circuitos cuánticos ni en
 compuertas físicas, sino en la aplicación directa de los
 operadores funcionales del algoritmo sobre el espacio de
 Hilbert moneda–posición:

     O : Oráculo
     G : Moneda de Grover
     S : Desplazamiento flip-flop

 Cada estado cuántico se representa mediante un vector de
 amplitudes complejas y la evolución del sistema se obtiene
 aplicando sucesivamente los operadores funcionales SKW.

 Sobre esta simulación se aplica SMEF-E
 (Software Engineering Module Evaluation Framework), considerando como componentes funcionales:

     B = {O, G, S}

 Para cada estado del sistema se construyen configuraciones
 parciales que preservan el orden original de ejecución.
 Los componentes ausentes se reemplazan implícitamente por
 operadores identidad.

 A partir de dichas configuraciones se calcula:

   1. Un observable funcional H_ener.
   2. La métrica funcional M_H.
   3. La función característica v(C).
   4. Los valores de Shapley de cada componente.

 El objetivo es cuantificar la contribución funcional del
 oráculo, la moneda de Grover y el desplazamiento dentro de
 la dinámica del algoritmo SKW, así como analizar el efecto
 de anomalías introducidas en la implementación.
