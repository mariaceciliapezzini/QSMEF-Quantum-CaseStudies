# *-
"""
Marco smef aplicado en el hipercubo acuñado con moneda de Grover y operador flip-flop.

SMEF-E APLICADO AL ALGORITMO SKW


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

 ============================================================

SKW:
  - Bloques: O (oráculo), G (moneda de Grover), S (shift)
   - Métrica funcional basada en H_ener
   - Shapley calculado sobre la métrica funcional M_H

Anomalía:
   - En el caso defectuoso, el oráculo aplica una fase incorrecta exp(i*theta_bug)
   - Se usa theta_bug = 0.70*pi para que la anomalía sea visible sin anular toda la dinámica
"""

import itertools
import math
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# IDIOMA / LANGUAGE
# ============================================================

LANG = "en"  # Usar "es" para español o "en" para inglés.

TEXT = {
    "es": {
        "value_error_n": "n debe ser >= 1",
        "unknown_operator": "Operador desconocido: {op}",
        "zero_norm": "El estado tiene norma cero.",
        "correct_label": "implementación correcta",
        "bug_label": "BUG: fase incorrecta en el oráculo",
        "shapley_table": "TABLA DE SHAPLEY SOBRE MÉTRICA FUNCIONAL",
        "max_efficiency_error": "Máximo error de eficiencia",
        "default_profile_title": "SMEF: perfil de Shapley | {label}",
        "oracle_legend": r"$\phi_O(t)$ Oráculo",
        "grover_legend": r"$\phi_G(t)$ Moneda de Grover",
        "shift_legend": r"$\phi_S(t)$ Desplazamiento",
        "x_step": "Paso $t$",
        "y_shapley": "Valor de Shapley / variación de la métrica funcional",
        "files_saved": "Archivos guardados: {png}, {pdf}",
        "oracle_summary": "RESUMEN COMPARATIVO DE LA CONTRIBUCIÓN DEL ORÁCULO",
        "phi_correct": "phi_O correcto",
        "phi_bug": "phi_O defectuoso",
        "difference": "diferencia",
        "max_window_difference": "Máxima diferencia absoluta en la ventana",
        "at_topt": (
            "En t_opt={t_opt}: phi_O correcto = {ok:.6f}, "
            "phi_O defectuoso = {bug:.6f}, diferencia = {diff:.6f}"
        ),
        "comparison_correct": r"$\phi_O(t)$ implementación correcta",
        "comparison_bug": r"$\phi_O(t)$ fase defectuosa",
        "profiles_difference": "Diferencia entre perfiles",
        "y_oracle": r"Contribución del oráculo $\phi_O(t)$",
        "comparison_title": "Anomalía en la fase del oráculo: comparación de perfiles",
        "main_header": "SMEF-E: SKW + ANOMALÍA COHERENTE EN LA FASE DEL ORÁCULO",
        "functional_order": "Orden funcional: {order}",
        "correct_phase": "Fase correcta: -1 = exp(i*pi)",
        "bug_phase": "Fase defectuosa: exp(i*{ratio:.2f}pi) = {phase:.4f}",
        "correct_plot_title": (
            "SMEF: implementación correcta | modo=energético | n={n}, objetivo={target}"
        ),
        "bug_plot_title": (
            "SMEF: fase incorrecta en el oráculo | theta=0.70pi | "
            "n={n}, objetivo={target}"
        ),
        "correct_filename": "skw_correcto",
        "bug_filename": "skw_fase_oraculo_incorrecta",
        "comparison_filename": "comparacion_oraculo_fase"
    },
    "en": {
        "value_error_n": "n must be >= 1",
        "unknown_operator": "Unknown operator: {op}",
        "zero_norm": "The state has zero norm.",
        "correct_label": "correct implementation",
        "bug_label": "modified implementation: incorrect oracle phase",
        "shapley_table": "SHAPLEY TABLE FOR THE FUNCTIONAL METRIC",
        "max_efficiency_error": "Maximum efficiency error",
        "default_profile_title": "SMEF: Shapley profile | {label}",
        "oracle_legend": r"$\phi_O(t)$ Oracle",
        "grover_legend": r"$\phi_G(t)$ Grover coin",
        "shift_legend": r"$\phi_S(t)$ Shift",
        "x_step": "Step $t$",
        "y_shapley": "Shapley value / functional metric variation",
        "files_saved": "Files saved: {png}, {pdf}",
        "oracle_summary": "COMPARATIVE SUMMARY OF THE ORACLE CONTRIBUTION",
        "phi_correct": "correct phi_O",
        "phi_bug": "modified phi_O",
        "difference": "difference",
        "max_window_difference": "Maximum absolute difference in the window",
        "at_topt": (
            "At t_opt={t_opt}: correct phi_O = {ok:.6f}, "
            "modified phi_O = {bug:.6f}, difference = {diff:.6f}"
        ),
        "comparison_correct": r"$\phi_O(t)$ correct implementation",
        "comparison_bug": r"$\phi_O(t)$ modified oracle phase",
        "profiles_difference": "Difference between profiles",
        "y_oracle": r"Oracle contribution $\phi_O(t)$",
        "comparison_title": "Oracle Phase Anomaly: Profile Comparison",
        "main_header": "SMEF-E: SKW + COHERENT ORACLE-PHASE ANOMALY",
        "functional_order": "Functional order: {order}",
        "correct_phase": "Correct phase: -1 = exp(i*pi)",
        "bug_phase": "Modified phase: exp(i*{ratio:.2f}pi) = {phase:.4f}",
        "correct_plot_title": (
            "SMEF: correct implementation | mode=energetic | n={n}, target={target}"
        ),
        "bug_plot_title": (
            "SMEF: incorrect oracle phase | theta=0.70pi | "
            "n={n}, target={target}"
        ),
        "correct_filename": "skw_correct",
        "bug_filename": "skw_incorrect_oracle_phase",
        "comparison_filename": "oracle_phase_comparison"
    }
}

