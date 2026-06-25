import numpy as np
import pandas as pd
import plotly.express as px
import scipy.stats as stats
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from sentence_transformers import SentenceTransformer, util
from collections import defaultdict
import seaborn as sns
from plotly.subplots import make_subplots
import plotly.express as px
from matplotlib import pyplot as plt

<<<<<<< HEAD
=======
import scipy.stats as stats
>>>>>>> 11cb7f5a46a2545ca456cbf2ad056364df88b847

# Generates the line plots for foreign percentage and domestic in function of the years
def generate_year_plot(df):
    average_percentages = df.groupby('Year')[['Foreign_Percentage', 'Domestic_Percentage']].mean()
    average_percentages = average_percentages.reset_index()
    average_percentages = average_percentages[(average_percentages['Year'] >= 2000) & (average_percentages['Year'] <= 2019)]
    average_percentages = average_percentages.rename(columns={'Foreign_Percentage':'Foreign Percentage', 'Domestic_Percentage':'Domestic Percentage'})

    fig = px.line(average_percentages, 
            x='Year', 
            y=['Domestic Percentage', 'Foreign Percentage'], 
            title='Average Percentages Over Time',
            labels={'value': 'Percentage', 'variable': 'Percentages'},
            width=1100,
            height=500
    )
    fig.update_layout(title=dict(text="Impact of Budget on Foreign Percentage", x=0.5, xanchor='center'))
    fig.show()


def create_box_plot(df, column, y_axis_title, title, log=False): 
    df['Foreign_higher'] = df.copy(deep=True)['Foreign_higher'].replace({
        0: "Domestic % > 50%",
        1: "Foreign % > 50%"
    })


    # Box plot grouped by Rating and Foreign_higher
    fig_box = px.box(df,
        x='Foreign_higher', 
        y=column,  
        color='Foreign_higher', 
        title="Box Plot for Two Classes",
        labels={'value': 'Percentage', 'variable': 'Type'},
        color_discrete_map={"Domestic % > 50%": "blue", "Foreign % > 50%": "red"},  # Customize colors
    )

    fig_box.update_layout(
        title={
            "text": f"Distribution of {title} by Class",
            "x": 0.5,  # Center the title
            "xanchor": "center",  # Anchor the title to the center
        },
        xaxis_title="Class",
        yaxis_title=y_axis_title,
        legend_title="Key",
        width=1100,  
        height=500
    )
    if log:
        fig_box.update_yaxes(
            type="log",
            tickvals=[1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9],  
            ticktext=["10", "100", "1k", "10k", "100k", "1M", "10M ", "100M", "1B"],  
            title_text=f"Log Scale of {y_axis_title}" 
        )
    return fig_box


# Grouped bar chart for counts of movies by Rating and Foreign_higher
def create_bar_plot(df, title, column): 
        
    fig_bar = px.histogram(
        df,
        x="Foreign_higher",
        color="Foreign_higher",  # Separate by Foreign_higher
        title=f"{title} by Class",
        color_discrete_map={"Domestic % > 50%": "blue", "Foreign % > 50%": "red"},  # Optional: Customize colors
    )

    # Update the layout of the bar chart
    fig_bar.update_layout(
        xaxis_title="Class",
        yaxis_title="Count of Movies",
        showlegend=False,  # Hide legend for the bar chart
        width=1100,  
        height=500,
        yaxis=dict(
            autorange="reversed",  # Flip the y-axis to make the bars go downward
        ),
    )
    return fig_bar

def fig_combined_plots(fig_box, fig_bar, title_name, log=False):
    # Create subplots: 2 rows, 1 column (vertical layout)
    fig_combined = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],  # More space for the box plot
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=["Class", ""],  # Empty title for second subplot
    )



    

    # Add all traces from the box plot to the first row
    for trace in fig_box['data']:
        fig_combined.add_trace(trace, row=1, col=1)

    # Add bar chart to the second row
    for trace in fig_bar['data']:
        fig_combined.add_trace(trace, row=2, col=1)

    # Update layout to center the title and maintain consistency in axis titles
        fig_combined.update_layout(
        title={
                "text": f"Distribution of Profitability and {title_name} by Class",
                "x": 0.5,
                "xanchor": "center"
        },
        boxmode="group",  # Group the box plots side-by-side
        yaxis=dict(
                title=title_name,
                type="log" if log else None,  # Log scale for the first plot if `log` is True
                tickvals=[1e-1, 1e0, 1e1, 1e2],  # Logarithmic scale tick values
                ticktext=["-1", "0", "1", "10"],
        ),


        showlegend=True,
        xaxis=dict(
            type="category",  # Categorical x-axis
            categoryorder="array",  # Explicitly set order to control spacing
            categoryarray=["Domestic % > 50%", "Foreign % > 50%"],  # Define category sequence
        ),
        yaxis2=dict(
            title="Count",
            autorange="reversed",  # Ensure count axis is reversed for downward bars
        ),

        margin=dict(t=50, b=80),  # Adjust top and bottom margins for proper spacing
        width=1100,
        height=500,
        annotations=[
            dict(
                y=-0.15,  # Position below the x-axis (outside the plot area)
                xref="paper",  # Reference paper (not data)
                yref="paper",
                showarrow=False,
                font=dict(size=14),
                align="center"
            )

        ]
    )
    return fig_combined


