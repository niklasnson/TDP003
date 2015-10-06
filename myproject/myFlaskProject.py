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
    return render_template("index.html", db = data.load("data.json"))

@app.route("/projects")
def projects():
    return render_template("projects.html", projects= data.load('data.json'))

@app.route('/project/<id>')
def project(id):
    return render_template('project.html', project= data.get_project(data.load('data.json'), int(id)), config= config.load())

@app.route("/techniques")
def techniques():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
