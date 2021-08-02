import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

plt.style.use('ggplot')
sns.set_palette('Set2')

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

def get_counted_list_genre(data):
    hash_map = dict()
    count = data.shape[0]
    for data_list in data:
        for data_item in data_list:
            data_item = data_item.strip()
            if data_item in hash_map:
                hash_map[data_item] += 1
            else:
                hash_map[data_item] = 1
    hash_map['Others'] = 0
    need_to_pop = []
    for k, v in hash_map.items():
        if v <= count * 0.1: # don't need to care about those who only accounted for less than 10%
            hash_map['Others'] += v
            need_to_pop.append(k)
    for k in need_to_pop:
        hash_map.pop(k)
    hash_map = dict(sorted(hash_map.items(), key=lambda item: item[1], reverse=True))
    
    values = list(hash_map.values())
    labels = list(hash_map.keys())
    
    return (labels, values)

def visualize_pair_grid(df):
    g = sns.PairGrid(df[['Type', 'Release Year', 'Added Delay', 'Duration']], hue='Type', height=5, aspect=1.2)
    g.map_upper(sns.scatterplot)
    g.map_lower(sns.kdeplot)
    g.map_diag(sns.kdeplot)
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle('RELEASE YEAR,YEAR BEFORE BEING ADDED, AND DURATION CORRELATION', fontsize = 20)
    g.add_legend(adjust_subtitles=True)
    plt.show()

def get_type_label_value(df, type):
    if type == 'TV Shows':
        tv_shows_genres = df[df['Type'] == 'TV Show']['Genre']
        return get_counted_list_genre(tv_shows_genres)
    elif type == 'Movies':
        movies_genres = df[df['Type'] == 'Movie']['Genre']
        return get_counted_list_genre(movies_genres)

def visualize_pie_chart_for_genres(df):
    movies_labels, movies_values = get_type_label_value(df, 'TV Shows')
    tv_shows_labels, tv_shows_values = get_type_label_value(df, 'Movies')

    fig = plt.figure(figsize = (15,8))
    ax1 = fig.add_subplot(1,2,1)
    ax1.pie(movies_values, autopct='%1.1f%%', pctdistance=.75)
    plt.legend(movies_labels,
               bbox_to_anchor=[0, 0, 1.05, 0],
               ncol=3,
               prop={'size': 9}
              )
    plt.title('Netflix Movies Genres', fontsize=20)

    ax2 = fig.add_subplot(1,2,2)
    ax2.pie(tv_shows_values, autopct='%1.1f%%', pctdistance=0.75)
    plt.legend(tv_shows_labels,
               bbox_to_anchor=[0, 0, 1.05, 0],
               ncol=3,
               prop={'size': 9}
              )
    plt.title('Netflix TV Show Genres', fontsize=20)

    plt.show()

def visualize_bar_chart_for_ratings(df):
    fig, ax = plt.subplots(figsize = (15,8))
    ax = sns.countplot(data=df, x='Rating', hue='Type', order=df['Rating'].value_counts().index)
    ax.legend(title='Type', fontsize=12, loc='upper right')
    ax.set_title('The Number Of Movies And TV Shows Of Each Rating', fontsize=20)
    plt.setp(ax.get_legend().get_title(), fontsize='14')
    ax.set(ylabel='Number Of Movies And TV Shows', xlabel='All Ratings')
    plt.show()

def visualize_bar_chart_for_directors(df):
    director_count = df['Director'].value_counts().iloc[:10]

    _, ax = plt.subplots(figsize = (15,8))
    ax = sns.countplot(data=df, y='Director', order=director_count.index).set(title='The Number Of Movies And TV Shows Of Each Director', xlabel='Number of movies and/or TV shows', ylabel='', xticks=list(range(director_count.min() - 1 if director_count.min() % 2 == 1 else director_count.min() - 2, director_count.max() + 1, 2)))
    plt.xlim(director_count.min() - 1 if director_count.min() % 2 == 1 else director_count.min() - 2, director_count.max() + 1)
    plt.show()

def get_casts_lists(df, n_rows):
    hash_map = dict()
    for casts in df['Cast']:
        for cast in casts:
            cast = cast.strip()
            if cast in hash_map:
                hash_map[cast] += 1
            else:
                hash_map[cast] = 1
    hash_map = dict(sorted(hash_map.items(), key=lambda item: item[1], reverse=True))
    return (list(hash_map.keys())[:n_rows], list(hash_map.values())[:n_rows])

def visualize_bar_chart_for_casts(df):
    casts, n_involved = get_casts_lists(df, 10)
    _, ax = plt.subplots(figsize = (15, 8))
    ax = sns.barplot(y = casts, x = n_involved).set(title='Top Netflix Casts',  xlabel='Number of movies and/or TV shows', xticks=list(range(min(n_involved) - 1 if min(n_involved) % 2 == 1 else min(n_involved) - 2, max(n_involved) + 1, 2)))
    plt.xlim(min(n_involved) - 1 if min(n_involved) % 2 == 1 else min(n_involved) - 2, max(n_involved) + 1)
    plt.show()

def get_durations_avg(df):  
    print('Average duration for a movie:', df[df['Type'] == 'Movie']['Duration'].mean(), 'minutes')
    print('Average duration for a tv show:', df[df['Type'] == 'TV Show']['Duration'].mean(), 'seasons')

def get_delay_date_avg(df):
    print('Delay time:', df['Added Delay'].mean(), 'years')

def get_date_year_description(df, year_start, year_end):
    if (year_end > df['Release Year'].max()):
        year_end = df['Release Year'].max()
    if (year_start < df['Release Year'].min()):
        year_start = df['Release Year'].min()
    for year in range(year_start, year_end):
        df['Added Delay'] = np.where(df['Added Delay'] < 0, 0, df['Added Delay'])
        print(year)
        display(df[df['Release Year'] == year]['Added Delay'].describe().T[['mean', 'max', 'min']].to_frame().T)