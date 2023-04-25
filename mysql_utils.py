import mysql.connector

cnx = mysql.connector.connect(user='root', password='test-root',
                              host='127.0.0.1')
cnx.close()