if LANG not in TEXT:
    raise ValueError("LANG must be 'es' or 'en'.")

TXT = TEXT[LANG]


# ============================================================
# 1. FUNCIONES BASE
# ============================================================

def position_dim(n):
    n = int(n)
    if n < 1:
        raise ValueError(TXT["value_error_n"])
    return 1 << n

def coin_dim(n):
    n = int(n)
    if n < 1:
        raise ValueError(TXT["value_error_n"])
    return n

def uniform_coin_state(n):
    return np.ones(int(n), dtype=complex) / np.sqrt(int(n))

def reshape_cp(psi_vec, n):
    return np.asarray(psi_vec, dtype=complex).reshape(coin_dim(n), position_dim(n))

def flatten_cp(psi_cp):
    return np.asarray(psi_cp, dtype=complex).reshape(-1)

def grover_coin_matrix(n):
    D = uniform_coin_state(n)
    return 2.0 * np.outer(D, D.conj()) - np.eye(int(n), dtype=complex)

# ============================================================
# 2. OPERADORES SKW
# ============================================================

def apply_oracle_cp(psi_cp, n, target, oracle_phase=-1.0):
    """
    Correcto:
        oracle_phase = -1 = exp(i*pi)

    Defectuoso:
        oracle_phase = exp(i*theta_bug), con theta_bug != pi

    """
    target = int(target)
    psi_out = psi_cp.copy()
    psi_out[:, target] *= oracle_phase
    return psi_out

def apply_grover_coin_cp(psi_cp, n):
    G = grover_coin_matrix(n)
    return G @ psi_cp

def apply_shift_flip_flop_cp(psi_cp, n):
    n = int(n)
    dP = position_dim(n)
    out = np.zeros_like(psi_cp, dtype=complex)

    for a in range(n):
        for x in range(dP):
            y = x ^ (1 << a)
            out[a, y] += psi_cp[a, x]

    return out

