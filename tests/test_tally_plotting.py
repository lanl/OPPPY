#!/usr/bin/env pyton
# ---------------------------*-python-*----------------------------------------#
# file   test_tally_plotting.py
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
import shlex

from opppy.tally import *
from opppy.plot_dictionary import *
from opppy.version import __version__

class test_dict_plotting(unittest.TestCase):
 
  def test_plot_tally(self):
    '''
    This test the append_pickle function
    '''
    from my_test_opppy_tally_parser import my_test_opppy_tally_parser

    # initialize the parser
    opppy_parser = my_test_opppy_tally_parser()
  
    # initialize a new data dictionary
    data = {}
    data['version'] = __version__
  
    # Append the thrid output file
    output_files = [dir_path+"example_tally1.txt",dir_path+"example_tally2.txt",dir_path+"example_tally3.txt"]
    # Build initial pickle
    append_tally_dictionary(data, output_files, opppy_parser)

    print(data)
    
    ploter = plot_dictionary()
    
    plot_time = 6.0
    for index, time in enumerate(data['time']):
        if time >= plot_time:
            break

    plot_string = "-dn cool_counts -y odd_counts -y even_counts -x bins" # -sa test.png --hide_plot"

    # generate the plotting arguments
    args = ploter.parse_input_string(plot_string)
    
    # check if data is available 
    print("Is data available ",ploter.is_data_available(args, data))

    # generate a plot given my plotting arguments, dictionary, and data name
    ploter.plot_dict(args, [data['tally_cycle_data'][index],data['tally_cycle_data'][index+1]], ["my_test_dict t ="+str(data['time'][index]), "my_test_dict t ="+str(data['time'][index+1])])
