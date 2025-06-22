import streamlit as st
import pickle
import pandas as pd
import requests
import os

from dotenv import load_dotenv
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Set page configuration for a wider layout and custom theme
st.set_page_config(page_title="🎮 Movie Recommender", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for neon cyberpunk theme
st.markdown("""
    <style>
    .main {
        background-color: #0a0a23;
        color: #ffffff;
        font-family: 'Orbitron', sans-serif; /* Cyberpunk-style font */
    }
    .stButton>button {
        background-color: #00d4ff;
        color: #0a0a23;
        border-radius: 15px;
        font-weight: bold;
        padding: 12px 24px;
        border: 2px solid #ff00ff;
        box-shadow: 0 0 10px #00d4ff;
    }
    .stButton>button:hover {
        background-color: #ff00ff;
        color: #ffffff;
        box-shadow: 0 0 15px #ff00ff;
    }
    .stSelectbox {
        background-color: #1a1a3d;
        color: #00d4ff;
        border-radius: 10px;
        border: 2px solid #ff00ff;
    }
    .movie-card {
        background-color: #1a1a3d;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        transition: transform 0.2s;
    }
    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(255, 0, 255, 0.7);
    }
    .movie-title {
        color: #ff00ff;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 0 0 5px #ff00ff;
    }
    .movie-details {
        color: #00d4ff;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .poster {
        border-radius: 10px;
        width: 100%;
        height: auto;
        border: 2px solid #ff00ff;
    }
    h1 {
        color: #ffffff;
        text-align: center;
        font-size: 60px;
        margin-bottom: 20px;
        text-shadow: 0 0 10px #ffffff, 0 0 20px #ff00ff;
    }
    </style>
""", unsafe_allow_html=True)

# Load a cyberpunk-style header image (placeholder URL)
st.markdown("""
    <div style="background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'); 
                height: 200px; background-size: cover; background-position: center; border-radius: 15px; margin-bottom: 20px;">
        <h1>🎬 Movie Recommender System 🍿</h1>
    </div>
""", unsafe_allow_html=True)

# Sidebar for additional info
with st.sidebar:
    st.markdown("### 🚀 About This App")
    st.markdown("Dive into a futuristic movie recommendation experience! Powered by content-based filtering, this app suggests 5 movies based on your pick. 🌠")
    st.markdown("Created with 💿 by Sanawer Batool")
    st.markdown("---")
    st.markdown("### 🌌 Fun Fact")
    st.markdown("The first sci-fi movie, *A Trip to the Moon* (1902), was a groundbreaking 14-minute silent film! 🎥")

# Load data
try:
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
except FileNotFoundError:
    st.error("❌ Could not find 'movies_dict.pkl' or 'similarity.pkl'. Please ensure these files are in the project directory.")
    st.stop()

# Function to fetch movie posters, genres, and ratings with error handling
def fetch_movie_details(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US')
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            poster = "https://image.tmdb.org/t/p/w500" + data['poster_path']
        else:
            poster = "https://via.placeholder.com/500x750?text=No+Poster+Available"
        genres = ", ".join([g['name'] for g in data.get('genres', [])]) or "Unknown"
        rating = data.get('vote_average', 0.0)
        return poster, genres, rating
    except (requests.RequestException, KeyError, TypeError):
        return "https://via.placeholder.com/500x750?text=No+Poster+Available", "Unknown", 0.0

# Recommendation function
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies = []
        recommended_posters = []
        recommended_genres = []
        recommended_ratings = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            poster, genres, rating = fetch_movie_details(movie_id)
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(poster)
            recommended_genres.append(genres)
            recommended_ratings.append(rating)
        return recommended_movies, recommended_posters, recommended_genres, recommended_ratings
    except IndexError:
        st.error(f"❌ Movie '{movie}' not found in the dataset.")
        return [], [], [], []

# Main content
st.markdown("### 🎮 Pick Your Movie! 🌠")
selected_movie_name = st.selectbox(
    'Choose a movie to explore the cosmos of recommendations!',
    movies['title'].values,
    help="Select a movie to get 5 futuristic recommendations!"
)

if st.button('🚀 Recommend Now!'):
    with st.spinner('🎥 Fetching recommendations...'):
        names, posters, genres, ratings = recommend(selected_movie_name)
        if names and posters:
            st.success(f"🎉 Here are 5 movies similar to **{selected_movie_name}**! 🌟")
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.markdown(f"""
                        <div class="movie-card">
                            <div class="movie-title">{names[idx]}</div>
                            <img src="{posters[idx]}" class="poster">
                            <div class="movie-details">Genres: {genres[idx]}</div>
                            <div class="movie-details">Rating: {ratings[idx]:.1f}/10 ⭐</div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No recommendations available. Try another movie! 🌑")
