# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
# from mongodb_utils import db_mongo
from pymongo import MongoClient

# connect with mongoDB datatbase - academicworld collections
client = MongoClient('mongodb://127.0.0.1:27017/')
# print(client.test)
db_mongo = client['academicworld']

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# 1st widget: dropdown list of years
df_years = pd.DataFrame(list(db_mongo.publications.aggregate([{'$match': {"year": {'$gte': 2012}}},
                                                              {'$group': {'_id': '$year',
                                                                          'pub_cnt': {'$sum': 1}}},
                                                              {'$sort': {
                                                                  '_id': -1}},
                                                              {'$limit': 20},
                                                              {'$project': {
                                                                  '_id': 1}}
                                                              ])))
# print(df_years['_id'].values.tolist())
list_of_years = df_years['_id'].values.tolist()

# 2nd widget: dropdown list of keywords
df_keywords = pd.DataFrame(list(db_mongo.publications.aggregate([{'$match': {"year": {'$gte': 2012}}},
                                                                 {'$unwind': '$keywords'},
                                                                 {'$group': {'_id': '$keywords.name',
                                                                             'pub_cnt': {'$sum': 1}}},
                                                                 {'$sort': {
                                                                     'pub_cnt': -1}},
                                                                 {'$limit': 10},
                                                                 {'$project': {
                                                                     '_id': 1}}
                                                                 ])))
# print(df_keywords['_id'].values.tolist())
list_of_keywords = df_keywords['_id'].values.tolist()

# 1st widget: components
first_title = dcc.Markdown(children='', style={'textAlign': 'center'})
first_dropdown_top_n = dcc.Dropdown(
    options=['10', '15', '20', '25'], value='10', clearable=False)
first_dropdown = dcc.Dropdown(
    options=list_of_years, value='2021', clearable=False)
first_graph = dcc.Graph(figure={})

# 2nd widget: components
second_title = dcc.Markdown(children='', style={'textAlign': 'center'})
second_dropdown = dcc.Dropdown(
    options=list_of_keywords, value='deep learning', clearable=False)
second_graph = dcc.Graph(figure={})

# 3rd widget: components
third_title = dcc.Markdown(children='', style={'textAlign': 'center'})
# second_dropdown = dcc.Dropdown(
#     options=list_of_keywords, value='deep learning', clearable=False)
third_table = html.Div(children=[])

# 4th widget: components
fourth_title = dcc.Markdown(children='', style={'textAlign': 'center'})
fourth_input = dcc.Input(placeholder='Search a keyword',
                         value='data mining', style={'textAlign': 'center'}, size='30')
fourth_table = html.Div(children=[])
# App layout
app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    first_title
                ], width=4),
                dbc.Col([
                    second_title
                ], width=4),
                dbc.Col([
                    third_title
                ], width=4)
            ], align='center'),
            dbc.Row([
                dbc.Col([
                    first_dropdown
                ], width=2),
                dbc.Col([
                    first_dropdown_top_n
                ], width=2),
                dbc.Col([
                    second_dropdown
                ], width=8)
            ], align='center'),
            dbc.Row([
                dbc.Col([first_graph
                         ], width=4),
                dbc.Col([
                    second_graph
                ], width=4),
                dbc.Col([
                    third_table
                ], width=4)
            ], align='center')]), color='dark'),
    dbc.Row([
        dbc.Col([
            fourth_title
        ], width=4)
    ], align='center'),
    dbc.Row([
        dbc.Col([
            fourth_input
        ], width=4)
    ], align='center'),
    dbc.Row([
        dbc.Col([
            fourth_table
        ], width=4)
    ], align='center')])
# app.layout = dbc.Container([
#     dbc.Row(dbc.Col(first_title, width=6), dbc.Col(second_title, width=6)),
#     dbc.Row(dbc.Col(first_dropdown, width=6),
#             dbc.Col(second_dropdown, width=6)),
#     dbc.Row(dbc.Col(first_graph, width=6), dbc.Col(second_graph, width=6))
# ])


