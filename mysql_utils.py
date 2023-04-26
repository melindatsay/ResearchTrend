import pymysql
from sqlalchemy import create_engine
from config import *


# use SQLalchemy for app.py
pymysql.install_as_MySQLdb()

user = MYSQL_USER
password = MYSQL_PASSWORD
host = '127.0.0.1'
port = 3306
database = 'academicworld'

engine = create_engine(
    "mysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
