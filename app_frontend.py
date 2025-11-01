import time
import requests
import streamlit as st

API_BASE = "https://neural-movie-recommender.onrender.com"
RECOMMEND_URL = f"{API_BASE}/recommend"
PING_URL = f"{API_BASE}/docs"  # cheap warm-up endpoint

st.set_page_config(page_title="Neural Movie Recommender", page_icon="🎬")
st.title("🎬 Neural Movie Recommender")

# ------------- Helpers -------------
def ping_backend(timeout=10):
    """Warm the backend (Render free tier cold-start)."""
    try:
        requests.get(PING_URL, timeout=timeout)
        return True
    except Exception:
        return False

def get_with_retry(url, params=None, retries=4, base_delay=1.5, timeout=20):
    """
    Robust GET with exponential backoff.
    Retries on any exception or non-200 status.
    """
    last_err = None
    for i in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=timeout)
            if resp.status_code == 200:
                # Try to parse JSON; if fail, keep retrying
                try:
                    return resp.json()
                except Exception as e:
                    last_err = f"Invalid JSON: {e}\nResponse text: {resp.text[:300]}"
            else:
                last_err = f"HTTP {resp.status_code}: {resp.text[:300]}"
        except Exception as e:
            last_err = str(e)

        # Backoff then retry
        sleep_s = base_delay * (2 ** i)
        with st.spinner(f"API waking… retry {i+1}/{retries} in {sleep_s:.0f}s"):
            time.sleep(sleep_s)

    raise RuntimeError(last_err or "Unknown error")

# ------------- UI -------------
col1, col2 = st.columns([3,1])
with col2:
    if st.button("🌡️ Wake API"):
        with st.spinner("Pinging backend…"):
            ok = ping_backend(timeout=20)
        if ok:
            st.success("Backend is awake ✅")
        else:
            st.error("Could not reach backend. Try again in a few seconds.")

# Auto-warm on first load (per session)
if "warmed" not in st.session_state:
    st.session_state["warmed"] = ping_backend(timeout=10)

movie_name = st.text_input("Enter a movie title:")

if st.button("Recommend"):
    title = movie_name.strip()
    if not title:
        st.warning("Please enter a movie title.")
    else:
        # Ensure backend is alive before querying
        if not st.session_state.get("warmed", False):
            with st.spinner("Warming backend…"):
                st.session_state["warmed"] = ping_backend(timeout=20)

        with st.spinner("Fetching recommendations…"):
            try:
                data = get_with_retry(RECOMMEND_URL, params={"title": title}, retries=4, base_delay=1.5, timeout=20)
                # Expecting: {"input_title": "...", "recommendations": [{"title": "...", "overview": "..."}]}
                st.subheader(f"🎥 Recommendations for: **{title}**")
                if not data.get("recommendations"):
                    st.info("No recommendations found.")
                else:
                    for rec in data["recommendations"]:
                        t = rec.get("title", "Untitled")
                        ov = rec.get("overview") or ""
                        st.markdown(f"✅ **{t}**")
                        if ov:
                            st.caption(ov)
            except Exception as e:
                st.error("🚨 Could not connect to backend API.")
                st.caption(str(e))
