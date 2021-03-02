#!/usr/bin/env pyton
# ---------------------------*-python-*----------------------------------------#
# file   test_output.py
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

from opppy.dump_utils import *
import unittest
from test import support

class test_opppy_dump_utils(unittest.TestCase):
    def test_dump_parser(self):
        '''
        Test a simple example opppy_dump parser
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        filename = dir_path + "example_dump.txt"
        # extract all data from the example dump file
        data = dump_parser.build_data_dictionary(filename)

        print(data)

        # extract a subset of data from the example dump file
        sub_data = dump_parser.build_data_dictionary(filename, ['time','density'])

        print(sub_data)

    def test_point_value(self):
        '''
        Thest the three different point value extraction functions
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        filename = dir_path + "example_dump.txt"
        # extract all data from the example dump file
        data = dump_parser.build_data_dictionary(filename)
        
        # extract a 1D data value
        point1d = point_value_1d(data, 'cell_id', 'pressure', 6.0);

        print(point1d)

        point2d = point_value_2d(data, 'x','y', 'temperature', 1.0, 2.0);

        print(point2d)
    
        print(data.keys())
        point3d = point_value_3d(data, 'x','y', 'z', 'density', 1.0, 2.0, 0.5);

        print(point3d)

    def test_point_series(self):
        '''
        Thest the three different point value extraction functions
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        data = []
        filename = dir_path + "example_dump.txt"
        # extract all data from the example dump file
        data.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path + "example_dump2.txt"
        data.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path + "example_dump3.txt"
        data.append(dump_parser.build_data_dictionary(filename))
        
        # extract a 1D data value
        tracer_x, tracer_y = extract_series_point(data,'time',"density",['x'], [1.0])
        print(tracer_x, tracer_y)
        tracer_x, tracer_y = extract_series_point(data,'time',"density",['x','y'], [1.0,2.0])
        print(tracer_x, tracer_y)
        tracer_x, tracer_y = extract_series_point(data,'time',"density",['x','y','z'], [1.0,2.0,5.0])
        print(tracer_x, tracer_y)

    

    def test_grid_data(self):
        '''
        Test the ability to extract contour
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        filename = dir_path + "example_dump.txt"
        # extract all data from the example dump file
        data = dump_parser.build_data_dictionary(filename)
        
        # extract data to a grid
        grid = data2grid(data, 'x', 'y', 'density')
        
        # plot the data as a check 
        PyPlot.imshow(grid['density'] , extent=(grid['x'].min(),grid['x'].max(),grid['y'].min(),grid['y'].max()), origin='lower')
        PyPlot.show()
        
        # plot the data in a bounding box
        gridbox = data2gridbox(data, 'x', 'y', 'density', 2.5, 1.0, 3.5, 1.8, method="linear")

        PyPlot.imshow(gridbox['density'] , extent=(gridbox['x'].min(),gridbox['x'].max(),gridbox['y'].min(),gridbox['y'].max()), origin='lower')
        PyPlot.show()

        # extract an x slice of data
        gridxslice = data2grid3Dslice(data, 'z', 'y', 'x', 'temperature', 5.0, npts=10,method='nearest')

        PyPlot.imshow(gridxslice['temperature'] , extent=(gridxslice['z'].min(),gridxslice['z'].max(),gridxslice['y'].min(),gridxslice['y'].max()), origin='lower')
        PyPlot.show()
        print(gridxslice['temperature'].T)

    def test_2D_series(self):
        '''
        Thest the 2D series function
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        data = []
        filename = dir_path + "example_dump.txt"
        # extract all data from the example dump file
        data.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path + "example_dump2.txt"
        data.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path + "example_dump3.txt"
        data.append(dump_parser.build_data_dictionary(filename))
        
        # extract a 1D data value
        tracer_t, tracer_grid = extract_series_2d(data,'time',"temperature",['x','y'], npts=5 )
        print(tracer_t, tracer_grid)
        tracer_t, tracer_grid = extract_series_2d(data,'time',"temperature",['x','y'], npts=5, box=[2.5, 1.0, 3.5, 1.8] )
        print(tracer_t, tracer_grid)

    def test_2D_slice_series(self):
        '''
        Thest the three different point value extraction functions
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        data = []
        filename = dir_path + "example_dump.txt"
        # extract all data from the example dump file
        data.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path + "example_dump2.txt"
        data.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path + "example_dump3.txt"
        data.append(dump_parser.build_data_dictionary(filename))
        
        # extract 2d plane data value
        tracer_t, tracer_grid = extract_series_2d_slice(data,'time',"temperature",['x','y','z'], 5.0, npts=5 )
        print(tracer_t, tracer_grid)



    def test_data_2_line(self):
        '''
        Test the ability to extract line data from 2 and 3D dump files
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        filename = dir_path + "example_dump.txt"
        # extract all data from the example dump file
        data = dump_parser.build_data_dictionary(filename)

        # plot the data in a bounding box
        x, y = data2line2d(data, 'x', 'y', 'temperature', 2.5, 1.0, 3.5, 1.8, npts=500, method="linear")

        PyPlot.plot(x, y)
        PyPlot.show()

        # plot the data in a bounding box
        x, y = data2line3d(data, 'x', 'y', 'z', 'temperature', 5.0, 1.0, 1.2,  5.0, 2.0, 1.75, npts=50, method="nearest")

        print(x,y)
        PyPlot.plot(x, y)
        PyPlot.show()

    def test_line_series(self):
        '''
        Thest the three different point value extraction functions
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        data = []
        filename = dir_path + "example_dump.txt"
        # extract all data from the example dump file
        data.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path + "example_dump2.txt"
        data.append(dump_parser.build_data_dictionary(filename))
        filename = dir_path + "example_dump3.txt"
        data.append(dump_parser.build_data_dictionary(filename))
        
        # extract a 1D data value
        tracer_t, tracer_grid = extract_series_line(data,'time',"temperature",['x'], [1.0],  [5.0], npts=5 )
        print(tracer_t, tracer_grid)
        tracer_t, tracer_grid = extract_series_line(data,'time',"temperature",['x','y'], [5.0, 1.0],  [5.0, 2.0], npts=5 )
        print(tracer_t, tracer_grid)
        tracer_t, tracer_grid = extract_series_line(data,'time',"temperature",['x','y','z'], [5.0, 1.0, 1.2],  [5.0, 2.0, 1.75], npts=5  )
        print(tracer_t, tracer_grid)
        


 
def test_main():
  support.run_unittest(test_opppy_dump_utils)

if __name__ == '__main__':
  test_main()
