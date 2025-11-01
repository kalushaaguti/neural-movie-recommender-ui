import streamlit as st
import requests

st.title("🎬 Neural Movie Recommender")

movie_name = st.text_input("Enter a movie title:")

if st.button("Recommend"):
    if movie_name.strip() != "":
        url = "https://neural-movie-recommender.onrender.com/recommend"
        params = {"title": movie_name}

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if response.status_code != 200:
                st.error(f"Backend error: {response.status_code}")
            
            else:
                st.subheader(f"🎥 Recommendations for: **{movie_name}**")
                for movie in data["recommendations"]:
                    st.write(f"✅ {movie['title']}")

        except Exception as e:
            st.error("🚨 Could not connect to backend API.")
            st.write(str(e))
