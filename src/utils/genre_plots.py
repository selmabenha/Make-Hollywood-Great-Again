import plotly.graph_objects as go
import random
import pandas as pd

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

def create_genre_revenue_plots(df_genre,genre_col, domestic_col, foreign_col):

    fig1 = px.box(
        df_genre,
        x=genre_col,
        y=domestic_col,
        color=genre_col,
        title='Distribution of Domestic Revenue by Genre',
        labels={domestic_col: 'Domestic Revenue (USD)'}
    )
    fig1.update_layout(
        width=700,
        height=800,
        yaxis_range=[0, 1.25e9],
        title_x=0.5
    )

    fig2 = px.box(
        df_genre,
        x=genre_col,
        y=foreign_col,
        color=genre_col,
        title='Distribution of Foreign Revenue by Genre',
        labels={foreign_col: 'Foreign Revenue (USD)'}
    )
    fig2.update_layout(
        width=700,
        height=800,
        yaxis_range=[0, 1.25e9],
        title_x=0.5
    )

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=('Domestic Revenue by Genre', 'Foreign Revenue by Genre')
    )

    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)

    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)

    fig.update_layout(
        width=1400,
        height=800,
        title_text='Revenue Distribution by Genre',
        title_x=0.5,
        showlegend=False
    )

    return fig


def create_stacked_genre_bar_chart(df_genre_domestic, df_genre_foreign):
    domestic_counts = df_genre_domestic.groupby('Genres').size().reset_index(name='count').sort_values(by='count', ascending=False)
    foreign_counts = df_genre_foreign.groupby('Genres').size().reset_index(name='count').sort_values(by='count', ascending=False)


    fig = go.Figure()
    for index, row in domestic_counts.iterrows():
        fig.add_trace(
            go.Bar(
                name=row['Genres'],
                x=['Movies with domestic % > 50%'],  # Single bar category for domestic
                y=[row['count']],
                hoverinfo='y'
            )
        )

    for index, row in foreign_counts.iterrows():
        fig.add_trace(
            go.Bar(
                name=row['Genres'],
                x=['Movies with foreign % > 50%'],  # Single bar category for foreign
                y=[row['count']],
                hoverinfo='y'
            )
        )

    fig.update_layout(
        barmode='stack',
        title='Stacked Bar Chart of Movies by Genre',
        xaxis_title='Category',
        yaxis_title='Count of Movies',
        legend_title='Genres',
        showlegend=True
    )

    fig.show()


def create_gernre_proportion_plot(df_genre,df_genre_domestic, df_genre_foreign):
    domestic_counts = df_genre_domestic.groupby('Genres').size().reset_index(name='count')
    foreign_counts = df_genre_foreign.groupby('Genres').size().reset_index(name='count')

    # Normalize counts to proportions
    domestic_counts['proportion'] = domestic_counts['count'] / domestic_counts['count'].sum()
    foreign_counts['proportion'] = foreign_counts['count'] / foreign_counts['count'].sum()

    # Function to generate a random RGB color
    def generate_random_color():
        r = random.randint(0, 255)  # Random value for red (0-255)
        g = random.randint(0, 255)  # Random value for green (0-255)
        b = random.randint(0, 255)  # Random value for blue (0-255)
        return f"rgb({r}, {g}, {b})"

    genre_colors = {genre: generate_random_color() for genre in df_genre['Genres'].unique()}

    # Sort the counts by proportion in ascending order
    domestic_counts_sorted = domestic_counts.sort_values('proportion', ascending=True)
    foreign_counts_sorted = foreign_counts.sort_values('proportion', ascending=True)

    # Create a figure
    fig2 = go.Figure()

    # Add each genre for Domestic Movies as a segment in the stacked bar
    for index, row in domestic_counts_sorted.iterrows():
        fig2.add_trace(
            go.Bar(
                name=row['Genres'],
                x=['Movies with domestic % > 50%'],  # Single bar category for domestic
                y=[row['proportion']],
                hoverinfo='y',
                marker_color=genre_colors[row['Genres']],
                showlegend=True  
            )
        )

    # Add each genre for Foreign Movies as a segment in the stacked bar
    for index, row in foreign_counts_sorted.iterrows():
        fig2.add_trace(
            go.Bar(
                name=row['Genres'],
                x=['Movies with foreign % > 50%'],  # Single bar category for foreign
                y=[row['proportion']],
                hoverinfo='y',
                marker_color=genre_colors[row['Genres']],
                showlegend=False  

            )
        )

    # Update layout to stack the bars and use consistent colors
    fig2.update_layout(
        barmode='stack',
        title={
            'text': 'Stacked Bar Chart of Movies by Genre (Proportional)',
            'x': 0.5,  # Centers the title
            'xanchor': 'center',  # Anchors the title at the center
        },
        xaxis_title='Category',
        yaxis_title='Proportion of Movies',
        legend_title='Genres',
        showlegend=True,
        bargap=0.5,  # Reduce gap between bars (default is 0.2)
        height=600,  # Increase the height of the plot to stretch vertically
        yaxis=dict(
            scaleanchor="x",
        ),
    )

    fig2.show()


