import streamlit as st
from supabase import create_client

@st.cache_resource
def get_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def save_feedback(name, rating, comments):
    get_client().table("feedback").insert({
        "name": name or "Anonymous",
        "rating": rating,
        "comments": comments,
    }).execute()

def get_feedback_stats():
    res = get_client().table("feedback").select("rating").execute()
    ratings = [row["rating"] for row in res.data]
    count = len(ratings)
    avg = sum(ratings) / count if count else 0
    return count, avg

def log_visit(page):
    get_client().table("app_visits").insert({
        "session_id": st.session_state.get("session_id", "unknown"),
        "page": page,
    }).execute()

def get_visit_count():
    res = get_client().table("app_visits").select("session_id").execute()
    return len({row["session_id"] for row in res.data})
