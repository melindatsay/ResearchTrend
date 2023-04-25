# Import packages
from dash import Dash, html, dash_table, callback, Output, Input, State, ctx, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from mongodb_utils import get_mongodb
from neo4j_utils import gds
from mysql_utils import engine
from widget_components import *

# get mongodb academicworld database
db_mongo = get_mongodb()


# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


# App layout
app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([first_title], width=6),
                dbc.Col([second_title], width=6),
            ], align='center'),
            dbc.Row([
                dbc.Col([first_dropdown], width=3),
                dbc.Col([first_dropdown_top_n], width=3),
                dbc.Col([second_dropdown], width=6),
            ], align='center'),
            dbc.Row([
                dbc.Col([first_graph], width=6),
                dbc.Col([second_graph], width=6),
            ], align="center")]), color='dark'),
    dbc.Row([
        dbc.Col([third_title], width=6),
        dbc.Col([fourth_title], width=6)], align='center'),
    dbc.Row([
        dbc.Col([third_input], width=3),
        dbc.Col([third_button_submit], width=3),
        dbc.Col([fourth_dropdown], width=6)], align='center'),
    dbc.Row([
        dbc.Col([third_error_alert], width=6)]),
    dbc.Row([
        dbc.Col([third_table], width=6),
        dbc.Col([fourth_graph], width=6)], align='center'),
    dbc.Row([
        dbc.Col([fifth_title], width=6),
        dbc.Col([sixth_title], width=6)], align='center'),
    dbc.Row([
        dbc.Col([fifth_input]),
        dbc.Col([fifth_button_add]),
        dbc.Col([sixth_dropdown]),
        dbc.Col([sixth_button_delete]),
        dbc.Col([sixth_title_keyword], width=6)], align='center'),
    dbc.Row([
        dbc.Col([fifth_error_alert], width=6)]),
    dbc.Row([
        dbc.Col([fifth_keyword_table], width=6),
        dbc.Col([fifth_publication_table], width=6)], align='center')
])


# query MongoDB
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

    fig = px.pie(df_first_widget,
                 values='pub_cnt',
                 names='_id',
                 hole=.3,
                 color_discrete_sequence=px.colors.sequential.RdBu).update_traces(
        textposition='inside',
        textinfo='percent+label').update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)')
    first_title = f'#### Top {int(user_radio_top_n)} Keywords in {user_dropdown_year}'
    return first_title, fig


