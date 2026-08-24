"""
Exploratory QPE/Shor cooperative-game analysis.

This script reproduces the coalition construction and numerical Shapley
values originally explored for the Quantum Phase Estimation (QPE) stage
of Shor's algorithm.

Subsequent methodological analysis showed that the decomposition used
here does not guarantee functional comparability across coalitions or
semantic invariance of the selected observable.

Therefore, the numerical Shapley values produced by this script must be
interpreted as results of an exploratory cooperative-game construction,
not as validated QSMEF functional contributions.

The script is retained for reproducibility and for documenting the
applicability analysis of QSMEF.
"""



from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFTGate
from qiskit.circuit import Gate
from qiskit.quantum_info import Statevector, Operator

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from math import gcd, ceil, log2, factorial
import itertools

def amod15(a: int):
    """
    Implementa U: |y> -> |a*y mod 15> sobre 4 qubits (y en binario).
    """
    if a not in [2, 4, 7, 8, 11, 13]:
        raise ValueError("'a' debe ser coprimo con 15 y estar en {2,4,7,8,11,13}")

    U = QuantumCircuit(4, name=f"{a} mod 15")

    
    if a in [2, 13]:
        U.swap(2, 3)
        U.swap(1, 2)
        U.swap(0, 1)
    if a in [7, 8]:
        U.swap(0, 1)
        U.swap(1, 2)
        U.swap(2, 3)
    if a in [4, 11]:
        U.swap(1, 3)
        U.swap(0, 2)
    if a in [7, 11, 13]:
        for q in range(4):
            U.x(q)

    return U.to_gate()

def controlled_amod15(a: int):
    """
    Versión controlada de U: un qubit de control + 4 de trabajo.
    """
    return amod15(a).control(1)


def inverse_qft(num_qubits: int) -> Gate:
    """Devuelve la puerta QFT inversa sobre num_qubits qubits (compatible con Qiskit 2.1+)."""
    # QFT directa con parámetros por defecto
    qft_gate = QFTGate(num_qubits)
    # Tomamos la inversa (adjunta)
    qft_dagger = qft_gate.inverse()
    qft_dagger.label = "QFT†"
    return qft_dagger


def build_shor_order_finding_circuit(a: int = 2,
                                     N: int = 15,
                                     precision: int = 4,
                                     measure: bool = True):
    """
    Construye el circuito cuántico de estimación de fase usado en Shor
    para hallar el período r de a^x mod N (aquí N=15).

    - Registro de conteo (precision qubits)
    - Registro de trabajo (4 qubits, porque 15 < 2^4)
    """
    if N != 15:
        raise NotImplementedError("Esta versión está hardcodeada para N=15.")

    # Registros
    count = QuantumRegister(precision, "count")   # registro superior (fase)
    work  = QuantumRegister(4, "work")           # registro inferior (a^x mod 15)

    if measure:
        c_reg = ClassicalRegister(precision, "c")
        qc = QuantumCircuit(count, work, c_reg)
    else:
        qc = QuantumCircuit(count, work)

    qc.x(work[0])

  
    qc.h(count)

    
    cU = controlled_amod15(a)   # 1 control + 4 target
    for k in range(precision):
        # Aplicar U^{2^k} controlada por count[k]
        for _ in range(2**k):
            qc.append(cU, [count[k]] + list(work))

   
    qc.append(inverse_qft(precision), count)

   
    if measure:
        qc.measure(count, c_reg)

    return qc



qc_shor = build_shor_order_finding_circuit(a=2, N=15, precision=4, measure=True)
qc_shor.draw(output='mpl')



qc_shor_quantum = build_shor_order_finding_circuit(a=2, N=15, precision=4, measure=False)
qc_shor_quantum.draw(output='mpl')


# Valores admitidos:
#   "es" -> castellano (tesis)
#   "en" -> inglés (paper CACIC)
LANGUAGE = "en"

