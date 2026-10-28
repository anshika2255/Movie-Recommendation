# Deployment Guide

## GitHub Deployment

1. Initialize a Git repository in the project folder:

```bash
cd Movie-Recommender
git init
git add .
git commit -m "Add movie recommendation system"
```

2. Create a repository on GitHub.
3. Add the remote URL and push:

```bash
git branch -M main
git remote add origin https://github.com/yourusername/movie-recommender.git
git push -u origin main
```

## Streamlit Cloud Deployment

1. Sign in to Streamlit Cloud.
2. Connect your GitHub account.
3. Choose the repository and set the entrypoint to `app.py`.
4. Add `requirements.txt`.
5. If you keep the pickle files in the repo, Streamlit Cloud will use them directly.

## Environment Variables

This project does not require environment variables for the sample app. If you add a TMDB API key for more advanced poster features, store it in Streamlit Cloud as `TMDB_API_KEY` and use `st.secrets` in `app.py`.
