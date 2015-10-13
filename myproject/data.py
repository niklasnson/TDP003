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
    '''return the number of projects in the database'''
    number = len(db)
    return number

def get_project(db, id):
    '''fetches a specific project from the database, you choose the project with its ID'''
    for i in db:
        if i["project_no"] == id:
            return i
    return None

def search(db, sort_by='start_date', 
           sort_order='desc',
           techniques=None, search=None, search_fields=None):
    '''search in the database by entering a search word, the field you want to search in. the function also sorts the fetched data by ascending or descending order. It can also check for specific techniques in each project that were fetched with the search function.'''
   
    search_results = []
    search_results = get_all_data(db, search, search_fields)
    if search_results != None: #tilläg
        
        if techniques != None and techniques != []:
            search_results = techs_used(search_results, techniques)
        sort_data(search_results, sort_by, sort_order)
    return search_results

def get_techniques(db):
    '''fetches all the techniques from the database.'''
    temp = []
    for i in db:
        for item in i["techniques_used"]:
            if not item in temp:
                temp.append(item)
    temp.sort()
    return temp

def get_technique_stats(db):
    '''Check which projects that have certain techniques and then  returns the id and name of those projects.'''
    techs = get_techniques(db)
    key = ''
    temp = {}
    for item in techs:
        temp.update({item: []})
        for i in db:
            if item in i["techniques_used"]:
                temp[item].append({'id':i["project_no"], "name":i["project_name"]})
        temp[item] = sorted(temp[item], key=itemgetter('id'))
    return temp
                
#---------homemade functions-------
def search_field_none(db, search):
    free_list = []
    for i in db:
            for item in i.items():
                if isinstance(item[1], str):
                    words_search = item[1].split()
                    if isinstance(search, str):
                        key_words = search.split()
                    else:
                        key_words = search
                    for s_word in words_search:
                        for k_word in key_words: 
                            if s_word.lower() == k_word.lower():
                                if i not in free_list:
                                    free_list.append(i)
                            elif item[0].lower() == k_word.lower():
                                if i not in free_list:
                                    free_list.append(i)
                else:
                    if item[1] == search:
                        free_list.append(i)
                    elif item[0] == search:
                        free_list.append(i)

    return free_list

def search_field_given(db, search):
    free_list = []
    for project in db:
            for item in project.items():
                for j in search_fields:
                    if isinstance(item[1], int):
                        if item[0] == j and item[1] == search:
                            free_list.append(project)
                    elif isinstance(item[i], list):
                        if item[0] == j and item[1] == search:
                            free_list.append(project) 
                    elif isinstance(item[1], str):
                        if item[0].lower() == j.lower() and item[1].lower() == search.lower():
                            free_list.append(project)
    return free_list

def get_all_data(db, search, search_fields):
    '''This is a sub function to the search function. This function search the database for the keyword entered.'''
    free_list = []
    i = 0
    if search == None and search_fields == None:
        return db
    if search_fields == None:
        free_list = search_field_none(db, search)
    elif search_fields == '':
        return None
    else:
        free_list = search_field_given(db, search)

    if free_list != []:                                           #tilläg
        return free_list
    else: return None

def convert_lower(string):
    return string.lower()

def sort_data(data, sort_by="project_no", sort_order ='desc'):
    '''this function sorts the data that the search function gathered.'''
    data.sort(key=itemgetter(sort_by), reverse=(sort_order=='desc'))

def techs_used(search, techs):
    '''this function checks if the projects that the search function gathered have certain techniques.'''
    temp = []
    for i in search:
        for tech in techs: 
            if tech in i['techniques_used']:
                if i not in temp:
                    temp.append(i)
    return temp

def get_sort_order(value):
    '''this function determine if you are going to sort the information gathered by the search function in ascending or descending order.'''
    if value == 'desc':
        return True
    else:
        return False
    
#------bullshit functions-------

def main():
    db = load("data.json")
    print(get_project_count(db))
    #get_project(db, 2)
    #get_techniques(db)
    #print(get_technique_stats(db))
    print(len(search(db, sort_by='start_date', sort_order='desc', techniques=None, search='tetris', search_fields=None)))


if __name__ == "__main__":
    main()
