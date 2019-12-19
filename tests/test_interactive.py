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
import unittest
from test import support
import shlex

class test_interactive_utils(unittest.TestCase):
    '''
    This test an example interactive plotter build with the
    interactive_output_parser class

    '''
    def test_help(self):
        os.system("python my_interactive_parser.py -h")
        os.system("python my_interactive_parser.py tally -h")
        os.system("python my_interactive_parser.py tally pickle -h")
        os.system("python my_interactive_parser.py tally iplot -h")
        os.system("python my_interactive_parser.py tally plot -h")
        os.system("python my_interactive_parser.py output -h")
        os.system("python my_interactive_parser.py output pickle -h")
        os.system("python my_interactive_parser.py output iplot -h")
        os.system("python my_interactive_parser.py output plot -h")
        os.system("python my_interactive_parser.py dump -h")
        os.system("python my_interactive_parser.py dump pickle -h")
        os.system("python my_interactive_parser.py dump 1d -h")
        os.system("python my_interactive_parser.py dump 2d -h")
        os.system("python my_interactive_parser.py dump 3d -h")
        os.system("python my_interactive_parser.py dump point -h")
        os.system("python my_interactive_parser.py dump line -h")

    def test_pickle_output(self):
        # This uses glob to pickle all the output data
        os.system("python my_interactive_parser.py output pickle -pf interactive.p -of output_example*.txt")

    def test_plot_pickle(self):
        # This uses glob to pickle all the output data
        os.system("python my_interactive_parser.py output pickle -pf interactive.p -of output_example*.txt")
        # This uses glob to pickle all the output data
        os.system("python my_interactive_parser.py output iplot -pf interactive.p < interactive_input.txt")
        # parse and plot the output data files
        os.system("python my_interactive_parser.py output iplot -of output_example*.txt < interactive_input.txt")

    def test_plot_dictionary(self):
        # This uses glob to pickle all the output data
        os.system("python my_interactive_parser.py output pickle -pf interactive.p -of output_example*.txt")
        # This uses glob to pickle all the output data
        os.system("python my_interactive_parser.py output plot -pf interactive.p -dn density -x time -y mat1 -sa density_mat1.png -hp")
        # parse and plot the output data files
        os.system("python my_interactive_parser.py output plot -of output_example*.txt -dn density -x time -y mat1 -sa density_mat1_pp.png -hp")

    def test_pickle_dumps(self):
        # This uses glob to pickle all the dump data
        os.system("python my_interactive_parser.py dump pickle -pf interactive_dump.p -df example_dump*.txt")

    def test_plot_dump(self):
        # This uses glob to pickle all the dump data
        os.system("python my_interactive_parser.py dump pickle -pf interactive_dump.p -df example_dump*.txt")

        # Parse and plot a 1d dump
        os.system("python my_interactive_parser.py dump 1d -dn example_dump.txt -x cell_id -y temperature")

        # Parse and plot a 1d dump
        os.system("python my_interactive_parser.py dump 1d -dn example_dump.txt -x cell_id -y temperature -kw cell_id temperature")

        # plot a 1d dump from a pickle file
        os.system("python my_interactive_parser.py dump 1d -dn example_dump.txt -pf interactive_dump.p -x cell_id -y temperature")

        # Parse and plot a 2d dump
        os.system("python my_interactive_parser.py dump 2d -dn example_dump.txt -x cell_id -y z -d temperature")

        # plot 2d dump from pickle file
        os.system("python my_interactive_parser.py dump 2d -dn example_dump.txt -pf interactive_dump.p -x cell_id -y z -d density")

        # Parse and plot a 2d dump only extract key_words
        os.system("python my_interactive_parser.py dump 2d -dn example_dump.txt -x cell_id -y z -d temperature -kw temperature cell_id z")

        # plot slice of 3d dump from dump file
        os.system("python my_interactive_parser.py dump 3d -dn example_dump.txt -x z -y y -z x -zs 5.0 -d temperature")

        # plot slice of 3d dump from pickle file
        os.system("python my_interactive_parser.py dump 3d -dn example_dump.txt -pf interactive_dump.p -x z -y y -z x -zs 5.0 -d temperature")

    def test_dump_series(self):
        # This uses glob to pickle all the dump data
        os.system("python my_interactive_parser.py dump pickle -pf interactive_dump.p -df example_dump*.txt")

        # Parse and plot a point series
        os.system("python my_interactive_parser.py dump point -df example_dump*.txt -df example_dump*.txt -dk x -p 5 -s time -d temperature -sy 10.0 -sy 1.0")

        # test individual scale x
        os.system("python my_interactive_parser.py dump point -df example_dump*.txt -df example_dump*.txt -dk x -p 5 -s time -d temperature -sx 10.0 -sx 1.0")

        # test scale all x
        os.system("python my_interactive_parser.py dump point -df example_dump*.txt -df example_dump*.txt -dk x -p 5 -s time -d temperature -sx 10.0")

        # test scale all y
        os.system("python my_interactive_parser.py dump point -df example_dump*.txt -df example_dump*.txt -dk x -p 5 -s time -d temperature -sy 10.0")

        # plot a point series from a pickled dump
        os.system("python my_interactive_parser.py dump point -pf interactive_dump.p interactive_dump.p -dk x -p 5 -s time -d temperature")

        # plot a line series from a pickled dump
        os.system("python my_interactive_parser.py dump line -pf interactive_dump.p interactive_dump.p -dk x -p0 1 -p1 5 -s time -d temperature")

        # plot a contour series from a pickled dump
        os.system("python my_interactive_parser.py dump contour -pf interactive_dump.p -dk x y -s time -d temperature -np 5")

        # plot a contour series slice from a 3d pickled dump
        os.system("python my_interactive_parser.py dump contour -pf interactive_dump.p -dk z y x -zs 5 -s time -d temperature")

    def test_pickle_tally(self):
        # This uses glob to pickle all the output data
        os.system("python my_interactive_parser.py tally pickle -pf interactive_tally.p -of example_tally*.txt")

    def test_plot_tally(self):
        # This uses glob to pickle all the output data
        os.system("python my_interactive_parser.py tally pickle -pf interactive_tally.p -tf example_tally*.txt")
        # This uses glob to pickle all the output data
        os.system("python my_interactive_parser.py tally iplot -pf interactive_tally.p < interactive_tally_input.txt")
        # parse and plot the output data files
        os.system("python my_interactive_parser.py tally iplot -tf example_tally*.txt < interactive_tally_input.txt")
        # parse and plot the output data files
        os.system("python my_interactive_parser.py tally plot -tf example_tally*.txt -sk cycle -dn cool_counts -x bins -xlab 'bin [#]'  -y odd_counts  -ylab 'Counts [#]'")
        os.system("python my_interactive_parser.py tally plot -pf interactive_tally.p -sk time -sv 5.0 -dn cool_counts -x bins -xlab 'bin [#]'  -y even_counts  -ylab 'Counts [#]'")
        # test scaling and log axis
        os.system("python my_interactive_parser.py tally plot -tf example_tally*.txt -tf example_tally*.txt -sk cycle -dn cool_counts -x bins -xlab 'bin [#]'  -y odd_counts  -ylab 'Counts  [#]' -lx -ly -sx 10 -sx 1e-3 -sy 10 -sy 1e-3 -xl 0.00001 1000 -yl 0.00001 10000")


 

def test_main():
  support.run_unittest(test_interactive_utils)

if __name__ == '__main__':
  unittest.main()
