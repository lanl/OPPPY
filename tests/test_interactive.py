#!/usr/bin/env pyton
# ---------------------------*-python-*----------------------------------------#
# file   test_interactive.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
import sys

sys.path.append('..')

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))+"/"
os.chdir(dir_path)


import os
import unittest
import shlex

class test_interactive_utils(unittest.TestCase):
    '''
    This test an example interactive plotter build with the
    interactive_output_parser class

    '''
    def test_help(self):
        assert(os.system("python my_interactive_parser.py -h")==0)
        assert(os.system("python my_interactive_parser.py tally -h")==0)
        assert(os.system("python my_interactive_parser.py tally pickle -h")==0)
        assert(os.system("python my_interactive_parser.py tally iplot -h")==0)
        assert(os.system("python my_interactive_parser.py tally plot -h")==0)
        assert(os.system("python my_interactive_parser.py output -h")==0)
        assert(os.system("python my_interactive_parser.py output pickle -h")==0)
        assert(os.system("python my_interactive_parser.py output iplot -h")==0)
        assert(os.system("python my_interactive_parser.py output plot -h")==0)
        assert(os.system("python my_interactive_parser.py dump -h")==0)
        assert(os.system("python my_interactive_parser.py dump pickle -h")==0)
        assert(os.system("python my_interactive_parser.py dump 1d -h")==0)
        assert(os.system("python my_interactive_parser.py dump 2d -h")==0)
        assert(os.system("python my_interactive_parser.py dump 3d -h")==0)
        assert(os.system("python my_interactive_parser.py dump point -h")==0)
        assert(os.system("python my_interactive_parser.py dump line -h")==0)

    def test_pickle_output(self):
        # This uses glob to pickle all the output data
        assert(os.system("python my_interactive_parser.py output pickle -pf interactive.p -of "+dir_path+"output_example*.txt")==0)
        # Test no threads
        assert(os.system("OPPPY_USE_THREADS=False python my_interactive_parser.py output pickle -pf interactive.p -of "+dir_path+"output_example*.txt")==0)

    def test_plot_pickle(self):
        # This uses glob to pickle all the output data
        assert(os.system("python my_interactive_parser.py output pickle -pf interactive.p -of "+dir_path+"output_example*.txt")==0)
        # This uses glob to pickle all the output data
        assert(os.system("python my_interactive_parser.py output iplot -pf interactive.p < "+dir_path+"interactive_input.txt")==0)
        # parse and plot the output data files
        assert(os.system("python my_interactive_parser.py output iplot -of "+dir_path+"output_example*.txt < "+dir_path+"interactive_input.txt")==0)

    def test_plot_dictionary(self):
        # This uses glob to pickle all the output data
        assert(os.system("python my_interactive_parser.py output pickle -pf interactive.p -of "+dir_path+"output_example*.txt")==0)
        # This uses glob to pickle all the output data
        assert(os.system("python my_interactive_parser.py output plot -pf interactive.p -dn density -x time -y mat1 -sa density_mat1.png -hp")==0)
        # parse and plot the output data files
        assert(os.system("python my_interactive_parser.py output plot -of "+dir_path+"output_example*.txt -dn density -x time -y mat1 -sa density_mat1_pp.png -hp")==0)

    def test_pickle_dumps(self):
        # This uses glob to pickle all the dump data
        assert(os.system("python my_interactive_parser.py dump pickle -pf interactive_dump.p -df "+dir_path+"example_dump*.txt")==0)
        # Test serial parsing
        assert(os.system("OPPPY_USE_THREADS=False python my_interactive_parser.py dump pickle -pf interactive_dump.p -df "+dir_path+"example_dump*.txt")==0)

    def test_plot_dump(self):
        # This uses glob to pickle all the dump data
        assert(os.system("python my_interactive_parser.py dump pickle -pf interactive_dump.p -df "+dir_path+"example_dump*.txt")==0)

        # Parse and plot a 1d dump
        assert(os.system("python my_interactive_parser.py dump 1d -dn "+dir_path+"example_dump.txt -x cell_id -y temperature")==0)

        # Parse and plot a 1d dump
        assert(os.system("python my_interactive_parser.py dump 1d -dn "+dir_path+"example_dump.txt -x cell_id -y temperature -kw cell_id temperature")==0)

        # plot a 1d dump from a pickle file
        assert(os.system("python my_interactive_parser.py dump 1d -dn example_dump.txt -pf interactive_dump.p -x cell_id -y temperature")==0)

        # Parse and plot a 2d dump
        assert(os.system("python my_interactive_parser.py dump 2d -dn "+dir_path+"example_dump.txt -x cell_id -y z -d temperature")==0)

        # plot 2d dump from pickle file
        assert(os.system("python my_interactive_parser.py dump 2d -dn example_dump.txt -pf interactive_dump.p -x cell_id -y z -d density")==0)

        # Parse and plot a 2d dump only extract key_words
        assert(os.system("python my_interactive_parser.py dump 2d -dn "+dir_path+"example_dump.txt -x cell_id -y z -d temperature -kw temperature cell_id z -ls")==0)

        # plot slice of 3d dump from dump file
        assert(os.system("python my_interactive_parser.py dump 3d -dn "+dir_path+"example_dump.txt -x z -y y -z x -zs 5.0 -d temperature -ls")==0)

        # plot slice of 3d dump from pickle file
        assert(os.system("python my_interactive_parser.py dump 3d -dn example_dump.txt -pf interactive_dump.p -x z -y y -z x -zs 5.0 -d temperature")==0)

    def test_dump_series(self):
        # This uses glob to pickle all the dump data
        assert(os.system("python my_interactive_parser.py dump pickle -pf interactive_dump.p -df "+dir_path+"example_dump*.txt")==0)

        # Parse and plot a point series
        assert(os.system("python my_interactive_parser.py dump point -df "+dir_path+"example_dump*.txt -df "+dir_path+"example_dump*.txt -dk x -p 5 -s time -d temperature -sy 10.0 -sy 1.0")==0)

        # test individual scale x
        assert(os.system("python my_interactive_parser.py dump point -df "+dir_path+"example_dump*.txt -df "+dir_path+"example_dump*.txt -dk x -p 5 -s time -d temperature -sx 10.0 -sx 1.0")==0)

        # test scale all x
        assert(os.system("python my_interactive_parser.py dump point -df "+dir_path+"example_dump*.txt -df "+dir_path+"example_dump*.txt -dk x -p 5 -s time -d temperature -sx 10.0")==0)

        # test scale all y
        assert(os.system("python my_interactive_parser.py dump point -df "+dir_path+"example_dump*.txt -df "+dir_path+"example_dump*.txt -dk x -p 5 -s time -d temperature -sy 10.0")==0)

        # plot a point series from a pickled dump
        assert(os.system("python my_interactive_parser.py dump point -pf interactive_dump.p interactive_dump.p -dk x -p 5 -s time -d temperature")==0)

        # plot a line series from a pickled dump
        assert(os.system("python my_interactive_parser.py dump line -pf interactive_dump.p interactive_dump.p -dk x -p0 1 -p1 5 -s time -d temperature")==0)

        # plot a contour series from a pickled dump
        assert(os.system("python my_interactive_parser.py dump contour -pf interactive_dump.p -dk x y -s time -d temperature -np 5 -ls")==0)

        # plot a contour series slice from a 3d pickled dump
        assert(os.system("python my_interactive_parser.py dump contour -pf interactive_dump.p -dk z y x -zs 5 -s time -d temperature -ls")==0)

    def test_pickle_tally(self):
        # This uses glob to pickle all the output data
        assert(os.system("python my_interactive_parser.py tally pickle -pf interactive_tally.p -tf "+dir_path+"example_tally*.txt")==0)
        # Test Serial parsing
        assert(os.system("OPPPY_USE_THREADS=False python my_interactive_parser.py tally pickle -pf interactive_tally.p -tf "+dir_path+"example_tally*.txt")==0)

    def test_plot_tally(self):
        # This uses glob to pickle all the output data
        assert(os.system("python my_interactive_parser.py tally pickle -pf interactive_tally.p -tf "+dir_path+"example_tally*.txt")==0)
        # This uses glob to pickle all the output data
        assert(os.system("python my_interactive_parser.py tally iplot -pf interactive_tally.p < "+dir_path+"interactive_tally_input.txt")==0)
        # parse and plot the output data files
        assert(os.system("python my_interactive_parser.py tally iplot -tf "+dir_path+"example_tally*.txt < "+dir_path+"interactive_tally_input.txt")==0)
        # parse and plot the output data files
        assert(os.system("python my_interactive_parser.py tally plot -tf "+dir_path+"example_tally*.txt -sk cycle -dn cool_counts -x bins -xlab 'bin [#]'  -y odd_counts  -ylab 'Counts [#]'")==0)
        assert(os.system("python my_interactive_parser.py tally plot -pf interactive_tally.p -sk time -sv 5.0 -dn cool_counts -x bins -xlab 'bin [#]'  -y even_counts  -ylab 'Counts [#]'")==0)
        # test scaling and log axis
        assert(os.system("python my_interactive_parser.py tally plot -tf "+dir_path+"example_tally*.txt -tf "+dir_path+"example_tally*.txt -sk cycle -dn cool_counts -x bins -xlab 'bin [#]'  -y odd_counts  -ylab 'Counts  [#]' -lx -ly -sx 10 -sx 1e-3 -sy 10 -sy 1e-3 -xl 0.00001 1000 -yl 0.00001 10000")==0)
