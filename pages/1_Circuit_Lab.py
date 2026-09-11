
import streamlit as st
import schemdraw
import schemdraw.elements as elm
from utils.circuit_logic import (
    series_circuit_calc,
    parallel_circuit_calc,
    show_worked_steps_series,
    show_worked_steps_parallel,
    draw_analog_meter,
    nice_max_scale,
    log_reading_attempt,
)


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

# Labels swap to match whichever component type is selected
comp_word = "Bulb" if component_type == "Bulb" else "Resistor"

voltage = st.slider("Battery Voltage (V)", 1, 24, 12)
r1 = st.slider(f"{comp_word} 1 (Ω)", 1, 100, 4)
r2 = st.slider(f"{comp_word} 2 (Ω)", 1, 100, 2)

if circuit_type == "Series Circuit":
    d = schemdraw.Drawing()
    d += (batt := elm.Battery().up().label(f"{voltage}V"))
    d += elm.Line().right().length(1)
    if component_type == "Bulb":
        d += elm.Lamp().right().label("L1")
        d += elm.Lamp().right().label("L2")
    else:
        d += elm.Resistor().right().label(f"R1={r1}Ω")
        d += elm.Resistor().right().label(f"R2={r2}Ω")
    d += elm.Line().down().length(1)
    d += elm.Line().to(batt.start)

    fig = d.draw(show=False)
    st.pyplot(fig.fig)

    result = series_circuit_calc(voltage, r1, r2)

    st.subheader("Read the meter")
    st.write(
        "The needle below is pointing at the real current in this circuit — just like a real "
        "ammeter would. Read it as carefully as you can, estimating between the tick marks if you need to."
    )

    meter_max = nice_max_scale(result["current"])
    meter_fig = draw_analog_meter(result["current"], meter_max, label="Ammeter", unit="A")
    st.pyplot(meter_fig)

    my_reading = st.number_input("What does the meter read? (A)", min_value=0.0, step=0.1, key="series_meter_reading")

    if st.button("Check My Reading"):
        tolerance = meter_max * 0.05
        is_correct = abs(my_reading - result["current"]) <= tolerance
        log_reading_attempt(is_correct, "Series Circuit")
        if is_correct:
            st.success(f"Good reading! The actual current is {result['current']:.2f} A.")
        else:
            st.warning(f"Not quite — look again at where the needle sits between the tick marks. Actual current: {result['current']:.2f} A.")

        show_worked_steps_series(voltage, r1, r2, result)

        if component_type == "Bulb":
            render_bulb("Bulb (series)", result["current"])
            st.info(
                "**General rule:** In series, adding more bulbs increases total resistance, so current "
                "drops and every bulb dims — and if one bulb blows, the whole circuit breaks. In parallel, "
                "each bulb sees the full battery voltage regardless of how many others are connected, so "
                "brightness stays the same as you add more, and one bulb blowing doesn't affect the rest."
            )

else:  # Parallel
    d = schemdraw.Drawing()
    d += (batt := elm.Battery().up().label(f"{voltage}V"))
    d += elm.Line().right().length(1)
    d.push()
    if component_type == "Bulb":
        d += elm.Lamp().down().label("L1")
    else:
        d += elm.Resistor().down().label(f"R1={r1}Ω")
    d.pop()
    d += elm.Line().right().length(2)
    if component_type == "Bulb":
        d += elm.Lamp().down().label("L2")
    else:
        d += elm.Resistor().down().label(f"R2={r2}Ω")
    d += elm.Line().left().tox(batt.start)

    fig = d.draw(show=False)
    st.pyplot(fig.fig)

    result = parallel_circuit_calc(voltage, r1, r2)

    st.subheader("Read the meter")
    st.write(
        "The needle below is pointing at the real TOTAL current drawn from the battery. "
        "Read it as carefully as you can, estimating between the tick marks if you need to."
    )

    meter_max = nice_max_scale(result["total_current"])
    meter_fig = draw_analog_meter(result["total_current"], meter_max, label="Ammeter", unit="A")
    st.pyplot(meter_fig)

    my_reading = st.number_input("What does the meter read? (A)", min_value=0.0, step=0.1, key="parallel_meter_reading")

    if st.button("Check My Reading", key="parallel_reveal"):
        tolerance = meter_max * 0.05
        is_correct = abs(my_reading - result["total_current"]) <= tolerance
        log_reading_attempt(is_correct, "Parallel Circuit")
        if is_correct:
            st.success(f"Good reading! The actual total current is {result['total_current']:.2f} A.")
        else:
            st.warning(f"Not quite — look again at where the needle sits between the tick marks. Actual total current: {result['total_current']:.2f} A.")

        show_worked_steps_parallel(voltage, r1, r2, result)

        if component_type == "Bulb":
            render_bulb("Bulb 1", result["current_r1"])
            render_bulb("Bulb 2", result["current_r2"])
            st.info(
                "**General rule:** In series, adding more bulbs increases total resistance, so current "
                "drops and every bulb dims — and if one bulb blows, the whole circuit breaks. In parallel, "
                "each bulb sees the full battery voltage regardless of how many others are connected, so "
                "brightness stays the same as you add more, and one bulb blowing doesn't affect the rest."
            )

# ---------------------------------------------------------------------------
# Everything below this line is OUTSIDE the if/else above (same indentation
# as "circuit_type = ..." near the top) — so it shows underneath BOTH views.
# ---------------------------------------------------------------------------

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