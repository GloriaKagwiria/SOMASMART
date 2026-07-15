import streamlit as st
import json
import os
from datetime import datetime

st.title("💬 Feedback")

DATA_FILE = "data/feedback_data.json"

def load_feedback():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_feedback(entry):
    data = load_feedback()
    data.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

with st.form("feedback_form"):
    name = st.text_input("Name (optional)")
    rating = st.slider("How helpful was this tool?", 1, 5, 3)
    comments = st.text_area("Comments")
    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        entry = {
            "name": name if name else "Anonymous",
            "rating": rating,
            "comments": comments,
            "timestamp": datetime.now().isoformat(),
        }
        save_feedback(entry)
        st.success("Thank you for your feedback!")

st.divider()
all_feedback = load_feedback()
st.write(f"**Total users who've given feedback:** {len(all_feedback)}")
if all_feedback:
    avg_rating = sum(f["rating"] for f in all_feedback) / len(all_feedback)
    st.write(f"**Average rating:** {avg_rating:.1f} / 5")