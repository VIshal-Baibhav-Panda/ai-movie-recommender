import pickle
import pandas as pd

# Load data
movies = pickle.load(open("model/movie_list.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))

def recommend(movie):
    movie = movie.lower()

    # Find movie index
    try:
        index = movies[movies['title'].str.lower() == movie].index[0]
    except:
        return ["Movie not found"]

    distances = similarity[index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []
    for i in movie_list:
        recommendations.append(movies.iloc[i[0]].title)

    return recommendations