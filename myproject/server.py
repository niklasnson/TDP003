from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

import data
import config

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", 
            db = data.load("data.json"), 
            config= config.load())

@app.route("/projects")
def projects():
    return render_template("projects.html", 
            projects= data.load('data.json'), 
            config= config.load())

@app.route('/project/<id>')
def project(id):
    return render_template('project.html', 
            project= data.get_project(data.load('data.json'), 
                int(id)), 
            config= config.load())

@app.route("/techniques")
def techniques():
    return render_template('index.html', config= config.load())

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
    # do search
        searchfor= request.form['searchfor']
        techniques = request.form.getlist("techniques")
        return render_template('search.html', 
                config= config.load(), 
                technics= data.get_techniques(data.load('data.json')), 
                techniques = techniques,
                searchfor = searchfor,
                result= data.search(data.load('data.json'), 
                    sort_by='start_date', 
                    sort_order='desc',
                    techniques=techniques, 
                    search=searchfor, 
                    search_fields=None))
    else:
    # render default page
        return render_template('search.html', 
                config= config.load(), 
                technics= data.get_techniques(data.load('data.json'))) 

if __name__ == "__main__":
    app.run(debug=True)