def apply_oracle_Rprime(psi, target, n, oracle_phase=-1.0):
    return flatten_cp(
        apply_oracle_cp(
            reshape_cp(psi, n),
            n=n,
            target=target,
            oracle_phase=oracle_phase
        )
    )

def apply_grover_coin_locally(psi, n):
    return flatten_cp(apply_grover_coin_cp(reshape_cp(psi, n), n))

def apply_shift_flip_flop(psi, n):
    return flatten_cp(apply_shift_flip_flop_cp(reshape_cp(psi, n), n))

def apply_step_skw(
    psi,
    n,
    target,
    order=("O", "G", "S"),
    oracle_phase=-1.0
):
    """
    Paso completo SKW.
    """
    out = psi.copy()

    for op in order:
        if op == "O":
            out = apply_oracle_Rprime(
                out,
                target=target,
                n=n,
                oracle_phase=oracle_phase
            )
        elif op == "G":
            out = apply_grover_coin_locally(out, n)
        elif op == "S":
            out = apply_shift_flip_flop(out, n)
        else:
            raise ValueError(TXT["unknown_operator"].format(op=op))

    return out

def apply_coalition(
    psi,
    coalition,
    n,
    target,
    order=("O", "G", "S"),
    oracle_phase=-1.0
):
    out = psi.copy()

    for op in order:
        if op in coalition:
            if op == "O":
                out = apply_oracle_Rprime(
                    out,
                    target=target,
                    n=n,
                    oracle_phase=oracle_phase
                )
            elif op == "G":
                out = apply_grover_coin_locally(out, n)
            elif op == "S":
                out = apply_shift_flip_flop(out, n)

    return out

# ============================================================
# 3. ESTADO INICIAL Y PROBABILIDAD
# ============================================================

def initial_state(n, pos0=0, uniform_pos=True):
    n = int(n)
    N = position_dim(n)

    coin_state = uniform_coin_state(n)

    if uniform_pos:
        pos_state = np.ones(N, dtype=complex) / np.sqrt(N)
    else:
        pos_state = np.zeros(N, dtype=complex)
        pos_state[int(pos0)] = 1.0

    return np.kron(coin_state, pos_state)

def success_probability(psi, target, n):
    psi_cp = reshape_cp(psi, n) if np.asarray(psi).ndim == 1 else np.asarray(psi)
    return float(np.real(np.sum(np.abs(psi_cp[:, int(target)]) ** 2)))

# ============================================================
# 4. MÉTRICA FUNCIONAL H_ener
# ============================================================

def hener_expectation(psi, n, target, gamma=1.0):
    """
    <H_ener>, con:

        H_ener = I_C \\otimes (-gamma A_P - |t><t|)
    """
    n = int(n)
    target = int(target)
    N = position_dim(n)

    psi_cp = reshape_cp(psi, n) if np.asarray(psi).ndim == 1 else np.asarray(psi, dtype=complex)

    norm = np.linalg.norm(flatten_cp(psi_cp))
    if norm == 0:
        raise ValueError(TXT["zero_norm"])
    if abs(norm - 1.0) > 1e-10:
        psi_cp = psi_cp / norm

    prob_target = np.sum(np.abs(psi_cp[:, target]) ** 2)

    adj_exp = 0.0 + 0.0j
    for a in range(n):
        for x in range(N):
            y = x ^ (1 << a)
            adj_exp += np.vdot(psi_cp[:, x], psi_cp[:, y])

    return float(np.real(-gamma * adj_exp - prob_target))

def functional_metric(psi, n, target, gamma=1.0):
    return hener_expectation(psi, n=n, target=target, gamma=gamma)
# ============================================================
# 5. SHAPLEY SOBRE MÉTRICA FUNCIONAL
# ============================================================

