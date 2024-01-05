#!/usr/bin/env pyton
# ---------------------------*-python-*----------------------------------------#
# file   test_dump_ploter.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
import sys
import matplotlib.pyplot as PyPlot

sys.path.append('..')

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))+"/"

import unittest
from test import support

from opppy.plot_dump_dictionary import *

class test_opppy_dump_utils(unittest.TestCase):

    def test_1d_dump_ploter(self):
        '''
        Thest the three different point value extraction functions
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        filename = dir_path+"example_dump.txt"
        # extract all data from the example dump file
        data = dump_parser.build_data_dictionary(filename)
        
        my_dumps = [data]
        names = [filename]

        dump_1d_ploter = plot_1d_dump_dictionary();

        plot_string = '-x cell_id -y temperature'
        args = dump_1d_ploter.parse_input_string(plot_string)

        print("Is data available", dump_1d_ploter.is_data_available(args, data))

        # generate a plot given my plotting arguments, dictionary, and data name
        dump_1d_ploter.plot_1d(args, my_dumps, names)

        # extract all data from the other example dump file
        filename = dir_path+"example_dump2.txt"
        names.append(filename)
        my_dumps.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path+"example_dump3.txt"
        names.append(filename)
        my_dumps.append(dump_parser.build_data_dictionary(filename))
        
        # generate a plot given my plotting arguments, dictionary, and data name
        dump_1d_ploter.plot_1d(args, my_dumps, names)

    def test_2d_dump_ploter(self):
        '''
        Thest the three different point value extraction functions
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        filename = dir_path+"example_dump.txt"
        # extract all data from the example dump file
        data = dump_parser.build_data_dictionary(filename)
        
        dump_2d_ploter = plot_2d_dump_dictionary();

        # using interpolate
        plot_string = '-x x -y y -d temperature'
        args = dump_2d_ploter.parse_input_string(plot_string)

        print("Is data available", dump_2d_ploter.is_data_available(args, data))

        # generate a plot given my plotting arguments, dictionary, and data name
        dump_2d_ploter.plot_2d(args, data)

        # using polygon patches
        plot_string = '-x x -y y -d temperature -v xy_verts -sm'
        args = dump_2d_ploter.parse_input_string(plot_string)

        # generate a plot given my plotting arguments, dictionary, and data name
        dump_2d_ploter.plot_2d(args, data)

        # using polygon patches with contour lines
        plot_string = '-x x -y y -d temperature -v xy_verts -sm -cl'
        args = dump_2d_ploter.parse_input_string(plot_string)

        # generate a plot given my plotting arguments, dictionary, and data name
        dump_2d_ploter.plot_2d(args, data)

        # using polygon patches with contour lines and set contour levels
        plot_string = '-x x -y y -d temperature -v xy_verts -sm -cl -clev 10.0 12.0 12.5 13.0'
        args = dump_2d_ploter.parse_input_string(plot_string)

        # generate a plot given my plotting arguments, dictionary, and data name
        dump_2d_ploter.plot_2d(args, data)

        # using contour lines
        plot_string = '-x x -y y -d temperature -cl'
        args = dump_2d_ploter.parse_input_string(plot_string)

        # generate a plot given my plotting arguments, dictionary, and data name
        dump_2d_ploter.plot_2d(args, data)

        # using contour lines with contour levels
        plot_string = '-x x -y y -d temperature -cl -clev 10.0 12.0 12.5 13.0'
        args = dump_2d_ploter.parse_input_string(plot_string)

        # generate a plot given my plotting arguments, dictionary, and data name
        dump_2d_ploter.plot_2d(args, data)

        # using contour map
        plot_string = '-x x -y y -d temperature -cm'
        args = dump_2d_ploter.parse_input_string(plot_string)

        # generate a plot given my plotting arguments, dictionary, and data name
        dump_2d_ploter.plot_2d(args, data)

        # using contour map with contour levels
        plot_string = '-x x -y y -d temperature -cm -clev 10.0 12.0 12.5 13.0'
        args = dump_2d_ploter.parse_input_string(plot_string)

        # generate a plot given my plotting arguments, dictionary, and data name
        dump_2d_ploter.plot_2d(args, data)




    def test_3d_dump_ploter(self):
        '''
        Thest the three different point value extraction functions
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        filename = dir_path+"example_dump.txt"
        # extract all data from the example dump file
        data = dump_parser.build_data_dictionary(filename)
        
        dump_3d_ploter = plot_3d_dump_dictionary();

        plot_string = '-x z -y y -z x -zs 5 -d temperature'
        args = dump_3d_ploter.parse_input_string(plot_string)

        print("Is data available", dump_3d_ploter.is_data_available(args, data))

        # generate a plot given my plotting arguments, dictionary, and data name
        dump_3d_ploter.plot_3d_slice(args, data)

    def test_point_series_plot(self):
        '''
        This test the ability to plot series data using the dump_1d_ploter
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        filename = dir_path+"example_dump.txt"
        names = [filename]
        # extract all data from the example dump file
        data = [dump_parser.build_data_dictionary(filename)]
        filename = dir_path+"example_dump2.txt"
        names.append(filename)
        data.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path+"example_dump3.txt"
        names.append(filename)
        data.append(dump_parser.build_data_dictionary(filename))

        series_data = []
        series_data_names = []
        density_series_data = {}
        tracer_x, tracer_y = extract_series_point(data,'time',"density",['x','y','z'], [1.0,2.0,5.0])
        # add data to series dictionary
        density_series_data.update(tracer_x)
        density_series_data.update(tracer_y)
        series_data.append(density_series_data)
        series_data_names.append("original_density")

        # fake a second series that has two times the density
        density_2x_series_data = {}
        density_2x_series_data.update(tracer_x)
        tracer_y["density"]=tracer_y["density"]*2.0
        density_2x_series_data.update(tracer_y)

        series_data.append(density_2x_series_data)
        series_data_names.append("2x_density")

        dump_1d_ploter = plot_1d_dump_dictionary();

        plot_string = '-x time -y density'
        args = dump_1d_ploter.parse_input_string(plot_string)

        print("Is data available", dump_1d_ploter.is_data_available(args, series_data))

        # generate a plot given my plotting arguments, dictionary, and data name
        dump_1d_ploter.plot_1d(args, series_data, series_data_names)

    def test_line_series_plot(self):
        '''
        This test the ability to plot series data using the dump_1d_ploter
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        filename = dir_path+"example_dump.txt"
        names = [filename]
        # extract all data from the example dump file
        data = [dump_parser.build_data_dictionary(filename)]
        filename = dir_path+"example_dump2.txt"
        names.append(filename)
        data.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path+"example_dump3.txt"
        names.append(filename)
        data.append(dump_parser.build_data_dictionary(filename))

        tracer_t, tracer_grid = extract_series_line(data,'time',"temperature",['x'], [1.0],  [5.0], npts=5 )
        series_data = [series_pair(tracer_t, tracer_grid)]
        series_data_names = ['temperature_series']

        line_series_ploter = plot_line_series_dictionary();

        plot_string = '-x distance -y temperature -ly'
        args = line_series_ploter.parse_input_string(plot_string)

        print("Is data available", line_series_ploter.is_data_available(args, series_data))

        # generate a plot given my plotting arguments, dictionary, and data name
        line_series_ploter.plot_1d_series(args, series_data, series_data_names)

    def test_contour_series_plot(self):
        '''
        This test the ability to plot series data using the dump_1d_ploter
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        filename = dir_path+"example_dump.txt"
        names = [filename]
        # extract all data from the example dump file
        data = [dump_parser.build_data_dictionary(filename)]
        filename = dir_path+"example_dump2.txt"
        names.append(filename)
        data.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path+"example_dump3.txt"
        names.append(filename)
        data.append(dump_parser.build_data_dictionary(filename))

        tracer_t, tracer_grid = extract_series_2d(data,'time',"temperature",['x','y'], npts=5 )
        series_data = series_pair(tracer_t, tracer_grid)

        contour_series_ploter = plot_2d_series_dictionary();

        plot_string = '-x x -y y -d temperature -xlab test_x'
        args = contour_series_ploter.parse_input_string(plot_string)

        print("Is data available", contour_series_ploter.is_data_available(args, series_data))

        # generate a plot given my plotting arguments, dictionary, and data name
        contour_series_ploter.plot_2d_series(args, series_data)

        tracer_t, tracer_grid = extract_series_2d_slice(data,'time',"temperature",['z','y','x'], 5.0, npts=10 )
        series_data = series_pair(tracer_t, tracer_grid)

        plot_string = '-x z -y y -d temperature -xlab test_x'
        args = contour_series_ploter.parse_input_string(plot_string)

        print("Is data available", contour_series_ploter.is_data_available(args, series_data))
        # generate a plot given my plotting arguments, dictionary, and data name
        contour_series_ploter.plot_2d_series(args, series_data)
