import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sample_movies = pd.DataFrame([
    {'movie_id': 1, 'title': 'The Matrix', 'overview': 'A hacker discovers reality is a simulation.', 'poster_path': '/dXNAPwY7VrqMAo51EKhhCJfaGb5.jpg', 'tags': 'sci-fi action keanu reeves laurence fishburne wachowski'},
    {'movie_id': 2, 'title': 'Inception', 'overview': 'A thief who steals corporate secrets through dream-sharing technology.', 'poster_path': '/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg', 'tags': 'sci-fi thriller leonardo dicaprio christopher nolan'},
    {'movie_id': 3, 'title': 'Interstellar', 'overview': 'A team travels through a wormhole in space.', 'poster_path': '/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg', 'tags': 'sci-fi drama matthew mcconaughey christopher nolan'},
    {'movie_id': 4, 'title': 'The Dark Knight', 'overview': 'Batman faces the Joker in Gotham City.', 'poster_path': '/qJ2tW6WMUDux911r6m7haRef0WH.jpg', 'tags': 'action thriller christian bale christopher nolan'},
    {'movie_id': 5, 'title': 'Toy Story', 'overview': 'A story of toys that come to life.', 'poster_path': '/rhIRbceoE9lR4veEXuwCC2wARtG.jpg', 'tags': 'animation family tom hanks john lasseter'}
])

vectorizer = CountVectorizer(max_features=5000, stop_words='english')
vectors = vectorizer.fit_transform(sample_movies['tags']).toarray()
similarity = cosine_similarity(vectors)

with open('movies.pkl', 'wb') as f:
    pickle.dump(sample_movies[['movie_id', 'title', 'overview', 'poster_path', 'tags']], f)

with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity, f)

print('Sample pickles created successfully.')
