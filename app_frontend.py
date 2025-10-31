import streamlit as st
import requests

st.title("🎬 Neural Movie Recommender")

movie_name = st.text_input("Enter a movie title:")

if st.button("Recommend"):
    if movie_name.strip() != "":
        url = "https://neural-movie-recommender.onrender.com/recommend" 
        params = {"title": movie_name}

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if "error" in data:
                st.error(data["error"])
            else:
                st.subheader(f"🎥 Recommendations for: **{movie_name}**")
                for movie in data["recommended_movies"]:
                    st.write(f"✅ {movie}")

        except Exception as e:
            st.error("🚨 Could not connect to backend API.")
