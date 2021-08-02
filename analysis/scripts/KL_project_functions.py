import pandas as pd
def load_and_process(url_or_path_to_csv_file):
    df = (
    pd.read_csv(url_or_path_to_csv_file) #read data
    .dropna() #drop all null rows
    .drop('show_id', axis = 1) #delete show id column as not interested
    .reset_index(drop=True)
    .assign(date_added = lambda x: pd.to_datetime(x['date_added']).dt.date) #change to date data to compare later on
    .assign(cast = lambda x: x['cast'].str.split(', ')) #cast into array to compare
    .assign(country = lambda x: x['country'].str.split(', ')) #country into array to compare
    .assign(listed_in = lambda x: x['listed_in'].str.split(', ')) #genre into array to compare
    .rename(columns = {"type": "Type", "title": "Title", "director": "Director", "cast": "Cast", "country": "Country", "date_added": "Date Added", "release_year": "Release Year", "rating": "Rating", "duration": "Duration", "listed_in": "Genre", "description": "Desctiption"}) #rename columns
    )
    return df