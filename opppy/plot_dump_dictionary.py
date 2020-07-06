# ---------------------------*-python-*----------------------------------------#
# file   plot_dump_dictionary.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
'''
Dictionary Plotting class

.. autosummary::
  
  plot_1d_dump_dictionary
  plot_2d_dump_dictionary
  plot_3d_dump_dictionary
'''

import matplotlib.pyplot as PyPloter
import matplotlib.axes as axes
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation
from matplotlib.animation import ArtistAnimation
import string, sys, os
import numpy as np
import re
from math import *
import argparse
import shlex
from collections import namedtuple

from opppy.plotting_help import *
from opppy.dump_utils import *

series_pair = namedtuple("pair", ['index', 'grid'])

class plot_1d_dump_dictionary():
    '''
    This class encapsolates a basic dictionary plotter. The important class
    options include:
        setup_parser
        parse_input_string
        is_data_available
        plot_1d


    '''
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="1D Dump ploter")
        self.setup_parser(self.parser)

    def parse_input_string(self, input_string):
        '''
        Parse an input string and return a plotting argument list

        arguments:
            input_string string of arguments to be parsed
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
            keys = dictionary.keys()
            if args.x_value_name not in keys:
                return False
            for yname in args.y_value_name:
                if yname not in keys:
                    return False
            return True
        except:
            return False
 
    def setup_parser(self, parser):
        '''
        setup the minimum parsing information need to plot a dictionary
        
        Input arguments:
            parser from argparse
        '''
        parser.add_argument('-x','--x_data', dest='x_value_name', help='dictionary data to be plotted on the x axes.', required=True)
        parser.add_argument('-y','--y_data', dest='y_value_names', help='dictionary data to be plotted on the y axes.', required=True, action='append')
        add_plot_options(parser);
    
    def plot_1d(self, args, dictionaries, data_names):
        '''
        argument 1d dump dictionary plotter.
    
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

        yname = ''
        xname = ''
        for data, filename, scale_x, scale_y in zip(dictionaries,data_names,args.scale_x,args.scale_y):
            new_file = True
            last_x = []
            last_y = []
            for yname in args.y_value_names:
                # clean file names
                if(args.data_file_name is not None):
                    outputfile = open(args.data_file_name+'_'+filename.split('/')[-1].strip('.p')+'.'+re.sub(r'[^\w]','',yname)+'.dat', 'w')
                xname = args.x_value_name
                try:
                    time_str = ' t='+str("%.5e"%data['time'])
                except:
                    time_str = ''
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
        
    
                    print('# ', header_xlabel, header_ylabel, time_str, file=outputfile)
                    for x_value, y_value in zip(x, y):
                        outstring = "%.9e"%(x_value*scale_x)+" %.9e"%(y_value*scale_y)+"\n"
                        outputfile.write(outstring)
                data_name = ''                    
                if(args.data_file_name is not None):
                    print("data saved as -- "+args.data_file_name+'_'+filename.split('/')[-1].strip('.p')+'.'+re.sub(r'[^\w]','',yname)+'.dat')
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
                
                data_name += time_str
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
            PyPloter.ylabel(yname)
        
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
            PyPloter.show()
    