PLOT_TEXTS = {
    "es": {
        "shapley_value": "Valor de Shapley",
        "initial_preparation": "Preparación inicial",
        "superposition": "Superposición",
        "controlled_phase": "Fase controlada",
        "correct": "Correcta",
        "faulty": "Perturbada",
        "comparison_title": "Comparación exploratoria de valores de Shapley: referencia vs. modificada",
        "shapley_correct_title": "Análisis exploratorio de Shapley para Shor-QPE",
        "shapley_faulty_title": "Análisis exploratorio de Shapley para Shor-QPE modificado",
         "correct": "Referencia",
         "faulty": "Modificada",
         "correct_case": "Configuración de referencia",
         "faulty_case": "Configuración modificada",
        "permutation_position": "Posición en la permutación (0 = primero, n-1 = último)",
        "player": "Componente",
        "average_marginal_by_position": "Contribución marginal promedio por posición",
        "marginal_contribution": "Contribución marginal",
        "zero_contribution": "Contribución cero",
        "marginal_distribution": "Distribución de contribuciones marginales por componente",
        "probability_density": "Densidad de probabilidad",
        "position_evolution": "Evolución de la contribución según la posición",
        "permutation_position_short": "Posición en la permutación",
        "average_marginal": "Contribución marginal promedio",
    },
    "en": {
        "shapley_value": "Shapley value",
        "initial_preparation": "Initial preparation",
        "superposition": "Superposition",
        "controlled_phase": "Controlled phase",
        "correct": "Correct",
        "faulty": "Perturbed",
        "comparison_title": "Exploratory comparison of Shapley values: reference vs. modified configuration",
        "shapley_correct_title": "Exploratory Shapley analysis for Shor-QPE",
        "shapley_faulty_title": "Exploratory Shapley analysis for modified Shor-QPE",
         "correct": "Reference",
        "faulty": "Modified",
        "correct_case": "Reference configuration",
         "faulty_case": "Modified configuration",
        "permutation_position": "Position in the permutation (0 = first, n-1 = last)",
        "player": "Component",
        "average_marginal_by_position": "Average marginal contribution by position",
        "marginal_contribution": "Marginal contribution",
        "zero_contribution": "Zero contribution",
        "marginal_distribution": "Distribution of marginal contributions by component",
        "probability_density": "Probability density",
        "position_evolution": "Evolution of the contribution by position",
        "permutation_position_short": "Position in the permutation",
        "average_marginal": "Average marginal contribution",
    },
}


def plot_text(key: str) -> str:
    """Devuelve el texto del gráfico en el idioma seleccionado."""
    if LANGUAGE not in PLOT_TEXTS:
        raise ValueError("LANGUAGE debe ser 'es' o 'en'.")
    return PLOT_TEXTS[LANGUAGE][key]

def multiplicative_order(a: int, N: int) -> int:
    if gcd(a, N) != 1:
        raise ValueError("a y N deben ser coprimos para que exista orden multiplicativo.")

    x = a % N
    r = 1

    while x != 1:
        x = (x * a) % N
        r += 1

        if r > 200_000:
            raise RuntimeError("Orden demasiado grande/no encontrado.")

    return r

def amodN_gate(a: int, N: int) -> Gate:
    if gcd(a, N) != 1:
        raise ValueError("a y N deben ser coprimos.")

    n = ceil(log2(N))
    dim = 2 ** n
    U = np.zeros((dim, dim), dtype=complex)

    for y in range(dim):
        out = (a * y) % N if y < N else y
        U[out, y] = 1.0

    qc = QuantumCircuit(n, name=f"{a} mod {N}")
    qc.unitary(Operator(U), list(range(n)))

    return qc.to_gate()


def controlled_amodN(a: int, N: int) -> Gate:
    """
    Versión controlada.
    El parámetro annotated=True evita errores internos de Qiskit
    al controlar unitarios definidos por matriz.
    """
    return amodN_gate(a, N).control(1, annotated=True)

