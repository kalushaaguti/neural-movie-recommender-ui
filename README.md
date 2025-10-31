# Neural Movie Recommender

A content-based movie recommendation system using neural sentence embeddings  
and FastAPI. Users input a movie title and receive similar movie suggestions  
based on semantic similarity (understanding the meaning of movie plots).

## Features
- Neural embeddings (Sentence Transformers)
- FastAPI backend API
- Cosine similarity recommendations
- Ready for deployment
- Can be upgraded to Streamlit UI or desktop app

## Project Structure
```
.
├── app.py                      # FastAPI backend
├── movies.csv                  # Movie metadata
├── indices.csv                 # Title → row index mapping
├── movie_embeddings.npy        # Neural embeddings
└── requirements.txt            # Dependencies
```

## How to Run Locally
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open your browser at:

```
http://127.0.0.1:8000/docs
```

## Roadmap
- Local backend working
- Deploy online
- Add posters using TMDB API
- Build Streamlit UI (Netflix style)
- Save user watch history

## Tech Stack
- Python
- FastAPI
- Scikit-Learn
- Sentence Transformers
- Uvicorn

## License
MIT License

---

## IMPORTANT
Don't delete or edit anything inside the ``` marks — they create code blocks.

---

### Now do this:

1. Replace your README file contents with the above
2. Save it
3. Run:

```bash
git add README.md
git commit -m "Clean README formatting"
git push