class plot_2d_dump_dictionary():
    '''
    This class encapsolates a basic dictionary plotter. The important class
    options include:
        setup_parser
        parse_input_string
        is_data_available
        plot_2d


    '''
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Dump ploter")
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
            keys = dictionary.keys()
            if args.x_value_name not in keys:
                return False
            elif args.y_value_name not in keys:
                return False
            elif args.data_name not in keys:
                return False
            else:
                return True
        except:
            return False
 
    def setup_parser(self, parser):
        '''
        setup the minimum parsing information need to plot a dictionary
        
        Input arguments:
            parser from argparse
        '''
        parser.add_argument('-d','--data_name',dest='data_name',help="data to be plotted on the (x,y) contour", type=str, required=True)
        parser.add_argument('-x','--x_data', dest='x_value_name', help='dictionary data to be plotted on the x axes.', required=True)
        parser.add_argument('-y','--y_data', dest='y_value_name', help='dictionary data to be plotted on the y axes.', required=True)
        parser.add_argument('-cm','--contour', dest='contour', help='Plot contour map.', nargs='?', type=bool, const=True, default=False)
        parser.add_argument('-cl','--contour_lines', dest='contour_lines', help='Plot contour lines.', nargs='?', type=bool, const=True, default=False)
        parser.add_argument('-clev','--contour_levels', dest='contour_levels', help='Contour levels.', nargs='+', type=float)
        group = parser.add_argument_group()
        group.add_argument('-v','--verts', dest='xy_verts_name', help='dictionary vertices for each cell.', type=str)
        group.add_argument('-sm','--show_mesh', dest='show_mesh', help='show mesh (only valid if verts are included).', nargs='?', type=bool, const=True, default=False)
        add_2d_plot_options(parser);

    def plot_2d(self, args, dictionary):
        '''
        argument 2d dump dictionary plotter.
    
        arguments:
            args parsed dictionary plotting arguments
            dictionaries a list of dictionaries to be plotted
        '''
        if(args.hide_plot):
            PyPloter.switch_backend('agg')

        data_name = args.data_name
        yname = args.y_value_name
        xname = args.x_value_name
        # clean file names
        if(args.data_file_name is not None):
            outputfile = open(args.data_file_name+'_'+re.sub(r'[^\w]','',data_name)+'.dat', 'w')
        data = np.array(dictionary[data_name])*args.scale_value
        x = np.array(dictionary[xname])*args.scale_x
        y = np.array(dictionary[yname])*args.scale_y

        if(args.data_file_name is not None):
            header_datalabel = data_name
            if(args.x_label is not None):
                header_xlabel = args.x_label
            else:
                header_xlabel = xname
            if(args.y_label is not None):
                header_ylabel = args.y_label
            else:
                header_ylabel = yname
        
    
            print('# ', header_xlabel, header_ylabel, header_datalabel, file=outputfile)
            for x_value, y_value, data_value in zip(x, y, data):
                outstring = "%.9e"%(x_value)+" %.9e"%(y_value)+" %.9e"%(data_value)+"\n"
                outputfile.write(outstring)
        if(args.data_file_name is not None):
            print("data saved as -- "+args.data_file_name+'_'+re.sub(r'[^\w]','',data_name)+'.dat')
            outputfile.close()

        if(args.data_bounds):
            vmin = args.data_bounds[0]
            vmax = args.data_bounds[1]
        else:
            vmin = None
            vmax = None

        if args.xy_verts_name is not None:
            fig, ax = PyPloter.subplots()
            if args.x_limits is None:
                args.x_limits = [min(x),max(x)]
            if args.y_limits is None:
                args.y_limits = [min(y),max(y)]
            ax.set_xlim(args.x_limits[0], args.x_limits[1])
            ax.set_ylim(args.y_limits[0], args.y_limits[1])

            xy_verts = dictionary[args.xy_verts_name]
            if vmin is None:
                vmin = min(data)
            if vmax is None:
                vmax = max(data)
            patches = []
            for verts in xy_verts:
                patches.append(Polygon(xy=verts))
            collection = PatchCollection(patches, cmap='jet', snap=True)
            collection.set_array(np.array(data))
            collection.set_clim(vmin,vmax)
            if args.show_mesh:
                collection.set_edgecolors("black")
            ax.add_collection(collection)
            ax.set_aspect('equal', adjustable='box')
            if(args.contour_lines):
                collection.set_alpha(0.3)
                if args.x_limits is None:
                    args.x_limits = [min(x),max(x)]
                if args.y_limits is None:
                    args.y_limits = [min(y),max(y)]
                ax.set_xlim(args.x_limits[0], args.x_limits[1])
                ax.set_ylim(args.y_limits[0], args.y_limits[1])
                ax.set_aspect('equal', adjustable='box')
                ax.tricontour(x,y,data,cmap='jet',levels=args.contour_levels)

            fig.colorbar(collection, ax=ax)
        elif(args.contour):
            fig, ax = PyPloter.subplots()
            if args.x_limits is None:
                args.x_limits = [min(x),max(x)]
            if args.y_limits is None:
                args.y_limits = [min(y),max(y)]
            ax.set_xlim(args.x_limits[0], args.x_limits[1])
            ax.set_ylim(args.y_limits[0], args.y_limits[1])
            ax.set_aspect('equal', adjustable='box')
            PyPloter.tricontourf(x,y,data,cmap='jet',levels=args.contour_levels)
        elif(args.contour_lines):
            fig, ax = PyPloter.subplots()
            if args.x_limits is None:
                args.x_limits = [min(x),max(x)]
            if args.y_limits is None:
                args.y_limits = [min(y),max(y)]
            ax.set_xlim(args.x_limits[0], args.x_limits[1])
            ax.set_ylim(args.y_limits[0], args.y_limits[1])
            ax.set_aspect('equal', adjustable='box')
            PyPloter.tricontour(x,y,data,cmap='jet',levels=args.contour_levels)
        else:
            if args.x_limits is not None or args.y_limits is not None:
                if args.x_limits is None:
                    args.x_limits = [min(x),max(x)]
                if args.y_limits is None:
                    args.y_limits = [min(y),max(y)]
                griddata = data2gridbox(dictionary,xname,yname,data_name,args.x_limits[0],args.y_limits[0],args.x_limits[1],args.y_limits[1],args.num_grid,args.interp_method)
            else:
                griddata = data2grid(dictionary,xname,yname,data_name,args.num_grid,args.interp_method)

          
            PyPloter.imshow(griddata[data_name], vmin=vmin, vmax=vmax, extent=(griddata[xname].min(),griddata[xname].max(),griddata[yname].min(),griddata[yname].max()), origin='lower', cmap='jet')
            PyPloter.colorbar()


        if(args.find_max_value):
            print(data_name, "max value ", x[y.index(max(data))], x[y.index(max(data))], max(data))
        if(args.find_min_value):
            print(data_name, "min value ", x[y.index(min(data))], x[y.index(min(data))], min(data))
        
        if args.plot_title is not None:
            PyPloter.title(args.plot_title)
        else:
            PyPloter.title(data_name)

        if(args.x_label is not None):
            PyPloter.xlabel(args.x_label)
        else:
            PyPloter.xlabel(xname)
        
        if(args.y_label is not None):
            PyPloter.ylabel(args.y_label)
        else:
            PyPloter.ylabel(yname)
        
        if(args.plot_grid):
            PyPloter.grid()
        
        PyPloter.legend(loc='best')
        if(args.figure_name is not None):
            fig = PyPloter.savefig(args.figure_name, bbox_inches='tight', dpi=args.figure_resolution)
            print("Plot save as -- "+args.figure_name)
        elif(not args.hide_plot):
            PyPloter.show()
    
    
