from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from mongodb_utils import get_mongodb


# get mongodb academicworld database
db_mongo = get_mongodb()

# use database technique: view
# 1st widget: dropdown list of years
df_years = pd.DataFrame(list(db_mongo.publication_after2012.aggregate([{'$group': {'_id': '$year',
                                                                                   'pub_cnt': {'$sum': 1}}},
                                                                       {'$sort': {
                                                                           '_id': -1}},
                                                                       {'$limit': 20},
                                                                       {'$project': {'_id': 1}}])))
list_of_years = df_years['_id'].values.tolist()

# 2nd widget: dropdown list of keywords
df_keywords = pd.DataFrame(list(db_mongo.publication_after2012.aggregate([{'$unwind': '$keywords'},
                                                                          {'$group': {'_id': '$keywords.name',
                                                                                      'pub_cnt': {'$sum': 1}}},
                                                                          {'$sort': {
                                                                              'pub_cnt': -1}},
                                                                          {'$limit': 15},
                                                                          {'$project': {'_id': 1}}])))

list_of_keywords = df_keywords['_id'].values.tolist()


# 1st widget: components
first_title = dcc.Markdown(children='', style={'textAlign': 'center'})
first_dropdown_top_n = dcc.Dropdown(
    options=['10', '15', '20', '25'], value='10', clearable=False, style={'textAlign': 'center'})
first_dropdown = dcc.Dropdown(
    options=list_of_years, value='2021', clearable=False, style={'textAlign': 'center'})
first_graph = dcc.Graph(figure={})


# 2nd widget: components
second_title = dcc.Markdown(children='', style={'textAlign': 'center'})
second_dropdown = dcc.Dropdown(
    options=list_of_keywords, value='deep learning', clearable=False, style={'textAlign': 'center'})
second_graph = dcc.Graph(figure={})


# 3rd widget: components
third_title = dcc.Markdown(children='', style={'textAlign': 'center'})
third_input = dcc.Input(placeholder='Search a keyword', style={
                        'textAlign': 'center'})
third_button_submit = dbc.Button(
    "search keyword", outline=True, color="light", className="me-1", n_clicks=0)
third_table = html.Div(children=[])
third_error_alert = dbc.Alert('Oops! Keyword typo or not in database!',
                              id="third_alert",
                              dismissable=True,
                              fade=False,
                              is_open=True)


# 4th widget: components
fourth_title = dcc.Markdown(children='', style={'textAlign': 'center'})
fourth_dropdown = dcc.Dropdown(
    options=list_of_keywords, value='algorithms', clearable=False, style={'textAlign': 'center'})
fourth_graph = dcc.Graph(figure={})


# 5th widget: components
fifth_title = dcc.Markdown('#### Add / Delete My Favorite Keywords', style={
                           'textAlign': 'center'})
fifth_input = dcc.Input(placeholder='Enter a keyword',
                        style={'textAlign': 'center'})
fifth_button_add = dbc.Button(
    "Add", outline=True, color="light", className="me-1", n_clicks=0)
fifth_keyword_table = html.Div(children=[])
fifth_publication_table = html.Div(children=[])
fifth_error_alert = dbc.Alert('Oops! Error: keyword typo or keyword already added or keyword not in database!',
                              id="fifth_alert",
                              dismissable=True,
                              fade=False,
                              is_open=True)


# 6th widget: components
sixth_title = dcc.Markdown('#### Top Publications Assoiciated with Favorite Keyword', style={
                           'textAlign': 'center'})
sixth_title_keyword = dcc.Markdown(children='', style={'textAlign': 'center'})
sixth_dropdown = dcc.Dropdown(options=[], style={'textAlign': 'center'})
sixth_button_delete = dbc.Button(
    "Delete", outline=True, color="light", className="me-1", n_clicks=0)
