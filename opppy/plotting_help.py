# ---------------------------*-python-*----------------------------------------#
# file   plotting_help.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
'''
Basic plotting help functions

.. autosummary::

  is_not_number
  is_number
  not_math_name
  str_vector_to_float_vector
  get_file_data
  get_value
  logplot
  add_plot_options
  add_2d_plot_options
'''

####################################################
# Useful helper functions for plotting
####################################################

import sys
import math
import numpy as np
import matplotlib.pyplot as PyPloter
import re
import ast


####################################################
# HELPER FUNCTIONS
####################################################

def is_not_number(s):
    '''
    Check if an input value is not a number
    '''
    try:
        float(s)
        return False
    except ValueError:
        return True

####################################################

def is_number(s):
    '''
    Check if an input value is a number
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False

####################################################

def not_math_name(name):
    '''
    Check if a provided string is a math operation

    supported math strings:
        pow
        sqrt
        exp
        sin
        cos
        atan
    '''
    if(name == 'pow'):
        return False
    elif(name == 'sqrt'):
        return False
    elif(name == 'exp'):
        return False
    elif(name == 'sin'):
        return False
    elif(name == 'cos'):
        return False
    elif(name == 'atan'):
        return False
    else:
        return True

####################################################

def str_vector_to_float_vector(sv):
    '''
    Convert a vector of string to a vector of floats
    '''
    float_vector = []
    for str in sv:
        if( not is_not_number(str.replace(",",""))):
            float_vector.append(float(str.replace(",","")))
    return float_vector

####################################################

def str_vector_to_int_vector(sv):
    '''
    Convert a vector of string to a vector of ints
    '''
    int_vector = []
    for str in sv:
        if( not is_not_number(str.replace(",",""))):
            int_vector.append(int(str.replace(",","")))
    return int_vector


####################################################

def get_file_data(file_name):
    '''
    A simple data extractor that converts a file containing
    a 2D ASCII data table into a two dimensional list of floats.

    arguments:
        file_name to be read

    returns:
        file_data a two dimensional list of numbers
    '''
    first = True
    file_data = [[]]
    file = open(file_name,'r')
    # loop over all lines in the file
    for line in file.redlines():
        # Create a vector of data
        data = line.split()
        # skip blank lines
        if(len(data)<1):
            continue
        # skip comments or headers
        elif(is_not_number(data[0])):
            continue
        elif(first):
            file_data[0]=str_vector_to_float_vector(data)
            first = False
        else:
            file_data.append(str_vector_to_float_vector(data));
    # all done now close the file
    file.close()
    # return the data
    return file_data;


####################################################

def get_value(y_value_name, names, data):
    '''
    This function evaluates a function string given a list of names and the data values associated with those names. 

    arguments:
        y_value_name is a math operations supported string (e.g. pow(x))
        names is a list of names associated with the data (e.g. [x])
        data is a list of data associated with the names (e.g. [2.0])

    In the example arguments above the function would return 4 (or pow(2,2))
    '''
    function_string = y_value_name

# parse the y_value_name for unique data names
    ynames = re.findall(r"[+-]?\d+\.\d+|\w+",y_value_name)
# print ynames
    unique_ynames = []
    for name in ynames:
        if name not in unique_ynames and not_math_name(name) and is_not_number(name):
            unique_ynames.append(name)

    if(len(unique_ynames)>5):
        print("Error: only 5 unique variables are allowed in yvalue functions:")
        sys.exit()

    #print unique_ynames
    # change and set the value names in the function string
    i=1
    for value_name in unique_ynames:
        found_name = False
        for name, value in zip(names, data):
            if(name.rstrip('\n') == value_name or is_number(value_name)):
                found_name = True
                if(i == 1):
                    i=i+1
                    function_string = function_string.replace(value_name,'a')
                    if(is_number(value_name)):
                        a = float(value_name)
                        break
                    else:
                        a = value
                elif(i == 2):
                    i=i+1
                    function_string = function_string.replace(value_name,'b')
                    if(is_number(value_name)):
                        b = float(value_name)
                        break
                    else:
                        b = value
                elif(i == 3):
                    i=i+1
                    function_string = function_string.replace(value_name,'c')
                    if(is_number(value_name)):
                        c = float(value_name)
                        break
                    else:
                        c = value
                elif(i == 4):
                    i=i+1
                    function_string = function_string.replace(value_name,'d')
                    if(is_number(value_name)):
                        d = float(value_name)
                        break
                    else:
                        d = value
                elif(i == 5):
                    i=i+1
                    function_string = function_string.replace(value_name,'e')
                    if(is_number(value_name)):
                        e = float(value_name)
                        break
                    else:
                        e = value
        if( not found_name):
            print("y_value_name = ", value_name," was not found")
            sys.exit()
    # Convert the function string to a function
    # print y_value_name, function_string
    function = ast.parse(function_string).compile()
    # return the function evaluation
    return eval(function)

####################################################

def logplot(xlog,ylog,x,y,label):
  '''
  Wrapper to call the correct logplot type

  parameters:
    bool xlog use a log scale on the x axis
    bool ylog use a log scale on the x axis
    array x x-data array
    array y x-data array
    string label data array

  '''
  if xlog == 1:
    if ylog == 1:
      PyPloter.loglog(x,y,label=label) 
    else:
      PyPloter.semilogx(x,y,label=label) 
  else:
    if ylog == 1:
      PyPloter.semilogy(x,y,label=label) 
    else:
      PyPloter.plot(x,y,label=label) 

def add_plot_options(parser):
    '''
    This function add general plotting options to an argparser object
    '''
    parser.add_argument('-ln','--line_name', dest='line_names', help='provide an alternative plotting line name in place of the y_data name', action='append')
    parser.add_argument('-lc','--line_color', dest='line_colors', help='tracer file line color',  action='append')
    parser.add_argument('-lt','--line_type', dest='line_types', help='tracer file line type (to used dash lines you must include a space in your quotes " -- ")', type=str, action='append')
    parser.add_argument('-xl','--x_limits', dest='x_limits', help='x plotting limits', type=float, nargs=2)
    parser.add_argument('-yl','--y_limits', dest='y_limits', help='y plotting limits', type=float, nargs=2)
    parser.add_argument('-sd','--save_data', dest='data_file_name', help='save as ASCII data')
    parser.add_argument('-sa','--save_as', dest='figure_name', help='save figure as "name"')
    parser.add_argument('-xlab','--xlab', dest='x_label', help='x axis label')
    parser.add_argument('-ylab','--ylabl', dest='y_label', help='y axis label')
    parser.add_argument('-nyn','--no_y_names', dest='no_y_names', help='prevent y_names from the key', nargs='?', type=bool, default=False, const=True )
    parser.add_argument('-lpo','--last_point_only', dest='last_point_only', help='only plot the last data point', nargs='?', type=bool, default=False, const=True )
    parser.add_argument('-ltv','--last_time_value', dest='last_time_value', help='only plot the last time value', nargs=1, type=float)
    parser.add_argument('-fr','--figure_resolution', dest='figure_resolution', help='figure resolution in  dpi', nargs='?', type=float, default=300.0)
    parser.add_argument('-fs','--font_size', dest='font_size', help='set the plot font size', type=float, default=None, nargs="?")
    parser.add_argument('-yev','--y_exceeds_value', dest='y_exceeds_value', help='y arrival value', nargs=1, type=float, default=0.0)
    parser.add_argument('-sy','--scale_y', dest='scale_y', help='scale y values', type=float, default=[], action="append")
    parser.add_argument('-sx','--scale_x', dest='scale_x', help='scale x values', type=float, default=[], action="append")
    parser.add_argument('-sz','--scale_z', dest='scale_z', help='scale z values', type=float, default=[], action="append")
    parser.add_argument('-fmaxy','--find_max_y', dest='find_max_y', help='find the maximum y value', nargs='?', type=bool, default=False, const=True )
    parser.add_argument('-fminy','--find_min_y', dest='find_min_y', help='find the minumum y value', nargs='?', type=bool, default=False, const=True )
    parser.add_argument('-pm','--plot_max', dest='plot_max', help='plot the max y values', type=bool, nargs='?', default=False, const=True )
    parser.add_argument('-pg','--plot_grid', dest='plot_grid', help='show grid on plot', type=bool, nargs='?', default=False, const=True )
    parser.add_argument('-hp','--hide_plot', dest='hide_plot', help='prevents plotting to the screen', nargs='?', type=bool, default=False, const=True )
    parser.add_argument('-pa','--plot_arrival', dest='plot_arrival', help='plot the arrival x value when (y>=y_exceeds_value)', nargs='?', type=bool, default=False, const=True )
    parser.add_argument('-lx','--log_x', dest='log_x', help='set log x axis', nargs='?', type=bool, default=False, const=True )
    parser.add_argument('-ly','--log_y', dest='log_y', help='set log y axis', nargs='?', type=bool, default=False, const=True )
    



def add_2d_plot_options(parser):
    '''
    This function add general plotting options to an argparser object
    '''
    parser.add_argument('-sd','--save_data', dest='data_file_name', help='save as ASCII data')
    parser.add_argument('-sa','--save_as', dest='figure_name', help='save figure as "name"')
    parser.add_argument('-xlab','--xlab', dest='x_label', help='x axis label')
    parser.add_argument('-ylab','--ylabl', dest='y_label', help='y axis label')
    parser.add_argument('-fr','--figure_resolution', dest='figure_resolution', help='figure resolution in  dpi', nargs='?', type=float, default=300.0)
    parser.add_argument('-fs','--font_size', dest='font_size', help='set the plot font size', type=float, default=None, nargs="?")
    parser.add_argument('-sv','--scale_value', dest='scale_value', help='scale values', type=float, default=1.0)
    parser.add_argument('-sx','--scale_x', dest='scale_x', help='scale x values', type=float, default=1.0)
    parser.add_argument('-sy','--scale_y', dest='scale_y', help='scale y values', type=float, default=1.0)
    parser.add_argument('-fmax','--find_max_value', dest='find_max_value', help='find the maximum value', nargs='?', type=bool, default=False, const=True )
    parser.add_argument('-fminv','--find_min_value', dest='find_min_value', help='find the minumum value', nargs='?', type=bool, default=False, const=True )
    parser.add_argument('-pg','--plot_grid', dest='plot_grid', help='show grid on plot', type=bool, nargs='?', default=False, const=True )
    parser.add_argument('-hp','--hide_plot', dest='hide_plot', help='prevents plotting to the screen', nargs='?', type=bool, default=False, const=True )
    parser.add_argument('-ls','--log_scale', dest='log_scale', help='plot data on a log scale', nargs='?', type=bool, default=False, const=True )
    parser.add_argument('-ng','--num_grid',dest='num_grid',help="number of grid points",nargs='?', type=int, default=200)
    parser.add_argument('-xl','--x_limits', dest='x_limits', help='x plotting limits', type=float, nargs=2)
    parser.add_argument('-yl','--y_limits', dest='y_limits', help='y plotting limits', type=float, nargs=2)
    parser.add_argument('-pt','--plot_title',dest='plot_title',help="Plot title",nargs='?', type=str, default='')
    parser.add_argument('-db','--data_bounds',dest='data_bounds',help="data (min,max) bounds to be ploted",nargs=2, type=float)
    parser.add_argument('-im','--interp_method',dest='interp_method',help="Specify the interpolation method to be used for gridding the data",nargs=1, default='nearest')


