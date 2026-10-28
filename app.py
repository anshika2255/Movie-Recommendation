import os
import pickle
from typing import Optional, Dict, Any

import requests
import streamlit as st
import json

def load_css():
    with open("styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

MOVIES_PICKLE = "movies.pkl"
SIMILARITY_PICKLE = "similarity.pkl"
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "").strip()
OMDB_API_KEY = "fd98524"

OMDB_BASE_URL = "https://www.omdbapi.com/"
PLACEHOLDER_POSTER = "https://via.placeholder.com/500x750?text=No+Poster+Available"
WATCHLIST_FILE = "watchlist.json"


def load_movie_data():
    """Load movie metadata and similarity matrix from pickle files."""
    with open(MOVIES_PICKLE, "rb") as file:
        movies = pickle.load(file)

    with open(SIMILARITY_PICKLE, "rb") as file:
        similarity = pickle.load(file)

    return movies, similarity


def extract_year(release_date: Optional[str]) -> Optional[str]:
    """Extract the release year from a date string."""
    if release_date and len(release_date) >= 4:
        return release_date[:4]
    return None


def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        try:
            with open(WATCHLIST_FILE, "r") as f:
                data = json.load(f)
                print("WATCHLIST LOADED:", data)
                return data
        except:
            return []
    return []


def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(watchlist, f)
    print("WATCHLIST SAVED:", watchlist)


def fetch_movie_metadata(title: str, fallback_row: Optional[dict] = None) -> Dict[str, Any]:
    """Return poster, rating, year, genres, and overview for a movie title."""
    info = {
        "title": title,
        "poster_url": PLACEHOLDER_POSTER,
        "rating": None,
        "runtime": None,
        "year": None,
        "genres": [],
        "overview": "",
    }

    if isinstance(fallback_row, dict):
        if fallback_row.get("overview"):
            info["overview"] = fallback_row.get("overview")
        if fallback_row.get("vote_average") is not None:
            info["rating"] = fallback_row.get("vote_average")
        if fallback_row.get("release_date"):
            info["year"] = extract_year(str(fallback_row.get("release_date")))
        if fallback_row.get("genres") and isinstance(fallback_row.get("genres"), list):
            info["genres"] = [str(g) for g in fallback_row.get("genres")][:3]
            
    try:    
        response = requests.get(
            OMDB_BASE_URL,
            params={
                "apikey": OMDB_API_KEY,
                "t": title
            },
            timeout=5
        )

        data = response.json()

        if data.get("Response") == "True":
            if data.get("Poster") and data.get("Poster") != "N/A":
                info["poster_url"] = data["Poster"]

            if data.get("imdbRating") and data["imdbRating"] != "N/A":
                info["rating"] = data["imdbRating"]

            if data.get("Year") and data["Year"] != "N/A":
                info["year"] = data["Year"]

            if data.get("Runtime") and data["Runtime"] != "N/A":
                info["runtime"] = data["Runtime"]

            if data.get("Genre") and data["Genre"] != "N/A":
                info["genres"] = data["Genre"].split(", ")[:3]

            if data.get("Plot") and data["Plot"] != "N/A":
                info["overview"] = data["Plot"]

    except Exception:
        pass

    return info


