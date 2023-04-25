from pymongo import MongoClient
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
from app import app

# connect with mongoDB datatbase - academicworld collections
client = MongoClient('mongodb://127.0.0.1:27017/')
# print(client.test)
db_mongo = client['academicworld']

# 1st widget: top #10 keyword by user selected year
# df = pd.DataFrame(list(db_mongo.publications.aggregate([
#     {"$match": {"year": {"$gte": 2012}}},
#     {"$unwind": "$keywords"},
#     {"$group": {"_id": "$keywords.name",
#                 "pub_cnt": {"$sum": 1}}},
#     {"$sort": {"pub_cnt": -1}},
#     {"$limit": 10}
# ])))