# query MongoDB use view
# 2nd widget: callback interaction
@app.callback(
    Output(second_title, component_property='children'),
    Output(second_graph, component_property='figure'),
    Input(second_dropdown, component_property='value')
)
def update_second_graph(user_dropdown_keyword):
    df_second_widget = pd.DataFrame(list(db_mongo.publication_after2012.aggregate([{'$unwind': "$keywords"},
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
    second_title = f'#### Keyword "{user_dropdown_keyword}" Trend Since 2012'
    return second_title, fig


# query MySql
# third widget: callback interaction
@app.callback(
    Output(third_error_alert, component_property='is_open'),
    Output(third_title, component_property='children'),
    Output(third_table, component_property='children'),
    Input(third_button_submit, 'n_clicks'),
    State(third_input, component_property='value')
)
def update_third_table(n_clicks, user_input_keyword):
    if user_input_keyword is None:
        user_input_keyword = "data mining"

    df_third_query = f"SELECT faculty.name AS Professors\
                        FROM publication_keyword\
                        JOIN keyword\
                        ON publication_keyword.keyword_id = keyword.id\
                        JOIN publication\
                        ON publication_keyword.publication_id = publication.id\
                        JOIN faculty_publication\
                        ON publication_keyword.publication_id = faculty_publication.publication_id\
                        JOIN faculty\
                        ON faculty_publication.faculty_id = faculty.id\
                        WHERE publication.year >= 2012 AND keyword.name='{user_input_keyword}'\
                        GROUP BY faculty.name\
                        ORDER BY COUNT(publication.num_citations) DESC\
                        LIMIT 10"
    df_third_widget = pd.read_sql(df_third_query, con=engine)
    if df_third_widget.empty:
        return True, no_update, no_update

    third_table = dash_table.DataTable(data=df_third_widget.to_dict('records'),
                                       columns=[{"name": i, "id": i}
                                                for i in df_third_widget.columns],
                                       style_cell={'textAlign': 'center'},

                                       style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
        style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    })
    third_title = f'#### Top Professors with Keyword "{user_input_keyword}" '
    return False, third_title, third_table


# query neo4j
# fourth widget: callback interaction
@app.callback(
    Output(fourth_title, component_property='children'),
    Output(fourth_graph, component_property='figure'),
    Input(fourth_dropdown, component_property='value')
)
def update_fourth_table(user_dropdown_keyword):
    df_fourth_query = f"MATCH (i:INSTITUTE)-[a:AFFILIATION_WITH]-(f:FACULTY)-[p: PUBLISH]-(pub:PUBLICATION)-[l: LABEL_BY]-(k:KEYWORD)\
                        WHERE pub.year>2012 AND k.name = '{user_dropdown_keyword}'\
                       RETURN i.name AS University, sum(pub.numCitations) AS nums_of_citations\
                     ORDER BY nums_of_citations DESC\
                        LIMIT 10"

    df_fourth_widget = gds.run_cypher(df_fourth_query)
    fig = px.scatter(data_frame=df_fourth_widget,
                     x='University', y='nums_of_citations').update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    fourth_title = f'#### University Citation Ranking with Keyword "{user_dropdown_keyword}"'
    return fourth_title, fig


# query MySql
# fifth and sixth widget: callback interaction
@app.callback(
    Output(fifth_error_alert, component_property='is_open'),
    Output(fifth_keyword_table, component_property='children'),
    Output(sixth_title_keyword, component_property='children'),
    Output(fifth_publication_table, component_property='children'),
    Output(sixth_dropdown, 'options'),
    Input(fifth_button_add, 'n_clicks'),
    State(fifth_input, component_property='value'),
    Input(sixth_button_delete, 'n_clicks'),
    State(sixth_dropdown, component_property='value')
)
def add_delete_keyword_to_fifth_table(add_n_clicks, user_input_keyword, delete_n_clicks, user_dropdown_keyword):
    word_just_deleted = None
    # button_id changed once the button comoponent has been moved in the layout
    button_clicked = ctx.triggered_id

    if button_clicked is not None:
        # add keyword to favorite_keyword table
        if button_clicked == '2ba4b180-cb69-ca38-5f3f-563838701a14' and user_input_keyword is not None:
            keyword_id_query = f"SELECT id FROM keyword WHERE name='{user_input_keyword}'"

            try:
                df_keyword_id = pd.read_sql(keyword_id_query, con=engine)
                insert_keyword_query = ("INSERT INTO favorite_keyword"
                                        "(id, name) "
                                        "VALUES (%s, %s)")
                engine.execute(insert_keyword_query,
                               (str(df_keyword_id.id[0]), user_input_keyword))
            except Exception:
                return True, no_update, no_update, no_update, no_update

        # delete keyword from favorite_keyword table
        if button_clicked == '12f175ff-ae3b-16ec-9a27-d85888c132ad' and user_dropdown_keyword is not None:
            word_just_deleted = user_dropdown_keyword
            delete_keyword_query = f"DELETE FROM favorite_keyword WHERE name='{user_dropdown_keyword}'"
            engine.execute(delete_keyword_query)

    # select all keywords from favorite_keyword table
    fifth_favorite_keyword_query = "SELECT name AS favorite_keyword FROM favorite_keyword ORDER BY name"
    df_fifth_keyword_widget = pd.read_sql(
        fifth_favorite_keyword_query, con=engine)

    fifth_keyword_table = dash_table.DataTable(data=df_fifth_keyword_widget.to_dict('records'),
                                               columns=[{"name": i, "id": i}
                                                        for i in df_fifth_keyword_widget.columns],
                                               style_cell={
        'textAlign': 'center'},
        style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
        style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    })

    if (user_input_keyword is None and word_just_deleted is None) or \
        (user_input_keyword is not None and user_input_keyword == word_just_deleted) or\
            (word_just_deleted is not None and user_input_keyword != word_just_deleted):
        if df_fifth_keyword_widget.empty == False:
            user_input_keyword = df_fifth_keyword_widget.favorite_keyword[0]

    # use view: pub_fav_keyword_after2012
    # select all publications using user_input_keyword
    fifth_publication_query = f"SELECT pub_title AS publication_title\
                            FROM pub_fav_keyword_after2012\
                            WHERE fav_key_name='{user_input_keyword}'\
                            GROUP BY pub_title\
                            ORDER BY COUNT(pub_num_citations) DESC\
                            LIMIT 10"

    df_fifth_publication_widget = pd.read_sql(
        fifth_publication_query, con=engine)

    fifth_publication_table = dash_table.DataTable(data=df_fifth_publication_widget.to_dict('records'),
                                                   columns=[{"name": i, "id": i}
                                                            for i in df_fifth_publication_widget.columns],
                                                   style_cell={
        'textAlign': 'left'},
        style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
        style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    })

    # update options for favorite keyword dropdown list for deleting
    sixth_dropdown = [k for k in df_fifth_keyword_widget.favorite_keyword]

    sixth_title_keyword = f'#### "{user_input_keyword}"'
    return False, fifth_keyword_table, sixth_title_keyword, fifth_publication_table, sixth_dropdown


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