def plot_critics_score_distribution(data_domestic, data_foreign, bin_edges=None, output_path=None, save=False):
    if bin_edges is None:
        bin_edges = np.linspace(0, 1, 51)

    plt.figure(figsize=(10, 6))

    sns.histplot(data_domestic, 
                 bins=bin_edges, 
                 kde=True, 
                 color='blue', 
                 label='Movies with domestic % > 50%', 
                 alpha=0.5)

    sns.histplot(data_foreign, 
                 bins=bin_edges, 
                 kde=True, 
                 color='red', 
                 label='Movies with foreign % > 50%', 
                 alpha=0.5)

    plt.title('Distribution of Critics Score with KDE', fontsize=16)
    plt.xlabel('Critics Score', fontsize=14)
    plt.ylabel('Movie Count', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(axis='y', alpha=0.75)

    plt.tight_layout()

    if save:
        plt.savefig(output_path, format='png', dpi=300)

    plt.show()

def plot_audience_score_distribution(data_domestic, data_foreign, bin_edges=None, output_path=None, save=False):
    if bin_edges is None:
        bin_edges = np.linspace(0, 1, 51)

    plt.figure(figsize=(10, 6))

    sns.histplot(data_domestic, 
                 bins=bin_edges, 
                 kde=True, 
                 color='blue', 
                 label='Movies with domestic % > 50%', 
                 alpha=0.5)

    sns.histplot(data_foreign, 
                 bins=bin_edges, 
                 kde=True, 
                 color='red', 
                 label='Movies with foreign % > 50%', 
                 alpha=0.5)

    plt.title('Distribution of Audience Score with KDE', fontsize=16)
    plt.xlabel('Audience Score', fontsize=14)
    plt.ylabel('Movie Count', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(axis='y', alpha=0.75)

    plt.tight_layout()

    if save:
        plt.savefig(output_path, format='png', dpi=300)

    plt.show()


<<<<<<< HEAD
def plot_rating_profit_count(rating_df):
    ## box plot check the plots.. 

    fig_box = px.box(
        rating_df,
        x="Rating", 
        y="log_profit",
        color="Foreign_higher",  
        title="Distribution of Log Profitability by Rating",
        labels={"Foreign_higher": "Revenue Type", "log_profit": "Log of Profitability"},
        color_discrete_map={"Domestic % > 50%": "blue", "Foreign % > 50%": "red"}, 
        category_orders={"Foreign_higher": [0, 1]}, 
    )

=======
def plot_rating_profit_count(final_df):
    # Box plot grouped by Rating and Foreign_higher
    fig_box = px.box(
        final_df,
        x="Rating",  # Group by Rating on the x-axis
        y="log_profit",  # Box plot for revenue
        color="Foreign_higher",  # Differentiate by Foreign_higher
        title="Distribution of Log Profitability by Rating",
        labels={"Foreign_higher": "Revenue Type", "log_profit": "Log of Profitability"},
        color_discrete_map={"Domestic % > 50%": "blue", "Foreign % > 50%": "red"},  # Customize colors
        category_orders={"Foreign_higher": [0, 1]},  # Ensure 0 comes before 1
    )

    # Update the legend labels dynamically
>>>>>>> 11cb7f5a46a2545ca456cbf2ad056364df88b847
    fig_box.for_each_trace(
        lambda t: t.update(name="")
    )

    fig_box.update_layout(
        title={
            "text": "Distribution of Log Profitability by Rating",
<<<<<<< HEAD
            "x": 0.5,  
            "xanchor": "center",  
=======
            "x": 0.5,  # Center the title
            "xanchor": "center",  # Anchor the title to the center
>>>>>>> 11cb7f5a46a2545ca456cbf2ad056364df88b847
        },
        xaxis_title="Rating",
        yaxis_title="Log of Profitability",
        legend_title="Revenue Type",
<<<<<<< HEAD
        boxmode="group",  
    )

    fig_bar = px.histogram(
        rating_df,
        x="Rating",
        color="Foreign_higher",  
        barmode="group",  
        title="Count of Movies by Rating (Separated by Foreign Percentage)",
        color_discrete_map={"Domestic % > 50%": "blue", "Foreign % > 50%": "red"}, 
    )


=======
        boxmode="group",  # Ensures box plots are grouped side-by-side
    )

    # Grouped bar chart for counts of movies by Rating and Foreign_higher
    fig_bar = px.histogram(
        final_df,
        x="Rating",
        color="Foreign_higher",  # Separate by Foreign_higher
        barmode="group",  # Group the bars for comparison
        title="Count of Movies by Rating (Separated by Foreign Percentage)",
       color_discrete_map={"Domestic % > 50%": "blue", "Foreign % > 50%": "red"},  # Optional: Customize colors
    )

    # Update the legend labels dynamically
>>>>>>> 11cb7f5a46a2545ca456cbf2ad056364df88b847
    fig_bar.for_each_trace(
        lambda t: t.update(name="Movies with domestic % > 50%" if t.name == "0" else "Movies with foreign % > 50%")
    )

<<<<<<< HEAD
    fig_bar.update_layout(
        xaxis_title="Rating",
        yaxis_title="Count of Movies",
        showlegend=False, 
        yaxis=dict(
            autorange="reversed",  
        )
    )

    fig_combined = fig_combined_plots(fig_box, fig_bar, "Movie Counts", log = False)
    return fig_combined


=======
    # Update the layout of the bar chart
    fig_bar.update_layout(
        xaxis_title="Rating",
        yaxis_title="Count of Movies",
        showlegend=False,  # Hide legend for the bar chart
        yaxis=dict(
            autorange="reversed",  # Flip the y-axis to make the bars go downward
        ),
    )

    # Create subplots: 2 rows, 1 column (vertical layout)
    fig_combined = make_subplots(
        rows=2, cols=1,
        row_heights=[0.8, 0.2],  # More space for the box plot
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=["Ratings", ""],  # Empty title for second subplot
    )

    # Add all traces from the box plot to the first row
    for trace in fig_box['data']:
        fig_combined.add_trace(trace, row=1, col=1)

    # Add bar chart to the second row
    for trace in fig_bar['data']:
        fig_combined.add_trace(trace, row=2, col=1)

    # Update layout to center the title and maintain consistency in axis titles
    fig_combined.update_layout(
        title={
            "text": "Distribution of Log Profitability and Movie Counts by Rating",
            "x": 0.5,
            "xanchor": "center"
        },
        boxmode="group",  # Group the box plots side-by-side
        yaxis_title="Log Profitability",
        showlegend=True,
        yaxis2=dict(
            title="Count",
            autorange="reversed",  # Ensure count axis is reversed for downward bars
        ),
        margin=dict(t=50, b=80),  # Adjust top and bottom margins for proper spacing
        width = 1100,
        height = 550,
        annotations=[
            dict(
                x=0.5,  # Position at the center
                y=-0.15,  # Position below the x-axis (outside the plot area)
                xref="paper",  # Reference paper (not data)
                yref="paper",
                showarrow=False,
                font=dict(size=14),
                align="center"
            )
        ]
    )

    return fig_combined





>>>>>>> 11cb7f5a46a2545ca456cbf2ad056364df88b847
def statistical_relevance_ratings(df):
    # 1. Shapiro-Wilk Test for Normality on log-transformed profitability
    shapiro_results = stats.shapiro(df["log_profit"])
    print(f"Shapiro-Wilk Test p-value: {shapiro_results.pvalue}")

    # If the p-value > 0.05, the data is likely normal, and we can proceed with ANOVA.

    # Filter data by Foreign_higher (0 and 1)
    df_domestic = df[df['Foreign_higher'] == 0]
    df_foreign = df[df['Foreign_higher'] == 1]

    # Perform the Kruskal-Wallis H test for each group if the data is not normal
    if shapiro_results.pvalue <= 0.05:
        print("Data is not normal, using Kruskal-Wallis H test.")

        # Kruskal-Wallis H Test for movies with Foreign_higher == 0 (Domestic movies)
        ratings_groups_domestic = [df_domestic[df_domestic['Rating'] == rating]["log_profit"] for rating in df_domestic['Rating'].unique() if rating != "G"]
        h_stat_domestic, p_value_kw_domestic = stats.kruskal(*ratings_groups_domestic)
        print(f"Kruskal-Wallis H Test (Domestic Movies) p-value: {p_value_kw_domestic}")

        # Kruskal-Wallis H Test for movies with Foreign_higher == 1 (Foreign movies)
        ratings_groups_foreign = [df_foreign[df_foreign['Rating'] == rating]["log_profit"] for rating in df_foreign['Rating'].unique() if rating != "G"]
        h_stat_foreign, p_value_kw_foreign = stats.kruskal(*ratings_groups_foreign)
        print(f"Kruskal-Wallis H Test (Foreign Movies) p-value: {p_value_kw_foreign}")

    else:
        print("Data is normal, you can use ANOVA.")

        # ANOVA test for comparing means if data is normal
        # Split the data based on ratings (exclude 'G' as per your earlier explanation)
        ratings_groups_domestic = [df_domestic[df_domestic['Rating'] == rating]["log_profit"] for rating in df_domestic['Rating'].unique() if rating != "G"]
        ratings_groups_foreign = [df_foreign[df_foreign['Rating'] == rating]["log_profit"] for rating in df_foreign['Rating'].unique() if rating != "G"]
        
        # Perform ANOVA for domestic movies
        f_stat_domestic, p_value_anova_domestic = stats.f_oneway(*ratings_groups_domestic)
        print(f"ANOVA p-value (Domestic Movies): {p_value_anova_domestic}")
        
        # Perform ANOVA for foreign movies
        f_stat_foreign, p_value_anova_foreign = stats.f_oneway(*ratings_groups_foreign)
<<<<<<< HEAD
        print(f"ANOVA p-value (Foreign Movies): {p_value_anova_foreign}")

def plot_emotion_pie(df):
    # Define a custom color map for emotions
    color_map = {
        'anger': 'red',
        'sadness': 'blue',
        'joy': 'gold',
        'disgust': 'green',
        'neutral': 'brown',
        'surprise': 'hotpink',
        'fear': 'purple'
    }

    # Separate data for each group
    domestic_counts = df[df['Foreign_higher'] == 0]['emotion'].value_counts().reset_index()
    domestic_counts.columns = ['emotion', 'Counts']

    foreign_counts = df[df['Foreign_higher'] == 1]['emotion'].value_counts().reset_index()
    foreign_counts.columns = ['emotion', 'Counts']

    # Create a subplot figure with two pie charts
    fig2 = make_subplots(
        rows=1, cols=2, 
        specs=[[{'type': 'domain'}, {'type': 'domain'}]], 
        subplot_titles=[
            "Movies with Domestic % > 50%", 
            "Movies with Foreign % > 50%"
        ]
    )

    # Add pie chart for domestic movies
    fig2.add_trace(
        px.pie(
            domestic_counts, 
            names='emotion', 
            values='Counts', 
            color='emotion',
            color_discrete_map=color_map
        ).data[0], 
        row=1, col=1
    )

    # Add pie chart for foreign movies
    fig2.add_trace(
        px.pie(
            foreign_counts, 
            names='emotion', 
            values='Counts', 
            color='emotion',
            color_discrete_map=color_map
        ).data[0], 
        row=1, col=2
    )

    # Update layout to center title, adjust subplot titles, and show the legend
    fig2.update_layout(
        title=dict(
            text="Emotion Distribution Comparison",
            x=0.5,  # Center align the title
            xanchor="center"
        ),
        showlegend=True,  # Enable the legend
        legend=dict(
            orientation="h",  # Horizontal legend
            x=0.5,
            xanchor="center",
            y=-0.1
        ),
        font=dict(
            size=12  # Adjust font size for subplot titles
        )
    )

    # Adjust subplot title font size
    for annotation in fig2['layout']['annotations']:
        annotation['font'] = dict(size=15)  # Smaller font for subplot titles

    return fig2
=======
        print(f"ANOVA p-value (Foreign Movies): {p_value_anova_foreign}")
>>>>>>> 11cb7f5a46a2545ca456cbf2ad056364df88b847
