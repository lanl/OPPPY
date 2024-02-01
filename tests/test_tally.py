#!/usr/bin/env pyton
# ---------------------------*-python-*----------------------------------------#
# file   test_tally.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
import sys

sys.path.append('..')

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))+"/"
OPPPY_UPGOLDS = os.getenv("OPPPY_UPGOLDS", 'False').lower() in ('true', '1', 't')

import unittest

from opppy.output import *
from opppy.tally import *

class test_opppy_tally(unittest.TestCase):
 
  def test_extract_cycle_data(self):
    '''
    This tests the extract cycle data. 
    '''
    # build up some simple cycle data
    my_cycle_string ='cycle: 1\ntime: 1.0\nbins: 1 2 3 4 5\nodd_counts: 1 2 5 7 9\neven_counts: 2 4 6 8 10\n\n' 
    
    # import the test parser
    from my_test_opppy_tally_parser import my_test_opppy_tally_parser
  
    # initialize the parser
    opppy_parser = my_test_opppy_tally_parser()
  
    my_dictionary = extract_cycle_data(my_cycle_string, opppy_parser)
    if(OPPPY_UPGOLDS):
        goldfile = open(dir_path+'gold_tally_extract_cycle.p', 'wb')
        pickle.dump(my_dictionary,goldfile)
        goldfile.close()

    goldfile = open(dir_path+'gold_tally_extract_cycle.p', 'rb')
    gold_data = pickle.load(goldfile)
    goldfile.close()
    for dic, gold_dic in zip(my_dictionary,gold_data):
        assert(dic==gold_dic)


    print(my_dictionary)
  
  
  def test_append_tally_dictionary(self):
    '''
    This test the append_pickle function
    '''
   
    # import the test parser
    from my_test_opppy_tally_parser import my_test_opppy_tally_parser
    from opppy.version import __version__
  
    # initialize the parser
    opppy_parser = my_test_opppy_tally_parser()
  
    # initialize the data dictionary
    data = {}
    data['version'] = __version__
  
    # Append the first output file
    tally_files = [dir_path+"example_tally1.txt"]
    # Build initial pickle
    append_tally_dictionary(data, tally_files, opppy_parser)

    print(data)
  
    # Append the second tally file
    tally_files = [dir_path+"example_tally2.txt"]
    # Build initial pickle
    append_tally_dictionary(data, tally_files, opppy_parser)
  
    print(data)
    
    # Append the thrid tally file
    tally_files = [dir_path+"example_tally3.txt"]
    # Build initial pickle
    append_tally_dictionary(data, tally_files, opppy_parser)

    print(data)
    if(OPPPY_UPGOLDS):
        goldfile = open(dir_path+'gold_tally.p', 'wb')
        pickle.dump(data,goldfile)
        goldfile.close()

    goldfile = open(dir_path+'gold_tally.p', 'rb')
    gold_data = pickle.load(goldfile)
    goldfile.close()
    # Don't check the version for a match
    gold_data.pop('version')
    data.pop('version')
    for dic, gold_dic in zip(data,gold_data):
        assert(dic==gold_dic)
  
    # initialize a new data dictionary
    data2 = {}
    data2['version'] = __version__
  
  
    # Append the thrid tally file
    tally_files = [dir_path+"example_tally1.txt",dir_path+"example_tally2.txt",dir_path+"example_tally3.txt"]
    # Build initial pickle
    append_tally_dictionary(data2, tally_files, opppy_parser)

    print(data2)
    # Don't check the version for a match
    data2.pop('version')
    for dic, gold_dic in zip(data2,gold_data):
        assert(dic==gold_dic)

    # initialize a new data dictionary
    data3 = {}
    data3['version'] = __version__
  
  
    # WITH THREADS
    # Append the thrid tally file
    tally_files = [dir_path+"example_tally1.txt",dir_path+"example_tally2.txt",dir_path+"example_tally3.txt"]
    # Build initial pickle
    append_tally_dictionary(data3, tally_files, opppy_parser, nthreads=-1)

    print(data3)
    # Don't check the version for a match
    data3.pop('version')
    for dic, gold_dic in zip(data3,gold_data):
        assert(dic==gold_dic)
