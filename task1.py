from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load and preprocess data
# data = pd.read_csv('netflix_titles.csv', encoding='latin')
data = pd.read_csv(r'C:\Users\oscar\Desktop\machine learning\Recommendation system\netflix_titles.csv', encoding='latin')
data['description'] = data['description'].fillna('')
titles = data['title'].tolist()

# Compute TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['description'])

# Cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Recommendation function
def get_recommendations(title):
    idx = data[data['title'].str.lower() == title.lower()].index
    if len(idx) == 0:
        return None
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_indices = [i[0] for i in sim_scores[1:11]]
    return data['title'].iloc[sim_indices].tolist()

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    title = ""
    if request.method == 'POST':
        title = request.form['title']
        recommendations = get_recommendations(title)
    return render_template('index.html', recommendations=recommendations, title=title)

if __name__ == '__main__':
    app.run(debug=True)