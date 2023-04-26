### Title: Use Keyword to Explore Opportunities in Academic World

### Purpose:

- **Application Scenario**: This application is designed to help users understand the research trend in the academic world using keywords.
- **Target Users**: Users who are interested in exploring opportunities in academic settings are our target users.
- **Objectives**: Users can learn research trends in the last ten years and its associated top professors and top universities. Besides, users can insert and delete their favorite keywords to the database in real time with related top publications provided.

### Demo:

https://mediaspace.illinois.edu/media/t/1_2ih7s1zn

### Installation:

```python
git clone https://github.com/CS411DSO-SP23/MengyunTsay.git
cd MengyunTsay
pip install pandas
pip install pymongo
pip install pymysql
pip install mysql-connector-python
pip install sqlalchemy
pip install graphdatascience
pip install dash
pip install dash-bootstrap-component
pip install plotly-express
```

### Usage:

- Run the code below to start the App.

```python
python db_technique.py
python app.py
```

- Go to http://127.0.0.1:8050/ for the app.

- Users can select options from the dropdown list or enter keywords in the text input field to query the databases. Besides, users can also insert / delete keywords to / from their favorite keywords table while updating or delete it from the databases.

  - **Querying Widgets**:

    - **1st widget - Top N Keywords in M Year:**

      - takes input N and M from the two dropdown lists from users
      - queries the MongoDB database
      - provides corresponding top keywords in the pie chart.

    - **2nd widget - Keyword “K” Trend Since 2012:**
      - takes input K from the dropdown list from users
      - queries the MongoDB database
      - provides the corresponding trend by number of citations since 2012 in the line chart.
    - **3rd widget - Top Professors with Keyword ”K”:**
      - takes input K from the text input field from users
      - queries MySQL database
      - provides corresponding top 10 professors by number of citations in the table.
      - pops an error if text input K is not in the database.
    - **4th widget - University Citation Ranking with Keyword “K”:**
      - takes input K from the dropdown list from users
      - queries the neo4j database
      - provides corresponding top 10 universities by number of citations in the scatter chart.

  - **Updating Widgets:**
    - **5th widget - Add My Favorite Keyword / Top Publications Associated with Favorite Keyword “K”:**
      - takes input K from the text input field from users
      - insert K to the favorite_keyword table in MySQL database
      - shows the inserted keyword in the Favorite Keyword as a table ordered alphabetically
      - shows K as one of the options in the dropdown list for deleting
      - queries MySQL database using K
      - provides corresponding top 10 publication titles in the table
      - pops an error if text input K is not in the database or already being inserted in the favorite_keyword table in MySQL database.
    - **6th widget - Delete My Favorite Keyword / Top Publications Associated with Favorite Keyword “K”:**
      - takes input K from the dropdown list from users
      - deletes K from the favorite_keyword table in MySQL database
      - removes the deleted keyword in the Favorite Keyword as a table ordered alphabetically
      - deletes K in the dropdown list for deleting
      - queries MySQL database using the first keyword in the table
      - provides corresponding top 10 publication titles in the table
      - if the favorite_keyword is empty, the top publications table will be empty.

### Design:

The application consisted of two parts, frontend and backend. Dash is the frontend framework of the application for user interface, while backend framework is supported by three databases, MySQL, MongoDB, neo4j.

- **Frontend:**
  - **app.py**: include app initialization, app layout and app callback functions for six widgets.
  - **widget_components.py**: include components for six widgets, which communicate with databases by importing connection from mysql_til.py, mongodb_utils.py and neo4j.py respectively.
- **Backend:**
  - **mysql_utils.py**: include connection to MySQL database through sqlacademy,
  - **mongodb_utils.py**: include connection to MongoDB database
  - **Neo4j_utils.py**: include connection to neo4j database
  - **db_technique.py**: include creation of favorite_keyword table, execution of four database techniques for MySQL database and execution of two database techniques for MongoDB database.

### Implementation:

Dash is the frontend framework of the application for user interface, while backend framework is supported by three databases, MySQL, MongoDB, neo4j. For consistent styling, dash bootstrap component library is also adopted. The following libraries are used for connecting to MySQL, MongoDB and neo4j respectively: mysql-connector / sqlalchemy, pymongo, graph data science.

Official tutorials from Dash, plotly, MySQL, MongoDB and neo4j are sufficient to understand the basics, which is a good starting point for building the application. It might take some time and effort to dig into callback functions for dashboard interactions and also differentiate between the shell syntax and python syntax when communicating with each database.

### Database Techniques:

**The implementation can be found in db_technique.py.**

- **For MySQL:**
  One of the functions of this application is to add and delete keywords to the favorite keyword table, which will insert and delete keywords in the favorite_keyword table in real time from the MySQL database. The favorite_keyword table is created in the MySQL database when executing db_technique.py before starting the application. The table has two fields, id and name, where id is the primary key.

  1. **Partition:** partitioned id in favorite_keyword table by hashing id into 5 partitions. This partition is used for the fifth and sixth widget.
  2. **View:** created view for publication table joined with favorite_keyword table on publication’s id and favorite_keyword where publication’s year is greater than 2012. This view is used for the fifth and sixth widget when querying the top publication with given keys.
  3. **Constraint:** added check constraint for favorite_keyword table where numbers of characters of name are greater than two. This constraint will be used for the fifth and sixth widget when users insert their favorite keyword by entering text in the given input field.
  4. **Indexing:** created indexes on id and name of favorite_keyword table. This indexing is used for the fifth and sixth widget.

- **For MongoDB:**
  1. **Indexing:** created indexes on id and name for keyword table. This indexing is used for the first and second widget.
  2. **View:** created view for publication table where publication year is greater than 2012. This view is used for the first and second widget.

### Contributions:

This project is completed solely by myself. I did all the tasks alone.
