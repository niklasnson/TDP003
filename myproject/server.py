from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import abort

import logging 
from logging.handlers import RotatingFileHandler

import data
import config

app = Flask(__name__)

# ---------------------------------------------------------------------------------------------------- #

def data_load(): 
    """ loads the db """
    if data.load('data.json') == None: abort(400)
    return data.load('data.json')
        
# ---------------------------------------------------------------------------------------------------- #

def config_load():
    if config.load('config.json') == None: abort(400)
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

    try: id = int(id) 
    except: 
        app.logger.error('projektet kunde inte hittas [id]: %s', id)     
        abort(404,id)
    
    if data.get_project(data_load(), id) == None: 
        app.logger.error('projektet kunde inte hittas [id]: %d', id)  
        abort(404,id)

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
        if searchfor== '': 
            searchfor_db= None
        else:
            searchfor_db = searchfor
            


        sel_techniques = request.form.getlist("techniques")
        app.logger.info('sökte efter: "%s" med "%s"', searchfor, sel_techniques)
        return render_template('search.html', 
                config= config_load(), 
                all_techniques= data.get_techniques(data_load()), 
                sel_techniques= sel_techniques,
                searchfor= searchfor,
                data= data.search(data_load(), 
                    sort_by='start_date', 
                    sort_order='desc',
                    techniques=sel_techniques, 
                    search=searchfor_db, 
                    search_fields=None))
    else:
    # render default page
        return render_template('search.html', 
                config= config_load(), 
                all_techniques= data.get_techniques(data_load())) 

# ---------------------------------------------------------------------------------------------------- #        

@app.errorhandler(400)
def data_base_not_readable(e):
    app.logger.error('databasen eller config filen kunde inte läsas')
    return render_template('data_error.html'), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', config= config_load()), 404
404

# ---------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    formatter = logging.Formatter( "%(asctime)s | %(funcName)s | %(levelname)s | %(message)s ")
    handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run(debug=True)
