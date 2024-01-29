#!/usr/bin/env pyton
# ---------------------------*-python-*----------------------------------------#
# file   test_output.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
import sys
import numpy as np

sys.path.append('..')

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))+"/"
OPPPY_UPGOLDS = os.getenv("OPPPY_UPGOLDS", 'False').lower() in ('true', '1', 't')

# suppress plotting for pytest
SHOW_PLOTS = os.getenv("SHOW_PLOTS", 'False').lower() in ('true', '1', 't')
import matplotlib
if(not SHOW_PLOTS):
    matplotlib.use('Agg')
import matplotlib.pyplot as PyPlot


from opppy.dump_utils import *
import unittest
import collections.abc

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
        if(OPPPY_UPGOLDS):
            goldfile = open(dir_path+'gold_dump0.p', 'wb')
            pickle.dump(data,goldfile)
            goldfile.close()

        goldfile = open(dir_path+'gold_dump0.p', 'rb')
        gold_data = pickle.load(goldfile)
        goldfile.close()
        print(data)
        print(gold_data)
        assert(data.keys()==gold_data.keys())
        for k, v in gold_data.items():
            try:
                np.testing.assert_allclose(data[k],v)
            except:
                assert(data[k]==v)


        # extract a subset of data from the example dump file
        sub_data = dump_parser.build_data_dictionary(filename, ['time','density'])

        print(sub_data)
        assert(data!=sub_data)
        if(OPPPY_UPGOLDS):
            goldfile = open(dir_path+'gold_sub_dump0.p', 'wb')
            pickle.dump(sub_data,goldfile)
            goldfile.close()

        goldfile = open(dir_path+'gold_sub_dump0.p', 'rb')
        gold_data = pickle.load(goldfile)
        goldfile.close()
        assert(sub_data.keys()==gold_data.keys())
        for k, v in gold_data.items():
            try:
                np.testing.assert_allclose(sub_data[k],v)
            except:
                assert(sub_data[k]==v)

    def test_append_dump_dictionary(self):
        '''
        This test the append_pickle function
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser
        from opppy.version import __version__

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        # initialize the data dictionary
        data = {}
        data['version'] = __version__
      
        # Append the first output file
        filenames = [dir_path + "example_dump.txt"]
        # Build initial pickle
        append_dumps(data, filenames, dump_parser)
     
        print(data)
      
        # Append the second output file
        filenames = [dir_path + "example_dump2.txt"]
        # Build initial pickle
        append_dumps(data, filenames, dump_parser)
      
        print(data)
        
        # Append the thrid output file
        filenames = [dir_path + "example_dump3.txt"]
        # Build initial pickle
        append_dumps(data, filenames, dump_parser)
     
        if(OPPPY_UPGOLDS):
            goldfile = open(dir_path+'gold_dumps.p', 'wb')
            pickle.dump(data,goldfile)
            goldfile.close()

        goldfile = open(dir_path+'gold_dumps.p', 'rb')
        gold_data = pickle.load(goldfile)
        goldfile.close()
        print(data)
        data.pop('version')
        gold_data.pop('version')
        assert(data.keys()==gold_data.keys())
        for dump_name, dump_dic in gold_data.items():
            assert(data[dump_name].keys()==dump_dic.keys())
            for k, v in dump_dic.items():
                try:
                    np.testing.assert_allclose(data[dump_name][k],v)
                except:
                    assert(data[dump_name][k]==v)

        # initialize a new data dictionary
        data2 = {}
        data2['version'] = __version__
      
      
        # Append the thrid output file
        filenames = [dir_path+"example_dump.txt",dir_path+"example_dump2.txt",dir_path+"example_dump3.txt"]
        # Build initial pickle
        append_dumps(data2, filenames, dump_parser)
     
        print(data2)
        # Don't check the version for a match
        data2.pop('version')
        assert(data2.keys()==gold_data.keys())
        for dump_name, dump_dic in gold_data.items():
            assert(data2[dump_name].keys()==dump_dic.keys())
            for k, v in dump_dic.items():
                try:
                    np.testing.assert_allclose(data2[dump_name][k],v)
                except:
                    assert(data2[dump_name][k]==v)

        # TEST WITH THREADS
        # initialize a new data dictionary
        data3 = {}
        data3['version'] = __version__
      
      
        # Append the thrid output file
        filenames = [dir_path+"example_dump.txt",dir_path+"example_dump2.txt",dir_path+"example_dump3.txt"]
        # Build initial pickle
        append_dumps(data3, filenames, dump_parser, nthreads=-1)
     
        print(data3)
        # Don't check the version for a match
        data3.pop('version')
        assert(data3.keys()==gold_data.keys())
        for dump_name, dump_dic in gold_data.items():
            assert(data3[dump_name].keys()==dump_dic.keys())
            for k, v in dump_dic.items():
                try:
                    np.testing.assert_allclose(data3[dump_name][k],v)
                except:
                    assert(data3[dump_name][k]==v)


        # extract subset of dump data
        sub_data = {}
        sub_data['version'] = __version__
        filenames = [dir_path+"example_dump.txt",dir_path+"example_dump2.txt",dir_path+"example_dump3.txt"]
        # Build initial pickle
        append_dumps(sub_data, filenames, dump_parser, ['time','density'])
     
        print(sub_data)
        if(OPPPY_UPGOLDS):
            goldfile = open(dir_path+'gold_sub_dumps.p', 'wb')
            pickle.dump(sub_data,goldfile)
            goldfile.close()

        goldfile = open(dir_path+'gold_sub_dumps.p', 'rb')
        gold_data = pickle.load(goldfile)
        goldfile.close()
        sub_data.pop('version')
        gold_data.pop('version')
        assert(sub_data.keys()==gold_data.keys())
        for dump_name, dump_dic in gold_data.items():
            assert(sub_data[dump_name].keys()==dump_dic.keys())
            for k, v in dump_dic.items():
                try:
                    np.testing.assert_allclose(sub_data[dump_name][k],v)
                except:
                    assert(sub_data[dump_name][k]==v)

        # TEST WITH THREADS
        # extract subset of dump data
        sub_data2 = {}
        sub_data2['version'] = __version__
        filenames = [dir_path+"example_dump.txt",dir_path+"example_dump2.txt",dir_path+"example_dump3.txt"]
        # Build initial pickle
        append_dumps(sub_data2, filenames, dump_parser, ['time','density'], nthreads=-1)
     
        sub_data2.pop('version')
        assert(sub_data2.keys()==gold_data.keys())
        for dump_name, dump_dic in gold_data.items():
            assert(sub_data2[dump_name].keys()==dump_dic.keys())
            for k, v in dump_dic.items():
                try:
                    np.testing.assert_allclose(sub_data2[dump_name][k],v)
                except:
                    assert(sub_data2[dump_name][k]==v)



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
        point_data = {}       
        # extract a 1D data value
        point1d = point_value_1d(data, 'cell_id', 'pressure', 6.0);
        point_data['poin1d'] = point1d
        print(point1d)

        point2d = point_value_2d(data, 'x','y', 'temperature', 1.0, 2.0);
        point_data['poin2d'] = point2d

        print(point2d)
    
        print(data.keys())
        point3d = point_value_3d(data, 'x','y', 'z', 'density', 1.0, 2.0, 0.5);
        point_data['poin3d'] = point3d

        print(point3d)
        if(OPPPY_UPGOLDS):
            goldfile = open(dir_path+'gold_point_data.p', 'wb')
            pickle.dump(point_data,goldfile)
            goldfile.close()

        goldfile = open(dir_path+'gold_point_data.p', 'rb')
        gold_data = pickle.load(goldfile)
        goldfile.close()
        assert(point_data == gold_data)


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
        tracer_data = {}
        # extract a 1D data value
        tracer_x, tracer_y = extract_series_point(data,'time',"density",['x'], [1.0])
        tracer_data["tracerx1"] = np.array([ x[0] for x in tracer_x['time']])
        tracer_data["tracery1"] = tracer_y['density']
        print(tracer_x, tracer_y)
        tracer_x, tracer_y = extract_series_point(data,'time',"density",['x','y'], [1.0,2.0])
        tracer_data["tracerx2"] = np.array([ x[0] for x in tracer_x['time']])

        tracer_data["tracery2"] = tracer_y['density']
        print(tracer_x, tracer_y)
        tracer_x, tracer_y = extract_series_point(data,'time',"density",['x','y','z'], [1.0,2.0,5.0])
        tracer_data["tracerx3"] = np.array([ x[0] for x in tracer_x['time']])
        tracer_data["tracery3"] = tracer_y['density']
        print(tracer_x, tracer_y)
        if(OPPPY_UPGOLDS):
            goldfile = open(dir_path+'gold_tracer_data.p', 'wb')
            pickle.dump(tracer_data,goldfile)
            goldfile.close()

        goldfile = open(dir_path+'gold_tracer_data.p', 'rb')
        gold_data = pickle.load(goldfile)
        goldfile.close()
        for k, v in gold_data.items():
            np.testing.assert_allclose(tracer_data[k],v)


    

    def test_grid_data(self):
        '''
        Test the ability to extract contour
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser
        import warnings
        warnings.filterwarnings("ignore")

        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        filename = dir_path + "example_dump.txt"
        # extract all data from the example dump file
        data = dump_parser.build_data_dictionary(filename)
        check_data = {}
        # extract data to a grid
        grid = data2grid(data, 'x', 'y', 'density')
        check_data['grid'] = grid
        
        # plot the data as a check 
        PyPlot.imshow(grid['density'] , extent=(grid['x'].min(),grid['x'].max(),grid['y'].min(),grid['y'].max()), origin='lower')
        PyPlot.show()
        
        # plot the data in a bounding box
        gridbox = data2gridbox(data, 'x', 'y', 'density', 2.5, 1.0, 3.5, 1.8, method="linear")
        check_data['gridbox'] = gridbox

        PyPlot.imshow(gridbox['density'] , extent=(gridbox['x'].min(),gridbox['x'].max(),gridbox['y'].min(),gridbox['y'].max()), origin='lower')
        PyPlot.show()

        # extract an x slice of data
        gridxslice = data2grid3Dslice(data, 'z', 'y', 'x', 'temperature', 5.0, npts=10,method='nearest')
        check_data['gridxslice'] = gridxslice

        PyPlot.imshow(gridxslice['temperature'] , extent=(gridxslice['z'].min(),gridxslice['z'].max(),gridxslice['y'].min(),gridxslice['y'].max()), origin='lower')
        PyPlot.show()
        print(gridxslice['temperature'].T)
        if(OPPPY_UPGOLDS):
            goldfile = open(dir_path+'gold_grid_data.p', 'wb')
            pickle.dump(check_data,goldfile)
            goldfile.close()

        goldfile = open(dir_path+'gold_grid_data.p', 'rb')
        gold_data = pickle.load(goldfile)
        goldfile.close()
        for key, gold_dic in  gold_data.items():
            for k, v in gold_dic.items():
                np.testing.assert_allclose(check_data[key][k],v)



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
        check_data = {}
        # extract a 1D data value
        tracer_t, tracer_grid = extract_series_2d(data,'time',"temperature",['x','y'], npts=5 )
        check_data['time1'] = np.array([t[0] for t in tracer_t['time']])
        for i in range(len(check_data['time1'])):
            check_data['temperature1'+str(i)] = tracer_grid[i]['temperature']
            check_data['x1'+str(i)] = tracer_grid[i]['x']
            check_data['y1'+str(i)] = tracer_grid[i]['y']
        
        print(tracer_t, tracer_grid)
        tracer_t, tracer_grid = extract_series_2d(data,'time',"temperature",['x','y'], npts=5, box=[2.5, 1.0, 3.5, 1.8] )
        check_data['time2'] = np.array([t[0] for t in tracer_t['time']])
        for i in range(len(check_data['time2'])):
            check_data['temperature2'+str(i)] = tracer_grid[i]['temperature']
            check_data['x2'+str(i)] = tracer_grid[i]['x']
            check_data['y2'+str(i)] = tracer_grid[i]['y']

        print(tracer_t, tracer_grid)
        print(check_data)
        if(OPPPY_UPGOLDS):
            goldfile = open(dir_path+'gold_2d_tracer_data.p', 'wb')
            pickle.dump(check_data,goldfile)
            goldfile.close()

        goldfile = open(dir_path+'gold_2d_tracer_data.p', 'rb')
        gold_data = pickle.load(goldfile)
        goldfile.close()
        for k, v in  gold_data.items():
            np.testing.assert_allclose(check_data[k],v)


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
        check_data = {}
        # extract 2d plane data value
        tracer_t, tracer_grid = extract_series_2d_slice(data,'time',"temperature",['x','y','z'], 5.0, npts=5 )
        check_data['time'] = tracer_t['time']
        check_data['temperature'] = tracer_grid[0]['temperature']
        print(tracer_t, tracer_grid)

        if(OPPPY_UPGOLDS):
            goldfile = open(dir_path+'gold_2d_slice_tracer_data.p', 'wb')
            pickle.dump(check_data,goldfile)
            goldfile.close()

        goldfile = open(dir_path+'gold_2d_slice_tracer_data.p', 'rb')
        gold_data = pickle.load(goldfile)
        goldfile.close()
        for k, v in  gold_data.items():
            np.testing.assert_allclose(check_data[k],v)


    def test_data_2_line(self):
        '''
        Test the ability to extract line data from 2 and 3D dump files
        '''
        from my_test_opppy_dump_parser import my_test_opppy_dump_parser
        import warnings
        warnings.filterwarnings("ignore")


        # initialize my test dump parser
        dump_parser = my_test_opppy_dump_parser()
        
        filename = dir_path + "example_dump.txt"
        # extract all data from the example dump file
        data = dump_parser.build_data_dictionary(filename)

        check_data = {}
        # plot the data in a bounding box
        x, y = data2line2d(data, 'x', 'y', 'temperature', 2.5, 1.0, 3.5, 1.8, npts=500, method="linear")
        check_data['x1'] = x
        check_data['y1'] = y

        PyPlot.plot(x, y)
        PyPlot.show()

        # plot the data in a bounding box
        x, y = data2line3d(data, 'x', 'y', 'z', 'temperature', 5.0, 1.0, 1.2,  5.0, 2.0, 1.75, npts=50, method="nearest")
        check_data['x2'] = x
        check_data['y2'] = y


        print(x,y)
        PyPlot.plot(x, y)
        PyPlot.show()
        if(OPPPY_UPGOLDS):
            goldfile = open(dir_path+'gold_2d_line_data.p', 'wb')
            pickle.dump(check_data,goldfile)
            goldfile.close()

        goldfile = open(dir_path+'gold_2d_line_data.p', 'rb')
        gold_data = pickle.load(goldfile)
        goldfile.close()
        for k, v in  gold_data.items():
            np.testing.assert_allclose(check_data[k],v)

       

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
        
        check_data = {}
        # extract a 1D data value
        tracer_t, tracer_grid = extract_series_line(data,'time',"temperature",['x'], [1.0],  [5.0], npts=5 )
        check_data['time1'] = np.array([t[0] for t in tracer_t['time']])
        for i in range(len(check_data['time1'])):
            check_data['temperature1'+str(i)] = tracer_grid[i]['temperature']
            check_data['x1'+str(i)] = tracer_grid[i]['distance']
 
        print(tracer_t, tracer_grid)
        tracer_t, tracer_grid = extract_series_line(data,'time',"temperature",['x','y'], [5.0, 1.0],  [5.0, 2.0], npts=5 )
        check_data['time2'] = np.array([t[0] for t in tracer_t['time']])
        for i in range(len(check_data['time2'])):
            check_data['temperature2'+str(i)] = tracer_grid[i]['temperature']
            check_data['x2'+str(i)] = tracer_grid[i]['distance']
 
        print(tracer_t, tracer_grid)
        tracer_t, tracer_grid = extract_series_line(data,'time',"temperature",['x','y','z'], [5.0, 1.0, 1.2],  [5.0, 2.0, 1.75], npts=5  )
        check_data['time3'] = np.array([t[0] for t in tracer_t['time']])
        for i in range(len(check_data['time3'])):
            check_data['temperature3'+str(i)] = tracer_grid[i]['temperature']
            check_data['x3'+str(i)] = tracer_grid[i]['distance']
        print(tracer_t, tracer_grid)

        if(OPPPY_UPGOLDS):
            goldfile = open(dir_path+'gold_line_data.p', 'wb')
            pickle.dump(check_data,goldfile)
            goldfile.close()

        goldfile = open(dir_path+'gold_line_data.p', 'rb')
        gold_data = pickle.load(goldfile)
        goldfile.close()
        for k, v in  gold_data.items():
            np.testing.assert_allclose(check_data[k],v)