def shapley_three_blocks_energy(
    psi_t,
    n,
    target,
    order=("O", "G", "S"),
    gamma=1.0,
    oracle_phase=-1.0
):
    """
    Shapley sobre la métrica funcional.

    v(C) = M_H(U_C psi_t) - M_H(psi_t)

    Eficiencia:
        phi_O + phi_G + phi_S = Delta_E_t
    """
    players = ["O", "G", "S"]

    m0 = functional_metric(psi_t, n=n, target=target, gamma=gamma)

    v = {frozenset(): 0.0}

    for r in range(1, len(players) + 1):
        for combo in itertools.combinations(players, r):
            C = frozenset(combo)

            psi_C = apply_coalition(
                psi_t,
                coalition=C,
                n=n,
                target=target,
                order=order,
                oracle_phase=oracle_phase
            )

            m_C = functional_metric(psi_C, n=n, target=target, gamma=gamma)
            v[C] = m_C - m0

    phi = {p: 0.0 for p in players}

    for perm in itertools.permutations(players):
        C = frozenset()
        for p in perm:
            C_next = frozenset(set(C) | {p})
            phi[p] += v[C_next] - v[C]
            C = C_next

    fact = math.factorial(len(players))
    for p in players:
        phi[p] /= fact

    full = frozenset(players)

    return {
        "phi": phi,
        "v_full": v[full],
        "v": v,
        "m_before": m0,
        "m_after_full": m0 + v[full],
    }

# ============================================================
# 6. SIMULACIÓN
# ============================================================

def run_and_collect(
    n=8,
    target=0,
    T=24,
    order=("O", "G", "S"),
    gamma=1.0,
    oracle_phase=-1.0,
    label=None,
    t_opt=19
):
    psi = initial_state(n=n, pos0=0, uniform_pos=True)

    states = []
    MH = []
    PS = []

    phi_O = []
    phi_G = []
    phi_S = []
    delta_E = []

    for step in range(T + 1):
        states.append(psi.copy())
        MH.append(functional_metric(psi, n=n, target=target, gamma=gamma))
        PS.append(success_probability(psi, target=target, n=n))

        if step < T:
            shap = shapley_three_blocks_energy(
                psi,
                n=n,
                target=target,
                order=order,
                gamma=gamma,
                oracle_phase=oracle_phase
            )

            phi_O.append(float(shap["phi"]["O"]))
            phi_G.append(float(shap["phi"]["G"]))
            phi_S.append(float(shap["phi"]["S"]))
            delta_E.append(float(shap["v_full"]))

            psi = apply_step_skw(
                psi,
                n=n,
                target=target,
                order=order,
                oracle_phase=oracle_phase
            )
    return {
        "ts": np.arange(T + 1),
        "steps": np.arange(T),
        "states": states,
        "MH": np.array(MH),
        "PS": np.array(PS),
        "phi": {
            "O": np.array(phi_O),
            "G": np.array(phi_G),
            "S": np.array(phi_S),
        },
        "delta_E": np.array(delta_E),
        "n": n,
        "target": target,
        "T": T,
        "order": order,
        "gamma": gamma,
        "oracle_phase": oracle_phase,
        "label": label if label is not None else TXT["correct_label"],
        "t_opt": int(t_opt),
    }

# ============================================================
# 7. TABLAS
# ============================================================

