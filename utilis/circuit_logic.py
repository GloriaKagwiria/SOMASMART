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


def nice_max_scale(value):
    """Picks a sensible round-number maximum for a meter dial, given the value it needs to display."""
    for m in [0.5, 1, 2, 5, 10, 15, 20, 30, 50, 100]:
        if value <= m * 0.9:
            return m
    return round(value * 1.2, 1)


def draw_analog_meter(value, max_value, label="Current", unit="A", needle_color="crimson"):
    """
    Draws a semicircular analog meter dial with a needle pointing at `value`,
    scaled against `max_value`. Returns a matplotlib figure — pass it to st.pyplot(fig).
    """
    fig, ax = plt.subplots(figsize=(3.2, 2.2))
    theta = np.linspace(180, 0, 100)
    xs = np.cos(np.radians(theta))
    ys = np.sin(np.radians(theta))
    ax.plot(xs, ys, color="black", linewidth=2)

    num_ticks = 6
    for i in range(num_ticks + 1):
        t = 180 - (180 * i / num_ticks)
        x1, y1 = 0.88 * np.cos(np.radians(t)), 0.88 * np.sin(np.radians(t))
        x2, y2 = 1.0 * np.cos(np.radians(t)), 1.0 * np.sin(np.radians(t))
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=1.2)
        val_label = max_value * i / num_ticks
        lx, ly = 1.18 * np.cos(np.radians(t)), 1.18 * np.sin(np.radians(t))
        ax.text(lx, ly, f"{val_label:.1f}", ha="center", va="center", fontsize=7.5)

    fraction = min(max(value / max_value, 0), 1)
    needle_angle = 180 - 180 * fraction
    nx, ny = 0.75 * np.cos(np.radians(needle_angle)), 0.75 * np.sin(np.radians(needle_angle))
    ax.plot([0, nx], [0, ny], color=needle_color, linewidth=2.5, solid_capstyle="round")
    ax.scatter([0], [0], color="black", s=25, zorder=5)

    ax.text(0, -0.32, f"{label} ({unit})", ha="center", fontsize=10, fontweight="bold")
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-0.45, 1.35)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig
