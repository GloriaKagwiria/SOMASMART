import streamlit as st
from utils.circuit_logic import get_reading_accuracy, get_practicals_attempted

st.title("📊 Physics Readiness Dashboard")
st.write(
    "Two different things make you ready for the Physics exam — how solid your theory is, "
    "and how comfortable you are actually taking readings in a practical. This page tracks both separately."
)

ALL_PRACTICALS = ["Series Circuit", "Parallel Circuit", "Resistance of a Wire", "Build Your Own Circuit"]


def percent_to_kcse_grade(pct):
    bands = [
        (80, "A"), (75, "A-"), (70, "B+"), (65, "B"), (60, "B-"),
        (55, "C+"), (50, "C"), (45, "C-"), (40, "D+"), (35, "D"),
        (30, "D-"), (0, "E"),
    ]
    for threshold, grade in bands:
        if pct >= threshold:
            return grade
    return "E"


# --- Theory Readiness ---------------------------------------------------
st.subheader("📘 Theory Readiness")
current_marks = st.number_input("Current average score in Physics (%)", min_value=0, max_value=100, value=65)
target_grade_percent = st.number_input("Target average score (%)", min_value=0, max_value=100, value=80)
remaining_assessments = st.number_input("Number of remaining assessments before the final exam", min_value=1, value=4)

if st.button("Calculate Theory Target"):
    total_points_needed = target_grade_percent * (remaining_assessments + 1)
    points_needed_per_assessment = (total_points_needed - current_marks) / remaining_assessments

    if points_needed_per_assessment > 100:
        st.error("This target may not be mathematically reachable in the remaining assessments — consider a smaller step-by-step goal.")
    else:
        st.success(f"You need to average **{points_needed_per_assessment:.1f}%** on each remaining assessment to hit your target.")
        target_letter = percent_to_kcse_grade(target_grade_percent)
        st.caption(f"Target of {target_grade_percent}% corresponds to roughly a **{target_letter}** on the KCSE scale.")

st.divider()

# --- Practical Skills Readiness -----------------------------------------
st.subheader("🔧 Practical Skills Readiness")
st.write(
    "This section fills in automatically from how you've used the Circuit Lab, Resistance of a Wire, "
    "and Build Your Own Circuit pages — there's nothing to type here yourself."
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