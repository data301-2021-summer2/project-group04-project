import pandas as pd

def load_and_process(url_or_path_to_csv_file):
    # Method Chain 1 (Load data and deal with missing data)
    df1 = (
        pd.read_csv(url_or_path_to_csv_file)
        .drop(['show_id', 'title', 'description'], axis = 1)
        .dropna(axis=0, how='any')
        .reset_index(drop=True)
    )
    # I won't rename first since it get harder for part 2 (with assign function)

    # Method Chain 2 (Create new columns, drop others, and do processing)
    df2 = (
        df1
        .assign(date_added=lambda x: pd.to_datetime(x['date_added']).dt.date)
        .assign(release_year=lambda x: pd.to_datetime(x['release_year'], format='%Y').dt.year)
        .assign(duration=lambda x: pd.to_numeric(x['duration'].str.split().apply(lambda x: x[0])))
        .assign(added_delay=lambda x: pd.to_datetime(x['date_added']).dt.year - x['release_year'])
        .assign(cast=lambda x: x['cast'].str.split(','))
        .assign(country=lambda x: x['country'].str.split(','))
        .assign(listed_in=lambda x: x['listed_in'].str.split(','))
        .rename(columns = {
            'type': 'Type',
            'director': 'Director',
            'cast': 'Cast',
            'country': 'Country',
            'date_added': 'Date Added',
            'release_year': 'Release Year',
            'rating': 'Rating',
            'duration': 'Duration',
            'listed_in': 'Genre',
            'added_delay': 'Added Delay',
        })
    )

    return df2