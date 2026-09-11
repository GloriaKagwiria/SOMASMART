
import matplotlib
matplotlib.use("Agg")
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def series_circuit_calc(voltage, r1, r2):
    """Simple series circuit: battery, R1, R2 in series."""
    total_resistance = r1 + r2
    current = voltage / total_resistance
    v_r1 = current * r1
    v_r2 = current * r2
    return {
        "total_resistance": total_resistance,
        "current": current,
        "voltage_r1": v_r1,
        "voltage_r2": v_r2,
    }


def parallel_circuit_calc(voltage, r1, r2):
    """Simple parallel circuit: battery, R1 and R2 in parallel."""
    total_resistance = 1 / ((1 / r1) + (1 / r2))
    total_current = voltage / total_resistance
    current_r1 = voltage / r1
    current_r2 = voltage / r2
    return {
        "total_resistance": total_resistance,
        "total_current": total_current,
        "current_r1": current_r1,
        "current_r2": current_r2,
    }


def show_worked_steps_series(voltage, r1, r2, result):
    st.markdown("**Step 1 — Total resistance (series adds up):**")
    st.latex(f"R_{{total}} = R_1 + R_2 = {r1} + {r2} = {result['total_resistance']:.1f}\\ \\Omega")
    st.markdown("**Step 2 — Current (Ohm's Law):**")
    st.latex(f"I = \\frac{{V}}{{R_{{total}}}} = \\frac{{{voltage}}}{{{result['total_resistance']:.1f}}} = {result['current']:.2f}\\ A")
    st.markdown("**Step 3 — Voltage across each resistor:**")
    st.latex(f"V_{{R1}} = I \\times R_1 = {result['voltage_r1']:.2f}\\ V \\qquad V_{{R2}} = I \\times R_2 = {result['voltage_r2']:.2f}\\ V")


def show_worked_steps_parallel(voltage, r1, r2, result):
    st.markdown("**Step 1 — Total resistance (parallel formula):**")
    st.latex(f"\\frac{{1}}{{R_{{total}}}} = \\frac{{1}}{{{r1}}} + \\frac{{1}}{{{r2}}} \\implies R_{{total}} = {result['total_resistance']:.2f}\\ \\Omega")
    st.markdown("**Step 2 — Current through each branch (each sees full voltage):**")
    st.latex(f"I_{{R1}} = \\frac{{V}}{{R_1}} = {result['current_r1']:.2f}\\ A \\qquad I_{{R2}} = \\frac{{V}}{{R_2}} = {result['current_r2']:.2f}\\ A")
    st.markdown("**Step 3 — Total current drawn from the battery:**")
    st.latex(f"I_{{total}} = I_{{R1}} + I_{{R2}} = {result['total_current']:.2f}\\ A")


def general_series_calc(voltage, resistances):
    """Series circuit with any number of components (list of resistances in ohms)."""
    total_resistance = sum(resistances)
    current = voltage / total_resistance
    voltages = [current * r for r in resistances]
    return {
        "total_resistance": total_resistance,
        "current": current,
        "voltages": voltages,
    }


def general_parallel_calc(voltage, resistances):
    """Parallel circuit with any number of branches (list of resistances in ohms)."""
    total_resistance = 1 / sum(1 / r for r in resistances)
    currents = [voltage / r for r in resistances]
    total_current = sum(currents)
    return {
        "total_resistance": total_resistance,
        "total_current": total_current,
        "currents": currents,
    }


# --- Meter dial scales -------------------------------------------------
_SCALE_PRESETS = [
    (0.5, 0.1, 0.02),
    (1,   0.2, 0.05),
    (2,   0.5, 0.1),
    (5,   1,   0.2),
    (10,  2,   0.5),
    (15,  3,   1),
    (20,  4,   1),
    (30,  5,   1),
    (50,  10,  2),
    (100, 20,  5),
]


