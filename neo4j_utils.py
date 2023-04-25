from graphdatascience import GraphDataScience
from config import *

host = "bolt://127.0.0.1"
user = "neo4j"
password = NEO4J_PASSWORD

gds = GraphDataScience(host, auth=(user, password))
gds.set_database("academicworld")
# df_fourth_query = f"MATCH (i:INSTITUTE)-[a:AFFILIATION_WITH]-(f:FACULTY)-[p: PUBLISH]-(pub:PUBLICATION)-[l: LABEL_BY]-(k:KEYWORD)\
#                         WHERE pub.year>2012 AND k.name = 'deep learning'\
#                        RETURN i.name AS University, sum(pub.numCitations) AS nums_of_citations\
#                      ORDER BY nums_of_citations DESC\
#                         LIMIT 10"

# df_fourth_widget = gds.run_cypher(df_fourth_query)
# print(df_fourth_widget)
