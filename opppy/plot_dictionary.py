# ---------------------------*-python-*----------------------------------------#
# file   plot_dictionary.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
'''
Dictionary Plotting class

.. autosummary::
  
  plot_dictionary

'''
import matplotlib.pyplot as PyPloter
import matplotlib.axes as axes
import string, sys, os
import numpy as np
import re
from math import *
import argparse
import shlex
import warnings

from opppy.plotting_help import *

class plot_dictionary():
    '''
    This class encapsolates a basic dictionary plotter. The important class
    options include:
        setup_parser
        parse_input_string
        is_data_available
        plot_dict


    '''
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Dictionary ploter")
        self.setup_parser(self.parser)

    def parse_input_string(self, input_string):
        '''
        Parse an input string and return a plotting argument list
        '''
        return self.parser.parse_args(shlex.split(input_string))

    def is_data_available(self, args, dictionary):
        '''
        Check the dictionary for valid plotting data
    
        arguments:
            args parsed dictionary plotting arguments 
            dictonary the dictonary to search for the x and y data value names
        '''
        try:
            if(args.series_key==args.x_value_name):
                return True
            data = dictionary[args.dictionary_name]
            x = data[args.x_value_name]
            if not (args.y_value_names[0] == "select_key"):
                for yname in args.y_value_names:
                    y = data[yname]
            return True
        except:
            return False
 
    def setup_parser(self, parser):
        '''
        setup the minimum parsing information need to plot a dictionary
        
        Input arguments:
            parser from argparse
        '''
        parser.add_argument('-dn','--dictionary_name', dest='dictionary_name', help='dictionary that the plotting data is contained in', required=True, type=str)
        parser.add_argument('-x','--x_data', dest='x_value_name', help='dictionary data to be plotted on the x axis.', required=True)
        parser.add_argument('-y','--y_data', dest='y_value_names', help='dictionary data to be plotted on the y axis.', required=True, action='append')
        add_plot_options(parser);
    


    def plot_dict(self, args, dictionaries, data_names):
        '''
        argument based dictionary plotting tool.
    
        arguments:
            args parsed dictionary plotting arguments
            dictionaries a list of dictionaries to be plotted
            data_names names associated with the dictionaries to be plotted
        '''
        if(args.hide_plot):
            PyPloter.switch_backend('agg')

        if len(dictionaries) is not len(data_names):
            print("Error: len of dictionaries do not match length of associated data names")
            sys.exit(0)
    
        dictionary_name = args.dictionary_name
        yname = ''
        xname = ''

        if len(args.scale_x) != len(dictionaries):
            if len(args.scale_x) == 0:
                args.scale_x = [1.0]*len(dictionaries)
            else:
                args.scale_x = [args.scale_x[-1]]*len(dictionaries)

        if len(args.scale_y) != len(dictionaries):
            if len(args.scale_y) == 0:
                args.scale_y = [1.0]*len(dictionaries)
            else:
                args.scale_y = [args.scale_y[-1]]*len(dictionaries)


        for dictionary, filename, scale_x, scale_y in zip(dictionaries,data_names,args.scale_x,args.scale_y):
            data = dictionary[dictionary_name]
            new_file = True
            last_x = []
            last_y = []
            last_z = []
            for yname in args.y_value_names:
                # clean file names
                if(args.data_file_name is not None):
                    outputfile = open(args.data_file_name+'_'+filename.split('/')[-1].strip('.p')+'.'+dictionary_name.replace(' ','_').replace('/','_').replace('#','num')+"."+re.sub(r'[^\w]','',yname)+'.dat', 'w')
                xname = args.x_value_name
                x = np.array(data[xname])*scale_x
                y = np.array(data[yname])*scale_y
                if args.last_time_value is not None:
                    for time, x_value, y_value in zip(data['time'],data[xname],data[yname]):
                        if value > last_time_value:
                            last_y.append(y_value*scale_y)
                            last_x.append(x_value*scale_x)
                elif args.last_point_only:
                    last_y.append(data[yname][-1]*scale_y)
                    last_x.append(data[xname][-1]*scale_x)
    
                if(args.data_file_name is not None):
                    if(args.x_label is not None):
                        header_xlabel = args.x_label
                    else:
                        header_xlabel = xname
                    if(args.y_label is not None):
                        header_ylabel = args.y_label
                    else:
                        header_ylabel = yname
        
    
                    print('# ', header_xlabel, header_ylabel, file=outputfile)
                    for x_value, y_value in zip(x, y):
                        outstring = "%.9e"%(x_value*scale_x)+" %.9e"%(y_value*scale_y)+"\n"
                        outputfile.write(outstring)
                data_name = ''                    
                if(args.data_file_name is not None):
                    print("data saved as -- "+args.data_file_name+'_'+filename.split('/')[-1].strip('.p')+'.'+dictionary_name.replace(' ','_').replace('/','_').replace('#','num')+"."+re.sub(r'[^\w]','',yname)+'.dat')
                    outputfile.close()
                if(args.line_names is not None):
                    if(len(args.line_names) != len(args.y_value_names)):
                        print("number of line names doesn't match the number of plotted lines")
                        print("line names have to be specified either for ALL or NONE of the plotted lines")
                        print("number of line names = ", len(args.tracer_names))
                        print("number of y_value_names = ", len(args.tracer_numbers))
                        sys.exit()
                    for temp_y_name, line_name in zip(args.y_value_names, args.line_names):
                            if(temp_y_name == yname):
                                data_name = filename.split('/')[-1] + " - " + line_name
                elif(args.no_y_names or args.last_point_only):
                    if(new_file or args.last_point_only):
                        data_name = filename.split('/')[-1]
                        new_file = False
                    else:
                        data_name = ''
                else:
                    data_name = filename.split('/')[-1] + " " +str(yname)
        
                data_line_type = ''
                if(args.line_types is not None):
                    if(len(args.line_types) != len(args.y_value_names)):
                        print("number of line types doesn't match the number of plotted lines")
                        print("line types have to be specified either for ALL or NONE of the lines")
                        print("number of line types = ", len(args.line_types))
                        print("number of y_value_names = ", len(args.tracer_numbers))
                        sys.exit()
                    for temp_y_name, line_type in zip(args.y_value_names, args.line_types):
                        if(temp_y_name == yname):
                            data_line_type = line_type.strip(' ')
        
                data_line_color = ''
                if(args.line_colors is not None):
                    if(len(args.line_colors) != len(args.filenames)):
                        print("number of line colors doesn't match the number of inputs plotted")
                        print("line colors have to be specified either for ALL or NONE of the lines")
                        print("number of line colors = ", len(args.line_colors))
                        print("number of files plotted = ", len(data_names))
                        sys.exit()
                    for temp_filename, line_color in zip(data_names, args.line_colors):
                        if(temp_filename == filename):
                            data_line_color = line_color
        
                if(args.last_point_only):
                    if(len(x)>0):
                        last_x.append(x[-1])
                        last_y.append(y[-1])
                
                if(args.plot_max):
                    last_y.append(sum(sorted(y,reverse=True)[0:2])/3.0)
                    last_x.append(x[-1])
                elif(args.plot_arrival):
                    continue
                elif(data_line_color != '' and data_line_type != ''):
                    PyPloter.plot(x,y,label = data_name, linestyle = data_line_type, color = data_line_color)
                elif(data_line_color != '' ):
                    PyPloter.plot(x,y,label = data_name, color = data_line_color)
                elif(data_line_type != '' ):
                    PyPloter.plot(x,y,label = data_name, linestyle = data_line_type)
                else:
                    PyPloter.plot(x,y,label = data_name)
        
                if(args.plot_arrival):
                    last_x = x[0]
                    last_y = y[0]
                    for x_value, y_value in zip(x,y):
                        if(y_value>args.y_exceeds_value):
                            dy = (args.y_exceeds_value - last_y)/(y_value - last_y)
                            interp_x = last_x + dy*(x_value-last_x)
                            print(data_name, "first exceeds ", y_exceeds_value, " at ", interp_x)
                            break
                        last_x = x_value
                        last_y = y_value
        
                if(args.find_max_y):
                    print(data_name, "max y value ", x[y.index(max(y))], max(y))
                if(args.find_min_y):
                    print(data_name, "max y value ", x[y.index(min(y))], min(y))
        
            if(args.last_point_only):
                PyPloter.plot(last_x, last_y, label = data_name)
            elif(args.plot_arrival or args.plot_max):
                print(last_x, last_y)
                PyPloter.plot(last_x, last_y, label = data_name)
        
        if(args.x_label is not None):
            PyPloter.xlabel(args.x_label)
        else:
            PyPloter.xlabel(xname)
        
        if(args.x_limits is not None):
            PyPloter.xlim(args.x_limits)
        
        if(args.y_label is not None):
            PyPloter.ylabel(args.y_label)
        else:
            PyPloter.ylabel(dictionary_name)
        
        if(args.y_limits is not None):
            PyPloter.ylim(args.y_limits)
        
        if(args.plot_grid):
            PyPloter.grid()
        
        PyPloter.legend(loc='best')
        if(args.log_x):
            PyPloter.xscale("log")
        if(args.log_y):
            PyPloter.yscale("log")
        if(args.figure_name is not None):
            fig = PyPloter.savefig(args.figure_name, dpi=args.figure_resolution)
            print("Plot save as -- "+args.figure_name)
        elif(not args.hide_plot):
            warnings.filterwarnings("ignore")
            PyPloter.show()
    
    