def inverse_qft_gate(m: int) -> Gate:
    r"""QFT^\dagger sobre m qubits."""
    qc = QuantumCircuit(m, name="QFT†")

    for j in range(m // 2):
        qc.swap(j, m - j - 1)

    for j in range(m):
        for k in range(j):
            angle = -np.pi / (2 ** (j - k))
            qc.cp(angle, j, k)
        qc.h(j)

    return qc.to_gate()

def default_eps_for_precision(precision: int, bins: float = 1.0) -> float:
    return bins / (2 ** precision)


def success_indices_eps(
    precision: int,
    r: int,
    eps: float,
    exclude_zero: bool = True
):
    M = 2 ** precision
    good = []
    s_start = 1 if exclude_zero else 0

    for m in range(M):
        frac = m / M

        for s in range(s_start, r):
            if abs(frac - (s / r)) < eps:
                good.append(m)
                break

    return good

def success_probability(
    state_after_readout: Statevector,
    precision: int,
    good_m
):
    if not good_m:
        return 0.0

    probs = state_after_readout.probabilities(qargs=list(range(precision)))
    good = [m for m in good_m if 0 <= m < len(probs)]

    return float(np.sum(probs[good]))

def build_shor_blocks(
    a: int,
    N: int,
    precision: int,
    faulty_phase_block=None,
    faulty_mode=None,
    faulty_a=None
):
    # Número de qubits necesarios para el registro de trabajo
    work_qubits = int(np.ceil(np.log2(N)))

    count = QuantumRegister(precision, "count")
    work = QuantumRegister(work_qubits, "work")

    B0 = QuantumCircuit(count, work, name="B0_prep")
    B0.x(work[0])

    B1 = QuantumCircuit(count, work, name="B1_H")
    for q in count:
        B1.h(q)

    phase_blocks = []
    cU_correct = controlled_amodN(a, N)

    for k in range(precision):
        Bk = QuantumCircuit(count, work, name=f"B2_phase_{k}")

        repeats = 2 ** k
        control_qubit = count[k]
        cU_block = cU_correct

        if faulty_phase_block is not None and k == faulty_phase_block:
            if faulty_mode == "missing_repeat":
                repeats = max(0, repeats - 1)

            elif faulty_mode == "wrong_control":
                control_qubit = count[(k + 1) % precision]

            elif faulty_mode == "wrong_unitary":
                if faulty_a is None:
                    raise ValueError("Indicar faulty_a para faulty_mode='wrong_unitary'.")

                if gcd(faulty_a, N) != 1:
                    raise ValueError("faulty_a y N deben ser coprimos.")

                cU_block = controlled_amodN(faulty_a, N)

            elif faulty_mode == "skip_block":
                repeats = 0

        for _ in range(repeats):
            Bk.append(cU_block, [control_qubit] + list(work))

        phase_blocks.append(Bk)

    blocks_all = [B0, B1] + phase_blocks

    labels = ["B0", "B1"] + [
        f"B2,{k}" for k in range(precision)
    ]

    readout = QuantumCircuit(count, work, name="Readout_QFTdg")
    readout.append(inverse_qft_gate(precision), list(count))

    return count, work, blocks_all, labels, readout

def smefe_shor_phase_blocks_shapley(
    a: int,
    N: int,
    precision: int,
    eps=None,
    eps_bins: float = 1.0,
    exclude_zero_peak: bool = True,
    plot: bool = True,
    save: bool = False,
    filename_prefix: str = "shapley_qpe",
    verbose: bool = True,
    faulty_phase_block=None,
    faulty_mode=None,
    faulty_a=None,
    plot_title_prefix: str = "Exploratory Shapley analysis for Shor-QPE"
):
    r = multiplicative_order(a, N)

    if eps is None:
        eps = default_eps_for_precision(
            precision,
            bins=eps_bins
        )

    good_m = success_indices_eps(
        precision=precision,
        r=r,
        eps=eps,
        exclude_zero=exclude_zero_peak
    )

    if verbose:
        print(
            f"N={N}, a={a}, precision={precision}, "
            f"r={r}, eps={eps:.6g}, good_m={good_m}"
        )

    count, work, blocks_all, labels, readout = build_shor_blocks(
        a=a,
        N=N,
        precision=precision,
        faulty_phase_block=faulty_phase_block,
        faulty_mode=faulty_mode,
        faulty_a=faulty_a
    )

    n_players = len(blocks_all)
    n_total = precision + work.size

   if verbose:
    print(
        "\n[NOTE] Exploratory QPE coalition construction. "
        "The resulting Shapley values are not interpreted as "
        "validated QSMEF functional contributions."
    )
    print(f"Jugadores: {labels}")
    print(f"n_players = {n_players}")

        if faulty_phase_block is not None:
            print(
                f"[FAULT] Bloque perturbado: "
                f"B_{{2,{faulty_phase_block}}}"
            )
            print(
                f"[FAULT] Tipo de anomalía: "
                f"{faulty_mode}"
            )

            if faulty_mode == "wrong_unitary":
                print(
                    f"[FAULT] Unidad incorrecta: "
                    f"a_fault = {faulty_a}"
                )

    num_coalitions = 2 ** n_players
    E_values = np.zeros(
        num_coalitions,
        dtype=float
    )

    if verbose:
        print(
            "\n=== Evaluando E(C) para todas las coaliciones ==="
        )

    for mask in range(num_coalitions):
        psi = Statevector.from_label(
            "0" * n_total
        )

        for b in range(n_players):
            if (mask >> b) & 1:
                psi = psi.evolve(
                    blocks_all[b]
                )

        psi_read = psi.evolve(
            readout
        )

        E_values[mask] = success_probability(
            psi_read,
            precision=precision,
            good_m=good_m
        )

    E_empty = E_values[0]
    v_values = E_values - E_empty

    shapley_vals = np.zeros(
        n_players,
        dtype=float
    )

    n_fact = factorial(
        n_players
    )

    if verbose:
        print(
            "\n=== Cálculo de Shapley ==="
        )

    for i in range(n_players):
        phi = 0.0

        for mask in range(num_coalitions):
            if (mask >> i) & 1:
                continue

            s = mask.bit_count()
            mask_with_i = mask | (1 << i)

            v_S = v_values[mask]
            v_Si = v_values[mask_with_i]

            weight = (
                factorial(s)
                * factorial(
                    n_players - s - 1
                )
                / n_fact
            )

            phi += weight * (
                v_Si - v_S
            )

        shapley_vals[i] = phi

        if verbose:
            print(
                f"{labels[i]}: "
                f"Shapley = {phi:.6f}"
            )

    full_mask = (
        1 << n_players
    ) - 1

    V_full = v_values[
        full_mask
    ]

    E_full = E_values[
        full_mask
    ]

    if verbose:
        print(
            f"\nE(∅) = {E_empty:.6f}"
        )
        print(
            f"E(N) = {E_full:.6f}"
        )
        print(
            f"v(N) = E(N) - E(∅) = "
            f"{V_full:.6f}"
        )

    if plot:
        colors = [
            "tab:gray"
            if lab == "B0"
            else "tab:orange"
            if lab == "B1"
            else "tab:blue"
            for lab in labels
        ]

        display_labels = [
            r"$B_0$"
            if lab == "B0"
            else r"$B_1$"
            if lab == "B1"
            else rf"$B_{{2,{lab.split(',')[1]}}}$"
            for lab in labels
        ]

        fig, ax = plt.subplots(
            figsize=(10, 4)
        )

        ax.bar(
            display_labels,
            shapley_vals,
            color=colors
        )

        ax.set_ylabel(
            plot_text("shapley_value")
        )

        suffix = ""

        if faulty_phase_block is not None:
            suffix = (
                f" | {plot_text('fault')}="
                f"$B_{{2,{faulty_phase_block}}}$, "
                f"{plot_text('mode')}="
                f"{faulty_mode}"
            )

            if faulty_mode == "wrong_unitary":
                suffix += (
                    f", $a_{{fault}}="
                    f"{faulty_a}$"
                )

        ax.set_title(
            f"{plot_title_prefix} "
            f"(N={N}, a={a}, "
            f"eps={eps:.3g})"
            f"{suffix}"
        )

        ax.tick_params(
            axis="x",
            rotation=45
        )

        ax.grid(
            axis="y",
            alpha=0.3
        )

        ax.legend(
            handles=[
                Patch(
                    facecolor="tab:gray",
                    label=(
                        rf"$B_0$ "
                        f"{plot_text('initial_preparation')}"
                    )
                ),
                Patch(
                    facecolor="tab:orange",
                    label=(
                        rf"$B_1$ "
                        f"{plot_text('superposition')}"
                    )
                ),
                Patch(
                    facecolor="tab:blue",
                    label=(
                        rf"$B_{{2,j}}$ "
                        f"{plot_text('controlled_phase')}"
                    )
                )
            ],
            loc="best"
        )

        fig.tight_layout()

        if save:
            fig.savefig(
                f"{filename_prefix}.png",
                dpi=600,
                bbox_inches="tight"
            )

            fig.savefig(
                f"{filename_prefix}.pdf",
                bbox_inches="tight"
            )

            if verbose:
                print(
                    "\nFiguras guardadas:"
                )
                print(
                    f"- {filename_prefix}.png "
                    f"(600 dpi)"
                )
                print(
                    f"- {filename_prefix}.pdf"
                )

        plt.show()
        plt.close(fig)

    return (
        labels,
        shapley_vals,
        v_values,
        E_values,
        good_m,
        r,
        eps,
        E_empty,
        E_full
    )

def check_shapley_efficiency(shapley_vals, v_values, tol: float = 1e-10):
    n_players = len(shapley_vals)
    full_mask = (1 << n_players) - 1

    lhs = float(np.sum(shapley_vals))
    rhs = float(v_values[full_mask])

    print("\n[CHECK] Suma Shapley =", lhs)
    print("[CHECK] v(N)         =", rhs)
    print("[CHECK] diferencia   =", lhs - rhs)

    if abs(lhs - rhs) < tol:
        print("[OK] Eficiencia verificada.")
    else:
        print("[WARN] Eficiencia NO se cumple.")


def shapley_via_permutations(v_values, n_players):
    phi_perm = np.zeros(n_players, dtype=float)
    players = list(range(n_players))
    perms = itertools.permutations(players)
    n_fact = factorial(n_players)

    for pi in perms:
        mask_S = 0

        for i in pi:
            v_S = v_values[mask_S]
            mask_Si = mask_S | (1 << i)
            v_Si = v_values[mask_Si]

            phi_perm[i] += (v_Si - v_S) / n_fact
            mask_S = mask_Si

    return phi_perm


def check_shapley_permutation_consistency(
    shapley_vals,
    v_values,
    max_players: int = 9,
    tol: float = 1e-10
):
    n_players = len(shapley_vals)

    if n_players > max_players:
        print(f"\n[CHECK] Permutaciones omitido: n_players={n_players} > {max_players}.")
        return

    phi_perm = shapley_via_permutations(v_values, n_players)

    print("\n[CHECK] Shapley por coaliciones   =", shapley_vals)
    print("[CHECK] Shapley por permutaciones =", phi_perm)
    print("[CHECK] diferencia                =", shapley_vals - phi_perm)

    if np.all(np.abs(shapley_vals - phi_perm) < tol):
        print("[OK] Coinciden coaliciones vs permutaciones.")
    else:
        print("[WARN] Diferencias detectables.")


def check_probability_range(E_values, tol: float = 1e-12):
    e_min = float(np.min(E_values))
    e_max = float(np.max(E_values))

    print("\n[CHECK] min E(C) =", e_min)
    print("[CHECK] max E(C) =", e_max)

    if e_min < -tol or e_max > 1 + tol:
        print("[WARN] Hay valores fuera del rango [0,1].")
    else:
        print("[OK] Todas las probabilidades E(C) están en [0,1].")

def build_H_per_count(precision: int, good_m):
    dim = 2 ** precision
    H = np.zeros((dim, dim), dtype=float)

    for m in good_m:
        if 0 <= m < dim:
            H[m, m] = 1.0

    return H


def build_H_per_full_matrix(precision: int, work_qubits: int, good_m):
    Hc = build_H_per_count(precision, good_m)
    Iw = np.eye(2 ** work_qubits)

    return np.kron(Iw, Hc)


def check_projector_properties(H, tol: float = 1e-12):
    H = np.asarray(H, dtype=complex)

    hermitian_error = np.linalg.norm(H - H.conj().T)
    projector_error = np.linalg.norm(H @ H - H)

    print("\n[CHECK] ||H - H†|| =", hermitian_error)
    print("[CHECK] ||H² - H|| =", projector_error)

    if hermitian_error < tol:
        print("[OK] H es hermitiano.")
    else:
        print("[WARN] H NO es hermitiano.")

    if projector_error < tol:
        print("[OK] H es proyector.")
    else:
        print("[WARN] H NO es proyector.")


def expected_value_full_operator(state: Statevector, H):
    vec = state.data
    return float(np.real(np.vdot(vec, H @ vec)))


def check_probability_vs_expectation(
    a: int,
    N: int,
    precision: int,
    good_m,
    coalition_mask: int,
    faulty_phase_block=None,
    faulty_mode=None,
    faulty_a=None
):
    count, work, blocks_all, labels, readout = build_shor_blocks(
        a=a,
        N=N,
        precision=precision,
        faulty_phase_block=faulty_phase_block,
        faulty_mode=faulty_mode,
        faulty_a=faulty_a
    )

    n_players = len(blocks_all)
    n_total = precision + work.size

    psi = Statevector.from_label("0" * n_total)

    for b in range(n_players):
        if (coalition_mask >> b) & 1:
            psi = psi.evolve(blocks_all[b])

    psi_read = psi.evolve(readout)

    E_prob = success_probability(
        psi_read,
        precision=precision,
        good_m=good_m
    )

    H_per_full = build_H_per_full_matrix(
        precision,
        work.size,
        good_m
    )

    E_exp = expected_value_full_operator(psi_read, H_per_full)

    print(f"\n[CHECK] Coalición mask = {coalition_mask}")
    print("[CHECK] E por suma de probabilidades =", E_prob)
    print("[CHECK] E por valor esperado         =", E_exp)
    print("[CHECK] diferencia                   =", E_prob - E_exp)

    if abs(E_prob - E_exp) < 1e-12:
        print("[OK] Coinciden probabilidad y valor esperado.")
    else:
        print("[WARN] NO coinciden.")

def compare_shapley_correct_vs_faulty(
    labels,
    shapley_ok,
    shapley_faulty,
    save: bool = False,
    filename_prefix: str = "shapley_qpe_comparison"
):
    x = np.arange(len(labels))
    width = 0.38

    display_labels = [
        r"$B_0$" if lab == "B0"
        else r"$B_1$" if lab == "B1"
        else rf"$B_{{2,{lab.split(',')[1]}}}$"
        for lab in labels
    ]

    fig, ax = plt.subplots(figsize=(11, 4))

    ax.bar(
        x - width / 2,
        shapley_ok,
        width=width,
        label=plot_text("correct")
    )

    ax.bar(
        x + width / 2,
        shapley_faulty,
        width=width,
        label=plot_text("faulty")
    )

    ax.set_xticks(x)
    ax.set_xticklabels(display_labels, rotation=45)

    ax.set_ylabel(plot_text("shapley_value"))
    ax.set_title(plot_text("comparison_title"))

    ax.grid(axis="y", alpha=0.3)
    ax.legend()

    fig.tight_layout()

    if save:
        fig.savefig(
            f"{filename_prefix}.png",
            dpi=600,
            bbox_inches="tight"
        )

        fig.savefig(
            f"{filename_prefix}.pdf",
            bbox_inches="tight"
        )

        print("\nFigura comparativa guardada:")
        print(f"- {filename_prefix}.png (600 dpi)")
        print(f"- {filename_prefix}.pdf")

    plt.show()
    plt.close(fig)


def print_numeric_summary(
    labels,
    shapley_vals,
    E_empty,
    E_full,
    v_values,
    title="Resumen"
):
    full_mask = (1 << len(labels)) - 1
    V_full = v_values[full_mask]

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(f"E(∅) = {E_empty:.6f}")
    print(f"E(N) = {E_full:.6f}")
    print(f"v(N) = E(N) - E(∅) = {V_full:.6f}")
    print(f"Suma Shapley = {np.sum(shapley_vals):.6f}")

    print("-" * 60)
    print(f"{'Bloque':<15} {'phi_b':>12}")
    print("-" * 60)

    for lab, phi in zip(labels, shapley_vals):
        print(f"{lab:<15} {phi:>12.6f}")

    print("=" * 60)


def print_comparison_table(
    labels,
    shapley_ok,
    shapley_faulty
):
    total_ok = np.sum(shapley_ok)
    total_faulty = np.sum(shapley_faulty)
    total_diff = total_faulty - total_ok

    print("\n" + "=" * 80)
    print("Comparación bloque por bloque: referencia vs modificada")
    print("=" * 80)

    print(
        f"{'Bloque':<15}"
        f"{'Correcta':>12}"
        f"{'Perturbada':>14}"
        f"{'Diferencia':>14}"
    )

    print("-" * 80)

    for lab, phi_ok, phi_fault in zip(
        labels,
        shapley_ok,
        shapley_faulty
    ):
        diff = phi_fault - phi_ok

        print(
            f"{lab:<15}"
            f"{phi_ok:>12.6f}"
            f"{phi_fault:>14.6f}"
            f"{diff:>14.6f}"
        )

    print("=" * 80)

    print(
        f"{'Suma':<15}"
        f"{total_ok:>12.6f}"
        f"{total_faulty:>14.6f}"
        f"{total_diff:>14.6f}"
    )

    print("=" * 80)

N = 21
a = 2
precision = 5

faulty_phase_block = 4
faulty_mode = "wrong_unitary"
faulty_a = 8

labels, shapley_vals, v_values, E_values, good_m, r, eps_used, E_empty, E_full = (
    smefe_shor_phase_blocks_shapley(
        a=a,
        N=N,
        precision=precision,
        eps=None,
        eps_bins=1.0,
        exclude_zero_peak=True,
        plot=True,
        save=True,
        filename_prefix="shapley_qpe_correct",
        verbose=True,
        faulty_phase_block=None,
        faulty_mode=None,
        faulty_a=None,
        plot_title_prefix=plot_text("shapley_correct_title")
    )
)

print("\nPeríodo r =", r)
print("eps usado =", eps_used)
print("Índices de éxito good_m =", good_m)
print("Bloques =", labels)
print("Shapley =", shapley_vals)
print("E(∅) =", E_empty)
print("E(N) =", E_full)

check_shapley_efficiency(
    shapley_vals,
    v_values
)

check_shapley_permutation_consistency(
    shapley_vals,
    v_values
)

check_probability_range(
    E_values
)

work_qubits = ceil(log2(N))

H_per_full = build_H_per_full_matrix(
    precision,
    work_qubits,
    good_m
)

check_projector_properties(
    H_per_full
)

check_probability_vs_expectation(
    a=a,
    N=N,
    precision=precision,
    good_m=good_m,
    coalition_mask=(1 << len(labels)) - 1,
    faulty_phase_block=None,
    faulty_mode=None,
    faulty_a=None
)

print_numeric_summary(
    labels,
    shapley_vals,
    E_empty,
    E_full,
    v_values,
    title="Configuración de referencia"
)

labels_fault, shapley_vals_fault, v_values_fault, E_values_fault, good_m_fault, r_fault, eps_fault, E_empty_fault, E_full_fault = (
    smefe_shor_phase_blocks_shapley(
        a=a,
        N=N,
        precision=precision,
        eps=None,
        eps_bins=1.0,
        exclude_zero_peak=True,
        plot=True,
        save=True,
        filename_prefix="shapley_qpe_faulty",
        verbose=True,
        faulty_phase_block=faulty_phase_block,
        faulty_mode=faulty_mode,
        faulty_a=faulty_a,
        plot_title_prefix=plot_text("shapley_faulty_title")
    )
)

print("\n[FAULTY] Período r =", r_fault)
print("[FAULTY] eps usado =", eps_fault)
print("[FAULTY] Índices de éxito good_m =", good_m_fault)
print("[FAULTY] Bloques =", labels_fault)
print("[FAULTY] Shapley =", shapley_vals_fault)
print("[FAULTY] E(∅) =", E_empty_fault)
print("[FAULTY] E(N) =", E_full_fault)

check_shapley_efficiency(
    shapley_vals_fault,
    v_values_fault
)

check_shapley_permutation_consistency(
    shapley_vals_fault,
    v_values_fault
)

check_probability_range(
    E_values_fault
)

H_per_full_fault = build_H_per_full_matrix(
    precision,
    work_qubits,
    good_m_fault
)

check_projector_properties(
    H_per_full_fault
)

check_probability_vs_expectation(
    a=a,
    N=N,
    precision=precision,
    good_m=good_m_fault,
    coalition_mask=(1 << len(labels_fault)) - 1,
    faulty_phase_block=faulty_phase_block,
    faulty_mode=faulty_mode,
    faulty_a=faulty_a
)

print_numeric_summary(
    labels_fault,
    shapley_vals_fault,
    E_empty_fault,
    E_full_fault,
    v_values_fault,
    title="Configuración modificada"
)

compare_shapley_correct_vs_faulty(
    labels,
    shapley_vals,
    shapley_vals_fault,
    save=True,
    filename_prefix="shapley_qpe_correct_vs_faulty"
)

print_comparison_table(
    labels,
    shapley_vals,
    shapley_vals_fault
)

def visualize_order_dependence(v_values, labels, title=None):
   
    if title is None:
        title = plot_text("order_dependence")

    n = len(labels)
    players = list(range(n))
    n_fact = factorial(n)

    # Matriz: filas = jugadores, columnas = posición (0 a n-1)
    position_contrib = np.zeros((n, n), dtype=float)

    # Lista para guardar TODAS las contribuciones marginales de cada jugador (para histograma)
    all_marginals = {i: [] for i in range(n)}

    print(f"\n=== Analizando {n_fact} permutaciones para visualizar el orden ===")

    # Iteramos sobre todas las permutaciones
    for pi in itertools.permutations(players):
        mask = 0
        for pos, player in enumerate(pi):
            mask_without = mask
            mask_with = mask | (1 << player)

            marginal = v_values[mask_with] - v_values[mask_without]

            # Acumulamos para el promedio de esta posición
            position_contrib[player, pos] += marginal / n_fact
            # Guardamos para el histograma
            all_marginals[player].append(marginal)

            mask = mask_with

    # --- GRÁFICO 1: MAPA DE CALOR (Heatmap) ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Heatmap de posición vs jugador
    im = axes[0].imshow(position_contrib, cmap='RdBu_r', aspect='auto', vmin=-0.2, vmax=0.2)
    axes[0].set_xticks(np.arange(n))
    axes[0].set_xticklabels(labels, rotation=45, ha='right')
    axes[0].set_yticks(np.arange(n))
    axes[0].set_yticklabels(labels)
    axes[0].set_xlabel(plot_text("permutation_position"))
    axes[0].set_ylabel(plot_text("player"))
    axes[0].set_title(f"{title}\n{plot_text('average_marginal_by_position')}")
    plt.colorbar(im, ax=axes[0], label=plot_text("marginal_contribution"))

    # --- GRÁFICO 2: HISTOGRAMAS DE CONTRIBUCIONES ---
    #
    for i, player in enumerate(players):
        # Normalizamos el histograma para que sea densidad
        axes[1].hist(all_marginals[player], bins=30, alpha=0.5, label=labels[i], density=True)

    axes[1].axvline(0, color='black', linestyle='--', linewidth=0.8, label=plot_text("zero_contribution"))
    axes[1].set_xlabel(plot_text("marginal_contribution"))
    axes[1].set_ylabel(plot_text("probability_density"))
    axes[1].set_title(plot_text("marginal_distribution"))
    axes[1].legend(loc='upper right', fontsize=8)
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

    # --- GRÁFICO 3: LÍNEAS DE POSICIÓN ---
    plt.figure(figsize=(10, 4))
    for i, player in enumerate(players):
        plt.plot(range(n), position_contrib[player, :], marker='o', label=labels[i], linewidth=2)
    plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
    plt.xlabel(plot_text("permutation_position_short"))
    plt.ylabel(plot_text("average_marginal"))
    plt.title(f"{title}\n{plot_text('position_evolution')}")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    return position_contrib, all_marginals

# Para el caso correcto:
pos_contrib_ok, marginals_ok = visualize_order_dependence(
    v_values,
    labels,
    title=plot_text("correct_case")
)

# Para el caso perturbado :
pos_contrib_fault, marginals_fault = visualize_order_dependence(
    v_values_fault,
    labels_fault,
    title=plot_text("faulty_case")
)