def recommend_movie(movie_name, movies, similarity_matrix):
    """Return the top 5 recommended movie rows for a selected movie."""
    if movie_name not in movies["title"].values:
        return []

    movie_index = movies[movies["title"] == movie_name].index[0]
    distances = list(enumerate(similarity_matrix[movie_index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in distances[1:6]:
        recommendations.append(movies.iloc[i[0]])
    return recommendations


def get_same_director_movies(selected_row, movies, max_results: int = 5):
    """Return up to max_results movies by the same director excluding the selected movie."""
    director = selected_row.get("director")
    if not director or "director" not in movies.columns:
        return []

    same_director = movies[
        (movies["director"] == director) &
        (movies["title"] != selected_row.get("title"))
    ]
    return [same_director.iloc[i] for i in range(min(max_results, len(same_director)))]


def render_movie_card(movie_row, show_watchlist_button=False, unique_key=""):
    """Render a card with poster, title, rating, year, genres, and overview."""
    try:
        row = movie_row.to_dict()
    except Exception:
        row = dict(movie_row)

    title = row.get("title", "Unknown")
    metadata = fetch_movie_metadata(title, fallback_row=row)

    st.image(metadata["poster_url"], width=180)
    
    # --- CHANGED BLOCK: Watchlist button is now verified on top of the title text ---
    if show_watchlist_button:
        if st.button("❤️", key=f"watch_{unique_key}"):
            if title not in st.session_state.watchlist:
                st.session_state.watchlist.append(title)
                save_watchlist(st.session_state.watchlist)
                st.toast(f"{title} added to Watchlist ❤️")
            else:
                st.toast("Movie already exists in Watchlist")

    st.markdown(f"### {title} {metadata.get('year') or ''}")
    # ---------------------------------------------------------------------------------

    if metadata.get("rating") is not None:
        st.markdown(f"⭐ **{metadata.get('rating')}/10**")
    if metadata.get("runtime"):
        st.markdown(f"⏱️ {metadata.get('runtime')}")
    if metadata.get("genres"):
        st.markdown(f"**Genres:** {', '.join(metadata.get('genres'))}")
    
    overview = metadata.get("overview", "")
    if overview:
      st.write(overview)


def main():
    st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
    load_css()

    st.markdown(
        """
        <h1 class="main-title">
            🎬 Movie Recommendation System
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p class="description">
            Discover movies similar to your favorites using AI-powered recommendations.
        </p>
        """,
        unsafe_allow_html=True
    )

   # if not TMDB_API_KEY:
       # st.warning("TMDB_API_KEY is not set. Poster images will use a placeholder image.")

    try:
        movies, similarity_matrix = load_movie_data()
    except FileNotFoundError:
        st.error("Pickle files are missing. Generate `movies.pkl` and `similarity.pkl` before running the app.")
        return

    if "title" not in movies.columns:
        st.error("The loaded movie file does not contain a title column.")
        return

    movie_titles = movies["title"].tolist()
    if not movie_titles:
        st.error("No movies were loaded from the pickle file.")
        return

    # Session State Initialization
    if "watchlist" not in st.session_state:
        st.session_state.watchlist = load_watchlist()
    if "show_watchlist" not in st.session_state:
        st.session_state.show_watchlist = False

    # Sidebar Construction
    with st.sidebar:
        st.header("Search & Controls")
        
        selected_movie = st.selectbox(
            "🎥 Choose a Movie",
            ["Select a movie..."] + movie_titles  
        )
        
        st.markdown("---")
        st.subheader("❤️ Watchlist")
        
        if st.button("View Watchlist"):
            st.session_state.show_watchlist = True
            st.rerun()

    # Watchlist Screen Display Logic
    if st.session_state.show_watchlist:
        st.title("❤️ My Watchlist")
        st.caption(f"{len(st.session_state.watchlist)} movies saved")

        if len(st.session_state.watchlist) == 0:
            st.info("Your watchlist is empty.")
        else:
            for movie in st.session_state.watchlist:
                col1, col2 = st.columns([8, 1])
                with col1:
                    st.markdown(f"**🎬 {movie}**")
                with col2:
                    if st.button("🗑️", key=f"remove_{movie}"):
                        st.session_state.watchlist.remove(movie)
                        save_watchlist(st.session_state.watchlist)
                        st.rerun()
                        
        st.markdown("---")
        
        if st.button("🏡 Close Watchlist"):
            st.session_state.show_watchlist = False
            st.rerun()
            
        return

    # Fallback structure validation for layout routine
    if selected_movie == "Select a movie...":
        st.info("🎬 Please select a movie from the sidebar to view details and recommendations.")
        return

    selected_row = movies[movies["title"] == selected_movie].iloc[0]

    # Home Layout view logic (Columns layout)
    left, right = st.columns([1, 2])

    with left:
       render_movie_card(selected_row, False, "main")

    with right:
        if st.button("❤️ Add to Watchlist"):
            if selected_movie not in st.session_state.watchlist:
                st.session_state.watchlist.append(selected_movie)
                save_watchlist(st.session_state.watchlist)
                st.toast(f"{selected_movie} added to Watchlist ❤️")
            else:
                 st.toast("Movie already in Watchlist")

        st.markdown("### Selected Movie Overview")
        st.write(selected_row.get("overview", "Overview not available."))

    st.markdown("---")
    st.markdown("## 🎯 Recommended Movies")

    with st.spinner("Generating recommendations..."):
        recommendations = recommend_movie(selected_movie, movies, similarity_matrix)

    if not recommendations:
        st.warning("No recommendations were found for this movie.")
        return

    for i in range(0, len(recommendations), 5):
        row_movies = recommendations[i : i + 5]
        cols = st.columns(len(row_movies))
    for j, (col, movie_row) in enumerate(zip(cols, row_movies)):
          with col:
            render_movie_card(movie_row, True, f"rec_{i}_{j}")

    st.markdown("---")
    st.subheader("More Movies by Same Director")
    same_director_movies = get_same_director_movies(selected_row, movies)
    
    if same_director_movies:
        for i in range(0, len(same_director_movies), 5):
            row_movies = same_director_movies[i : i + 5]
            cols = st.columns(len(row_movies))
            for j, (col, movie_row) in enumerate(zip(cols, row_movies)):
                   with col:
                       render_movie_card(movie_row, True, f"dir_{i}_{j}")
    else:
        st.info("No other movies by this director were found.")

    st.markdown("---")


if __name__ == "__main__":
    main()