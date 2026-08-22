import matplotlib
matplotlib.use("Agg")
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
from utils.circuit_logic import (
    general_series_calc,
    general_parallel_calc,
    draw_analog_meter,
    nice_max_scale,
)


def render_bulb(label, current, max_current=5):
    brightness = min(current / max_current, 1.0)
    opacity = 0.25 + 0.75 * brightness
    size = 40 + 40 * brightness
    st.markdown(
        f"<div style='text-align:center'>"
        f"<span style='font-size:{size}px; opacity:{opacity:.2f};'>💡</span>"
        f"<div>{label}: {current:.2f} A</div></div>",
        unsafe_allow_html=True,
    )


def draw_general_series(voltage, components, include_ammeter, include_galvanometer, probe_index):
    d = schemdraw.Drawing()
    d += (batt := elm.Battery().up().label(f"{voltage}V"))
    d += elm.Line().right().length(1)
    if include_ammeter:
        d += elm.MeterI().right().label("A")
    if include_galvanometer:
        d += elm.MeterAnalog().right().label("G")

    comp_elements = []
    for i, comp in enumerate(components):
        label = f"L{i+1}" if comp["type"] == "Bulb" else f"R{i+1}={comp['value']}Ω"
        elem_cls = elm.Lamp if comp["type"] == "Bulb" else elm.Resistor
        d += (e := elem_cls().right().label(label))
        comp_elements.append(e)

    d += elm.Line().down().length(1)
    d += elm.Line().to(batt.start)

    # Voltmeter drawn as a real branch across the probed component
    probe = comp_elements[probe_index]
    d += elm.Line().at(probe.start).up().length(1.3)
    d += elm.MeterV().right().tox(probe.end).label("V")
    d += elm.Line().down().toy(probe.end)

    return d.draw(show=False)


def draw_general_parallel(voltage, components, include_ammeter, include_galvanometer, probe_index):
    d = schemdraw.Drawing()
    d += (batt := elm.Battery().up().label(f"{voltage}V"))
    d += elm.Line().right().length(1)
    if include_ammeter:
        d += elm.MeterI().right().label("A")
    if include_galvanometer:
        d += elm.MeterAnalog().right().label("G")

    n = len(components)
    comp_elements = []
    for i, comp in enumerate(components):
        is_last = (i == n - 1)
        label = f"L{i+1}" if comp["type"] == "Bulb" else f"R{i+1}={comp['value']}Ω"
        elem_cls = elm.Lamp if comp["type"] == "Bulb" else elm.Resistor

        if not is_last:
            d.push()
            d += (e := elem_cls().down().label(label))
            d.pop()
            d += elm.Line().right().length(2)
        else:
            d += (e := elem_cls().down().label(label))
        comp_elements.append(e)

    d += elm.Line().left().tox(batt.start)

    probe = comp_elements[probe_index]
    d += elm.Line().at(probe.start).right().length(1.3)
    d += elm.MeterV().down().toy(probe.end).label("V")
    d += elm.Line().left().tox(probe.end)

    return d.draw(show=False)


st.title("🛠️ Build Your Own Circuit")
st.write(
    "Choose how many components you want, what each one is, and how they're arranged — "
    "then read the meters yourself and record what you find, just like designing your own practical."
)

arrangement = st.selectbox("Arrangement", ["Series", "Parallel"])
num_components = st.slider("How many components?", 1, 4, 2)
if num_components == 1 and arrangement == "Parallel":
    st.caption("With only one component, series and parallel are the same circuit — there's nothing to branch.")

st.subheader("Meters to include")
mcol1, mcol2 = st.columns(2)
include_ammeter = mcol1.checkbox("Ammeter (main circuit)", value=True)
include_galvanometer = mcol2.checkbox("Galvanometer (main circuit)", value=False)
st.caption(
    "A voltmeter is always included below, placed across whichever component you choose — "
    "that's how voltmeters are actually connected in a real circuit, unlike an ammeter or "
    "galvanometer, which sit directly in the main loop."
)

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

probe_index = st.selectbox(
    "Where would you like to place the voltmeter?",
    options=list(range(num_components)),
    format_func=lambda i: f"Across Component {i+1} ({components[i]['type']})",
)

