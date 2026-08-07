import streamlit as st

st.set_page_config(page_title="SomaSmart", page_icon="📘", layout="centered")

st.title("SomaSmart")
st.write("Welcome. Use the sidebar to navigate between Circuit Lab, Grade Predictor, and Feedback.")

from utils.db import get_visit_count
st.caption(f"👥 {get_visit_count()} students have used SomaSmart so far.")

import uuid
from utils.db import log_visit

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "counted_visit" not in st.session_state:
    log_visit("home")
    st.session_state.counted_visit = True