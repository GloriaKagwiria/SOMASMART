import streamlit as st
st.title("📊 Grade Predictor")

current_marks = st.number_input("Your current average score (%)", min_value=0, max_value=100, value=65)
target_grade_percent = st.number_input("Target average score (%)", min_value=0, max_value=100, value=80)
remaining_assessments = st.number_input("Number of remaining assessments before final exam", min_value=1, value=4)

if st.button("Calculate"):
    total_points_needed = target_grade_percent * (remaining_assessments + 1)
    # Assuming current_marks represents performance so far on a notional "1 unit" of assessment already done
    points_needed_per_assessment = (total_points_needed - current_marks) / remaining_assessments

    if points_needed_per_assessment > 100:
        st.error("This target may not be mathematically reachable in the remaining assessments — consider a smaller step-by-step goal.")
    else:
        st.success(f"You need to average **{points_needed_per_assessment:.1f}%** on each remaining assessment to hit your target.")