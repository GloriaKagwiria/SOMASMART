import streamlit as st
import uuid
from utils.db import log_visit, get_visit_count

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "counted_visit" not in st.session_state:
    log_visit("home")
    st.session_state.counted_visit = True

st.caption(f"👥 {get_visit_count()} students have used SomaSmart so far.")
st.set_page_config(page_title="SomaSmart", page_icon="📘", layout="centered")

st.title("SomaSmart")
st.write("Welcome. Use the sidebar to navigate between Circuit Lab, Grade Predictor, and Feedback." 
         
"👋Hi, I'm the Circuit Lab." 

"I started building this after watching my sister meet her first real ammeter on the day of her KCSE practical exam — not before, not in a lesson, just once, when it counted most. That stuck with me. But this isn't only for students in her exact situation."

"It's for any student who wants to actually understand circuits — whether your school's lab is fully stocked, shared between too many classes, or doesn't exist at all. It's lightweight by design: no downloads, no fast internet required, works on a basic shared phone as easily as a laptop. If you've ever wanted to just *try* a circuit and see what happens, this is built for you too."

"Set values, build a circuit, take a real measurement, actually understand it."

"Here's hoping every curious hand finds its ammeter — early, and often, and just for the joy of it.")

from utils.db import get_visit_count
st.caption(f"👥 {get_visit_count()} students have used SomaSmart so far.")
