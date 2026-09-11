import streamlit as st
from utils.circuit_logic import get_reading_accuracy, get_practicals_attempted

st.title("📊 Practicals Readiness Dashboard")
st.write(
    "This page tracks how comfortable you are actually taking readings in a practical — "
    "built automatically from how you use Circuit Lab, Resistance of a Wire, and Build Your Own Circuit."
)

ALL_PRACTICALS = ["Series Circuit", "Parallel Circuit", "Resistance of a Wire", "Build Your Own Circuit"]

# --- Practical Skills Readiness -----------------------------------------
st.subheader("🔧 Practical Skills Readiness")
st.write(
    "This section fills in automatically from your activity on the other pages — "
    "there's nothing to type here yourself."
)

accuracy, attempt_count = get_reading_accuracy()
if accuracy is None:
    st.info("No meter readings checked yet. Try the Circuit Lab or Build Your Own Circuit page, then come back here.")
else:
    st.metric("Reading accuracy", f"{accuracy}%", help=f"Based on {attempt_count} checked readings so far this session.")

st.write("**Practicals attempted:**")
attempted = get_practicals_attempted()
for practical in ALL_PRACTICALS:
    if practical in attempted:
        st.write(f"✅ {practical}")
    else:
        st.write(f"⬜ {practical} — not tried yet")

st.divider()

# --- Pacing --------------------------------------------------------------
st.subheader("📅 Pacing")
weeks_to_exam = st.number_input("Weeks remaining until your KCSE exam", min_value=0, value=20)
if weeks_to_exam:
    st.caption(f"That's about {weeks_to_exam // 4} months away.")

st.divider()

# --- Summary --------------------------------------------------------------
st.subheader("Summary")
summary_parts = []

if accuracy is not None:
    if accuracy >= 70:
        summary_parts.append(f"Practical reading accuracy is strong at {accuracy}%.")
    else:
        summary_parts.append(f"Practical reading accuracy is {accuracy}% — more practice on Circuit Lab or Build Your Own Circuit would help.")
else:
    summary_parts.append("No practical reading data yet — try Circuit Lab or Build Your Own Circuit to start building this up.")

missing = [p for p in ALL_PRACTICALS if p not in attempted]
if missing:
    summary_parts.append(f"Not yet attempted: {', '.join(missing)}.")

st.info(" ".join(summary_parts))