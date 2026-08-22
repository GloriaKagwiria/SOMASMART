import matplotlib
matplotlib.use("Agg")
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
from utils.circuit_logic import draw_analog_meter, nice_max_scale

st.title("🧵 Resistance of a Wire — Practical")
st.write(
    "This replicates the classic KCSE setup: a resistance wire mounted on a board, "
    "where a sliding contact (jockey) changes the length of wire in the circuit. "
    "Move the jockey, record a reading, repeat at a few different lengths, then plot your graph — "
    "same as you would in the lab, just without needing the physical wire and board."
)

resistivity_per_m = st.slider(
    "Wire resistance per metre (Ω/m)", 1.0, 10.0, 4.0, step=0.5,
    help="In a real practical your teacher gives you this, or you calculate it from your own data — it depends on the wire's material and thickness."
)
voltage = st.slider("Battery Voltage (V)", 1.0, 12.0, 6.0, step=0.5)
length_cm = st.slider("Jockey position — length of wire in the circuit (cm)", 5, 100, 50)

length_m = length_cm / 100
resistance = resistivity_per_m * length_m
current = voltage / resistance

# --- Circuit diagram (shows the topology: battery -> ammeter -> wire -> back) ---
d = schemdraw.Drawing()
d += (batt := elm.Battery().up().label(f"{voltage}V"))
d += elm.Line().right().length(1)
d += elm.MeterI().right().label("A")
d += elm.Resistor().right().label(f"Wire\n({length_cm} cm)")
d += elm.Line().down().length(1)
d += elm.Line().to(batt.start)
circuit_fig = d.draw(show=False)
st.pyplot(circuit_fig.fig)

# --- Live meters: the needles move as you drag the sliders above ---
st.subheader("Live readings")
st.caption("These update instantly as you move the sliders — just like watching the needles move as you slide the jockey in a real practical.")

meter_col1, meter_col2 = st.columns(2)
with meter_col1:
    amp_max = nice_max_scale(current)
    st.pyplot(draw_analog_meter(current, amp_max, label="Ammeter", unit="A"))
with meter_col2:
    volt_max = nice_max_scale(voltage)
    st.pyplot(draw_analog_meter(voltage, volt_max, label="Voltmeter", unit="V"))

st.write(f"At **{length_cm} cm**: R = {resistance:.2f} Ω, I = {current:.3f} A")

if "wire_readings" not in st.session_state:
    st.session_state.wire_readings = []

col1, col2 = st.columns(2)
if col1.button("📏 Record this reading"):
    st.session_state.wire_readings.append({
        "Length (cm)": length_cm,
        "Resistance (Ω)": round(resistance, 2),
        "Voltage (V)": voltage,
        "Current (A)": round(current, 3),
    })
if col2.button("🗑️ Clear all readings"):
    st.session_state.wire_readings = []

if st.session_state.wire_readings:
    st.subheader("Your recorded readings")
    st.table(st.session_state.wire_readings)

    if len(st.session_state.wire_readings) >= 2:
        st.subheader("Plot a graph")
        st.write("Choose what you want to investigate — pick two different quantities to plot against each other.")

        axis_options = ["Length (cm)", "Resistance (Ω)", "Voltage (V)", "Current (A)"]
        col3, col4 = st.columns(2)
        x_axis = col3.selectbox("X-axis", axis_options, index=0)
        y_axis = col4.selectbox("Y-axis", axis_options, index=1)

        if x_axis == y_axis:
            st.warning("Pick two different quantities so there's something to compare.")
        else:
            x_vals = [r[x_axis] for r in st.session_state.wire_readings]
            y_vals = [r[y_axis] for r in st.session_state.wire_readings]

            graph_fig, ax = plt.subplots()
            ax.scatter(x_vals, y_vals, color="tab:blue")
            gradient, intercept = np.polyfit(x_vals, y_vals, 1)
            x_line = np.linspace(min(x_vals), max(x_vals), 50)
            ax.plot(x_line, gradient * x_line + intercept, color="tab:red", linestyle="--")
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"{y_axis} vs {x_axis}")
            st.pyplot(graph_fig)

            st.info(
                f"Gradient of this line ≈ **{gradient:.4f}** ({y_axis} per unit of {x_axis}) — "
                "in a real practical, this is what you'd work out by hand from your own graph."
            )
    else:
        st.caption("Record at least one more reading at a different length to see the graph.")
else:
    st.caption("No readings yet — move the length slider and click **Record this reading** at a few different lengths, just like moving the jockey in the lab.")
