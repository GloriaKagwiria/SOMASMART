import matplotlib
matplotlib.use("Agg")
import streamlit as st
import schemdraw
import schemdraw.elements as elm
from utils.circuit_logic import general_series_calc, general_parallel_calc


def render_bulb(label, current, max_current=5):
    """Draws a simple bulb icon whose size/brightness scales with current."""
    brightness = min(current / max_current, 1.0)
    opacity = 0.25 + 0.75 * brightness
    size = 40 + 40 * brightness
    st.markdown(
        f"<div style='text-align:center'>"
        f"<span style='font-size:{size}px; opacity:{opacity:.2f};'>💡</span>"
        f"<div>{label}: {current:.2f} A</div></div>",
        unsafe_allow_html=True,
    )


def draw_general_series(voltage, components, meter_type):
    d = schemdraw.Drawing()
    d += (batt := elm.Battery().up().label(f"{voltage}V"))
    d += elm.Line().right().length(1)
    if meter_type == "Ammeter":
        d += elm.MeterI().right().label("A")
    else:
        d += elm.MeterAnalog().right().label("G")
    for i, comp in enumerate(components):
        label = f"L{i+1}" if comp["type"] == "Bulb" else f"R{i+1}={comp['value']}Ω"
        elem_cls = elm.Lamp if comp["type"] == "Bulb" else elm.Resistor
        d += elem_cls().right().label(label)
    d += elm.Line().down().length(1)
    d += elm.Line().to(batt.start)
    return d.draw(show=False)


def draw_general_parallel(voltage, components, meter_type):
    d = schemdraw.Drawing()
    d += (batt := elm.Battery().up().label(f"{voltage}V"))
    d += elm.Line().right().length(1)
    if meter_type == "Ammeter":
        d += elm.MeterI().right().label("A")
    else:
        d += elm.MeterAnalog().right().label("G")

    n = len(components)
    for i, comp in enumerate(components):
        is_last = (i == n - 1)
        label = f"L{i+1}" if comp["type"] == "Bulb" else f"R{i+1}={comp['value']}Ω"
        elem_cls = elm.Lamp if comp["type"] == "Bulb" else elm.Resistor

        if not is_last:
            d.push()
            d += elem_cls().down().label(label)
            d.pop()
            d += elm.Line().right().length(2)
        else:
            d += elem_cls().down().label(label)

    d += elm.Line().left().tox(batt.start)
    return d.draw(show=False)


st.title("🛠️ Build Your Own Circuit")
st.write(
    "Choose how many components you want, what each one is, and how they're arranged — "
    "then take readings, just like designing your own practical."
)

arrangement = st.selectbox("Arrangement", ["Series", "Parallel"])
meter_type = st.radio("Meter in the main circuit", ["Ammeter", "Galvanometer"], horizontal=True,
    help="Both read current the same way here — a galvanometer is just the more sensitive, "
         "analog-style meter used for very small currents in real labs.")
num_components = st.slider("How many components?", 2, 4, 2)

st.subheader("Set up each component")
components = []
cols = st.columns(num_components)
for i, col in enumerate(cols):
    with col:
        st.markdown(f"**Component {i+1}**")
        comp_type = st.selectbox("Type", ["Resistor", "Bulb"], key=f"type_{i}")
        comp_value = st.slider("Ω", 1, 100, 4 + i * 2, key=f"value_{i}")
        components.append({"type": comp_type, "value": comp_value})

voltage = st.slider("Battery Voltage (V)", 1, 24, 12)

# --- Draw the circuit ---
if arrangement == "Series":
    fig = draw_general_series(voltage, components, meter_type)
else:
    fig = draw_general_parallel(voltage, components, meter_type)
st.pyplot(fig.fig)

# --- Compute values ---
resistances = [c["value"] for c in components]
if arrangement == "Series":
    result = general_series_calc(voltage, resistances)
else:
    result = general_parallel_calc(voltage, resistances)

st.subheader("Take a reading")
probe_index = st.selectbox(
    "Where would you place a voltmeter?",
    options=list(range(len(components))),
    format_func=lambda i: f"Across Component {i+1} ({components[i]['type']})",
)

if st.button("Read meters"):
    if arrangement == "Series":
        st.success(f"Main circuit current ({meter_type}): **{result['current']:.2f} A**")
        st.info(f"Voltmeter across Component {probe_index+1}: **{result['voltages'][probe_index]:.2f} V**")
        for i, comp in enumerate(components):
            if comp["type"] == "Bulb":
                render_bulb(f"Bulb {i+1}", result["current"])
    else:
        st.success(f"Main circuit total current ({meter_type}): **{result['total_current']:.2f} A**")
        branch_voltage = voltage  # every branch sees full voltage in parallel
        st.info(f"Voltmeter across Component {probe_index+1}: **{branch_voltage:.2f} V** (same as the battery — that's the defining feature of parallel)")
        for i, comp in enumerate(components):
            if comp["type"] == "Bulb":
                render_bulb(f"Bulb {i+1}", result["currents"][i])

    st.caption(
        "Note: bulbs here are modeled as a fixed resistance, same as a resistor — good enough for "
        "comparing brightness and current at this level, not a physically exact lamp model."
    )
