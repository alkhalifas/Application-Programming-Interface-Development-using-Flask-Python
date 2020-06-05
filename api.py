import flask
from flask import request, jsonify
import sqlite3
import numpy as np 

# Debug allows for changes to be seen in real time.
app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dictFactory(cursor, row):
    """
    Function that parses the entries of the database and returns them as a list of dictionaries.

    @param cursor -- A cursor object using sqlite.
    @param row -- The row of the database being parsed.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def homePage():
    return '''
    <h1>Datascience Jobs Database</h1>
    <h3>You have reached: /home/</h3>
    <p>To view all entries in the database: '127.0.0.1:5000/api/v1/jobs/datascience/all' </p>
    <p>To filter entries based on country : '127.0.0.1:5000/api/v1/jobs/datascience?country=United%20States' </p>
    <p>To filter entries based on post id : '127.0.0.1:5000/api/v1/jobs/datascience?id=81953194' </p>
'''

@app.route('/api/v1/jobs/datascience/all', methods=['GET'])
def apiViewAll():
    conn = sqlite3.connect('data/datasciencejobs_database.db')
    conn.row_factory = dictFactory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM tblJobs;').fetchall()

    return jsonify(all_books)

@app.errorhandler(404)
def pageNotFound(e):
    return "<h1>Error 404</h1><p>Page not found.</p>", 404

@app.route('/api/v1/jobs/datascience', methods=['GET'])
def apiViewByFilter():
    '''
    Function that allows users to filter the results in the API based on specified input.
    '''
    query_parameters = request.args

    id = query_parameters.get('id')
    dateTime = query_parameters.get('dateTime')
    cleanContent = query_parameters.get('cleanContent')
    country = query_parameters.get('country')

    query = "SELECT * FROM tblJobs WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)

    if dateTime:
        query += ' dateTime=? AND'
        to_filter.append(dateTime)

    if cleanContent:
        query += ' cleanContent=? AND'
        to_filter.append(cleanContent)
    
    if country:
        query += ' country=? AND'
        to_filter.append(country)

    if not (id or dateTime or cleanContent or country):
        return pageNotFound(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('data/datasciencejobs_database.db')
    conn.row_factory = dictFactory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()