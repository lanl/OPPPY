#!/usr/bin/env pyton
# ---------------------------*-python-*----------------------------------------#
# file   test_output.py
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

class test_opppy_outputs(unittest.TestCase):
  def test_get_output_lines(self):
    '''
    This tests get_output_lines in two ways. One extracts data using a
    file_end_string and one test does not. With the file_end_string
    the function should extract all information in the file. Without
    the file_end_string the function assumes that the final cycle data
    is incomplete so it is excluded from the final list of cycle data.
    '''
    # read all of the data
    cycle_strings = get_output_lines(dir_path+"example_output.txt","#cycle","#cycle","#end of file")
    print("All Data: ", cycle_strings)
    # only read cycle 1 data 
    cycle_strings2 = get_output_lines(dir_path+"example_output.txt","#cycle","#cycle")
    print("Cycle 1 Data:",cycle_strings2)
    # only read cycle 2 data
    cycle_strings3 = get_output_lines(dir_path+"example_output.txt","#cycle 2","#")
    print("Cycle 2 Data:", cycle_strings3)
    # only read cycle 2 data
    cycle_strings4 = get_output_lines(dir_path+"example_output.txt","#","#")
    print("No end file data:", cycle_strings4)
    # read nothing
    cycle_strings5 = get_output_lines(dir_path+"example_output.txt","#","junk")
    print("Bad end cycle string so no data:", cycle_strings5)
    # read nothing
    cycle_strings6 = get_output_lines(dir_path+"example_output.txt","junk","#")
    print("Bad start cycle string so no data:", cycle_strings6)
  
  def test_extract_cycle_data(self):
    '''
    This tests the extract cycle data. 
    '''
    # build up some simple cycle data
    my_cycle_string ='# cycle 1\ntime 1\ntest_data1 = 1\ntest_data2=10\n' 
    
    # import the test parser
    from my_test_opppy_parser import my_test_opppy_parser
  
    # initialize the parser
    opppy_parser = my_test_opppy_parser()
  
    my_dictionary = extract_cycle_data(my_cycle_string, opppy_parser)
  
    print(my_dictionary)
  
  
  def test_append_output_dictionary(self):
    '''
    This test the append_pickle function
    '''
   
    # import the test parser
    from my_test_opppy_parser import my_test_opppy_parser
    from opppy.version import __version__
  
    # initialize the parser
    opppy_parser = my_test_opppy_parser()
  
    # initialize the data dictionary
    data = {}
    data['version'] = __version__
  
    # Append the first output file
    output_files = [dir_path+"output_example1.txt"]
    # Build initial pickle
    append_output_dictionary(data, output_files, opppy_parser)

    print(data)
  
    # Append the second output file
    output_files = [dir_path+"output_example2.txt"]
    # Build initial pickle
    append_output_dictionary(data, output_files, opppy_parser)
  
    print(data)
    
    # Append the thrid output file
    output_files = [dir_path+"output_example3.txt"]
    # Build initial pickle
    append_output_dictionary(data, output_files, opppy_parser)

    print(data)
  
    # initialize a new data dictionary
    data2 = {}
    data2['version'] = __version__
  
  
    # Append the thrid output file
    output_files = [dir_path+"output_example1.txt",dir_path+"output_example2.txt",dir_path+"output_example3.txt"]
    # Build initial pickle
    append_output_dictionary(data2, output_files, opppy_parser)

    print(data2)
  
  
def test_main():
  support.run_unittest(test_opppy_outputs)

if __name__ == '__main__':
  test_main()
