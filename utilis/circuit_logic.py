import streamlit as st 
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
     
