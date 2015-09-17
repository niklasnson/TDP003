#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from operator import itemgetter, attrgetter, methodcaller
#---------neccesary functions------
def load(filename):
    '''load the file and reads it. Puts the content in a list'''
    try:
        with open(filename) as json_file:
            list_of_data = json.load(json_file)
        return list_of_data
    except:
        return None

def get_project_count(db):
    number = len(db)
    return number

def get_project(db, id):
    for i in db:
        if i["project_no"] == id:
            return i
    return None

def search(db, sort_by='start_date', 
           sort_order='desc',
           techniques=None, search=None, search_fields=None):

    search_results = []
    search_results = get_all_data(db, search, search_fields)
    if techniques != None:
        search_results = techs_used(search_results, techniques)
    sort_data(search_results, sort_by, sort_order)
    return search_results

def get_techniques(db):
    temp = []
    for i in db:
        for item in i["techniques_used"]:
            if not item in temp:
                temp.append(item)
    temp.sort()
    return temp

def get_technique_stats(db):
    techs = get_techniques(db)
    key = ''
    temp = {}
    for item in techs:
        temp.update({item: []})
        
        for i in db:
            if item in i["techniques_used"]:
                
                temp[item].append({'id':i["project_no"], "name":i["project_name"]})
    
        temp[item] = sorted(temp[item], key=itemgetter('id'))
        
    print(temp['csv'])
    return temp
                
#---------homemade functions-------

def get_all_data(db, search, search_fields):
    free_list = []
    i = 0
    if search_fields == None:
        for i in db:
            for item in i.items():
                if item[1] == search:
                    free_list.append(i)
                elif item[0] == search:
                    free_list.append(i)

    elif search_fields == '':
        return None

    else:
        for project in db:
            for item in project.items():
                for j in search_fields:
                    if item[0] == j and item[1] == search:
                        free_list.append(project)
                        
    return free_list

def sort_data(data, sort_by="project_no", sort_order ='desc'):
    sort_order = get_sort_order(sort_order)
    data.sort(key=itemgetter(sort_by), reverse=sort_order)
    print(data)
    

def techs_used(search, techs):
    temp = []
    for i in search:
        for tech in techs:
            if tech in i['techniques_used']:
                temp.append(i)
    return temp

def get_sort_order(value):
    if value == 'desc':
        return True
    else:
        return False
    
    

#------bullshit functions-------

def main():
    db = load("data.json")
    #get_project_count(db)
    #get_project(db, 2)
    #get_techniques(db)
    get_technique_stats(db)
    #search(db, sort_by='project_name', 
          # sort_order='desc',
           #techniques=None, search="no no no", search_fields=None)


if __name__ == "__main__":
    main()
