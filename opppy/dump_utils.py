# ---------------------------*-python-*----------------------------------------#
# file   dump_utils.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
'''


.. autosummary::

  point_value_1d
  point_value_2d
  point_value_3d
  data2grid
  data2gridbox
  data2grid3Dslice
  data2line1d
  data2line2d
  data2line3d
  extract_series_point
  extract_series_line
  extract_series_2d
  extract_series_2d_slice
'''

from numpy import *
import os
import sys
import pickle
import math
import platform
import pickle
if "linux" in platform.system().lower(): 
    from multiprocessing import Process, Manager, cpu_count
else:
    # Protect against multiprocessing fork issue on Windows and Mac
    from multiprocess import Process, Manager, cpu_count

from opppy.progress import progress

def point_value_1d(data, x_key, value_key, x_value, method='nearest'):
    '''
    Grid data function. This function takes a 1D data structure from dictionary
    and interpolates the value at point.

    arguments:
      data   - 2D data set from in dictionary format
      x_key  - string to access x data
      value_key  - string to access data values
      x_value - float to indicate the x location of point
      method - Method for interpolation

    '''

    from scipy.interpolate import griddata

    X = data[x_key]

    value = data[value_key]
    grid_data = griddata((X), value, ([x_value]), method).T

    return grid_data



def point_value_2d(data, x_key, y_key, value_key, x_value, y_value, method='nearest'):
    '''
    Grid data function. This function takes a 2D data structure from dictionary
    and interpolates it at a single 2d point.

    arguments:
      data   - 2D data set from in dictionary format
      x_key  - string to access x data
      y_key  - string to access y data
      value_key  - string to access data values
      x_value - x location to interpolate at
      y_value - y location to interpolate at
      method - Method for interpolation
    
    '''

    from scipy.interpolate import griddata

    X = data[x_key]
    Y = data[y_key]

    value = data[value_key]
    grid_data = griddata((X, Y), value, ([x_value], [y_value]), method).T

    return grid_data

def point_value_3d(data, x_key, y_key, z_key, value_key, x_value, y_value, z_value, method='nearest'):
    '''
    Grid data function. This function takes a 2D data structure from dictionary
    and creates a 2D grid for each array by interpolating. This is useful for
    plotting.

   arguments:
     data   - 2D data set from in dictionary format
     x_key  - string to access x data
     y_key  - string to access y data
     z_key  - string to access y data
     value_key  - string to access data values
     x_value - x location to interpolate at
     y_value - y location to interpolate at
     z_value - z location to interpolate at
     method - Method for interpolation

    '''

    from scipy.interpolate import griddata

    X = data[x_key]
    Y = data[y_key]
    Z = data[z_key]

    value = data[value_key]
    grid_data = griddata((X, Y, Z), value, ([x_value], [y_value], [z_value]), method).T

    return grid_data



def data2grid(data, x_key, y_key, value_key, npts=500, method='nearest', log_scale=False):
    '''
    This function takes a 2D data structure from dictionary and creates a 2D
    grid for each array by interpolating. This is useful for plotting.

   arguments:
     data   - 2D data set from in dictionary format
     x_key  - string to access x data
     y_key  - string to access y data
     value_key  - string to access data values
     npts   - Number of points in both x & y to interpolate with 
     method - Method for interpolation

    '''

    from scipy.interpolate import griddata

    X = data[x_key]
    Y = data[y_key]
    xi, yi = mgrid[X.min():X.max():complex(npts), Y.min():Y.max():complex(npts)]
    grid_data = {}
    value = data[value_key]
    grid_data[value_key] = griddata((X, Y), value, (xi, yi), method).T
    if(log_scale):
        grid_data[value_key] = [[0.0 if val<=0.0 else math.log10(val) for val in vals] for vals in
                grid_data[value_key]]
    grid_data[x_key] = xi
    grid_data[y_key] = yi

    return grid_data



