import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import plotly.express as px


# Function calculating the VIF (Variance inflation factor)
def calculate_vif(dataframe):

    # Ensuring the data contains only numeric columns
    data = dataframe.select_dtypes(include=['number'])

    data = sm.add_constant(data)

    # Compute VIF for each feature
    vif_data = pd.DataFrame()
    vif_data["Feature"] = data.columns
    vif_data["VIF"] = [variance_inflation_factor(data.values, i) for i in range(data.shape[1])]

    # Drop the constant row from the VIF results
    return vif_data[vif_data["Feature"] != "const"]

def plot_feature_coefficients(dataframe, title):
    """
    Plots a bar chart for feature coefficients.

    Parameters:
        dataframe (pd.DataFrame): DataFrame containing the feature statistics to plot.
        title (str): Title of the bar chart.
       
    Returns:
        fig: The Plotly bar chart figure.
    """
    # Aranges the features in descending order base on their coeffecients
    dataframe_sorted = dataframe.sort_values(by="Coefficient", ascending=False)

    # Create the bar plot
    fig = px.bar(
        dataframe_sorted,
        x='Feature',
        y='Coefficient',
        hover_data=['Std_Error', 't_value', 'p_value'],
        color='Coefficient',
        labels={'Feature': 'Feature Names', 'Coefficient': 'Coefficient Value'},
        title=title,
        height=400
    )

    # Centering the title and changing the font

    fig.update_layout(
        title={
            'text': title,
            'y': 0.95,  # Vertical alignment of the title
            'x': 0.5,   # Horizontal alignment of the title
            'xanchor': 'center',
            'yanchor': 'top'
        },
        title_font=dict(
            size=20,
            color="black"    
        )
    )


    return fig


