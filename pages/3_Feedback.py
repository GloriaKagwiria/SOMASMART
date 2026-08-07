import streamlit as st
from utils.db import save_feedback, get_feedback_stats

st.title("💬 Feedback")

with st.form("feedback_form"):
    name = st.text_input("Name (optional)")
    rating = st.slider("How helpful was this tool?", 1, 5, 3)
    comments = st.text_area("Comments")
    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        save_feedback(name, rating, comments)
        st.success("Thank you for your feedback!")

st.divider()
count, avg_rating = get_feedback_stats()
st.write(f"**Total users who've given feedback:** {count}")
if count:
    st.write(f"**Average rating:** {avg_rating:.1f} / 5")