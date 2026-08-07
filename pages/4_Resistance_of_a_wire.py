import matplotlib
matplotlib.use("Agg")
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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

st.write(f"At **{length_cm} cm**: R = {resistance:.2f} Ω, I = {current:.3f} A")

if "wire_readings" not in st.session_state:
    st.session_state.wire_readings = []

col1, col2 = st.columns(2)
if col1.button("📏 Record this reading"):
    st.session_state.wirereadings.append({
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
        lengths = [r["Length (cm)"] for r in st.session_state.wire_readings]
        resistances = [r["Resistance (Ω)"] for r in st.session_state.wire_readings]

        fig, ax = plt.subplots()
        ax.scatter(lengths, resistances, color="tab:blue")
        gradient, intercept = np.polyfit(lengths, resistances, 1)
        x_line = np.linspace(min(lengths), max(lengths), 50)
        ax.plot(x_line, gradient * x_line + intercept, color="tab:red", linestyle="--")
        ax.set_xlabel("Length (cm)")
        ax.set_ylabel("Resistance (Ω)")
        ax.set_title("Resistance vs Length")
        st.pyplot(fig)

        st.info(
            f"Gradient of this line ≈ **{gradient:.3f} Ω/cm** — in a real practical, this is what "
            "you'd work out by hand from your own graph, and it tells you the wire's resistance per unit length."
        )
    else:
        st.caption("Record at least one more reading at a different length to see the graph.")
else:
    st.caption("No readings yet — move the length slider and click **Record this reading** at a few different lengths, just like moving the jockey in the lab.")