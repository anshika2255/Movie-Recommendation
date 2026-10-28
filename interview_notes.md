# Interview Preparation Notes

## Project Explanation

This project is a content-based movie recommender. It uses metadata such as genres, cast, keywords, and director names to recommend similar movies. The main idea is to compare movie descriptions in a numeric space using text vectorization and cosine similarity.

## Working Flow

1. Load the TMDB movie and credits datasets.
2. Merge the datasets so each movie row contains cast and crew details.
3. Clean missing values and keep relevant columns.
4. Build text tags from genres, keywords, cast, and directors.
5. Use `CountVectorizer` to convert tags into numeric vectors.
6. Compute cosine similarity between all movie vectors.
7. Save the prepared movie data and similarity matrix.
8. In Streamlit, load pickle files and recommend the top 5 similar movies.

## Technology Justification

- Python: easy syntax and strong support for data projects.
- Pandas: reading CSV files and manipulating tables.
- NumPy: numerical arrays and matrix operations.
- Scikit-learn: vectorization and similarity calculations.
- Streamlit: quick web UI for beginner-friendly apps.
- Pickle: saving processed objects for fast app startup.

## Cosine Similarity Explanation

Cosine similarity measures the angle between two vectors. If two movie tag vectors point in the same direction, the cosine similarity is close to 1, which means the movies are very similar.

## CountVectorizer Explanation

`CountVectorizer` builds a vocabulary from text and counts how often each word appears. This turns movie tag text into numeric vectors that can be compared.

## Limitations of the System

- Only uses movie metadata, not user rating history.
- Can miss good recommendations when metadata is incomplete.
- Does not adapt to personal taste or watch history.
- Similar movies may be too generic if tags are broad.

## Future Improvements

- Add collaborative filtering based on user ratings.
- Use TF-IDF instead of raw counts for better weighting.
- Include plot summaries and reviews for deeper context.
- Add filters such as year, genre, or rating.
- Improve UI layout and mobile responsiveness.
