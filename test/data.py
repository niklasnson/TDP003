#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
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
    search_results = free_search(db, search, search_fields)
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
    return temp
                
#---------homemade functions-------

def free_search(db, search, search_fields):
    free_list = []
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
        for i in db:
            for item in i.items():
                if item[0] == search_fields and item[1] == search:
                    free_list.append(i)
    
    return free_list
                
    


#------bullshit functions-------

def main():
    db = load("data.json")
    get_project_count(db)
    get_project(db, 2)
    get_techniques(db)
    get_technique_stats(db)
    search(db, sort_by='start_date', 
           sort_order='desc',
           techniques=None, search=None, search_fields=None)


if __name__ == "__main__":
    main()
