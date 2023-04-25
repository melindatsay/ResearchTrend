from pymongo import MongoClient

# connect with mongoDB datatbase - academicworld collections


def get_mongodb():
    client = MongoClient('mongodb://127.0.0.1:27017/')
    return client['academicworld']


# # get mongodb academicworld database
# db_mongo = get_mongodb()
