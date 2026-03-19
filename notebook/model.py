import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load data
df = pd.read_csv("../data/movies.csv")

# Combine features
df["tags"] = df["overview"] + " " + df["genre"]

# Vectorize
tfidf = TfidfVectorizer(stop_words='english')
vectors = tfidf.fit_transform(df["tags"]).toarray()

# Similarity
similarity = cosine_similarity(vectors)

# Save
pickle.dump(similarity, open("../model/similarity.pkl", "wb"))
pickle.dump(df, open("../model/movie_list.pkl", "wb"))

print("Advanced model created successfully!")