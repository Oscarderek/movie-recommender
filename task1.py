from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String(200))
    recommended_title = db.Column(db.String(200))
    feedback = db.Column(db.String(10))

with app.app_context():
    db.create_all()

data = pd.read_csv(r'C:\Users\oscar\Desktop\machine learning\Recommendation system\netflix_movies_detailed_up_to_2025.csv', encoding='latin')
data['description'] = data['description'].fillna('')
titles = data['title'].tolist()

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['description'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

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

@app.route('/feedback', methods=['POST'])
def feedback():
    original = request.form['original_title']
    recommended = request.form['recommended_title']
    fb = request.form['feedback']

    new_feedback = Feedback(
        original_title=original,
        recommended_title=recommended,
        feedback=fb
    )
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({'message': 'Thank you for your feedback!'})

@app.route('/feedback_stats', methods=['POST'])
def feedback_stats():
    data = request.get_json()
    recommended_title = data.get('recommended_title')
    
    total = Feedback.query.filter_by(recommended_title=recommended_title).count()
    likes = Feedback.query.filter_by(recommended_title=recommended_title, feedback='like').count()

    if total == 0:
        percent_liked = None
    else:
        percent_liked = round((likes / total) * 100)

    return jsonify({'percent_liked': percent_liked})

if __name__ == '__main__':
    app.run(debug=True)