def print_shapley_table(res, start=15, end=23, decimals=6):
    steps = res["steps"]
    O = res["phi"]["O"]
    G = res["phi"]["G"]
    S = res["phi"]["S"]
    sum_phi = O + G + S
    delta_E = res["delta_E"]
    error = sum_phi - delta_E

    mask = (steps >= start) & (steps <= end)

    print("\n" + "=" * 105)
    print(f"{TXT['shapley_table']} | {res['label']}")
    print("=" * 105)
    print(
        f"{'t':>4} | {'phi_O':>12} | {'phi_G':>12} | {'phi_S':>12} | "
        f"{'sum_phi':>12} | {'Delta_E':>12} | {'error':>12}"
    )
    print("-" * 105)

    for t, o, g, s, total, de, err in zip(
        steps[mask], O[mask], G[mask], S[mask], sum_phi[mask], delta_E[mask], error[mask]
    ):
        print(
            f"{int(t):>4} | "
            f"{o:>12.{decimals}f} | "
            f"{g:>12.{decimals}f} | "
            f"{s:>12.{decimals}f} | "
            f"{total:>12.{decimals}f} | "
            f"{de:>12.{decimals}f} | "
            f"{err:>12.2e}"
        )

    print("-" * 105)
    print(f"{TXT['max_efficiency_error']} |Σφ - ΔE| = {np.max(np.abs(error)):.3e}")
    print("=" * 105)

# ============================================================
# 8. GRÁFICOS
# ============================================================

def signed_stacked_bars(ax, x, series, labels, colors, width=0.72):
    pos_bottom = np.zeros(len(x))
    neg_bottom = np.zeros(len(x))

    for values, label, color in zip(series, labels, colors):
        values = np.asarray(values)
        bottom = np.where(values >= 0, pos_bottom, neg_bottom)

        ax.bar(
            x,
            values,
            width=width,
            bottom=bottom,
            label=label,
            color=color,
            alpha=0.88,
            edgecolor="black",
            linewidth=0.6
        )

        pos_bottom = np.where(values >= 0, pos_bottom + values, pos_bottom)
        neg_bottom = np.where(values < 0, neg_bottom + values, neg_bottom)

def plot_shapley_profile(
    res,
    start=15,
    end=23,
    title=None,
    filename_prefix="skw_profile",
    save=True
):
    steps = res["steps"]
    O = res["phi"]["O"]
    G = res["phi"]["G"]
    S = res["phi"]["S"]

    sum_phi = O + G + S
    delta_E = res["delta_E"]
    t_opt = res["t_opt"]

    mask = (steps >= start) & (steps <= end)

    t = steps[mask]
    phi_O = O[mask]
    phi_G = G[mask]
    phi_S = S[mask]
    sp = sum_phi[mask]
    de = delta_E[mask]


    max_err = np.max(np.abs(sp - de))

    if title is None:
        title = TXT["default_profile_title"].format(label=res["label"])

    fig, ax = plt.subplots(figsize=(10.5, 5.8))

    signed_stacked_bars(
        ax,
        t,
        [phi_O, phi_G, phi_S],
        [
            TXT["oracle_legend"],
            TXT["grover_legend"],
            TXT["shift_legend"]
        ],
        ["#D55E00", "#56B4E9", "#009E73"]
    )

    ax.plot(
        t,
        de,
        "-o",
        color="black",
        linewidth=2.4,
        markersize=6,
        label=r"$\Delta E_t$",
        zorder=5
    )

    ax.plot(
        t,
        sp,
        "--x",
        color="gray",
        linewidth=2,
        markersize=7,
        label=r"$\sum_b \phi_b(t)$",
        zorder=6
    )

    ax.axhline(
        0,
        color="black",
        linewidth=0.9
    )

    ax.axvline(
        t_opt,
        linestyle="--",
        color="red",
        linewidth=1.8,
        alpha=0.75
    )

    fig.canvas.draw()

    y_min, y_max = ax.get_ylim()

    ax.text(
        t_opt + 0.12,
        y_max - 0.06 * (y_max - y_min),
        rf"$t_{{\mathrm{{opt}}}}={t_opt}$",
        color="red",
        fontsize=11,
        fontweight="bold",
        ha="left",
        va="top"
    )

    residual_text = (
        rf"$\max_t\left|"
        rf"\sum_b \phi_b(t)-\Delta E_t"
        rf"\right|={max_err:.2e}$"
    )

    ax.text(
        0.985,
        0.965,
        residual_text,
        transform=ax.transAxes,
        ha="right",
        va="top",
        bbox=dict(
            facecolor="white",
            alpha=0.90,
            edgecolor="gray",
            boxstyle="round,pad=0.25"
        ),
        fontsize=10,
        zorder=10
    )

    ax.set_xlabel(
        TXT["x_step"],
        fontsize=12
    )

    ax.set_ylabel(
        TXT["y_shapley"],
        fontsize=12
    )

    ax.set_title(
        title,
        fontsize=14,
        pad=10
    )

    ax.set_xticks(t)
    ax.grid(True, axis="y", alpha=0.3)

    ax.legend(
        loc="lower left",
        bbox_to_anchor=(0.02, 0.02),
        fontsize=9,
        framealpha=0.95
    )

    plt.tight_layout()

    if save:
        png = f"{filename_prefix}.png"
        pdf = f"{filename_prefix}.pdf"

        fig.savefig(
            png,
            dpi=600,
            bbox_inches="tight"
        )

        fig.savefig(
            pdf,
            bbox_inches="tight"
        )

        print(TXT["files_saved"].format(png=png, pdf=pdf))

    plt.show()
    plt.close(fig)

