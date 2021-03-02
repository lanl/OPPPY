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

import unittest
from test import support

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
  
    # initialize a new data dictionary
    data2 = {}
    data2['version'] = __version__
  
  
    # Append the thrid tally file
    tally_files = [dir_path+"example_tally1.txt",dir_path+"example_tally2.txt",dir_path+"example_tally3.txt"]
    # Build initial pickle
    append_tally_dictionary(data2, tally_files, opppy_parser)

    print(data2)
  
  
def test_main():
  support.run_unittest(test_opppy_tally)

if __name__ == '__main__':
  test_main()
