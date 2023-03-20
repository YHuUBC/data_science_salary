import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Load the data
df = pd.read_csv("data/salaries.csv")

# Define the company size options
df['company_size'] = df['company_size'].replace({'S': 'Small', 'M': 'Middle', 'L': 'Large'})
df['experience_level'] = df['experience_level'].replace({'EN': 'Entry-level', 'MI': 'Mid-level', 
                                                         'SE': 'Senior-level', 'EX': 'Executive-level'})

#company_sizes = df['company_size'].unique()
#years = df['work_year'].unique()
company_sizes = ['Small', 'Middle', 'Large']
years = [2020, 2021, 2022, 2023]
experiences = ['Entry-level', 'Mid-level','Senior-level','Executive-level']

# Create the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

# Define the layout
app.layout = html.Div(children=[
    html.H1('Data Scientist Salary', style={'color': 'gold'}),
    html.H2('Based on the year of data collection, company size, and experience level', 
                            style={'color': 'orange'}),
    html.Label("Select a year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in years],
        value=2020,
        #style={'fontSize': '24px'}
    ),
    #html.Br(),
    html.Label("Select a compnay size:"),    
    dcc.Dropdown(
        id='size-dropdown',
        options=[{'label': size, 'value': size} for size in company_sizes],
        value=company_sizes[0]
    ),
    #html.Br(),
    html.Label("Select an experience level:"),    
    dcc.Dropdown(
        id='experience-dropdown',
        options=[{'label': experience, 'value': experience} for experience in experiences],
        value=experiences[0]
    ),
    dcc.Graph(id='salary-graph',
              #style={'height': '800px', 'width': '800px'}
             )
])

# Define the callback function
@app.callback(Output('salary-graph', 'figure'),
              [Input('year-dropdown', 'value'),
               Input('size-dropdown', 'value'),
              Input('experience-dropdown', 'value')])

def update_graph(year, size, experience):
    filtered_df = df[(df['work_year'] == year) & (df['company_size'] == size) & (df['experience_level'] == experience)]
    filtered_df_group = filtered_df.groupby('job_title').mean()
    filtered_df_group = filtered_df_group.sort_values(by = 'salary_in_usd', ascending = False)
    sorted_job_title = filtered_df_group.index.tolist()
    salaries = filtered_df_group['salary_in_usd'].tolist()
    
    trace = go.Bar(
        x = sorted_job_title,
        y = salaries,
        marker = {"color":"gold"}
    )
    layout = go.Layout(
        title=f'Average Data Scientist Salaries at {size} Companies with {experience} Experience in {year} Sorted by Job Titles',
        xaxis = dict(
                title = 'Job Title',
                titlefont=dict(
                              size= 15,
                              #color='darkgreen'
                )
        ),
        yaxis={'title': 'Salary (USD)'}
    )
    return {'data': [trace], 'layout': layout}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)