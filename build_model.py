import ast
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def safe_ast_eval(text):
    """Convert a string representation of a list into a Python list safely."""
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return []


def extract_names(items):
    """Extract the 'name' value from each item in a list of dictionaries."""
    return [item.get('name', '').replace(' ', '') for item in items if item.get('name')]


def get_genres(text):
    """Extract genre names from the genres column."""
    return extract_names(safe_ast_eval(text))


def get_keywords(text):
    """Extract keyword names from the keywords column."""
    return extract_names(safe_ast_eval(text))


def get_cast(text):
    """Extract up to 5 cast members from the cast column."""
    cast_data = safe_ast_eval(text)
    return [member.get('name', '').replace(' ', '') for member in cast_data[:5] if member.get('name')]


def get_director(text):
    """Extract the director name from the crew column for tag generation."""
    crew_data = safe_ast_eval(text)
    for member in crew_data:
        if member.get('job') == 'Director':
            return [member.get('name', '').replace(' ', '')]
    return []


def get_director_name(text):
    """Extract the director name from the crew column for storage."""
    crew_data = safe_ast_eval(text)
    for member in crew_data:
        if member.get('job') == 'Director':
            return member.get('name', '').strip()
    return ''


def create_tags(row):
    """Create a combined tag string from movie features."""
    genres = get_genres(row['genres'])
    keywords = get_keywords(row['keywords'])
    cast = get_cast(row['cast'])
    director = get_director(row['crew'])
    
    overview = str(row['overview']).split()
    
    tag_list = genres + keywords + cast + director + overview
    return ' '.join(tag_list).lower()


def load_data(movies_path, credits_path):
    """Load movie and credit data from CSV files."""
    movies_df = pd.read_csv(movies_path)
    credits_df = pd.read_csv(credits_path)
    return movies_df, credits_df


def preprocess_data(movies_df, credits_df):
    """Merge datasets and prepare the movie tags."""
    merged = movies_df.merge(credits_df, on='title')
    
    # --- MODIFIED: Step 1 (Removed 'poster_path') ---
    merged = merged[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

    merged.dropna(subset=['genres', 'keywords', 'cast', 'crew'], inplace=True)
    merged.reset_index(drop=True, inplace=True)

    merged['overview'] = merged['overview'].fillna('')
    merged['tags'] = merged.apply(create_tags, axis=1)
    merged['director'] = merged['crew'].apply(get_director_name)
    return merged


def build_similarity_matrix(movie_tags):
    """Convert text tags to vectors and compute cosine similarity."""
    vectorizer = CountVectorizer(max_features=5000, stop_words='english')
    vectors = vectorizer.fit_transform(movie_tags).toarray()
    return cosine_similarity(vectors)


def save_pickle(data, filename):
    """Save Python objects to a pickle file."""
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def main():
    movies_path = 'data/tmdb_5000_movies.csv'
    credits_path = 'data/tmdb_5000_credits.csv'

    print('Loading datasets...')
    movies_df, credits_df = load_data(movies_path, credits_path)

    print('Preprocessing movie metadata...')
    processed_movies = preprocess_data(movies_df, credits_df)

    print('Building similarity matrix...')
    similarity = build_similarity_matrix(processed_movies['tags'])

    print('Saving movies.pkl...')
    save_pickle(processed_movies[['movie_id', 'title', 'overview', 'tags', 'director']], 'movies.pkl')

    print('Saving similarity.pkl...')
    save_pickle(similarity, 'similarity.pkl')

    print('Finished generating pickle files.')


if __name__ == '__main__':
    main()