def print_oracle_anomaly_summary(res_ok, res_bug, start=15, end=23):
    """
    Tabla simple para verificar que la anomalía sea visible en phi_O.
    """
    steps = res_ok["steps"]
    mask = (steps >= start) & (steps <= end)

    t = steps[mask]
    O_ok = res_ok["phi"]["O"][mask]
    O_bug = res_bug["phi"]["O"][mask]
    diff = O_bug - O_ok

    print("\n" + "=" * 90)
    print(TXT["oracle_summary"])
    print("=" * 90)
    print(f"{'t':>4} | {TXT['phi_correct']:>16} | {TXT['phi_bug']:>18} | {TXT['difference']:>14}")
    print("-" * 90)

    for ti, ok, bug, d in zip(t, O_ok, O_bug, diff):
        print(f"{int(ti):>4} | {ok:>16.6f} | {bug:>18.6f} | {d:>14.6f}")

    print("-" * 90)
    print(f"{TXT['max_window_difference']} = {np.max(np.abs(diff)):.6f}")

    if res_ok["t_opt"] in t:
        idx = int(np.where(t == res_ok["t_opt"])[0][0])
        print(TXT["at_topt"].format(
            t_opt=res_ok["t_opt"], ok=O_ok[idx], bug=O_bug[idx], diff=diff[idx]
        ))

    print("=" * 90)

def plot_comparison_lines(
    res_ok,
    res_bug,
    start=15,
    end=23,
    filename_prefix="Comparacion_Oraculo_Bug_Fase",
    save=True
):
    """
    Compara la contribución del oráculo entre la implementación
    correcta y la implementación con una fase incorrecta.
    """
    steps = res_ok["steps"]
    mask = (steps >= start) & (steps <= end)

    t = steps[mask]
    O_ok = res_ok["phi"]["O"][mask]
    O_bug = res_bug["phi"]["O"][mask]
    diff = O_bug - O_ok

    fig, ax = plt.subplots(figsize=(10.2, 5.2))

    ax.plot(
        t,
        O_ok,
        "-o",
        color="#D55E00",
        linewidth=2.5,
        markersize=6,
        label=TXT["comparison_correct"]
    )

    ax.plot(
        t,
        O_bug,
        "--s",
        color="#0072B2",
        linewidth=2.5,
        markersize=6,
        label=TXT["comparison_bug"]
    )

    ax.fill_between(
        t,
        O_ok,
        O_bug,
        color="gray",
        alpha=0.18,
        label=TXT["profiles_difference"]
    )

    ax.axhline(
        0,
        color="black",
        linewidth=0.9
    )

    ax.axvline(
        res_ok["t_opt"],
        linestyle="--",
        color="red",
        linewidth=1.8,
        alpha=0.75
    )

    if res_ok["t_opt"] in t:
        idx = int(np.where(t == res_ok["t_opt"])[0][0])

        ax.annotate(
            rf"$\Delta\phi_O({res_ok['t_opt']})={diff[idx]:.3f}$",
            xy=(res_ok["t_opt"], O_bug[idx]),
            xytext=(
                res_ok["t_opt"] + 0.35,
                O_bug[idx] - 0.12
            ),
            arrowprops=dict(
                arrowstyle="->",
                color="red",
                linewidth=1.4
            ),
            fontsize=10,
            color="red"
        )

    ax.set_xlabel(
        TXT["x_step"],
        fontsize=12
    )

    ax.set_ylabel(
        TXT["y_oracle"],
        fontsize=12
    )

    ax.set_title(
        TXT["comparison_title"],
        fontsize=14
    )

    ax.set_xticks(t)
    ax.grid(True, alpha=0.3)

    ax.legend(
        loc="best",
        fontsize=9,
        framealpha=0.95
    )

    plt.tight_layout()

    if save:
        png = f"{filename_prefix}.png"
        pdf = f"{filename_prefix}.pdf"

        fig.savefig(
            png,
            dpi=600,
            bbox_inches="tight"
        )

        fig.savefig(
            pdf,
            bbox_inches="tight"
        )

        print(TXT["files_saved"].format(png=png, pdf=pdf))

    plt.show()
    plt.close(fig)


