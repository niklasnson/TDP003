from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

import data
import config

app = Flask(__name__)

# ---------------------------------------------------------------------------------------------------- #

def data_load(): 
    """ loads the db """
    return data.load('data.json')

# ---------------------------------------------------------------------------------------------------- #

def config_load(): 
    return config.load('config.json')

# ---------------------------------------------------------------------------------------------------- #

@app.route("/")
def index():
    # get last project from the db
    last_project= data.search(data_load(), sort_by='start_date', 
           sort_order='desc',
           techniques=None, search=None, search_fields=None)[-1]

    return render_template("index.html", 
            db = data_load(), 
            config= config_load(),
            data= last_project
            )

# ---------------------------------------------------------------------------------------------------- #

@app.route("/projects")
def projects():
    return render_template("projects.html", 
            projects= data_load(), 
            config= config_load())

# ---------------------------------------------------------------------------------------------------- #

@app.route('/project/<id>')
def project(id):
    return render_template('project.html', 
            data= data.get_project(data_load(), 
                int(id)), 
            config= config_load())

# ---------------------------------------------------------------------------------------------------- #
    
@app.route("/techniques")
def techniques():
    return render_template('techniques.html', 
            config= config_load(), 
            data= data.get_technique_stats(data_load()))

# ---------------------------------------------------------------------------------------------------- #

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
    # do search
        searchfor= request.form['searchfor']
        techniques = request.form.getlist("techniques")
        return render_template('search.html', 
                config= config_load(), 
                technics= data.get_techniques(data_load()), 
                techniques = techniques,
                searchfor = searchfor,
                data= data.search(data_load(), 
                    sort_by='start_date', 
                    sort_order='desc',
                    techniques=techniques, 
                    search=searchfor, 
                    search_fields=None))
    else:
    # render default page
        return render_template('search.html', 
                config= config_load(), 
                technics= data.get_techniques(data_load())) 

# ---------------------------------------------------------------------------------------------------- #        

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', config= config_load()), 404

# ---------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    app.run(debug=True)