def data2gridbox(data, x_key, y_key, value_key, xmin, ymin, xmax, ymax,npts=500, method='nearest',
        log_scale=False):
    '''
    This function takes a 2D data structure from a data dictionary and creates
    a 2D grid for each array by interpolating in a user defined region.

    This is useful for plotting.
    
    arguments:
      data   - 2D data dump dictionary
      x_key  - string to access x data
      y_key  - string to access y data
      value_key  - string to access data values
      xmin   - lower x bound
      ymin   - lower y bound
      xmax   - upper x bound
      ymax   - upper y bound
      npts   - Number of points in both x & y to interpolate with 
      method - Method for interpolation
    
    '''
    from scipy.interpolate import griddata

    X = data[x_key]
    Y = data[y_key]
    xi, yi = mgrid[xmin:xmax:complex(npts), ymin:ymax:complex(npts)]

    grid_data = {}
    value = data[value_key]
    grid_data[value_key] = griddata((X, Y), value, (xi, yi), method).T
    if(log_scale):
        grid_data[value_key] = [[0.0 if val<=0.0 else math.log10(val) for val in vals] for vals in
                grid_data[value_key]]
    grid_data[x_key] = xi
    grid_data[y_key] = yi

    return grid_data



def data2grid3Dslice(data, x_key, y_key, z_key, value_key, z_slice_value, npts=500,method='nearest',
        log_scale=False):
    ''' 
    This function takes a 3D data structure from a data dictionary and creates
    a 2D grid for each array by interpolating. This is useful for plotting.
    
    arguments:
      data   - 2D data dump dictionary 
      x_key  - string to access x data
      y_key  - string to access y data
      z_key  - string to access z data
      value_key  - string to access data values
      z_slice_value = float value where z data should be sliced
      npts   - Number of points in both x & y to interpolate with 
      method - Method for interpolation
    
    '''
    from scipy.interpolate import griddata
    X = data[x_key]
    Y = data[y_key]
    Z = data[z_key]
    xi, yi, zi = mgrid[X.min():X.max():complex(npts), Y.min():Y.max():complex(npts), z_slice_value:z_slice_value:1j]

    grid_data = {}
    V = data[value_key]
    grid_data[value_key] = griddata((X, Y, Z), V, (xi, yi, zi), method).T[0]
    if(log_scale):
        grid_data[value_key] = [[0.0 if val<=0.0 else math.log10(val) for val in vals] for vals in
                grid_data[value_key]]
    grid_data[x_key] = xi.T[0]
    grid_data[y_key] = yi.T[0]

    return grid_data

def data2line1d(data, x_key, value_key, x1, x2, npts=500, method='nearest'):
    '''
    Extract a 1D lineout from a 1D data dictionary.

    arguments:
        data - a data 1D data dictionary with dump data
        x_key - the key for the x data location
        y_key - the key for the y data location
        value_key - the key for the value data to extract
        x1 - the initial x position of the line out
        y1 - the initial y position of the line out
        x2 - the finial x position of the line out
        y2 - the final y position of the line out
    '''
    from scipy.interpolate import griddata
    X = data[x_key]
    dX = x2-x1
    line = linspace(0,dX,npts)
    xi = zeros(npts)
    dx = dX/npts
    for i in range(0,npts):
        xi[i]=x1 + dx*i
    V = data[value_key]
    grid_data = griddata((X), V, (xi), method)
    return line, grid_data



def data2line2d(data, x_key, y_key, value_key, x1, y1, x2, y2, npts=500, method='nearest'):
    '''
    Extract a 1D lineout from a 2D data dictionary.

    arguments:
        data - a data 2D data dictionary with dump data
        x_key - the key for the x data location
        y_key - the key for the y data location
        value_key - the key for the value data to extract
        x1 - the initial x position of the line out
        y1 - the initial y position of the line out
        x2 - the finial x position of the line out
        y2 - the final y position of the line out
    '''
    from scipy.interpolate import griddata
    X = data[x_key]
    Y = data[y_key]
    dX = x2-x1
    dY = y2-y1
    line = linspace(0,sqrt(pow(dX,2)+pow(dY,2)),npts)
    xi = zeros(npts)
    yi = zeros(npts)
    dx = dX/npts
    dy = dY/npts
    for i in range(0,npts):
        xi[i]=x1 + dx*i
        yi[i]=y1 + dy*i
    V = data[value_key]
    grid_data = griddata((X, Y), V, (xi, yi), method)
    return line, grid_data


