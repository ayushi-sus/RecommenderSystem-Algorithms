import json
import pickle
import streamlit as st
from classifier import KNearestNeighbours
from operator import itemgetter
import requests
import pandas as pd

#from app1 import recommend

# Load data and movies list from corresponding JSON files
with open(r'data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open(r'titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)


def knn(test_point, k):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Distances to most distant movie
    max_dist = sorted(model.distances, key=itemgetter(0))[-1]
    # Print list of 10 recommendations < Change value of k for a different number >
    table = list()
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2]])
    return table


if __name__ == '__main__':
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']

    movies = [title[0] for title in movie_titles]
    st.header('Movie Recommendation System')
    apps = ['--Select--', 'Movie based', 'Genres based']
    app_options = st.selectbox('How do you want movie to be recommended? ', apps)


    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=e33390a56d934fd5336aeaca6feff9f4&language=en-US".format(
            movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path


    if app_options == 'Movie based':
        def fetch_poster(movie_id):
            url = "https://api.themoviedb.org/3/movie/{}?api_key=e33390a56d934fd5336aeaca6feff9f4&language=en-US".format(
                movie_id)
            data = requests.get(url)
            data = data.json()
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path


        def recommend(movie):
            movie_index = movies[movies['title'] == movie].index[0]
            distances = similarity[movie_index]
            movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

            recommended_movies_names = []
            recommended_movies_posters = []
            for i in movies_list:
                movie_id = movies.iloc[i[0]].movie_id
                recommended_movies_names.append(movies.iloc[i[0]].title)
                recommended_movies_posters.append(fetch_poster(movie_id))
            return recommended_movies_names, recommended_movies_posters


        # st.header('Movie Recommender System')

        movies_dict = pickle.load(open('movieD_list.pkl', 'rb'))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open('similarity.pkl', 'rb'))

        selected_movie_name = st.selectbox(
            'Select the movie',
            movies['title'].values
        )

        if st.button(' Show Recommendations '):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_movie_names[0])
                st.image(recommended_movie_posters[0])
            with col2:
                st.text(recommended_movie_names[1])
                st.image(recommended_movie_posters[1])

            with col3:
                st.text(recommended_movie_names[2])
                st.image(recommended_movie_posters[2])
            with col4:
                st.text(recommended_movie_names[3])
                st.image(recommended_movie_posters[3])
            with col5:
                st.text(recommended_movie_names[4])
                st.image(recommended_movie_posters[4])

        #movie_select = st.selectbox('Select movie:', ['--Select--'] + movies)
        # if movie_select == '--Select--':
        #     st.write('Select a movie')
        # else:
        #     n = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
        #     genres = data[movies.index(movie_select)]
        #     test_point = genres
        #     table = knn(test_point, n)
        #     for movie, link in table:
        #         # Displays movie title with link to imdb
        #         st.markdown(f"[{movie}]({link})")
    if app_options == apps[2]:
        options = st.multiselect('Select genres:', genres)
        if options:
            imdb_score = st.slider('IMDb score:', 1, 10, 8)
            n = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
            test_point = [1 if genre in options else 0 for genre in genres]
            test_point.append(imdb_score)
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")

        else:
            st.write("This is a simple Movie Recommender application. "
                     "You can select the genres and change the IMDb score.")

    else:
        st.write('Select')