# ============================================================
# 9. EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    n = 8
    target = 0
    T = 24
    gamma = 1.0
    order = ("O", "G", "S")
    t_opt = 19

    # Oráculo: aplica una fase π al estado objetivo.
    # Como exp(iπ) = -1, usamos directamente el valor real -1.
    phase_ok = -1.0

    # Defectuoso: fase incorrecta.
    #
    # Para mostrar una anomalía, pero manteniendo dinámica observable,
    # usamos una fase cercana pero distinta de pi:
    #
    #   correcto:   theta = 1.00*pi  => fase -1
    #   defectuoso: theta = 0.70*pi  => fase incorrecta
    #
    # Con este valor el oráculo conserva efecto, pero su perfil de contribución
    # cambia en la ventana alrededor de t_opt.
    theta_bug = 0.70 * np.pi
    phase_bug = np.exp(1j * theta_bug)

    print("=" * 80)
    print(TXT["main_header"])
    print("=" * 80)
    print(f"n={n}, N={position_dim(n)}, target={target}, T={T}, gamma={gamma}")
    print(TXT["functional_order"].format(order=order))
    print(TXT["correct_phase"])
    print(TXT["bug_phase"].format(ratio=theta_bug/np.pi, phase=phase_bug))

    res_ok = run_and_collect(
        n=n,
        target=target,
        T=T,
        order=order,
        gamma=gamma,
        oracle_phase=phase_ok,
        label=TXT["correct_label"],
        t_opt=t_opt
    )

    res_bug = run_and_collect(
        n=n,
        target=target,
        T=T,
        order=order,
        gamma=gamma,
        oracle_phase=phase_bug,
        label=TXT["bug_label"],
        t_opt=t_opt
    )

    print_shapley_table(res_ok, start=15, end=23)
    print_shapley_table(res_bug, start=15, end=23)
    print_oracle_anomaly_summary(res_ok, res_bug, start=15, end=23)

    plot_shapley_profile(
        res_ok,
        start=15,
        end=23,
        title=TXT["correct_plot_title"].format(n=n, target=target),
        filename_prefix=TXT["correct_filename"],
        save=True
    )

    plot_shapley_profile(
        res_bug,
        start=15,
        end=23,
        title=TXT["bug_plot_title"].format(n=n, target=target),
        filename_prefix=TXT["bug_filename"],
        save=True
    )

    plot_comparison_lines(
        res_ok,
        res_bug,
        start=15,
        end=23,
        filename_prefix=TXT["comparison_filename"],
        save=True
    )