def data2line3d(data, x_key, y_key, z_key, value_key, x1, y1, z1,  x2, y2, z2, npts=500, method='nearest'):
    '''
    Extract a 1D lineout from a 3D data dictionary.

    arguments:
        data - a data 2D data dictionary with dump data
        x_key - the key for the x data location
        y_key - the key for the y data location
        value_key - the key for the value data to extract
        x1 - the initial x position of the line out
        y1 - the initial y position of the line out
        x2 - the finial x position of the line out
        y2 - the final y position of the line out
    '''
    from scipy.interpolate import griddata
    X = data[x_key]
    Y = data[y_key]
    Z = data[z_key]
    dX = x2-x1
    dY = y2-y1
    dZ = y2-y1
    line = linspace(0,sqrt(pow(dX,2)+pow(dY,2)+pow(dZ,2)),npts)
    xi = zeros(npts)
    yi = zeros(npts)
    zi = zeros(npts)
    dx = dX/npts
    dy = dY/npts
    dz = dZ/npts
    for i in range(0,npts):
        xi[i]=x1 + dx*i
        yi[i]=y1 + dy*i
        zi[i]=z1 + dz*i

    V = data[value_key]
    grid_data = griddata((X, Y, Z), V, (xi, yi,zi), method)
    return line, grid_data



def extract_series_point(data_list,series_key,value_key,dim_keys,point_values,method='nearest'):
    '''
    This function extracts the data values at a specified position from a
    series of data dictionaries.

    arguments:
        data_list - a list of data dictionaries with dump data
        series_key - the key for the x tracer data
        value_key - the key for the y tracer data
        dim_keys - list of keys to extract the data points for example:
            ['x'], ['x','y'], or  ['x','y','z']
        point values - list of float values to interpolate to for each designated point keys
        method - Method for interpolation
    '''
    dim = len(dim_keys)
    if len(point_values) is not dim:
        print("ERROR: length of point values do not match the length of point keys")
        sys.exit(0)
    T = []
    Y = []
    for data in data_list:
        if dim == 1:
            T.append(data[series_key])
            if len(data[value_key]) == 1:
                Y.append(data[value_key][0])
            else:
                Y.append(point_value_1d(data, dim_keys[0], value_key, point_values[0], method)[0])
        elif dim == 2:
            T.append(data[series_key])
            if len(data[value_key]) == 1:
                Y.append(data[value_key][0])
            else:
                Y.append(point_value_2d(data, dim_keys[0], dim_keys[1], value_key, point_values[0], point_values[1], method)[0])
        else:
            T.append(data[series_key])
            if len(data[value_key]) == 1:
                Y.append(data[value_key][0])
            else:
                Y.append(point_value_3d(data, dim_keys[0], dim_keys[1], dim_keys[2], value_key, point_values[0], point_values[1], point_values[2], method)[0])
    
    t = {}
    t[series_key] = array(T)
    grid = {}
    grid[value_key] = array(Y)

    return t, grid

def extract_series_line(data_list,series_key,value_key,dim_keys,point0_values,point1_values, npts=500, method='nearest'):
    '''
    This function extracts the data values along a specified line from a
    series of data dictionaries.

    arguments:
        data_list - a list of data dictionaries with dump data
        series_key - the key for the series increment (i.e. time or cycle)
        value_key - the key for the value data
        dim_keys - list of keys to extract the data points for example:
            ['x'], ['x','y'], or  ['x','y','z']
        point0_values - Starting location of the line 
        point1_values - Final location of the line
        method - Method for interpolation
    '''
    dim = len(dim_keys)
    if len(point0_values) is not dim:
        print("ERROR: length of point values do not match the length of point keys")
        sys.exit(0)
    if len(point1_values) is not dim:
        print("ERROR: length of point values do not match the length of point keys")
        sys.exit(0)
    T = []
    grid = []
    for data in data_list:
        T.append(data[series_key])
        my_grid = {}
        if dim == 1:
            my_grid['distance'], my_grid[value_key] = data2line1d(data, dim_keys[0], value_key, point0_values[0], point1_values[0], npts, method)
            grid.append(my_grid)
        elif dim == 2:
            my_grid['distance'], my_grid[value_key]  = data2line2d(data, dim_keys[0], dim_keys[1], value_key, point0_values[0], point0_values[1], point1_values[0], point1_values[1], npts, method)
            grid.append(my_grid)
        else:
            my_grid['distance'], my_grid[value_key] = data2line3d(data, dim_keys[0], dim_keys[1], dim_keys[2], value_key, point0_values[0], point0_values[1], point0_values[2], point1_values[0], point1_values[1], point1_values[2], npts, method)
            grid.append(my_grid)

    t = {}
    t[series_key] = array(T)

    return t, grid

