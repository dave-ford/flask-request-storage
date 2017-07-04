import sqlite3
from flask import Flask, g, render_template_string, request
import os

app = Flask(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE_NAME'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.route('/home', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
def home():
    # Save request data in the DB
    method = request.method
    url = request.url
    #print(method + ': ' + url)
    query = 'INSERT INTO request ("url", "method") VALUES (?,?);'
    # Insert your code here.
    # get the URL and the method and store it in the Database
    c = g.db.cursor()
    c.execute(query, (url,method))
    g.db.commit()
    g.db.close()
    return 'Success', 200


@app.route('/dashboard')
def dashboard():
    # Fetch all requests from the DB
    query = 'SELECT url, method FROM request;'
    c = g.db.cursor()
    result = c.execute(query)

    base_html = """
        <html>
            <h1>Total requests: {{total_requests}}</h1>
            <h3>GET requests: {{total_per_method['GET']}}</h3>
            <h3>POST requests: {{total_per_method['POST']}}</h3>
            <h3>PUT requests: {{total_per_method['PUT']}}</h3>
            <h3>PATCH requests: {{total_per_method['PATCH']}}</h3>
            <h3>DELETE requests: {{total_per_method['DELETE']}}</h3>
        </html>
    """
    # build these dictionaries out of the data retrieved from the database
    
    d = result.fetchall()
    
    total_requests = len(d)
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    total_per_method = {m:len([elem for elem in d if elem[1] == m]) for m in methods} 


    return render_template_string(
        base_html,
        total_requests=total_requests,
        total_per_method=total_per_method
    )
