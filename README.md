## Derek's Movie Recommender

A Flask-based movie recommendation system that suggests similar Netflix shows based on description similarity, and collects real-time user feedback (like/dislike).

## Features
- **Movie Recommendations** based on description similarity (TF-IDF + Cosine Similarity).
- **Like/Dislike Feedback** on each recommendation.
- Real-time feedback statistics displayed after voting.
- Feedback stored in a SQLite database using SQLAlchemy.
- Modern, responsive UI with Bootstrap 5 and Bootstrap Icons.
- Dynamic UI updates without page reloads (using fetch API + modals).

## How It Works
1. User enters a Netflix show title.
2. The app finds the top 10 most similar shows based on description similarity.
3. User can "like" or "dislike" each recommended show.
4. Feedback is saved in the database, and the "percent liked" is calculated and displayed in real-time.

## Tech Stack

| Technology         | Purpose                          |
|---------------------|----------------------------------|
| Python             | Backend Programming             |
| Flask              | Web Framework                   |
| SQLAlchemy         | ORM and Database Management     |
| SQLite             | Database                        |
| Pandas             | CSV File Handling               |
| scikit-learn       | TF-IDF + Cosine Similarity      |
| Bootstrap 5        | Frontend Styling                |
| Bootstrap Icons    | UI Icons                        |
| JavaScript (Fetch API) | Dynamic Updates              |