def extract_series_2d(data_list, series_key, value_key, dim_keys, npts=500, method='nearest',
        log_scale=False, box=[]):
    '''
    This function extracts the data values along a specified line from a
    series of data dictionaries.

    arguments:
        data_list - a list of data dictionaries with dump data
        series_key - the key for the series increment (i.e. time or cycle)
        dim_keys - list of keys to extract the data points for example:
            ['x','y']
        npts - optional number of sample points
        method - optional method for interpolation
        box - optional grid box corner points:
            [x1, y1, x2, y2]
    '''
    dim = len(dim_keys)
    if dim != 2:
        print("ERROR: 2D series can only be used with 2 dimensional data")
        sys.exit(0)
    T = []
    grid = []
    for data in data_list:
        T.append(data[series_key])
        if len(box) == 0:
            if(data[value_key].ndim == 2 and 
               data[value_key].shape[1] == data[dim_keys[0]].shape[0] and 
               data[value_key].shape[0] == data[dim_keys[1]].shape[0]):
                grid.append(data)
            else:
                grid.append(data2grid(data, dim_keys[0], dim_keys[1], value_key, npts, method, log_scale))
        else:
            grid.append(data2gridbox(data, dim_keys[0], dim_keys[1], value_key, box[0], box[1],
                box[2], box[3],npts,method, log_scale))

    t = {}
    t[series_key] = array(T)

    return t, grid

def extract_series_2d_slice(data_list,series_key,value_key,dim_keys, slice_value, npts=500,
        method='nearest', log_scale=False):
    '''
    This function extracts the data values along a specified line from a
    series of data dictionaries.

    arguments:
        data_list - a list of data dictionaries with dump data
        series_key - the key for the series increment (i.e. time or cycle)
        value_key - the key for the value data
        dim_keys - list of keys to extract the data points for example:
            ['x','y','z']
        slice_values - the slice location in the 3rd dimension
        method - Method for interpolation
    '''
    dim = len(dim_keys)
    if dim != 3:
        print("ERROR: 3d slice can only be used with 3 dimensional data")
        sys.exit(0)
    T = []
    grid = []
    for data in data_list:
        if len(data[series_key]) == 1:
            T.append(data[series_key][0])
        else:
            print("Error: series_key dictionary item must return a single value (i.e. cycle or time)")
            sys.exit(0)

        grid.append(data2grid3Dslice(data, dim_keys[0], dim_keys[1], dim_keys[2],value_key,
            slice_value, npts, method, log_scale))

    t = {}
    t[series_key] = array(T)

    return t, grid

def append_dumps(data, dump_files, opppy_parser, key_words=None, nthreads=0):
    '''
    Append output data from a list of output_files to a user provided dictionary using a user proved
    opppy_parser. By default this function will use the multiprocessing option to parallelize the
    parsing of multiple dumps. The parallel parsing can be disabled by setting
    the environment variable 'OPPPY_USE_THREADS=False'

    Input options:
        data opppy input dictionary to be append to (must have a 'verion' opppy key)
        output_files a list of output files to parse
        opppy_parser a user defined OPPPY parser for the output files
        key_words limit the extrated dump data to the variables in the key_words list
        nthreads specify the number of threads to use for parsing (-1 nthreads=cpu_count, 0 serial, >0 user_specified number of threads)
    '''

    total = len(dump_files)
    count = 0
    print('')
    print("Number of files to be read: ", total)
    nthreads = cpu_count() if nthreads < 0 else nthreads
    if(nthreads>0):
        def thread_all(file_name, key_words, result_d):
            result_d[file_name.split('/')[-1]] = opppy_parser.build_data_dictionary(file_name,key_words)
        print("Number of threads used for processing: ",nthreads)
        for stride in range(math.ceil(float(total)/float(nthreads))):
            files = dump_files[nthreads*stride:array([nthreads*(stride+1),len(dump_files)]).min()]
            with Manager() as manager:
                result_d = manager.dict()
                threads = []
                for file_name in files:
                    thread = Process(target=thread_all, args=(file_name, key_words, result_d,))
                    thread.start()
                    threads.append(thread)
                for thread in threads:
                    thread.join()
                    count += 1
                    progress(count,total, 'of input files read')
                data.update(result_d)
                del result_d
                del threads
    else:
        for dump in dump_files:
          # append new dictionary data to the pickle file
          data[dump.split('/')[-1]] = opppy_parser.build_data_dictionary(dump,key_words)
          count += 1
          progress(count,total, 'of dump files read')

    print('')
    print('')
    print_dump_dictionary_data(data)

