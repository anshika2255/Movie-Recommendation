# Movie Recommendation System

A beginner-friendly content-based movie recommender built with Python, Pandas, NumPy, Scikit-learn, Streamlit, and Pickle.

## Project Overview

This project recommends movies based on similar genres, cast members, keywords, and directors. It uses `CountVectorizer` and `cosine_similarity` to convert movie metadata into feature vectors and compute similarity scores.

## Folder Structure

```
Movie-Recommender/
├── app.py
├── model.ipynb
├── movies.pkl
├── similarity.pkl
├── data/
│   └── (downloaded datasets go here)
├── assets/
│   └── .gitkeep
├── requirements.txt
└── README.md
```

## Installation Guide

1. Install Python 3.9 or higher.
2. Create a virtual environment:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Dataset Setup

1. Download the TMDB dataset files:
   - `tmdb_5000_movies.csv`
   - `tmdb_5000_credits.csv`

2. Place them in the `data/` folder.

## TMDB API Key (optional but recommended)

To display movie posters and richer metadata the app can query TMDB. Follow these steps to add your TMDB API key:

1. Create an account at https://www.themoviedb.org/ and get an API key from your account settings.
2. Locally, set an environment variable (Windows PowerShell example):

```powershell
setx TMDB_API_KEY "your_tmdb_api_key_here"
# Restart your terminal / editor after setting the variable
```

Alternatively, if you deploy on Streamlit Cloud add `TMDB_API_KEY` in the app's Secrets (Settings -> Secrets).

If the key is not provided the app will still run but will show placeholder poster images.

## Model Training and Pickle Generation

1. Open `model.ipynb` in Jupyter Notebook or VS Code.
2. Run each cell to preprocess the data, create tags, generate the cosine similarity matrix, and save `movies.pkl` and `similarity.pkl`.

## Run the Streamlit App

```bash
streamlit run app.py
```

Then open the provided local URL in your browser.

## Deployment Guide

### GitHub Deployment

1. Initialize a Git repository:

   ```bash
   git init
   git add .
   git commit -m "Initial movie recommender project"
   ```

2. Create a repository on GitHub.
3. Push the code to GitHub:

   ```bash
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

### Streamlit Cloud Deployment

1. Sign in to Streamlit Cloud.
2. Connect your GitHub repository.
3. Add `requirements.txt` and set the entry file to `app.py`.
4. Provide dataset files in the repository or load them dynamically with a public URL.

## Interview Preparation

### Project Explanation

This system is a content-based recommender. It learns from movie metadata instead of user ratings and recommends films that share similar content features.

### Working Flow

1. Load movie metadata.
2. Extract and clean features like genres, cast, keywords, and crew.
3. Create a combined text "tag" for each movie.
4. Use `CountVectorizer` to convert text tags into numeric vectors.
5. Compute cosine similarity between movie vectors.
6. Recommend the nearest movies.

### Technology Justification

- `Python`: easy to read and widely used in machine learning.
- `Pandas`: handles CSV files and manipulates data.
- `NumPy`: supports numeric arrays and vector operations.
- `Scikit-learn`: provides `CountVectorizer` and cosine similarity.
- `Streamlit`: builds a simple web UI quickly.
- `Pickle`: saves processed data for fast loading.

### Cosine Similarity Explanation

Cosine similarity measures how close two vectors are by comparing their direction. In this system, each movie becomes a vector and higher similarity means more related content.

### CountVectorizer Explanation

`CountVectorizer` converts text into a matrix of token counts. It turns movie tags into numbers that machine learning functions can work with.

### Limitations

- Recommendations are based only on movie metadata.
- It does not use user ratings or behavior.
- The system may struggle when metadata is sparse.

### Future Improvements

- Add user-based collaborative filtering.
- Use TF-IDF for better text weighting.
- Support more metadata such as reviews and release year.
- Add advanced UI features like filters and more movie details.
