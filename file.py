import streamlit as st
import sqlite3
import pandas as pd

def get_data(query, params=None):
    conn = sqlite3.connect('movies_database.db')
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

st.title("Movie Chatbot")

question = st.text_input("Ask a question about movies:")

if question:
    
    if "how many movies" in question.lower() and "dataset" in question.lower():
        query = "SELECT COUNT(*) AS total_movies FROM movies"
        data = get_data(query)
        response = f"There are a total of {data['total_movies'][0]} movies in the dataset."

    elif "highest rating" in question.lower():
        query = "SELECT title, rating FROM movies ORDER BY rating DESC LIMIT 1"
        data = get_data(query)
        if not data.empty:
            response = f"The highest-rated movie is '{data['title'][0]}' with a rating of {data['rating'][0]}."
        else:
            response = "No data found."

    elif "lowest rating" in question.lower():
        query = "SELECT title, rating FROM movies ORDER BY rating ASC LIMIT 1"
        data = get_data(query)
        if not data.empty:
            response = f"The lowest-rated movie is '{data['title'][0]}' with a rating of {data['rating'][0]}."
        else:
            response = "No data found."

    elif "movies in" in question.lower():
        genre = question.lower().split("in")[-1].strip()  # Get the genre
        query = f"SELECT title FROM movies WHERE genre LIKE '%{genre}%'"
        data = get_data(query)
        if not data.empty:
            response = f"Movies in {genre}: {', '.join(data['title'])}."
        else:
            response = f"There are no movies found in the genre: {genre}."

    elif "average rating" in question.lower():
        query = "SELECT AVG(rating) AS average_rating FROM movies"
        data = get_data(query)
        if not data.empty:
            response = f"The average movie rating is {data['average_rating'][0]:.2f}."
        else:
            response = "No data found."

    elif "top" in question.lower() and "movies" in question.lower() and "votes" in question.lower():
        query = "SELECT title, votes FROM movies ORDER BY votes DESC LIMIT 5"
        data = get_data(query)
        if not data.empty:
            response = f"The top 5 movies by votes are: {', '.join(data['title'])}."
        else:
            response = "No data found."
    
    elif "list the movies name in" in question.lower():
        ch = question.lower().split("in")[-1].strip()
        query = "SELECT title FROM movies WHERE LOWER(title) LIKE ?"
        data = get_data(query, params=(f"{ch}%",))
        
        if not data.empty:
            response = f"Movies containing '{ch}': {', '.join(data['title'])}."
        else:
            response = f"There are no movies containing '{ch}' in the dataset."
    
    elif "highest votes" in question.lower():
        query = "SELECT title, votes FROM movies ORDER BY votes DESC LIMIT 1"
        data = get_data(query)
        if not data.empty:
            response = f"The movie with the highest votes is '{data['title'][0]}'."
        else:
            response = "No data found."

    elif "lowest votes" in question.lower():
        query = "SELECT title, votes FROM movies ORDER BY votes ASC LIMIT 1"
        data = get_data(query)
        if not data.empty:
            response = f"The movie with the lowest votes is '{data['title'][0]}'."
        else:
            response = "No data found."


    elif "description of" in question.lower():
        title = question.lower().split("of")[-1].strip() 
        query = "SELECT title, description FROM movies WHERE LOWER(title) = ?"
        data = get_data(query, params=(title,))
        
        if not data.empty:
            response = f"**Description of '{data['title'][0]}':** {data['description'][0]}"
        else:
            response = f"No description found for the movie titled '{title}'."

    elif "duration of" in question.lower():
        title = question.lower().split("of")[-1].strip()  # Extract movie title
        query = "SELECT title, duration FROM movies WHERE LOWER(title) = ?"
        data = get_data(query, params=(title,))
        
        if not data.empty:
            response = f"The duration of '{data['title'][0]}' is {data['duration'][0]} minutes."
        else:
            response = f"No data found for the movie: {title}."
    
    elif "stars of" in question.lower():
        title = question.lower().split("of")[-1].strip()  # Extract the movie title
        query = "SELECT stars FROM movies WHERE LOWER(title) = ?"
        data = get_data(query, params=(title.lower(),))

        if not data.empty:
            response = f"The stars of '{title}' are: {data['stars'][0]}."
        else:
            response = f"No stars found for the movie '{title}'."

    else:
        response = "I'm sorry, I can't answer that question. Please ask something else."

    
    st.write(response)