# 1st widget: callback interaction
@app.callback(
    Output(first_title, component_property='children'),
    Output(first_graph, component_property='figure'),
    Input(first_dropdown, component_property='value'),
    Input(first_dropdown_top_n, component_property='value')
)
def update_first_graph(user_dropdown_year, user_radio_top_n):
    df_first_widget = pd.DataFrame(list(db_mongo.publications.aggregate([
        {"$match": {"year": {"$eq": int(user_dropdown_year)}}},
        {"$unwind": "$keywords"},
        {"$group": {"_id": "$keywords.name",
                    "pub_cnt": {"$sum": 1}}},
        {"$sort": {"pub_cnt": -1}},
        {"$limit": int(user_radio_top_n)}
    ])))

    # print(df_first_widget)
    # fig = px.scatter(data_frame=df_first_widget,
    #                  x='_id', y='pub_cnt', color='_id').update_layout(
    #     template='plotly_dark',
    #     plot_bgcolor='rgba(0, 0, 0, 0)',
    #     paper_bgcolor='rgba(0, 0, 0, 0)',
    #     showlegend=False)
    fig = px.pie(df_first_widget,
                 values='pub_cnt',
                 names='_id',
                 hole=.3,
                 color_discrete_sequence=px.colors.sequential.RdBu).update_traces(
        textposition='inside', textinfo='percent+label').update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)')
    first_title = f'### Top {int(user_radio_top_n)} Keywords in {user_dropdown_year}'
    return first_title, fig


# 2nd widget: callback interaction
@app.callback(
    Output(second_title, component_property='children'),
    Output(second_graph, component_property='figure'),
    Input(second_dropdown, component_property='value')
)
def update_second_graph(user_dropdown_keyword):
    df_second_widget = pd.DataFrame(list(db_mongo.publications.aggregate([{'$unwind': "$keywords"},
                                                                          {'$match': {"keywords.name": {
                                                                              '$eq': user_dropdown_keyword}}},
                                                                          {'$group': {"_id": "$year",
                                                                                      'pub_cnt': {'$sum': 1}}},
                                                                          {'$sort': {
                                                                              '_id': -1}},
                                                                          {'$limit': 20}
                                                                          ])
                                         ))

    fig = px.line(data_frame=df_second_widget,
                  x='_id', y='pub_cnt').update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    second_title = f'### Keyword "{user_dropdown_keyword}" Trend Over Past 20 Years'
    return second_title, fig


# 3rd widget: callback interaction
@app.callback(
    Output(third_title, component_property='children'),
    Output(third_table, component_property='children'),
    Input(second_dropdown, component_property='value')
)
def update_third_table(user_dropdown_keyword):
    df_third_widget = pd.DataFrame(list(db_mongo.publications.aggregate([
        {'$unwind': "$keywords"},
        {'$match': {'$and': [{"numCitations": {'$gt': 0}},
                             {"keywords.name": user_dropdown_keyword}]}},
        {'$lookup': {'from': "faculty", 'localField': "id",
                     'foreignField': "publications", 'as': "fac"}},
        {'$unwind': "$fac"},
        {'$group': {"_id": "$fac.affiliation.name",
                    'numCitations': {'$sum': 1}
                    }},
        {'$sort': {'numCitations': -1}},
        {'$limit': 10}])

    ))

    third_table = dash_table.DataTable(data=df_third_widget.to_dict('records'),
                                       columns=[{"name": i, "id": i}
                                                for i in df_third_widget.columns],
                                       style_cell={'textAlign': 'left'},
                                       style_cell_conditional=[
        {
            'if': {'column_id': 'numCitations'},
            'textAlign': 'right'
        }
    ],
        style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
        style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    })
    third_title = f'### Keyword "{user_dropdown_keyword}" num of citations ranking'
    return third_title, third_table


# 4th widget: callback interaction
@app.callback(
    Output(fourth_title, component_property='children'),
    Output(fourth_table, component_property='children'),
    Input(fourth_input, component_property='value')
)
def update_fourth_table(user_input_keyword):
    df_fourth_widget = pd.DataFrame(list(db_mongo.publications.aggregate([
        {'$match': {'$and': [{"year": {'$gt': 2012}},
                             {"numCitations": {'$gt': 0}}]}},
        {'$unwind': "$keywords"},
        {'$match': {"keywords.name": user_input_keyword}},
        {'$lookup': {'from': "faculty", 'localField': "id",
                     'foreignField': "publications", 'as': "fac"}},
        {'$unwind': "$fac"},

        {'$group': {"_id": "$fac.name",
                    'numCitations': {'$sum': 1}
                    }},
        {'$sort': {'numCitations': -1}},
        {'$limit': 10}
    ])

    ))

    fourth_table = dash_table.DataTable(data=df_fourth_widget.to_dict('records'),
                                        columns=[{"name": i, "id": i}
                                                 for i in df_fourth_widget.columns],
                                        style_cell={'textAlign': 'center'},

                                        style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
        style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    })
    fourth_title = f'### Top Professor Ranking with Keyword "{user_input_keyword}" '
    return fourth_title, fourth_table


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
