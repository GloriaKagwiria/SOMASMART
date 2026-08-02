import streamlit as st
import schemdraw
import schemdraw.elements as elm
from utilis.circuit_logic import series_circuit_calc, parallel_circuit_calc, show_worked_steps_series, show_worked_steps_parallel

def render_bulb(label, current, max_current=5):
    """Draws a simple bulb icon whose size/brightness scales with current."""
    brightness = min(current / max_current, 1.0)
    opacity = 0.25 + 0.75 * brightness   # never fully invisible, so "off" is still visible as dim
    size = 40 + 40 * brightness
    st.markdown(
        f"<div style='text-align:center'>"
        f"<span style='font-size:{size}px; opacity:{opacity:.2f};'>💡</span>"
        f"<div>{label}: {current:.2f} A</div></div>",
        unsafe_allow_html=True,
    )

st.title("🔌 Circuit Lab")

circuit_type = st.selectbox("Choose a circuit", ["Series Circuit", "Parallel Circuit"])
component_type = st.radio("Component type", ["Resistor", "Bulb"], horizontal=True)

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
        show_worked_steps_series(voltage, r1, r2, result)          # ← this is the new line

        if component_type == "Bulb":
            render_bulb("Bulb (series)", result["current"])
    st.info(
        "**General rule:** In series, adding more bulbs increases total resistance, so current "
        "drops and every bulb dims — and if one bulb blows, the whole circuit breaks. In parallel, "
        "each bulb sees the full battery voltage regardless of how many others are connected, so "
        "brightness stays the same as you add more, and one bulb blowing doesn't affect the rest."
    )

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

    st.subheader("Predict first, then reveal")
    guess = st.number_input("What is the TOTAL current (A) drawn from the battery?", min_value=0.0, step=0.1)

    if st.button("Reveal Answer", key="parallel_reveal"):
        show_worked_steps_parallel(voltage, r1, r2, result)
        if component_type =="Bulb":
            render_bulb("Bulb 1", result["current_r1"])
            render_bulb("Bulb 2", result["current_r2"])
            st.info(
                "**General rule:** In series, adding more bulbs increases total resistance, so current "
                    "drops and every bulb dims — and if one bulb blows, the whole circuit breaks. In parallel, "
                    "each bulb sees the full battery voltage regardless of how many others are connected, so "
                    "brightness stays the same as you add more, and one bulb blowing doesn't affect the rest."
                )
            
        if abs(guess - result["total_current"]) < 0.1:
            st.success("Close! Good instinct.")
        else:
            st.info("Not quite — in parallel, each branch sees the full voltage, so lower resistance branches pull more current.")

st.divider()
st.subheader("Ohm's Law Explorer")
st.write("Leave ONE field at 0 — that's the value it will solve for.")
 
v_in = st.number_input("Voltage (V)", min_value=0.0, value=0.0, key="ohm_v")
i_in = st.number_input("Current (A)", min_value=0.0, value=0.0, key="ohm_i")
r_in = st.number_input("Resistance (Ω)", min_value=0.0, value=0.0, key="ohm_r")
 
zeros = [x == 0 for x in (v_in, i_in, r_in)]
if sum(zeros) != 1:
    st.warning("Enter exactly two values and leave the third at 0.")
else:
    if v_in == 0:
        st.success(f"V = I × R = **{i_in * r_in:.2f} V**")
    elif i_in == 0:
        st.success(f"I = V ÷ R = **{v_in / r_in:.2f} A**")
    else:
        st.success(f"R = V ÷ I = **{v_in / i_in:.2f} Ω**")
 
