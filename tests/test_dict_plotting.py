#!/usr/bin/env pyton
# ---------------------------*-python-*----------------------------------------#
# file   test_dict_plotting.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
import sys

sys.path.append('..')

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))+"/"

import unittest, tempfile
import shlex

from opppy.output import *
from opppy.plot_dictionary import *
from opppy.version import __version__

class test_dict_plotting(unittest.TestCase):
 
  def test_plot_dictionary(self):
    '''
    This test the append_pickle function
    '''
    from my_test_opppy_parser import my_test_opppy_parser

    # initialize the parser
    opppy_parser = my_test_opppy_parser()
  
    # initialize a new data dictionary
    data = {}
    data['version'] = __version__
  
    # Append the thrid output file
    output_files = [dir_path+"output_example1.txt",dir_path+"output_example2.txt",dir_path+"output_example3.txt"]
    # Build initial pickle
    append_output_dictionary(data, output_files, opppy_parser)

    print(data)
    
    ploter = plot_dictionary()
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_dir_path = tmp_dir.name + "/"
    plot_string = "-dn density -y mat1 -x time -sa "+tmp_dir_path+"test.png --hide_plot"

    # generate the plotting arguments
    args = ploter.parse_input_string(plot_string)
    
    # check if data is available 
    print("Is data available ",ploter.is_data_available(args, data))

    # generate a plot given my plotting arguments, dictionary, and data name
    ploter.plot_dict(args, [data], ["my_test_dict"])