class plot_3d_dump_dictionary():
    '''
    This class encapsolates a basic dictionary plotter. The important class
    options include:
        setup_parser
        parse_input_string
        is_data_available
        plot_3d_slice


    '''
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Dump ploter")
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
            keys = dictionary.keys()
            if args.x_value_name not in keys:
                return False
            elif args.y_value_name not in keys:
                return False
            elif args.z_value_name not in keys:
                return False
            elif args.data_name not in keys:
                return False
            else:
                return True
        except:
            return False
 
    def setup_parser(self, parser):
        '''
        setup the minimum parsing information need to plot a dictionary
        
        Input arguments:
            parser from argparse
        '''
        parser.add_argument('-d','--data_name',dest='data_name',help="data to be plotted on the (x,y) contour", type=str, required=True)
        parser.add_argument('-x','--x_data', dest='x_value_name', help='dictionary data to be plotted on the x axes.', required=True)
        parser.add_argument('-y','--y_data', dest='y_value_name', help='dictionary data to be plotted on the y axes.', required=True)
        parser.add_argument('-z','--z_data', dest='z_value_name', help='dictionary data to be plotted on the z axes.', required=True)
        parser.add_argument('-sz','--scale_z', dest='scale_z', help='Scale the z axis data', type=float, default=1.0)
        parser.add_argument('-zs','--z_slice', dest='z_slice', help='Slice location along the z axes', type=float, required=True)
        parser.add_argument('-zlab','--zlab', dest='z_label', help='z axes label')
        add_2d_plot_options(parser);

    def plot_3d_slice(self, args, dictionary):
        '''
        argument 2d dump dictionary plotter.
    
        arguments:
            args parsed dictionary plotting arguments
            dictionaries a list of dictionaries to be plotted
        '''
        if(args.hide_plot):
            PyPloter.switch_backend('agg')

        data_name = args.data_name
        xname = args.x_value_name
        yname = args.y_value_name
        zname = args.z_value_name
        # clean file names
        if(args.data_file_name is not None):
            outputfile = open(args.data_file_name+'_'+re.sub(r'[^\w]','',data_name)+'.dat', 'w')
        data = np.array(dictionary[data_name])*args.scale_value
        x = np.array(dictionary[xname])*args.scale_x
        y = np.array(dictionary[yname])*args.scale_y
        z = np.array(dictionary[zname])*args.scale_z

        if(args.data_file_name is not None):
            header_datalabel = data_name
            if(args.x_label is not None):
                header_xlabel = args.x_label
            else:
                header_xlabel = xname
            if(args.y_label is not None):
                header_ylabel = args.y_label
            else:
                header_ylabel = yname
            if(args.z_label is not None):
                header_zlabel = args.z_label
            else:
                header_zlabel = zname
        
            print('# ', header_xlabel, header_ylabel, header_zlabel, header_datalabel, file=outputfile)
            for x_value, y_value, z_value, data_value in zip(x, y, z, data):
                outstring = "%.9e"%(x_value)+" %.9e"%(y_value)+" %.9e"%(z_value)+" %.9e"%(data_value)+"\n"
                outputfile.write(outstring)
        if(args.data_file_name is not None):
            print("data saved as -- "+args.data_file_name+'_'+re.sub(r'[^\w]','',data_name)+'.dat')
            outputfile.close()
        
        griddata = data2grid3Dslice(dictionary,xname,yname,zname,data_name,args.z_slice,args.num_grid,args.interp_method)

        if(args.data_bounds):
            vmin = args.data_bounds[0]
            vmax = args.data_bounds[1]
        else:
            vmin = None
            vmax = None

        PyPloter.imshow(griddata[data_name], vmin=vmin,vmax=vmax, extent=(griddata[xname].min(),griddata[xname].max(),griddata[yname].min(),griddata[yname].max()), origin='lower', cmap='jet')
        PyPloter.colorbar()
        
        if(args.find_max_value):
            print(data_name, "max value ", x[y.index(max(data))], x[y.index(max(data))], max(data))
        if(args.find_min_value):
            print(data_name, "min value ", x[y.index(min(data))], x[y.index(min(data))], min(data))
        
        if args.plot_title is not None:
            PyPloter.title(args.plot_title)
        else:
            PyPloter.title(data_name)

        if(args.x_label is not None):
            PyPloter.xlabel(args.x_label)
        else:
            PyPloter.xlabel(xname)
        
        if(args.y_label is not None):
            PyPloter.ylabel(args.y_label)
        else:
            PyPloter.ylabel(yname)
        
        if(args.plot_grid):
            PyPloter.grid()
        
        PyPloter.legend(loc='best')
        if(args.figure_name is not None):
            fig = PyPloter.savefig(args.figure_name, dpi=args.figure_resolution)
            print("Plot save as -- "+args.figure_name)
        elif(not args.hide_plot):
            PyPloter.show()


