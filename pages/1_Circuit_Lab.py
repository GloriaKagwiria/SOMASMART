import streamlit as st
import schemdraw
import schemdraw.elements as elm
from utilis.circuit_logic import series_circuit_calc, parallel_circuit_calc

st.title("🔌 Circuit Lab")

circuit_type = st.selectbox("Choose a circuit", ["Series Circuit", "Parallel Circuit"])

voltage = st.slider("Battery Voltage (V)", 1, 24, 12)
r1 = st.slider("Resistor 1 (Ω)", 1, 100, 4)
r2 = st.slider("Resistor 2 (Ω)", 1, 100, 2)

if circuit_type == "Series Circuit":
    d = schemdraw.Drawing()
    d += elm.Battery().label(f"{voltage}V")
    d += elm.Resistor().label(f"R1={r1}Ω")
    d += elm.Resistor().label(f"R2={r2}Ω")
    d += elm.Line().dot()

    fig = d.draw(show=False)
    st.pyplot(fig.fig)

    result = series_circuit_calc(voltage, r1, r2)

    st.subheader("Predict first, then reveal")
    guess = st.number_input("What is the current (A) flowing through this circuit?", min_value=0.0, step=0.1)

    if st.button("Reveal Answer"):
        st.write(f"**Actual current:** {result['current']:.2f} A")
        st.write(f"Voltage across R1: {result['voltage_r1']:.2f} V")
        st.write(f"Voltage across R2: {result['voltage_r2']:.2f} V")
        if abs(guess - result['current']) < 0.1:
            st.success("Close! Good instinct.")
        else:
            st.info("Not quite — look at how total resistance affects current (V = IR).")

else:  # Parallel
    d = schemdraw.Drawing()
    d += elm.Battery().label(f"{voltage}V")
    d += (r1_elm := elm.Resistor().label(f"R1={r1}Ω"))
    d += elm.Line().right()
    d += elm.Resistor().label(f"R2={r2}Ω")

    fig = d.draw(show=False)
    st.pyplot(fig.fig)

    result = parallel_circuit_calc(voltage, r1, r2)
    st.write(f"**Total current:** {result['total_current']:.2f} A")
    st.write(f"Current through R1: {result['current_r1']:.2f} A")
    st.write(f"Current through R2: {result['current_r2']:.2f} A")