# --- Draw the circuit ---
if arrangement == "Series" or num_components == 1:
    fig = draw_general_series(voltage, components, include_ammeter, include_galvanometer, probe_index)
else:
    fig = draw_general_parallel(voltage, components, include_ammeter, include_galvanometer, probe_index)
st.pyplot(fig.fig)

# --- Compute values ---
resistances = [c["value"] for c in components]
if arrangement == "Series" or num_components == 1:
    result = general_series_calc(voltage, resistances)
    main_current = result["current"]
    probe_voltage = result["voltages"][probe_index]
else:
    result = general_parallel_calc(voltage, resistances)
    main_current = result["total_current"]
    probe_voltage = voltage  # every branch sees full voltage in parallel

# --- Live meters, read directly off the dial ---
st.subheader("Read the meters")
gauge_cols = st.columns(sum([include_ammeter, include_galvanometer, True]))
col_i = 0
if include_ammeter:
    with gauge_cols[col_i]:
        st.pyplot(draw_analog_meter(main_current, nice_max_scale(main_current), label="Ammeter", unit="A"))
    col_i += 1
if include_galvanometer:
    with gauge_cols[col_i]:
        st.pyplot(draw_analog_meter(main_current, nice_max_scale(main_current), label="Galvanometer", unit="A"))
    col_i += 1
with gauge_cols[col_i]:
    st.pyplot(draw_analog_meter(probe_voltage, nice_max_scale(probe_voltage), label="Voltmeter", unit="V"))

for i, comp in enumerate(components):
    if comp["type"] == "Bulb":
        branch_current = main_current if (arrangement == "Series" or num_components == 1) else result["currents"][i]
        render_bulb(f"Bulb {i+1}", branch_current)

# --- Record readings ---
st.divider()
st.subheader("Record this reading")

if "circuit_readings" not in st.session_state:
    st.session_state.circuit_readings = []

rcol1, rcol2 = st.columns(2)
if rcol1.button("📏 Record this reading"):
    st.session_state.circuit_readings.append({
        "Reading #": len(st.session_state.circuit_readings) + 1,
        "Arrangement": arrangement,
        "Voltage (V)": voltage,
        "Main Current (A)": round(main_current, 3),
        "Probed Component": f"Component {probe_index+1}",
        "Voltmeter Reading (V)": round(probe_voltage, 3),
    })
if rcol2.button("🗑️ Clear all readings"):
    st.session_state.circuit_readings = []

if st.session_state.circuit_readings:
    st.table(st.session_state.circuit_readings)

    if len(st.session_state.circuit_readings) >= 2:
        st.subheader("Plot a graph")
        axis_options = ["Reading #", "Voltage (V)", "Main Current (A)", "Voltmeter Reading (V)"]
        gcol1, gcol2 = st.columns(2)
        x_axis = gcol1.selectbox("X-axis", axis_options, index=1)
        y_axis = gcol2.selectbox("Y-axis", axis_options, index=2)

        if x_axis == y_axis:
            st.warning("Pick two different quantities so there's something to compare.")
        else:
            x_vals = [r[x_axis] for r in st.session_state.circuit_readings]
            y_vals = [r[y_axis] for r in st.session_state.circuit_readings]
            graph_fig, ax = plt.subplots()
            ax.scatter(x_vals, y_vals, color="tab:blue")
            if len(set(x_vals)) > 1:
                gradient, intercept = np.polyfit(x_vals, y_vals, 1)
                x_line = np.linspace(min(x_vals), max(x_vals), 50)
                ax.plot(x_line, gradient * x_line + intercept, color="tab:red", linestyle="--")
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"{y_axis} vs {x_axis}")
            st.pyplot(graph_fig)
    else:
        st.caption("Record at least one more reading (try changing the voltage or a component value first) to see a graph.")
else:
    st.caption("No readings yet — click **Record this reading** to start building your data set.")

st.caption(
    "Note: bulbs here are modeled as a fixed resistance, same as a resistor — good enough for "
    "comparing brightness and current at this level, not a physically exact lamp model."
)