class plot_line_series_dictionary():
    '''
    This class encapsolates a basic dictionary plotter. The important class
    options include:
        setup_parser
        parse_input_string
        is_data_available
        plot_1d


    '''
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Line series ploter")
        self.setup_parser(self.parser)

    def parse_input_string(self, input_string):
        '''
        Parse an input string and return a plotting argument list

        arguments:
            input_string string of arguments to be parsed
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
            keys = dictionary.keys()
            if args.x_value_name not in keys:
                return False
            for yname in args.y_value_name:
                if yname not in keys:
                    return False
            return True
        except:
            return False
 
    def setup_parser(self, parser):
        '''
        setup the minimum parsing information need to plot a dictionary
        
        Input arguments:
            parser from argparse
        '''
        parser.add_argument('-x','--x_data', dest='x_value_name', help='dictionary data to be plotted on the x axes.', required=True)
        parser.add_argument('-y','--y_data', dest='y_value_name', help='dictionary data to be plotted on the y axes.', required=True)
        add_plot_options(parser);
    
    def plot_1d_series(self,args, series_pairs,  data_names):
        '''
        Initial lines 
        
        arguments:
            args parsed dictionary plotting arguments
            series_pair a list of 1D series pairs(index, grid)
            data_names names associated with the dictionaries to be plotted
        '''
        fig = PyPloter.figure()
        def init_lines():
            '''
            Initial lines 
        
            arguments:
                args parsed dictionary plotting arguments
                dictionaries a list of 1D series dictionary data to be plotted
                data_names names associated with the dictionaries to be plotted
            '''
            if(args.hide_plot):
                PyPloter.switch_backend('agg')

            if len(series_pairs) is not len(data_names):
                print("Error: len of dictionaries do not match length of associated data names")
                sys.exit(0)
            xname = args.x_value_name
            yname = args.y_value_name

            if len(args.scale_x) != len(series_pairs):
                if len(args.scale_x) == 0:
                    args.scale_x = [1.0]*len(series_pairs)
                else:
                    args.scale_x = [args.scale_x[-1]]*len(series_pairs)

            if len(args.scale_y) != len(series_pairs):
                if len(args.scale_y) == 0:
                    args.scale_y = [1.0]*len(series_pairs)
                else:
                    args.scale_y = [args.scale_y[-1]]*len(series_pairs)


            for series_pair, filename, scale_x, scale_y in zip(series_pairs, data_names,args.scale_x,args.scale_y):
                series_data = series_pair.grid
                index_key =  next(iter(series_pair.index))
                # find min and max of the data and write it to a file if necessary
                # clean file names
                if(args.data_file_name is not None):
                    outputfile = open(args.data_file_name+'_'+filename.split('/')[-1]+'.'+re.sub(r'[^\w]','',yname)+'.dat', 'w')

                xmin=(np.array(series_data[0][xname])*scale_x).min()
                xmax=(np.array(series_data[0][xname])*scale_x).max()
                ymin=(np.array(series_data[0][yname])*scale_y).min()
                ymax=(np.array(series_data[0][yname])*scale_y).max()
                for data, index_value in zip(series_data, series_pair.index[index_key]):
                    x = np.array(data[xname])*scale_x
                    y = np.array(data[yname])*scale_y
                    xmin = min(x.min(),xmin)
                    xmax = max(x.max(),xmax)
                    ymin = min(y.min(),ymin)
                    ymax = max(y.max(),ymax)
                    if(args.data_file_name is not None):
                        if(args.x_label is not None):
                            header_xlabel = args.x_label
                        else:
                            header_xlabel = xname
                        if(args.y_label is not None):
                            header_ylabel = args.y_label
                        else:
                            header_ylabel = yname
            
        
                        print('# ', index_key, header_xlabel, header_ylabel, file=outputfile)
                        for x_value, y_value in zip(x, y):
                            outstring = "%.9e"%(index_value)+" %.9e"%(x_value*scale_x)+" %.9e"%(y_value*scale_y)+"\n"
                            outputfile.write(outstring)
                if(args.data_file_name is not None):
                    print("data saved as -- "+args.data_file_name+'_'+filename.split('/')[-1]+'.'+re.sub(r'[^\w]','',yname)+'.dat')
                    outputfile.close()
            if(args.find_max_y):
                print(yname, "max y value ", ymax)
            if(args.find_min_y):
                print(yname, "min y value ", ymin)

            # initialize the figure and axes
            axes = PyPloter.axes(xlim=(xmin,xmax), ylim=(ymin,ymax))

            lines = []
            # initialize lines data
            for filename in data_names:
                data_name = ''                    
                line, = axes.plot([],[])
                if(args.line_names is not None):
                    if(len(args.line_names) != len(args.data_names)):
                        print("number of line names doesn't match the number of plotted lines")
                        print("line names have to be specified either for ALL or NONE of the plotted lines")
                        print("number of line names = ", len(args.tracer_names))
                        print("number of y_value_names = ", len(args.tracer_numbers))
                        sys.exit()
                    for temp_name, line_name in zip(args.data_names, args.line_names):
                            if(temp_name == filename):
                                data_name = filename.split('/')[-1] + " - " + line_name
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
                
                if(data_line_color != '' and data_line_type != ''):
                    line, = axes.plot([],[],label = data_name, linestyle = data_line_type, color = data_line_color)
                elif(data_line_color != '' ):
                    line, = axes.plot([],[],label = data_name, color = data_line_color)
                elif(data_line_type != '' ):
                    line, = axes.plot([],[],label = data_name, linestyle = data_line_type)
                else:
                    line, = axes.plot([],[],label = data_name)
                
                lines.append(line)
                        
            if(args.x_label is not None):
                PyPloter.xlabel(args.x_label)
            else:
                PyPloter.xlabel(xname)
            
            if(args.x_limits is not None):
                PyPloter.xlim(args.x_limits)
            
            if(args.y_label is not None):
                PyPloter.ylabel(args.y_label)
            else:
                PyPloter.ylabel(yname)
            
            if(args.y_limits is not None):
                PyPloter.ylim(args.y_limits)
            
            if(args.plot_grid):
                PyPloter.grid()
            
            PyPloter.legend(loc='best')
            if(args.log_x):
                PyPloter.xscale("log")
            if(args.log_y):
                PyPloter.yscale("log")
             
            return lines

        lines = init_lines()
        def animate(i):
            xname = args.x_value_name
            yname = args.y_value_name
            for j in range(0,len(series_pairs)):
                data = series_pairs[j].grid[i]
                lines[j].set_data(np.array(data[xname])*args.scale_x[j],np.array(data[yname])*args.scale_y[j])
            return lines

        ani = FuncAnimation(fig, animate, frames=len(series_pairs[0].grid), blit=True)

        if(args.figure_name is not None):
            ani.save(args.figure_name, fps=30, extra_args=['-vcodec', 'libx264'])
            print("Plot save as -- "+args.figure_name)
        elif(not args.hide_plot):
            PyPloter.show()

class plot_2d_series_dictionary():
    '''
    This class encapsolates a basic 2D series ploter
    options include:
        setup_parser
        parse_input_string
        is_data_available
        plot_1d


    '''
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="2d series ploter")
        self.setup_parser(self.parser)

    def parse_input_string(self, input_string):
        '''
        Parse an input string and return a plotting argument list

        arguments:
            input_string string of arguments to be parsed
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
            keys = dictionary.keys()
            if args.x_value_name not in keys:
                return False
            elif args.y_value_name not in keys:
                return False
            elif args.z_value_name not in keys:
                return False
            elif args.data_name not in keys:
                return False
            else:
                return True
        except:
            return False
 
    def setup_parser(self, parser):
        '''
        setup the minimum parsing information need to plot a dictionary
        
        Input arguments:
            parser from argparse
        '''
        parser.add_argument('-d','--data_name',dest='data_name',help="data to be plotted on the (x,y) contour", type=str)
        parser.add_argument('-x','--x_data', dest='x_value_name', help='dictionary data to be plotted on the x axes.', required=True)
        parser.add_argument('-y','--y_data', dest='y_value_name', help='dictionary data to be plotted on the y axes.', required=True)
        group = parser.add_argument_group()
        group.add_argument('-v','--verts', dest='xy_verts_name', help='dictionary vertices for each cell.', type=str)
        group.add_argument('-sm','--show_mesh', dest='show_mesh', help='show mesh (only valid if verts are included).', nargs='?', type=bool, const=True, default=False)
        add_2d_plot_options(parser);
    
    def plot_2d_series(self,args, series_pair):
        '''
        Initial lines 
        
        arguments:
            args parsed dictionary plotting arguments
            series_pair a 2d series pairs(index, grid)
            data_names names associated with the dictionaries to be plotted
        '''
        fig = PyPloter.figure()
        def init_contour():
            '''
            Initial lines 
        
            arguments:
                args parsed dictionary plotting arguments
                dictionaries a list of 1D series dictionary data to be plotted
                data_names names associated with the dictionaries to be plotted
            '''
            if(args.hide_plot):
                PyPloter.switch_backend('agg')

            dname = args.data_name
            xname = args.x_value_name
            yname = args.y_value_name

            series_data = series_pair.grid
            index_key =  next(iter(series_pair.index))
            # find min and max of the data and write it to a file if necessary
            # clean file names
            if(args.data_file_name is not None):
                outputfile = open(args.data_file_name+'_'+filename.split('/')[-1]+'.'+re.sub(r'[^\w]','',yname)+'.dat', 'w')

            vmin=(np.array(series_data[0][dname])*args.scale_value).min()
            vmax=(np.array(series_data[0][dname])*args.scale_value).max()
            xmin=(np.array(series_data[0][xname])*args.scale_x).min()
            xmax=(np.array(series_data[0][xname])*args.scale_x).max()
            ymin=(np.array(series_data[0][yname])*args.scale_y).min()
            ymax=(np.array(series_data[0][yname])*args.scale_y).max()
            for data, index_value in zip(series_data, series_pair.index[index_key]):
                v = np.array(data[dname])*args.scale_value
                x = np.array(data[xname])*args.scale_x
                y = np.array(data[yname])*args.scale_y
                vmin = min(v.min(),vmin)
                vmax = max(v.max(),vmax)
                xmin = min(x.min(),xmin)
                xmax = max(x.max(),xmax)
                ymin = min(y.min(),ymin)
                ymax = max(y.max(),ymax)
                if(args.data_file_name is not None):
                    if(args.x_label is not None):
                        header_xlabel = args.x_label
                    else:
                        header_xlabel = xname
                    if(args.y_label is not None):
                        header_ylabel = args.y_label
                    else:
                        header_ylabel = yname
            
        
                    print('# ', index_key, header_xlabel, header_ylabel, dname, file=outputfile)
                    for x_value, y_value, v_value in zip(x, y, v):
                        outstring = "%.9e"%(index_value)+" %.9e"%(x_value*args.scale_x)+" %.9e"%(y_value*args.scale_y)+" %.9e"%(v_value*args.scale_value)+"\n"
                        outputfile.write(outstring)
            if(args.data_file_name is not None):
                print("data saved as -- "+args.data_file_name+'_'+filename.split('/')[-1]+'.'+re.sub(r'[^\w]','',dname)+'.dat')
                outputfile.close()

            if(args.find_max_value):
                print(dname, "max value ", vmax)
            if(args.find_min_value):
                print(dname, "min value ", vmin)

            # initialize the figure and axes
            axes = PyPloter.axes(xlim=(xmin,xmax), ylim=(ymin,ymax))
                        
            if(args.x_label is not None):
                PyPloter.xlabel(args.x_label)
            else:
                PyPloter.xlabel(xname)
            
            if(args.x_limits is not None):
                PyPloter.xlim(args.x_limits)
            
            if(args.y_label is not None):
                PyPloter.ylabel(args.y_label)
            else:
                PyPloter.ylabel(yname)
            
            if(args.y_limits is not None):
                PyPloter.ylim(args.y_limits)
            
            if(args.plot_grid):
                PyPloter.grid()
            
            PyPloter.legend(loc='best')
            
            if(args.data_bounds):
                vmin = args.data_bounds[0]
                vmax = args.data_bounds[1]

            imshow = PyPloter.imshow(series_pair.grid[0][dname], extent=(xmin,xmax,ymin,ymax), vmin=vmin, vmax=vmax, origin='lower', animated=True, cmap='jet')
            PyPloter.colorbar()
            
            return imshow, xmin, xmax, ymin, ymax, vmin, vmax

        imshow, xmin, xmax, ymin, ymax, vmin, vmax = init_contour()
        ims = []
        for data in series_pair.grid:
            ims.append([PyPloter.imshow(data[args.data_name], extent=(xmin,xmax,ymin,ymax), vmin=vmin, vmax=vmax, origin='lower', animated=True, cmap='jet')])

        ani = ArtistAnimation(fig, ims, interval=200, blit=True)

        if(args.figure_name is not None):
            ani.save(args.figure_name, fps=30, extra_args=['-vcodec', 'libx264'])
            print("Plot save as -- "+args.figure_name)
        elif(not args.hide_plot):
            PyPloter.show()           
