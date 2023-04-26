from graphdatascience import GraphDataScience
from config import *

host = "bolt://127.0.0.1"
user = NEO4J_USER
password = NEO4J_PASSWORD

gds = GraphDataScience(host, auth=(user, password))
gds.set_database("academicworld")
