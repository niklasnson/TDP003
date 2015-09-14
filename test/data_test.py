#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011, IDA, Linköping University
# Copyright (C) 2011, Torbjörn Lönnemark <tobbez@ryara.net>
# Copyright (C) 2014, Daniel Persson
import unittest
import data
import hashlib
import sys
from operator import itemgetter

def print_tech_dict(d):
    for k,v in d.items():
        print("{}: {}".format(k,v))
        for e in v:
            print(e)
        print()

def sort_dict(d,sort_key):
    for k in d.keys():
        d[k] = sorted(d[k], key = itemgetter(sort_key))
    return d;

md5 = hashlib.md5
class DataTest(unittest.TestCase):
    def setUp(self):
        self.expected_data = [{'big_image': 'XXX',
                               'project_name': 'python data-module test script',
                               'course_name': 'OK\xc4NT',
                               'group_size': 2, 'end_date': '2009-09-06',
                               'techniques_used': ['python'],
                               'academic_credits': 'WUT?',
                               'small_image': 'X',
                               'long_description': 'no no no',
                               'course_id': 'TDP003',
                               'project_no': 1,
                               'external_link': 'YY',
                               'short_description': 'no',
                               'start_date': '2009-09-05',
                               'lulz_had': 'many'},
                              {'big_image': 'XXX',
                               'project_name': 'NEJ',
                               'course_name': 'OK\xc4NT',
                               'group_size': 4,
                               'end_date': '2009-09-08',
                               'techniques_used': ['c++', 'csv', 'python'],
                               'academic_credits': 'WUT?',
                               'small_image': 'X',
                               'long_description': 'no no no',
                               'course_id': 'TDP003',
                               'project_no': 3,
                               'external_link': 'YY',
                               'short_description': 'no',
                               'start_date': '2009-09-07',
                               'lulz_had': 'few'},
                              {'big_image': 'XXX',
                               'project_name': '2007',
                               'course_name': 'OK\xc4NT',
                               'group_size': 6,
                               'end_date': '2009-09-09',
                               'techniques_used': ['ada', 'python'],
                               'academic_credits': 'WUT?',
                               'small_image': 'X',
                               'long_description': 'no no no',
                               'course_id': 'TDP003',
                               'project_no': 2,
                               'external_link': 'YY',
                               'short_description': 'no',
                               'start_date': '2009-09-08',
                               'lulz_had': 'medium'},
                              {'big_image': 'XXX',
                               'project_name': ',',
                               'course_name': 'HOHO',
                               'group_size': 8,
                               'end_date': '2009-09-07',
                               'techniques_used': [],
                               'academic_credits': 'WUT?',
                               'small_image': 'X',
                               'long_description': 'no no no',
                               'course_id': ' "',
                               'project_no': 4,
                               'external_link': 'YY',
                               'short_description': 'no',
                               'start_date': '2009-09-06',
                               'lulz_had': 'over 9000'}
                              ]
        self.expected_data = sorted(self.expected_data, key=itemgetter('project_no'))

        self.expected_technique_data = ['ada', 'c++', 'csv', 'python']
        self.expected_technique_stat_data = {'python': [{'id': 2, 'name': '2007'},
                                                        {'id': 3, 'name': 'NEJ'},
                                                        {'id': 1, 'name': 'python data-module test script'}],
                                             'csv': [{'id': 3, 'name': 'NEJ'}],
                                             'c++': [{'id': 3, 'name': 'NEJ'}],
                                             'ada': [{'id': 2, 'name': '2007'}]}
        self.loaded_data = sorted(data.load("data.json"), key=itemgetter('project_no'))

    def test_load(self):
        self.assertEqual(self.loaded_data, self.expected_data)
        self.assertEqual(data.load("/dev/this_file_does_not_exist"), None)

    def test_get_project_count(self):
        self.assertEqual(data.get_project_count(self.loaded_data), 4)
        
    def test_get_project(self):
        self.assertEqual(data.get_project(self.loaded_data, 1)['project_no'], 1)
        self.assertEqual(data.get_project(self.loaded_data, 2)['project_no'], 2)
        self.assertEqual(data.get_project(self.loaded_data, 3)['project_no'], 3)
        self.assertEqual(data.get_project(self.loaded_data, 4)['project_no'], 4)
        self.assertEqual(data.get_project(self.loaded_data, 42), None)

    def test_search(self):
        self.assertEqual(len(data.search(self.loaded_data)), 4)

        self.assertEqual(len(data.search(self.loaded_data, techniques=['csv'])), 1)

        res = data.search(self.loaded_data, sort_order='asc',techniques=["python"])
        #Hur avgör vi ordningen i detta fall? Jo genom start_date
#        self.assertEqual(res[0]['project_no'], 2) #2
#        self.assertEqual(res[1]['project_no'], 3) #3
#        self.assertEqual(res[2]['project_no'], 1) #1
        self.assertEqual(res[0]['start_date'], '2009-09-05')
        self.assertEqual(res[1]['start_date'], '2009-09-07')
        self.assertEqual(res[2]['start_date'], '2009-09-08')


        res = data.search(self.loaded_data, 
                                     sort_by="end_date", 
                                     search='okänt', 
                                     search_fields=['project_no','project_name','course_name'])
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0]['project_no'], 2)
        self.assertEqual(res[1]['project_no'], 3)
        self.assertEqual(res[2]['project_no'], 1)
        print('here')
        
        res = data.search(self.loaded_data, 
                                     search="okänt", 
                                     search_fields=["project_no","project_name","course_name"])
        self.assertEqual(len(res), 3)

        res = data.search(self.loaded_data,
                                     techniques=[],
                                     search="okänt",
                                     search_fields=["project_no","project_name","course_name"])
        self.assertEqual(len(res), 3)

        res = data.search(self.loaded_data, search="okänt", search_fields=[])
        self.assertEqual(len(res), 0)
        res = data.search(self.loaded_data, sort_by='group_size')
#        print('loaded:')
#        for d in self.loaded_data:
#            print('no:',d['project_no'], 'size:', d['group_size'])
#        print('expected:')
#        for d in self.expected_data:
#            print('no:',d['project_no'], 'size:', d['group_size'])
#        print('search result:')
#        for d in res:
#            print('no:',d['project_no'], 'size:', d['group_size'])
        #default is descending order
        self.assertEqual(res[0]['project_no'], 4) #1
        self.assertEqual(res[1]['project_no'], 2) #2
        self.assertEqual(res[2]['project_no'], 3) #3
        self.assertEqual(res[3]['project_no'], 1) #4

    def test_get_techniques(self):
        res = data.get_techniques(self.loaded_data)
        self.assertEqual(res, self.expected_technique_data)

    def test_get_technique_stats(self):
        res = data.get_technique_stats(self.loaded_data)
   #     print("before sorted:")
   #     print_tech_dict(res)
        res = sort_dict(res,'id')
   #     print("after sorted:")
   #     print_tech_dict(res)
   #     print("res: ",res)
        
        self.expected_technique_stat_data = sort_dict(self.expected_technique_stat_data,'id')
    #    print_tech_dict(self.expected_technique_stat_data)

        self.assertEqual(res, self.expected_technique_stat_data)


if __name__ == '__main__':
    #print "Test:     ", md5.new(sys.argv[0]).hexdigest()
    #print "Test data:", md5.new("data.json").hexdigest()
    print ("Test:     ", md5(sys.argv[0].encode('UTF-8')).hexdigest())
    print ("Test data:", md5(b"data.json").hexdigest())
    print()
    unittest.main()
