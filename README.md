# Movie-Recommender-system
I have built a filter-based Movie Recommendation system...

Domain: "https://movie-recommendations-model.streamlit.app/" has issues because the files that it needs are too big to upload on github

## Types of Recommendation system:

1. Content Based-[content similarity based] which recommends content based on content similarity, recommendations are made based on tags of the content(like listening songs on YT and getting recommendations)
2. Collaborative filtering based- [user similarity based] It recommends based on user’s interest(if we have 2 users(A, B) with same interest i.e., they like same kinds of movies, now next time if user A likes a movie we will recommend the same movie to user B )→ i.e., on Instagram if our friend liked a reel, it will suggest it to us
3. Hybrid- it combines both content based and collaborative filtering based approach

_____________________________

In this Movie Recommender system, I am going to use content based approach:

Project Flow: DATA → PREPROCESSING → ML MODEL → WEBSITE → DEPLOY
You will choose a movie and it will recommend you 5 movies based on your interest
I have used streamlit for frontend, bag of words for text vectorization using scikit-learn library, and to find similarities between movies I have used cosine similarity.
