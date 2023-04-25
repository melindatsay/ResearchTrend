import mysql.connector
from mysql.connector import errorcode
from mongodb_utils import get_mongodb
from config import *

# connect to mysqlshow
try:
    cnx = mysql.connector.connect(user='root',
                                  password=MYSQL_PASSWORD,
                                  host='127.0.0.1',
                                  database='academicworld')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

cursor = cnx.cursor()


# create favorite_keyword table for the 5th and 6th widget
TABLES = {}
TABLES['favorite_keyword'] = (
    "CREATE TABLE favorite_keyword(id INT NOT NULL, name VARCHAR(512), PRIMARY KEY(id))")


def create_sql_tables(tables):
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


create_sql_tables(TABLES)


# database technique in MySQL
# 1: partition id in favorite keyword table for 5th and 6th widget
partition_favorite_keyword_name = ("ALTER TABLE favorite_keyword\
                                   PARTITION BY hash(id) PARTITIONS 5")
cursor.execute(partition_favorite_keyword_name)
# explain select * from favorite_keyword;


# 2: create view for publication table joined with favorite_keyword table and year > 2012 for 5th and 6th widget
create_view_pub_fav_keyword_after2012 = ("CREATE VIEW pub_fav_keyword_after2012\
                                       AS (SELECT publication.id AS pub_id,\
		                                          publication.title AS pub_title,\
                                                  publication.year AS pub_year,\
                                                  publication.num_citations AS pub_num_citations,\
                                                  favorite_keyword.id AS fav_key_id,\
                                                  favorite_keyword.name AS fav_key_name\
                                             FROM publication_keyword \
                                             JOIN favorite_keyword\
                                               ON publication_keyword.keyword_id = favorite_keyword.id\
                                             JOIN publication\
                                               ON publication_keyword.publication_id = publication.id\
                                            WHERE publication.year >= 2012)")
cursor.execute(create_view_pub_fav_keyword_after2012)
# show tables;
# drop view pub_fav_keyword_after2012;


# 3: Add check constraint for favorite_keyword table where nums of characters of keyword name >2 for 5th and 6th widget
check_constraint = ("ALTER TABLE favorite_keyword\
                  ADD CONSTRAINT name_len_2\
                           CHECK ((CHAR_LENGTH(name) > 2))")
cursor.execute(check_constraint)
# show create table favorite_keyword;
# alter table favorite_keyword drop constraint name_len_2;


# 4: Indexing on favorite_keyword table for id and name for 5th and 6th widget
indexing_fav_key = (
    "CREATE UNIQUE INDEX fav_keyword_indexing ON favorite_keyword (id, name)")
cursor.execute(indexing_fav_key)
# show index from favorite_keyword;
# ALTER TABLE favorite_keyword DROP INDEX (fav_keyword_indexing);
cnx.close()


# get mongodb academicworld database
db_mongo = get_mongodb()

# database technique for MongoDB
# 1: Indexing for keyword table for 1st and 2nd widget
db_mongo.keyword.create_index("query for keyword trend")

# shell command:
# db.keyword.createIndex({"id": 1, "name": 1}, {"name": "query for keyword trend"})
# db.keyword.getIndexes()
# db.keyword.dropIndex('query for keyword trend')

# 2: create view for publication table after year 2012 for 1st and 2nd widget:
db_mongo.command('create', 'publication_after2012',
                 viewOn='publications',
                 pipeline=[{"$match": {"year": {"$gte": 2012}}}])

# shell command:
# db_mongo.createView("publication_after2012", "publication", [{"$match": {"year": {"$gte": 2012}}}])
# show collections
# db.publication_after2012.drop()