def _pick_scale(raw_value):
    """Given a raw value the needle needs to point at, pick a clean dial scale for it."""
    for max_value, major_step, minor_step in _SCALE_PRESETS:
        if raw_value <= max_value * 0.9:
            return max_value, major_step, minor_step
    max_value = round(raw_value * 1.2, 1)
    return max_value, max_value / 5, max_value / 25


def nice_max_scale(value):
    """Kept for compatibility with existing pages — returns just the dial's max value."""
    max_value, _, _ = _pick_scale(value)
    return max_value


def get_minor_step(value):
    """
    Returns the size of one minor tick on the dial this value would be drawn on.
    Use this as the tolerance when checking a student's typed-in reading.
    """
    _, _, minor_step = _pick_scale(value)
    return minor_step


def draw_analog_meter(value, max_value=None, label="Current", unit="A", needle_color="crimson"):
    """
    Draws a semicircular analog meter dial with a needle pointing at `value`.
    Minor ticks are sized to a clean, stated increment shown on the dial itself.
    `max_value` is accepted for backward compatibility but no longer required.
    """
    dial_max, major_step, minor_step = _pick_scale(value)
    minor_per_major = round(major_step / minor_step)
    n_minor_total = round(dial_max / minor_step)

    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    theta = np.linspace(180, 0, 100)
    ax.plot(np.cos(np.radians(theta)), np.sin(np.radians(theta)), color="black", linewidth=2)

    for i in range(n_minor_total + 1):
        v = i * minor_step
        t = 180 - 180 * (v / dial_max)
        is_major = (i % minor_per_major == 0)
        r_in = 0.88 if is_major else 0.93
        lw = 1.4 if is_major else 0.8
        x1, y1 = r_in * np.cos(np.radians(t)), r_in * np.sin(np.radians(t))
        x2, y2 = 1.0 * np.cos(np.radians(t)), 1.0 * np.sin(np.radians(t))
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=lw)
        if is_major:
            lx, ly = 1.18 * np.cos(np.radians(t)), 1.18 * np.sin(np.radians(t))
            ax.text(lx, ly, f"{v:.2g}", ha="center", va="center", fontsize=7.5)

    fraction = min(max(value / dial_max, 0), 1)
    needle_angle = 180 - 180 * fraction
    nx, ny = 0.75 * np.cos(np.radians(needle_angle)), 0.75 * np.sin(np.radians(needle_angle))
    ax.plot([0, nx], [0, ny], color=needle_color, linewidth=2.5, solid_capstyle="round")
    ax.scatter([0], [0], color="black", s=25, zorder=5)

    ax.text(0, -0.30, f"{label} ({unit})", ha="center", fontsize=10, fontweight="bold")
    ax.text(0, -0.42, f"each small mark = {minor_step:g} {unit}", ha="center", fontsize=7, color="gray")
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-0.55, 1.35)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


# --- Practical-skills tracking, used by the Physics Readiness Dashboard ---

def mark_practical_attempted(practical_name):
    """Records that a student has tried a given practical at least once this session."""
    if "practicals_attempted" not in st.session_state:
        st.session_state.practicals_attempted = set()
    st.session_state.practicals_attempted.add(practical_name)


def log_reading_attempt(correct, practical_name):
    """Records one meter-reading check (right or wrong) against a specific practical."""
    if "reading_attempts" not in st.session_state:
        st.session_state.reading_attempts = []
    st.session_state.reading_attempts.append({"correct": correct, "practical": practical_name})
    mark_practical_attempted(practical_name)


def get_reading_accuracy():
    """Returns (accuracy_percent, attempt_count). accuracy_percent is None if nothing recorded yet."""
    attempts = st.session_state.get("reading_attempts", [])
    if not attempts:
        return None, 0
    correct_count = sum(1 for a in attempts if a["correct"])
    return round(100 * correct_count / len(attempts), 1), len(attempts)


def get_practicals_attempted():
    """Returns the set of practical names the student has touched this session."""
    return st.session_state.get("practicals_attempted", set())