def print_dump_dictionary_data(data):
    '''
    List the data available in the python dictionary
    
    args:
       data - python dump dictionary data to be read
    '''
    print("######################################################")
    print("##      Built with: OPPPY " +data['version']+ '     ##')
    print("######################################################")
    print("#############     APPEND FILE HISTORY      ###########")
    print("######################################################")
    print("This pickle has been appended in the following order:")
    print("######################################################")
    for file_name in list(data.keys()):
        print(file_name)
    print("######################################################")

    print("This pickle has the following dictionary items:")
    print("######################################################")
    for key in list(data.keys()):
        if key == 'appended_files' or key == 'version':
            continue
        print(key,":", end='\n  ')
        keys = list(data[key].keys())
        print("keys:")
        stride = 2
        count = 0
        total = len(list(data[key].keys()))
        for data_key in list(data[key].keys()):
            try:
                len(data[key][data_key])
                print("    ", data_key, ": size = ",len(data[key][data_key])," min =", min(data[key][data_key]), " max = ",max(data[key][data_key]),end='\n')
            except:
                print("    ", data_key, ": value = ",data[key][data_key],end='\n')
        print('')
    print("######################################################")

def generate_dump_dictionary_list(dump_names, opppy_dump_parser, key_words=None, pickle_files=None, case_files=None ):
    dictionaries = []
    if pickle_files is not None:
        # get the dictionaries from the pickle files
        for filename in pickle_files:
            pickle_data = pickle.load(open(filename,'rb'))
            for dump_name in dump_names:
                if dump_name in list(pickle_data.keys()):
                    dictionaries.append(pickle_data[dump_name])
    elif case_files is not None:
        for case_file in case_files:
            dictionaries = build_case_data_list(case_file, dump_names, opppy_dump_parser, key_words)
    else:
        # Parse data from dump files
        dictionaries = build_data_list(dump_names, opppy_dump_parser, key_words)

    return dictionaries

def build_data_list(dump_names, opppy_dump_parser, key_words=None):
    '''
    This function generates a opppy output dictionary
    data from an output file.
    
    args:
      args - Parsed input arguments
    '''
    # build a new dictionary
    dictionary_data = []
    total = len(dump_names)
    count = 0
    for dump in dump_names:
      # append new dictionary data to the pickle file
      dictionary_data.append(opppy_dump_parser.build_data_dictionary(dump,key_words))
      count += 1
      progress(count,total, 'of dump files read')

    return dictionary_data


def append_case(data, case_file, opppy_parser, key_words=None, dump_names=None):
    '''
    Append case file data to an existing opppy dictionary

    Input options:
        data opppy input dictionary to be append to (must have a 'verion' opppy key)
        case_file case file to extract data from
        opppy_parser a user defined OPPPY parser for the output files
        append_date bool to specify if the data should be appended to the file
            name for tracking purposes 
    '''
    # append new dictionary data to the pickle file
    data = opppy_parser.append_case_dictionary(data,case_file,key_words,dump_names)

    print('')
    print('')
    print_dump_dictionary_data(data)

def build_case_data_list(case_file, dump_names, opppy_dump_parser, key_words=None):
    '''
    This function generates a opppy dump dictionary
    data from a case file.
    
    args:
      args - Parsed input arguments
    '''
    # build a new dictionary
    dictionary_data = []
    data = {}
    data['version'] = __version__
    append_case(data, case_file, opppy_dump_parser, key_words, dump_names)
    data.pop('version')
    if dump_names is None:
        for key in list(data.keys()):
            dictionary_data.append(data[key])
    else:
        for key in list(data.keys()):
            if key in dump_names:
                dictionary_data.append(data[key])

    return dictionary_data


