import pandas as pd
import sqlite3

df = pd.read_csv('n_movies.csv')


conn = sqlite3.connect('movies_database.db')

df.to_sql('movies', conn, if_exists='replace', index=False)


conn.close()

print("Database created successfully.")