def create_genre_gross_plot(df, df_genre): 

    genre_gross = {genre: {'Domestic(USD)_Inflated': 0, 'Foreign(USD)_Inflated': 0} for genre in df_genre['Genres'].unique()}  # Dictionary to store the gross for each genre

    df_filtered_dom_for_gen = df[['Genres', 'Domestic(USD)_Inflated', 'Foreign(USD)_Inflated']]  # Keeping only the relevant columns


    # Iterating through the filtered dataset and summing gross for each genre
    for idx, row in df_filtered_dom_for_gen.iterrows():
        genres = str(row['Genres']).replace('/', ', ').split(', ')# Splitting the genres of the current movie ('/' and ', ' considered as separations)
        domestic = row['Domestic(USD)_Inflated']                          # Storing the corresponding Domestic(USD) value
        foreign = row['Foreign(USD)_Inflated']                            # Storing the corresponding Foreign(USD) value
        
        for genre in genres:
            # If the genre is in the top 20, we sum the gross to that genre
            if genre in df_genre['Genres'].unique():
                genre_gross[genre]['Domestic(USD)_Inflated'] += domestic
                genre_gross[genre]['Foreign(USD)_Inflated'] += foreign

    # Converting the dictionary into a DataFrame for plotting
    df_genre_gross = pd.DataFrame(genre_gross).T  # Transposing
    df_genre_gross = df_genre_gross[['Domestic(USD)_Inflated', 'Foreign(USD)_Inflated']]  # Keeping only the relevant columns for plotting

    df_genre_gross = df_genre_gross.rename(columns={'Domestic(USD)_Inflated': 'Domestic Revenue (USD)', 'Foreign(USD)_Inflated': 'Foreign Revenue (USD)'})

    fig_gross = px.bar(
        df_genre_gross,
        barmode = 'group',
        title = 'Domestic and Foreign Gross Revenue by Genre',
        labels={'value': 'Gross (USD)', 'variable': 'Revenue Type', 'index': 'Genre'}
    ) 
    fig_gross.update_layout(
        title_x=0.5
    )

    fig_gross.show()

    # Creating a new DataFrame excluding rows with NaN in the relevant columns so it doesn't affect the final plots
def create_genre_percentage_plot(df, df_genre):  
    df_percentage = df[['Genres', 'Domestic_Percentage', 'Foreign_Percentage']]

    # Initializing a dictionary to store mean percentages for each genre in the top 20
    genre_percentages = {genre: {'Domestic_Percentage': [], 'Foreign_Percentage': []} for genre in df_genre['Genres'].unique()}

    # Iterating through the filtered dataset and collecting percentages for each genre
    for idx, row in df_percentage.iterrows():
        genres = str(row['Genres']).replace('/', ', ').split(', ')# Splitting the genres of the current movie ('/' and ', ' considered as separations)
        Domestic_Percentage = row['Domestic_Percentage']          # Storing the corresponding Domestic_Percentage value
        Foreign_Percentage = row['Foreign_Percentage']            # Storing the corresponding Foreign_Percentage value
        
        for genre in genres:
            # If the genre is in the top 20, we collect the percentages for that genre
            if genre in df_genre['Genres'].unique():
                genre_percentages[genre]['Domestic_Percentage'].append(Domestic_Percentage)
                genre_percentages[genre]['Foreign_Percentage'].append(Foreign_Percentage)

    # Calculating the mean percentages for each genre
    mean_percentages = {
        genre: {
            'Domestic_Percentage': sum(values['Domestic_Percentage']) / len(values['Domestic_Percentage']),
            'Foreign_Percentage': sum(values['Foreign_Percentage']) / len(values['Foreign_Percentage']),
        }
        for genre, values in genre_percentages.items() if len(values['Domestic_Percentage']) > 0
    }

    df_genre_percentages = pd.DataFrame(mean_percentages).T 
    df_genre_percentages = df_genre_percentages[['Domestic_Percentage', 'Foreign_Percentage']] 

    df_genre_percentages = df_genre_percentages.rename(columns={'Domestic_Percentage': 'Domestic Revenue (%)', 'Foreign_Percentage': 'Foreign Revenue (%)'})

    fig_percentage = px.bar(
        df_genre_percentages,
        barmode='group',
        labels={'value': 'Percentage (%)', 'variable': 'Revenue Type', 'index': 'Genre'}
    )

    fig_percentage.update_layout(
        title='Mean Domestic and Foreign Revenue Percentage by Genre',
        title_x=0.5
    )

    fig_percentage.show()