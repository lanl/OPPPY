# ---------------------------*-python-*----------------------------------------#
# file   interactive_utils.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
'''
Interactive utilities define a set of function for command line interaction

.. autosummary::

  get_option_num
  get_key_num_vec
  interactive_output_parser
  interactive_dump_parser
  interactive_tally_parser
'''
import sys
import re
from os import listdir, chdir
from os.path import isfile, getmtime
from matplotlib.pyplot import *
import argparse
from numpy import *

from opppy.version import __version__
from opppy.dump_utils import *
from opppy.plot_dictionary import *
from opppy.plot_dump_dictionary import *
from opppy.output import *
from opppy.plotting_help import *
from opppy.tally import *

def get_option_num(nmax):
    '''
    Interactive request for a valid number in a range from 1 to nmax provided
    to the user

    '''
    while(1):
        nvar = input('Enter the option number for the variable to plot - ')
        if nvar == '-q' or nvar == 'q': sys.exit()
        if nvar == '': nvar = '1'
        try:
          nvar = int(nvar)
          if nvar < 1 or nvar > nmax: raise
        except:
          print("Must chose between 1 and " + str(nmax))
          continue
        break
    return nvar

def get_option_series_value(series_name, series_data):
    '''
    Interactive request for a valid series value

    arguments:
        series_name - string 
        series_data - numpy.array of available series data
    '''
    while(1):
        value = input('Enter the series location value ('+series_name+' min='+str(min(series_data))+' max='+str(max(series_data))+') [default uses max_value]: ')
        if value == '-q' or value == 'q': sys.exit()
        if value == 'max_value': value = max(series_data)
        if value == '': value = max(series_data)
        try:
          value = float(value)
          if value < min(series_data) or value > max(series_data): raise
        except:
            print("Must chose between"+' min='+str(min(series_data))+' max='+str(max(series_data))+' : ')
            continue
        break
    return value



def get_key_num_vec(keys):
    '''
    Interactive request for a valid set of numbers (e.g. [1, 2, 5]) in a range
    from 1 to nmax provided to the user

    '''

    nmax = len(keys)+1
    while(1):
        nvar = input('Enter the option number to plot (this can be a vector [1,2,3,..]) - ')
        if nvar == 'q': sys.exit()
        if nvar == '': nvar = '1'
        # split number verctor
        nvar = re.findall(r'\d+', nvar)
        vals = []
        for var in nvar:
          try:
            val = int(var)
            if val < 1 or val > nmax: raise
            vals.append(val)
          except:
            print("Must chose between 1 and " + str(nmax))
            continue
        break

    return_keys = []
    for val in vals:
        return_keys.append(keys[val-1])

    return return_keys
 
class interactive_output_parser:
    '''
    This is an interactive output parser and plotting class. It provides three
    basic interactive options:
        pickle_output generates a pickled python dictionary to be used for plotting
        plot_output provides pre-formated interactive plotting
        plot_dictionary provides command line dictionary plotting of pickled python dictionaries

    A user must supply:
        opppy_parser a user define parser to extract cycle dictionary data from a user defined outputfile
        option_string a user defined string the specifies dictionary plotting options
        argument_parser a user defined argparser object to attach the subparser options to

    '''
    def __init__(self, opppy_parser, option_string, argument_parser):
        self.opppy_parser = opppy_parser
        self.option_string = option_string
        self.parser = argument_parser
        self.subparser = self.parser.add_subparsers(help="Output options")
        self.pickle_output_parser(self.subparser)
        self.plot_dictionary_parser(self.subparser)
        self.plot_output_parser(self.subparser)

    def append_pickle(self, args):
        '''
        append_pickle - 
          This function generates/appends a opppy pickle file of dictionary
          data from an output file.
        
          arguments:
            args - Parsed input arguments
        '''
        data = {}
        data['version'] = __version__
        try:
          data = pickle.load(open(args.pickle_name,'rb'))
          print("Appending to the existing pickle file - ", args.pickle_name)
        except:
          print("Generating a new pickle file - ", args.pickle_name)
    
        if not 'version' in data or not (data['version'] == __version__):
          print('')
          print("Error: pickle file does not match this version of OPPPY")
          if 'version' in data:
            print(args.pickle_name, "was build with version", data['version'])
          else:
            print("This ", args.pickle_name," has no version")
          print("This version of OPPPY is ", __version__)
          print("Delete the old ", args.pickle_name, "file and rebuild it")
          sys.exit(0)

        if hasattr(self.opppy_parser, "pre_parse"):
            self.opppy_parser.pre_parse(args)

        # append new dictionary data to the pickle file
        append_output_dictionary(data, args.output_files, self.opppy_parser, args.append_date, args.nthreads)

        if hasattr(self.opppy_parser, "post_parse"):
            self.opppy_parser.post_parse(args, data)

   
        pickle.dump(data,open(args.pickle_name,"wb"))
        print("Output Data Saved To: ", args.pickle_name)


    def pickle_output_parser(self, subparser):
        pickle_parser = subparser.add_parser('pickle', help=" A simple example: pickle_output --pickle_file your_output_pickle_file.p --output_files you_output_files_to_pickle  ")
        pickle_parser.add_argument('-of','--output_files', dest='output_files', help='output files to generate/append the pickle file', nargs='+', required=True )
        pickle_parser.add_argument('-pf','--pickle_file', dest='pickle_name', help='Pickle file name to be created or appended to', required=True )
        pickle_parser.add_argument('-ad','--append_date', dest='append_date', help='Append the date and time to the output file name', nargs='?', type=bool, const=True, default=False)
        pickle_parser.add_argument('-nt','--nthreads', dest='nthreads', help='Number of threads to use during parsing', nargs='?', type=int, default=0)
        if hasattr(self.opppy_parser, "add_parser_args"):
            self.opppy_parser.add_parser_args(pickle_parser)
        pickle_parser.set_defaults(func=self.append_pickle)
 

    def plot_dictionary_parser(self, subparser):
        '''
        Add a parser for the dictionary plotter to a user provided subparser
        '''
        plot_parser = subparser.add_parser('plot', help=" A simple example: plot_dictionary -pf your_pickle_file.p --dictionary_name mat_eng --x_data time --y_data mat_name  ")
        input_type_parser = plot_parser.add_mutually_exclusive_group(required=True)
        input_type_parser.add_argument('-pf','--pickle_files', dest='pickle_files', help='pickle files to be plotted (run1.p run2.p etc...)', nargs='+' )
        input_type_parser.add_argument('-of','--output_files', dest='output_files', help='output files to be parsed and plotted (output_file1.txt output_file2.txt etc...)', nargs='+', action='append')
        plot_parser.add_argument('-nt','--nthreads', dest='nthreads', help='Number of threads to use during parsing', nargs='?', type=int, default=0)
        self.dict_ploter = plot_dictionary()
        self.dict_ploter.setup_parser(plot_parser)
        if hasattr(self.opppy_parser, "add_parser_args"):
            self.opppy_parser.add_parser_args(plot_parser)
        plot_parser.set_defaults(func=self.plot_dictionary)
    
    def plot_dictionary(self, args):
        '''
        Command line based dictionary plotting tool.
    
        arguments:
            args parsed dictionary plotting arguments
        '''
        dictionaries = []
        file_names = []
        if args.output_files is not None:
            if hasattr(self.opppy_parser, "pre_parse"):
                self.opppy_parser.pre_parse(args)
            dictionaries, file_names = build_output_dictionary_list(args.output_files,
                                                                    self.opppy_parser,
                                                                    nthreads=args.nthreads)
            if hasattr(self.opppy_parser, "post_parse"):
                for data in dictionaries:
                    self.opppy_parser.post_parse(args, data)
        else:
            # get the dictionaries from the pickle files
            file_names = args.pickle_files
            for filename in args.pickle_files:
                pickle_data = pickle.load(open(filename,'rb'))
                dictionaries.append(pickle_data)
    
        # plot dictionaries based on input arguments
        self.dict_ploter.plot_dict(args,dictionaries,file_names)
    
    def plot_output_parser(self, subparser):
        plot_output_parser = subparser.add_parser('iplot',help='Load a previously created pickle files (your_run.p) for interactive plotting or a set of output files to be parsed and plotted')
        input_type_parser = plot_output_parser.add_mutually_exclusive_group(required=True)
        input_type_parser.add_argument('-pf','--pickle_files', dest='pickle_files', help='pickle files to be plotted (run1.p run2.p etc...)', nargs='+' )
        input_type_parser.add_argument('-of','--output_files', dest='output_files', help='output files to be parsed and plotted (output_file1.txt output_file2.txt etc...)', nargs='+', action='append')
        plot_output_parser.add_argument('-nt','--nthreads', dest='nthreads', help='Number of threads to use during parsing', nargs='?', type=int, default=0)
        if hasattr(self.opppy_parser, "add_parser_args"):
            self.opppy_parser.add_parser_args(plot_output_parser)
        plot_output_parser.set_defaults(func=self.plot_output)
    
    def get_plot_option(self):
        '''
        Interactive request for valid plotting options
    
        '''
        while(1):
          opt = input('Additional options (-h for list and -q to quit): ')
          input_args = opt.split()
          parser = self.get_interactive_plot_parser()
          try:
            args=parser.parse_args(input_args)
            break
          except:
            parser.print_help()
          
        if args.quit:
          sys.exit(0)
    
        return args
    
    def get_interactive_plot_parser(self):
      '''
      return parser object that contains interactive plotting options
    
      '''
    
      parser = argparse.ArgumentParser(description=" Output Plotting options ", 
        epilog =" Specify the desired plotting options ", usage='')
      parser.add_argument('-q','--quit', dest='quit', help='quit program', nargs='?', type=bool, const=True, default=False)
      parser.add_argument('-n','--new', dest='new', help='generate a new plot', nargs='?', type=bool, const=True, default=False)
      parser.add_argument('-bg','--background', dest='background', help='keep plot in background', nargs='?', type=bool, const=True, default=False)
      parser.add_argument('-p','--plot', dest='plot', help='re-open plot', nargs='?', type=bool, const=True, default=False)
      parser.add_argument('-l','--labels', dest='legend_labels', help='specify the legend labels [line1_label, line2_label,...]', type=str, nargs='+')
      parser.add_argument('-rs','--resize', dest='plot_size', help='specify the plot size [x_size, y_size]', type=float, nargs=2)
      parser.add_argument('-nt','--nthreads', dest='nthreads', help='Number of threads to use during parsing', nargs='?', type=int, default=0)
    
      add_plot_options(parser)
      return parser
    
    def plot_output(self, args):
        '''
        This is an interactive plotter for a python dictionary.
        The plotting option are specified via an option string.
        
        arguments:
          args - argeparse data structure with pickle name info
          option_string - a string to be passed to get_plot_options for pre-designed plots
    
        '''
        dictionary_data=[]
        dictionary_names=[]
        if args.output_files is not None:
            if hasattr(self.opppy_parser, "pre_parse"):
                self.opppy_parser.pre_parse(args)
            dictionary_data, dictionary_names = build_output_dictionary_list(args.output_files,
                                                                             self.opppy_parser,
                                                                             nthreads=args.nthreads)
            if hasattr(self.opppy_parser, "post_parse"):
                for data in dictionary_data:
                    self.opppy_parser.post_parse(args, data)
        else:
            # We no longer flatten this data
            #file_list = []
            #for sublist in args.pickle_files:
            #  for item in sublist:
            #    file_list.append(item)
            # get the dictionaries from the pickle files
            for pickle_file_name in args.pickle_files:
                dictionary_names.append(pickle_file_name.split('/')[-1].split('.p')[0])
                dictionary_data.append(pickle.load(open(pickle_file_name,'rb')))

        option_parser = self.get_interactive_plot_parser()
        option = option_parser.parse_args(["--new"])
        ptype = []
        while(1):
          if option.new or option.background:
            close()
            plot_labels = self.get_plot_options(self.option_string)
     
            xsize = 8
            ysize = 5

            try:
                fig = figure(figsize=(xsize,ysize))
            except:
                PyPloter.switch_backend('agg')
                fig = figure(figsize=(xsize,ysize))
    
            xlog_flag = 0
            ylog_flag = 0
    
            counter = 1
            labels = []
            for i in range(len(plot_labels)):
              if self.dict_ploter.is_data_available(plot_labels[i][-1],dictionary_data[0]):
                labels.append(plot_labels[i])
                counter = counter + 1
            
            for i in range(0,len(labels),2):
              if i+1<counter-1:
                print('%3i  %-50s  %3i %-50s' %(i+1, labels[i][0], i+2, labels[i+1][0]))
              else:
                print('%3i  %-50s' %(i+1, labels[i][0]))
    
            plot_num = get_option_num(counter)-1
            label = labels[plot_num][0]
            plot_args = labels[plot_num][-1]
            if plot_args.y_value_names[0] == "select_key":    
                keys = list(dictionary_data[-1][plot_args.dictionary_name].keys())
                keys.remove('cycle')
                keys.remove('time')
                for i, key in zip(list(range(len(keys))),keys): 
                  if (i & 1)==0:
                    print('%3i  %-50s' %(i+1, key), end=' ')
                  else:
                    print('%3i  %-50s' %(i+1, key))
                print()
                plot_args.y_value_names = get_key_num_vec(keys)
    
          last_xmin = None
          last_xmax = None
          last_ymin = None
          last_ymax = None

          if len(plot_args.scale_x) != len(dictionary_data):
              if len(plot_args.scale_x) == 0:
                plot_args.scale_x = [1.0]*len(dictionary_data)
              else:
                plot_args.scale_x = [plot_args.scale_x[-1]]*len(dictionary_data)

          if len(plot_args.scale_y) != len(dictionary_data):
              if len(plot_args.scale_y) == 0:
                plot_args.scale_y = [1.0]*len(dictionary_data)
              else:
                plot_args.scale_y = [plot_args.scale_y[-1]]*len(dictionary_data)


          for dictionary, name, scale_x, scale_y in zip(dictionary_data, dictionary_names, plot_args.scale_x, plot_args.scale_y):
            data = dictionary[plot_args.dictionary_name]
    
            xmin = []
            xmax = []
            ymin = []
            ymax = []
            plabels = []
            x = []
            y = []
            xmin.append(min(data[plot_args.x_value_name])*scale_x)
            xmax.append(max(data[plot_args.x_value_name])*scale_x)
            ymin.append(min(data[plot_args.y_value_names[0]])*scale_y)
            ymax.append(max(data[plot_args.y_value_names[0]])*scale_y)
            # material specific plot
            for yname in plot_args.y_value_names:
              x.append(array(data[plot_args.x_value_name])*scale_x)
              ymin[-1] = min(ymin[-1],min(data[yname])*scale_y)
              ymax[-1] = max(ymin[-1],max(data[yname])*scale_y)
              plabels.append(label+" "+yname)
              if (option.no_y_names):
                  plabels[-1] = ''
              y.append(array(data[yname])*scale_y)
    
            xmin = array(xmin)
            xmax = array(xmax)
            ymin = array(ymin)
            ymax = array(ymax)
            if last_xmin is not None:
              xmin = min(last_xmin,xmin.min())
              xmax = max(last_xmax,xmax.max())
              ymin = min(last_ymin,ymin.min())
              ymax = max(last_ymax,ymax.max())
            else:
              xmin = xmin.min()
              xmax = xmax.max()
              ymin = ymin.min()
              ymax = ymax.max()
            last_xmin = xmin
            last_xmax = xmax
            last_ymin = ymin
            last_ymax = ymax
    
            xlab = plot_args.x_label
            ylab = plot_args.y_label
            if option.x_limits is not None:
              xmin = option.x_limits[0] 
              xmax = option.x_limits[1]
            if option.y_limits is not None:
              ymin = option.y_limits[0] 
              ymax = option.y_limits[1]
            if option.x_label is not None:
              xlab = option.x_label
            if option.y_label is not None:
              ylab = option.y_label
            if option.legend_labels is not None:
              if len(plabels) < len(option.legend_labels):
                  print("You specified more labels then there are plots")
              else:
                  for i in range(len(option.legend_labels)):
                      plabels[i] = option.legend_labels[i]
            if option.plot_size is not None:
              fig = figure(figsize=(option.plot_size[0],option.plot_size[1]))
              if not option.hide_plot:
                show(block=False)
    
            for i in range(len(x)):
              logplot(option.log_x,option.log_y,x[i],y[i],label=name+" "+plabels[i])
    
            if option.data_file_name is not None:
              output_file_temp = option.data_file_name 
              for i in range(len(x)):
                outfile_name = output_file_temp.strip()+"_"+str(name+"_"+plabels[i]).replace(" ","_").replace('/','_').replace('#','num')
                outfile =  open(outfile_name,'w')
                print("# ", xlab, ylab, file=outfile)
                for j in range(len(x[i])):
                  print('%15e  %15e' %(x[i][j], y[i][j]), file=outfile)
                print("Data written to - ", outfile_name)
                outfile.close()
      
            xlabel(xlab)
            ylabel(ylab)
            
            legend(loc='best').draw_frame(0)
            xlim(xmin,xmax)
            ylim(ymin,ymax)
            
            if not option.hide_plot:
              show(block=False)
    
            draw()
    
    
          if option.figure_name is not None:
            savefig(option.figure_name)
          
          if not option.hide_plot:
            show(block=False)
    
          option = self.get_plot_option()
          if option.background:
            figure()
          else:
            clf()
    
    def get_plot_options(self, label_string):
      '''
      Get pre-formated plotting options for the interactive ploter
       
      Input Options:
        label_string preformated string for expected data in a
        dictionary
    
      This expects a two column semicolon (;) separated text
      format string. The first column is an arbitrary string that
      will be printed by the interactive plotter as a plot the
      user can pick. The second column in a dictionary plotting
      command (more details in the examples below).
    
      examples:
        "your first fancy plot name; -dn your_dictionary_key -x your_x_data_key   -xlab "time [s]"  -y your_y_data_key  -ylab "RSS [%]";
        "your second fancy plot name; -dn your_dictionary_key -x time   -xlab "time [s]"  -y select_key  -ylab "RSS [%]";
    
     The dictionary plotting command has some basic requirements
     include a dictionary name (-dn) the x variable key (-x), the y
     variable key (-y), the x axis lable (-xlab), and the y axis
     label (-y). There are more details about available plotting
     options in plot_dictionary.py. The "-y select_key" value is a
     magic key word that tells the interactive ploter to provide a
     list of all y_data options for the designated dictionary.
      '''
      plot_labels = []
    
      label_file = io.StringIO(label_string)
      raw = label_file.readlines()
      for line in raw:
          lines = line.strip().split(';')
          if len(lines) == 3:
            labels = []
            labels.append(lines[0])
            labels.append(self.parse_output_plot_args(lines[1]))
            plot_labels.append(labels)
      return plot_labels
    
    def parse_output_plot_args(self, input_string):
      '''
      Returns a set of parsed dictionary plotting options from an input_string
    
      '''
      parser = argparse.ArgumentParser(description=" Output Plotting options ", 
        epilog =" Specify the desired plotting options ", usage='')
      parser.add_argument('-dn','--dictionary_name', dest='dictionary_name', help='dictionary that the plotting data is contained in', required=True, type=str)
      parser.add_argument('-x','--x_data', dest='x_value_name', help='dictionary data to be plotted on the x axis.', required=True)
      parser.add_argument('-y','--y_data', dest='y_value_names', help='dictionary data to be plotted on the y axis.', required=True, action='append')
      if hasattr(self.opppy_parser, "add_parser_args"):
          self.opppy_parser.add_parser_args(parser)
      add_plot_options(parser);
    
      return parser.parse_args(shlex.split(input_string))
    
    def run(self,input_string = None):
        if input_string:
            args = self.parser.parse_args(shlex.split(input_string))
        else:
            args = self.parser.parse_args()
        args.func(args)


class interactive_dump_parser:
    '''
    This is an interactive dump parser and plotting class. It provides three
    basic interactive options:
        plot_1D plot 1D data set from dump
        plot_2D plot 2D data set from dump
        plot_tracer plot data at a tracer location


    A user must supply:
        opppy_dump_parser a user define parser to extract cycle dictionary data from a user defined outputfile
        argument_parser a user defined argparser object to attach the subparser options to

    '''
    def __init__(self, opppy_dump_parser, argument_parser):
        '''
        set the dump parser and build up the argument parser
        '''
        self.dump_parser = opppy_dump_parser
        self.parser = argument_parser
        self.subparser = self.parser.add_subparsers(help="Dump options", dest='command')
        self.pickle_dumps_parser(self.subparser)
        self.plot_1d_parser(self.subparser)
        self.plot_2d_parser(self.subparser)
        self.plot_3d_parser(self.subparser)
        self.plot_series_point_parser(self.subparser)
        self.plot_series_line_parser(self.subparser)
        self.plot_series_contour_parser(self.subparser)

    def plot_1d_parser(self, subparser):
        '''
        Setup up a subparser for 1D plots

        Input arguments:
            subparser - A argparser subparser to append the plotting options to.
        '''
        plot_parser = subparser.add_parser('1d', help=" A simple example: dump 1d -df my_dump.txt -x x -y temperature  ")
        plot_parser.add_argument('-dn','--dump_names', dest='dump_names', help='name of dump file to be plotted', nargs='+', required=True )
        plot_parser.add_argument('-cf','--case_files', dest='case_files', help='Case file to be plotted', nargs='+', default=None)
        plot_parser.add_argument('-pf','--pickle_files', dest='pickle_files', help='pickle files to retrieve the dumps_names from', nargs='+', default=None )
        plot_parser.add_argument('-kw','--key_words', dest='key_words', help='Only extract the specified key_words', nargs='+', default=None )
        self.ploter_1d = plot_1d_dump_dictionary()
        self.ploter_1d.setup_parser(plot_parser)
        if hasattr(self.dump_parser, "add_parser_args"):
          self.dump_parser.add_parser_args(plot_parser)
        plot_parser.set_defaults(func=self.plot_1d)

    def plot_2d_parser(self, subparser):
        '''
        Setup up a subparser for 2D plots

        Input arguments:
            subparser - A argparser subparser to append the plotting options to.
        '''
        plot_parser = subparser.add_parser('2d', help=" A simple example: dump 2d -df my_dump.txt -x x -y -d temperature ")
        plot_parser.add_argument('-dn','--dump_name', dest='dump_names', help='name of dump file to be plotted', nargs=1, required=True )
        plot_parser.add_argument('-cf','--case_files', dest='case_files', help='Case file to be plotted', nargs='+', default=None)
        plot_parser.add_argument('-pf','--pickle_files', dest='pickle_files', help='pickle files to retrieve the dumps_name from', nargs='+', default=None )
        plot_parser.add_argument('-kw','--key_words', dest='key_words', help='Only extract the specified key_words', nargs='+', default=None )
        self.ploter_2d = plot_2d_dump_dictionary()
        self.ploter_2d.setup_parser(plot_parser)
        if hasattr(self.dump_parser, "add_parser_args"):
          self.dump_parser.add_parser_args(plot_parser)
        plot_parser.set_defaults(func=self.plot_2d)

    def plot_3d_parser(self, subparser):
        '''
        Setup up a subparser for 3D plots

        Input arguments:
            subparser - A argparser subparser to append the plotting options to.
        '''
        plot_parser = subparser.add_parser('3d', help=" A simple example: dump 3d -df my_dump.txt -x x -y -z z -zs 5.0 -d temperature ")
        plot_parser.add_argument('-dn','--dump_name', dest='dump_names', help='name of dump file to be plotted', nargs=1, required=True )
        plot_parser.add_argument('-cf','--case_files', dest='case_files', help='Case file to retrieve the dump_name from', nargs='+', default=None)
        plot_parser.add_argument('-pf','--pickle_files', dest='pickle_files', help='pickle files to retrieve the dumps_name from', nargs='+', default=None )
        plot_parser.add_argument('-kw','--key_words', dest='key_words', help='Only extract the specified key_words', nargs='+', default=None )
        self.ploter_3d = plot_3d_dump_dictionary()
        self.ploter_3d.setup_parser(plot_parser)
        if hasattr(self.dump_parser, "add_parser_args"):
          self.dump_parser.add_parser_args(plot_parser)
        plot_parser.set_defaults(func=self.plot_3d)

    def plot_3d(self, args):
        dictionaries = generate_dump_dictionary_list(args.dump_names, self.dump_parser, args.key_words, args.pickle_files, args.case_files)
        self.ploter_3d.plot_3d_slice(args, dictionaries[0])


    def plot_2d(self, args):
        dictionaries = generate_dump_dictionary_list(args.dump_names, self.dump_parser, args.key_words, args.pickle_files, args.case_files)
        self.ploter_2d.plot_2d(args, dictionaries[0])



    def plot_1d(self, args):
        dictionaries = generate_dump_dictionary_list(args.dump_names, self.dump_parser, args.key_words, args.pickle_files, args.case_files)
        self.ploter_1d.plot_1d(args, dictionaries, args.dump_names)


    def pickle_dumps_parser(self, subparser):
        pickle_parser = subparser.add_parser('pickle', help=" A simple example: pickle --pickle_file your_dump_file_to_pickle.p --output_files you_output_files_to_pickle  ")
        input_type_parser = pickle_parser.add_mutually_exclusive_group(required=True)
        input_type_parser.add_argument('-df','--dump_files', dest='dump_files', help='name of dump file to be pickled', nargs='+' )
        input_type_parser.add_argument('-cf','--case_file', dest='case_file', help='Case file to be pickled', nargs='?')
        pickle_parser.add_argument('-pf','--pickle_file', dest='pickle_name', help='Pickle file name to be created or appended to', required=True )
        pickle_parser.add_argument('-kw','--key_words', dest='key_words', help='Only extract the specified key_words', nargs='+', default=None )
        pickle_parser.add_argument('-nt','--nthreads', dest='nthreads', help='Specify number of threads for dump parsing', nargs='?', type=int, default=0 )
        if hasattr(self.dump_parser, "add_parser_args"):
          self.dump_parser.add_parser_args(pickle_parser)
        pickle_parser.set_defaults(func=self.pickle_dumps)
 
    def pickle_dumps(self, args):
        '''
        This function generates/appends a opppy pickle file of dictionary
        data from an output file.
        
        arguments:
          args - Parsed input arguments
        '''
        print("Pickle Dumps")
        dumps = {} 
        dumps['version'] = __version__
        try:
          dumps = pickle.load(open(args.pickle_name,'rb'))
          print("Appending to the existing pickle file - ", args.pickle_name)
        except:
          print("Generating a new pickle file - ", args.pickle_name)
    
        if not 'version' in dumps or not (dumps['version'] == __version__):
          print('')
          print("Error: pickle file does not match this version of OPPPY")
          if 'version' in data:
            print(args.pickle_name, "was build with version", data['version'])
          else:
            print("This ", args.pickle_name," has no version")
          print("This version of OPPPY is ", __version__)
          print("Delete the old ", args.pickle_name, "file and rebuild it")
          sys.exit(0)

        if args.dump_files is not None:
            append_dumps(dumps,args.dump_files,self.dump_parser,args.key_words,args.nthreads)
        else:
            append_case(dumps,args.case_file,self.dump_parser,args.key_words)

    
        pickle.dump(dumps,open(args.pickle_name,"wb"))
        print("Dump Data Saved To: ", args.pickle_name)



    def plot_series_point_parser(self, subparser):
        '''
        Setup up a subparser for tracer plots

        Input arguments:
            subparser - A argparser subparser to append the plotting options to.
        '''
        plot_parser = subparser.add_parser('point', help=" A simple example: plot_dictionary -pf your_pickle_file.p --dictionary_name mat_eng --x_data time --y_data mat_name  ", conflict_handler='resolve')
        input_type_parser = plot_parser.add_mutually_exclusive_group(required=True)
        input_type_parser.add_argument('-pf','--pickle_files', dest='pickle_files', help='pickle files to be plotted (run1.p run2.p etc...)', nargs='+')
        input_type_parser.add_argument('-df','--dump_files', dest='dump_files', help='dump files to be parsed and plotted (output_file1.txt output_file2.txt etc...)', nargs='+', action='append')
        input_type_parser.add_argument('-cf','--case_files', dest='case_files', help='Case file to be ploted', nargs='+')
        plot_parser.add_argument('-nt','--nthreads', dest='nthreads', help='Specify number of threads for dump parsing', nargs='?', type=int, default=0 )
        plot_parser.add_argument('-kw','--key_words', dest='key_words', help='Only extract the specified key_words', nargs='+', default=None )
        plot_parser.add_argument('-dk','--dimension_keys', dest='dimension_keys', help='keys used to extract the points (e.g. [x], [x,y], or [x,y,x]', nargs='+', required=True )
        plot_parser.add_argument('-p','--point', dest='point', help='point location to extract data (e.g. [1], [1,2], or [1,2,3]', nargs='+', required=True, type=float )
        plot_parser.add_argument('-s','--series_key', dest='series_key', help='keys used to extract the series axis data (e.g. cycle or time)', nargs='?', required=True )
        plot_parser.add_argument('-d','--data_key', dest='data_key', help='keys used to extract the data (e.g. temperature, pressure, etc)', nargs='?', required=True )
        plot_parser.add_argument('-im','--interpolation_method', dest='interpolation_method', help='Method used to interpolate the data to points', nargs='?', default='nearest' )

        self.ploter_1d = plot_1d_dump_dictionary()
        self.ploter_1d.setup_parser(plot_parser)
        # suppress the x and y variable request
        plot_parser.add_argument('-x','--x_data',dest='x_value_name', help=argparse.SUPPRESS)
        plot_parser.add_argument('-y','--y_data',dest='y_value_name', help=argparse.SUPPRESS)
        if hasattr(self.dump_parser, "add_parser_args"):
          self.dump_parser.add_parser_args(plot_parser)
        plot_parser.set_defaults(func=self.plot_series_point)

    def plot_series_point(self, args):
        series_names = []
        series_data = []
        if args.dump_files is not None:
            for dumps in args.dump_files:
                dictionary_list = build_data_list(dumps, self.dump_parser, args.key_words)
                tracer_x, tracer_y = extract_series_point(dictionary_list, args.series_key, args.data_key, args.dimension_keys, args.point, args.interpolation_method) 
                series_dictionary = {}
                series_dictionary.update(tracer_x)
                series_dictionary.update(tracer_y)
                series_data.append(series_dictionary)
                series_names.append(dumps[0].split('/')[-1])
        elif args.pickle_files is not None:
            for pickle_file in args.pickle_files:
                dictionary = pickle.load(open(pickle_file,'rb'))
                dictionary.pop('version')
                dictionary_list = []
                for key in list(dictionary.keys()):
                    dictionary_list.append(dictionary[key])
                tracer_x, tracer_y = extract_series_point(dictionary_list, args.series_key, args.data_key, args.dimension_keys, args.point) 
                series_dictionary = {}
                series_dictionary.update(tracer_x)
                series_dictionary.update(tracer_y)
                series_data.append(series_dictionary)
                series_names.append(pickle_file.split('/')[-1].split('.p')[0])
        elif args.case_files is not None:
            for case_file in args.case_files:
                dictionary_list = build_case_data_list(case_file, None, self.dump_parser, args.key_words)
                tracer_x, tracer_y = extract_series_point(dictionary_list, args.series_key, args.data_key, args.dimension_keys, args.point, args.interpolation_method) 
                series_dictionary = {}
                series_dictionary.update(tracer_x)
                series_dictionary.update(tracer_y)
                series_data.append(series_dictionary)
                series_names.append(case_file.split('/')[-1])
        args.x_value_name = args.series_key
        args.y_value_names = [args.data_key]
        self.ploter_1d.plot_1d(args, series_data, series_names)


    def plot_series_line_parser(self, subparser):
        '''
        Setup up a subparser for tracer plots

        Input arguments:
            subparser - A argparser subparser to append the plotting options to.
        '''
        plot_parser = subparser.add_parser('line', help=" A simple example: plot_dictionary -pf your_pickle_file.p --dictionary_name mat_eng --x_data time --y_data mat_name  ", conflict_handler='resolve')
        input_type_parser = plot_parser.add_mutually_exclusive_group(required=True)
        input_type_parser.add_argument('-pf','--pickle_files', dest='pickle_files', help='pickle files to be plotted (run1.p run2.p etc...)', nargs='+')
        input_type_parser.add_argument('-cf','--case_files', dest='case_files', help='Case file to be ploted', nargs='+')
        input_type_parser.add_argument('-df','--dump_files', dest='dump_files', help='dump files to be parsed and plotted (output_file1.txt output_file2.txt etc...)', nargs='+', action='append')
        plot_parser.add_argument('-nt','--nthreads', dest='nthreads', help='Specify number of threads for dump parsing', nargs='?', type=int, default=0 )
        plot_parser.add_argument('-kw','--key_words', dest='key_words', help='Only extract the specified key_words', nargs='+', default=None )
        plot_parser.add_argument('-dk','--dimension_keys', dest='dimension_keys', help='keys used to extract the points (e.g. [x], [x,y], or [x,y,x]', nargs='+', required=True )
        plot_parser.add_argument('-p0','--point0', dest='point0', help='beginning point location to extract data (e.g. [1], [1,2], or [1,2,3]', nargs='+', required=True, type=float )
        plot_parser.add_argument('-p1','--point1', dest='point1', help='end point location to extract data (e.g. [1], [1,2], or [1,2,3]', nargs='+', required=True, type=float )
        plot_parser.add_argument('-s','--series_key', dest='series_key', help='keys used to extract the series axis data (e.g. cycle or time)', nargs='?', required=True )
        plot_parser.add_argument('-d','--data_key', dest='data_key', help='keys used to extract the data (e.g. temperature, pressure, etc)', nargs='?', required=True )
        plot_parser.add_argument('-np','--number_of_points', dest='number_of_points', help='Number of sample points used to extract the data', nargs='?', type=int, default=500 )
        plot_parser.add_argument('-im','--interpolation_method', dest='interpolation_method', help='Method used to interpolate the data to points', nargs='?', default='nearest' )
        self.ploter_1d_series = plot_line_series_dictionary()
        self.ploter_1d_series.setup_parser(plot_parser)
        # suppress the x and y variable request
        plot_parser.add_argument('-x','--x_data',dest='x_value_name', help=argparse.SUPPRESS)
        plot_parser.add_argument('-y','--y_data',dest='y_value_name', help=argparse.SUPPRESS)
        if hasattr(self.dump_parser, "add_parser_args"):
          self.dump_parser.add_parser_args(plot_parser)
        plot_parser.set_defaults(func=self.plot_series_line)

    def plot_series_line(self, args):
        
        series_names = []
        series_data = []
        if args.dump_files is not None:
            for dumps in args.dump_files:
                dictionary_list = build_data_list(dumps, self.dump_parser, args.key_words)
                tracer_t, tracer_grid = extract_series_line(dictionary_list, args.series_key, args.data_key, args.dimension_keys, args.point0, args.point1, args.number_of_points, args.interpolation_method) 
                series_data.append(series_pair(tracer_t, tracer_grid))
                series_names.append(dumps[0].split('/')[-1])
        elif args.pickle_files:
            for pickle_file in args.pickle_files:
                dictionary = pickle.load(open(pickle_file,'rb'))
                dictionary.pop('version')
                dictionary_list = []
                for key in list(dictionary.keys()):
                    dictionary_list.append(dictionary[key])
                tracer_t, tracer_grid = extract_series_line(dictionary_list, args.series_key, args.data_key, args.dimension_keys, args.point0, args.point1, args.number_of_points, args.interpolation_method) 
                series_data.append(series_pair(tracer_t, tracer_grid))

                series_names.append(pickle_file.split('/')[-1].split('.p')[0])
        if args.case_files is not None:
            for case_file in args.case_files:
                dictionary_list = build_case_data_list(case_file, None, self.dump_parser, args.key_words)
                tracer_t, tracer_grid = extract_series_line(dictionary_list, args.series_key, args.data_key, args.dimension_keys, args.point0, args.point1, args.number_of_points, args.interpolation_method) 
                series_data.append(series_pair(tracer_t, tracer_grid))
                series_names.append(case_file.split('/')[-1])
        args.x_value_name='distance'
        args.y_value_name= args.data_key
        self.ploter_1d_series.plot_1d_series(args, series_data, series_names)

    def plot_series_contour_parser(self, subparser):
        '''
        Setup up a subparser for tracer plots

        Input arguments:
            subparser - A argparser subparser to append the plotting options to.
        '''
        plot_parser = subparser.add_parser('contour', help=" A simple example: dump contour -dk x y -s time -d temperature ", conflict_handler='resolve')
        input_type_parser = plot_parser.add_mutually_exclusive_group(required=True)
        input_type_parser.add_argument('-pf','--pickle_file', dest='pickle_file', help='pickle file to be plotted', nargs='?')
        input_type_parser.add_argument('-cf','--case_file', dest='case_file', help='Case file to be ploted', nargs='?')
        input_type_parser.add_argument('-df','--dump_files', dest='dump_files', help='dump files to be parsed and plotted (output_file1.txt output_file2.txt etc...)', nargs='+')
        plot_parser.add_argument('-nt','--nthreads', dest='nthreads', help='Specify number of threads for dump parsing', nargs='?', type=int, default=0 )
        plot_parser.add_argument('-kw','--key_words', dest='key_words', help='Only extract the specified key_words', nargs='+', default=None )
        plot_parser.add_argument('-dk','--dimension_keys', dest='dimension_keys', help='keys used to extract the points dimensions in the dictionary (e.g. [x,y], or [my_x,my_y,my_z]', nargs='+', required=True )
        plot_parser.add_argument('-zs','--z_slice_location', dest='z_slice_location', help='location along the z plane to slice the data', nargs='?', type=float, default=None)
        plot_parser.add_argument('-s','--series_key', dest='series_key', help='keys used to extract the series axis data (e.g. cycle or time)', nargs='?', required=True )
        plot_parser.add_argument('-np','--number_of_points', dest='number_of_points', help='Number of sample points used to extract the data', nargs='?', type=int, default=500 )
        plot_parser.add_argument('-im','--interpolation_method', dest='interpolation_method', help='Method used to interpolate the data to points', nargs='?', default='nearest' )
        self.ploter_2d_series = plot_2d_series_dictionary()
        self.ploter_2d_series.setup_parser(plot_parser)
        # suppress the x and y variable request
        plot_parser.add_argument('-x','--x_data',dest='x_value_name', help=argparse.SUPPRESS)
        plot_parser.add_argument('-y','--y_data',dest='y_value_name', help=argparse.SUPPRESS)
        if hasattr(self.dump_parser, "add_parser_args"):
          self.dump_parser.add_parser_args(plot_parser)
        plot_parser.set_defaults(func=self.plot_series_contour)

    def plot_series_contour(self, args):
        
        if args.dump_files is not None:
            dictionary_list = build_data_list(args.dump_files, self.dump_parser, args.key_words)
            tracer_t = {}
            tracer_grid = {}
            if args.z_slice_location is not None:
                if len(args.dimension_keys) != 3:
                    print('Error: z_slice_location specified so length of dimension_keys must be 3')
                    sys.exit(0)
                tracer_t, tracer_grid = extract_series_2d_slice(dictionary_list, args.series_key,
                        args.data_name, args.dimension_keys, args.z_slice_location,
                        args.number_of_points, args.interpolation_method, args.log_scale) 
            else:
                if len(args.dimension_keys) != 2:
                    print('Error: z_slice_location specified is not specified so length of dimension_keys must be 2')
                tracer_t, tracer_grid = extract_series_2d(dictionary_list, args.series_key,
                        args.data_name, args.dimension_keys, args.number_of_points,
                        args.interpolation_method, args.log_scale) 
            series_data = series_pair(tracer_t, tracer_grid)
        elif args.pickle_file is not None:
            dictionary = pickle.load(open(args.pickle_file,'rb'))
            dictionary.pop('version')
            dictionary_list = []
            for key in list(dictionary.keys()):
                dictionary_list.append(dictionary[key])
            tracer_t = {}
            tracer_grid = {}
            if args.z_slice_location is not None:
                if len(args.dimension_keys) != 3:
                    print('Error: z_slice_location specified so length of dimension_keys must be 3')
                    sys.exit(0)
                tracer_t, tracer_grid = extract_series_2d_slice(dictionary_list, args.series_key,
                        args.data_name, args.dimension_keys, args.z_slice_location,
                        args.number_of_points, args.interpolation_method, args.log_scale) 
            else:
                if len(args.dimension_keys) != 2:
                    print('Error: z_slice_location specified is not specified so length of dimension_keys must be 2')
                tracer_t, tracer_grid = extract_series_2d(dictionary_list, args.series_key,
                        args.data_name, args.dimension_keys, args.number_of_points,
                        args.interpolation_method, args.log_scale) 
            series_data = series_pair(tracer_t, tracer_grid)
        if args.case_file is not None:
            dictionary_list = build_case_data_list(args.case_file, None, self.dump_parser, args.key_words)
            tracer_t = {}
            tracer_grid = {}
            if args.z_slice_location is not None:
                if len(args.dimension_keys) != 3:
                    print('Error: z_slice_location specified so length of dimension_keys must be 3')
                    sys.exit(0)
                tracer_t, tracer_grid = extract_series_2d_slice(dictionary_list, args.series_key,
                        args.data_name, args.dimension_keys, args.z_slice_location,
                        args.number_of_points, args.interpolation_method, args.log_scale) 
            else:
                if len(args.dimension_keys) != 2:
                    print('Error: z_slice_location specified is not specified so length of dimension_keys must be 2')
                tracer_t, tracer_grid = extract_series_2d(dictionary_list, args.series_key,
                        args.data_name, args.dimension_keys, args.number_of_points,
                        args.interpolation_method, args.log_scale) 
            series_data = series_pair(tracer_t, tracer_grid)

        args.x_value_name= args.dimension_keys[0]
        args.y_value_name= args.dimension_keys[1]
        self.ploter_2d_series.plot_2d_series(args, series_data)

    def run(self,input_string = None):
        '''
        Run the program

        Optional input:
            input_string - A string to be parsed in favor of the command line program arguments
        '''
        if input_string:
            args = self.parser.parse_args(shlex.split(input_string))
        else:
            args = self.parser.parse_args()
        args.func(args)

class interactive_tally_parser:
    '''
    This is an interactive tally parser and plotting class. It provides three
    basic interactive options:
        pickle generates a pickled python dictionary to be used for plotting
        iplot interactive plotting option based on a user defined option string
        plot provides command line dictionary plotting of pickled python dictionaries

    A user must supply:
        opppy_tally_parser a user define parser to extract cycle dictionary data from a user defined tally file
        option_string a user defined string the specifies dictionary plotting options
        argument_parser a user defined argparser object to attach the subparser options to

    '''
    def __init__(self, opppy_tally_parser, option_string, argument_parser):
        self.opppy_parser = opppy_tally_parser
        self.option_string = option_string
        self.parser = argument_parser
        self.subparser = self.parser.add_subparsers(help="Tally options")
        self.pickle_tally_parser(self.subparser)
        self.plot_tally_parser(self.subparser)
        self.plot_interactive_tally_parser(self.subparser)

    def append_pickle(self, args):
        '''
        append_pickle - 
          This function generates/appends a opppy pickle file of dictionary
          data from an output file.
        
          arguments:
            args - Parsed input arguments
        '''
        data = {}
        data['version'] = __version__
        try:
          data = pickle.load(open(args.pickle_name,'rb'))
          print("Appending to the existing pickle file - ", args.pickle_name)
        except:
          print("Generating a new pickle file - ", args.pickle_name)
    
        if not 'version' in data or not (data['version'] == __version__):
          print('')
          print("Error: pickle file does not match this version of OPPPY")
          if 'version' in data:
            print(args.pickle_name, "was build with version", data['version'])
          else:
            print("This ", args.pickle_name," has no version")
          print("This version of OPPPY is ", __version__)
          print("Delete the old ", args.pickle_name, "file and rebuild it")
          sys.exit(0)
    
        if hasattr(self.opppy_parser, "pre_parse"):
            self.opppy_parser.pre_parse(args)

        # append new dictionary data to the pickle file
        append_tally_dictionary(data, args.tally_files, self.opppy_parser, args.append_date, args.nthreads)

        if hasattr(self.opppy_parser, "post_parse"):
            self.opppy_parser.post_parse(args, data)
    
        pickle.dump(data,open(args.pickle_name,"wb"))
        print("Output Data Saved To: ", args.pickle_name)


    def pickle_tally_parser(self, subparser):
        pickle_parser = subparser.add_parser('pickle', help=" A simple example: pickle --pickle_file your_output_pickle_file.p --tally_files your_tally_files_to_pickle  ")
        pickle_parser.add_argument('-tf','--tally_files', dest='tally_files', help='output files to generate/append the pickle file', nargs='+', required=True )
        pickle_parser.add_argument('-pf','--pickle_file', dest='pickle_name', help='Pickle file name to be created or appended to', required=True )
        pickle_parser.add_argument('-ad','--append_date', dest='append_date', help='Append the date and time to the output file name', nargs='?', type=bool, const=True, default=False)
        pickle_parser.add_argument('-nt','--nthreads', dest='nthreads', help='Number of threads to use during parsing', nargs='?', type=int, default=0)
        if hasattr(self.opppy_parser, "add_parser_args"):
          self.opppy_parser.add_parser_args(pickle_parser)
        pickle_parser.set_defaults(func=self.append_pickle)
 

    def plot_tally_parser(self, subparser):
        '''
        Add a parser for the dictionary plotter to a user provided subparser
        '''
        plot_parser = subparser.add_parser('plot', help=" A simple example: plot -pf your_pickle_file.p --dictionary_name mat_eng --x_data time --y_data mat_name  ")
        input_type_parser = plot_parser.add_mutually_exclusive_group(required=True)
        input_type_parser.add_argument('-pf','--pickle_files', dest='pickle_files', help='pickle files to be plotted (run1.p run2.p etc...)', nargs='+' )
        input_type_parser.add_argument('-tf','--tally_files', dest='tally_files', help='tally files to be parsed and plotted (tally_file1.txt tally_file2.txt etc...)', nargs='+', action='append')
        plot_parser.add_argument('-sk','--series_key', dest='series_key', help='Series key string to access the data (i.e time or cycle)', nargs='?', required=True)
        plot_parser.add_argument('-sv','--series_value', dest='series_value', help='Series value to plot the data at (default is the last value of the series_key data)', nargs='?', type=float, default=None)
        plot_parser.add_argument('-nt','--nthreads', dest='nthreads', help='Number of threads to use during parsing', nargs='?', type=int, default=0)
        self.dict_ploter = plot_dictionary()
        self.dict_ploter.setup_parser(plot_parser)
        if hasattr(self.opppy_parser, "add_parser_args"):
          self.opppy_parser.add_parser_args(plot_parser)
        plot_parser.set_defaults(func=self.plot_tally)
    
    def plot_tally(self, args):
        '''
        Command line based tally plotting tool.
    
        arguments:
            args parsed dictionary plotting arguments
        '''
        raw_dictionary_data=[]
        raw_dictionary_names=[]
        if args.tally_files is not None:
            if hasattr(self.opppy_parser, "pre_parse"):
                self.opppy_parser.pre_parse(args)
            raw_dictionary_data, raw_dictionary_names = build_tally_dictionary_list(args.tally_files, 
                                                                                    self.opppy_parser, 
                                                                                    nthreads=args.nthreads)
            if hasattr(self.opppy_parser, "post_parse"):
                for data in raw_dictionary_data:
                    self.opppy_parser.post_parse(args, data)
        else:
            for pickle_file_name in args.pickle_files:
                raw_dictionary_names.append(pickle_file_name.split('/')[-1].split('.p')[0])
                raw_dictionary_data.append(pickle.load(open(pickle_file_name,'rb')))

        # build up plotting dictionary list and names
        dictionary_data = []
        dictionary_names = []
        for dictionary, name in zip(raw_dictionary_data,raw_dictionary_names):
            found = False
            times = dictionary[args.series_key]
            if args.series_value is not None:
                for index, time in enumerate(times):
                    if(time >= args.series_value):
                        found = True
                        tally = dictionary['tally_cycle_data'][index]
                        dictionary_data.append(tally)  
                        dictionary_names.append(name + ' ' + args.series_key + " = " + str(time))
                        break
                    
            if not found:
                tally = dictionary['tally_cycle_data'][-1]
                dictionary_data.append(tally)  
                dictionary_names.append(name + ' ' + args.series_key + " = " + str(times[-1]))



        # plot dictionaries based on input arguments
        self.dict_ploter.plot_dict(args,dictionary_data,dictionary_names)
    
    def plot_interactive_tally_parser(self, subparser):
        plot_parser = subparser.add_parser('iplot',help='Load a previously created pickle files (your_run.p) for interactive plotting or a set of output files to be parsed and plotted')
        input_type_parser = plot_parser.add_mutually_exclusive_group(required=True)
        input_type_parser.add_argument('-pf','--pickle_files', dest='pickle_files', help='pickle files to be plotted (run1.p run2.p etc...)', nargs='+' )
        input_type_parser.add_argument('-tf','--tally_files', dest='tally_files', help='tally files to be parsed and plotted (tally_file1.txt tally_file2.txt etc...)', nargs='+', action='append')
        plot_parser.add_argument('-nt','--nthreads', dest='nthreads', help='Number of threads to use during parsing', nargs='?', type=int, default=0)
        if hasattr(self.opppy_parser, "add_parser_args"):
          self.opppy_parser.add_parser_args(plot_parser)
        plot_parser.set_defaults(func=self.plot_interactive_tally)
    
    def get_plot_option(self):
        '''
        Interactive request for valid plotting options
    
        '''
        while(1):
          opt = input('Additional options (-h for list and -q to quit): ')
          input_args = opt.split()
          parser = self.get_interactive_plot_parser()
          try:
            args=parser.parse_args(input_args)
            break
          except:
            parser.print_help()
          
        if args.quit:
          sys.exit(0)
    
        return args
    
    def get_interactive_plot_parser(self):
      '''
      return parser object that contains interactive plotting options
    
      '''
    
      parser = argparse.ArgumentParser(description=" Output Plotting options ", 
        epilog =" Specify the desired plotting options ", usage='')
      parser.add_argument('-q','--quit', dest='quit', help='quit program', nargs='?', type=bool, const=True, default=False)
      parser.add_argument('-n','--new', dest='new', help='generate a new plot', nargs='?', type=bool, const=True, default=False)
      parser.add_argument('-bg','--background', dest='background', help='keep plot in background', nargs='?', type=bool, const=True, default=False)
      parser.add_argument('-p','--plot', dest='plot', help='re-open plot', nargs='?', type=bool, const=True, default=False)
      parser.add_argument('-l','--labels', dest='legend_labels', help='specify the legend labels [line1_label, line2_label,...]', type=str, nargs='+')
      parser.add_argument('-rs','--resize', dest='plot_size', help='specify the plot size [x_size, y_size]', type=float, nargs=2)
      add_plot_options(parser)
      if hasattr(self.opppy_parser, "add_parser_args"):
          self.opppy_parser.add_parser_args(parser)
      return parser
    
    def plot_interactive_tally(self, args):
        '''
        This is an interactive plotter for a python dictionary.
        The plotting option are specified via an option string.
        
        arguments:
          args - argeparse data structure with pickle name info
          self.option_string - a string to be passed to get_plot_options for pre-designed plots
    
        '''
        raw_dictionary_data=[]
        raw_dictionary_names=[]
        if args.tally_files is not None:
            if hasattr(self.opppy_parser, "pre_parse"):
                self.opppy_parser.pre_parse(args)
            raw_dictionary_data, raw_dictionary_names = build_tally_dictionary_list(args.tally_files,
                                                                                    self.opppy_parser,
                                                                                    nthreads=args.nthreads)
            if hasattr(self.opppy_parser, "post_parse"):
                for data in raw_dictionary_data:
                    self.opppy_parser.post_parse(args, data)
        else:
            for pickle_file_name in args.pickle_files:
                raw_dictionary_names.append(pickle_file_name.split('/')[-1].split('.p')[0])
                raw_dictionary_data.append(pickle.load(open(pickle_file_name,'rb')))

        option_parser = self.get_interactive_plot_parser()
        option = option_parser.parse_args(["--new"])
        ptype = []
        while(1):
          if option.new or option.background:
            close()
            plot_labels = self.get_plot_options(self.option_string)
     
            xsize = 8
            ysize = 5

            try:
                fig = figure(figsize=(xsize,ysize))
            except:
                PyPloter.switch_backend('agg')
                fig = figure(figsize=(xsize,ysize))
    
            xlog_flag = 0
            ylog_flag = 0
    
            counter = 1
            labels = []
            for i in range(len(plot_labels)):
              if self.dict_ploter.is_data_available(plot_labels[i][-1],raw_dictionary_data[0]['tally_cycle_data'][-1]):
                labels.append(plot_labels[i])
                counter = counter + 1
            
            for i in range(0,len(labels),2):
              if i+1<counter-1:
                print('%3i  %-50s  %3i %-50s' %(i+1, labels[i][0], i+2, labels[i+1][0]))
              else:
                print('%3i  %-50s' %(i+1, labels[i][0]))
    
            plot_num = get_option_num(counter)-1
            label = labels[plot_num][0]
            plot_args = labels[plot_num][-1]
            plot_args.series_value = get_option_series_value(plot_args.series_key,raw_dictionary_data[0][plot_args.series_key])

            # build up plotting dictionary list and names
            dictionary_data = []
            dictionary_names = []
            for dictionary, name in zip(raw_dictionary_data,raw_dictionary_names):
                found = False
                times = dictionary[plot_args.series_key]
                if plot_args.series_value is not None:
                    for index, time in enumerate(times):
                        if(time >= plot_args.series_value):
                            found = True
                            tally = dictionary['tally_cycle_data'][index]
                            dictionary_data.append(tally)  
                            dictionary_names.append(name + ' ' + plot_args.series_key + " = " + str(time))
                            break
                        
                if not found:
                    tally = dictionary['tally_cycle_data'][-1]
                    dictionary_data.append(tally)  
                    dictionary_names.append(name + ' ' + plot_args.series_key + " = " + str(times[-1]))


            if plot_args.y_value_names[0] == "select_key":    
                keys = list(dictionary_data[-1][plot_args.dictionary_name].keys())
                keys.remove(plot_args.x_value_name)
                for i, key in zip(list(range(len(keys))),keys): 
                  if (i & 1)==0:
                    print('%3i  %-50s' %(i+1, key), end=' ')
                  else:
                    print('%3i  %-50s' %(i+1, key))
                print()
                plot_args.y_value_names = get_key_num_vec(keys)
    
          last_xmin = None
          last_xmax = None
          last_ymin = None
          last_ymax = None
          
          if len(plot_args.scale_x) != len(dictionary_data):
              if len(plot_args.scale_x) == 0:
                plot_args.scale_x = [1.0]*len(dictionary_data)
              else:
                plot_args.scale_x = [plot_args.scale_x[-1]]*len(dictionary_data)

          if len(plot_args.scale_y) != len(dictionary_data):
              if len(plot_args.scale_y) == 0:
                plot_args.scale_y = [1.0]*len(dictionary_data)
              else:
                plot_args.scale_y = [plot_args.scale_y[-1]]*len(dictionary_data)

          for dictionary, name, scale_x, scale_y in zip(dictionary_data, dictionary_names, plot_args.scale_x, plot_args.scale_y):
            data = dictionary[plot_args.dictionary_name]
    
            xmin = []
            xmax = []
            ymin = []
            ymax = []
            plabels = []
            x = []
            y = []
            xmin.append(min(data[plot_args.x_value_name])*scale_x)
            xmax.append(max(data[plot_args.x_value_name])*scale_x)
            ymin.append(min(data[plot_args.y_value_names[0]])*scale_y)
            ymax.append(max(data[plot_args.y_value_names[0]])*scale_y)
            # material specific plot
            for yname in plot_args.y_value_names:
              x.append(array(data[plot_args.x_value_name])*scale_x)
              ymin[-1] = min(ymin[-1],min(data[yname])*scale_y)
              ymax[-1] = max(ymin[-1],max(data[yname])*scale_y)
              plabels.append(label+" "+yname)
              if (option.no_y_names):
                  plabels[-1] = ''
              y.append(array(data[yname])*scale_y)
    
            xmin = array(xmin)
            xmax = array(xmax)
            ymin = array(ymin)
            ymax = array(ymax)
            if last_xmin is not None:
              xmin = min(last_xmin,xmin.min())
              xmax = max(last_xmax,xmax.max())
              ymin = min(last_ymin,ymin.min())
              ymax = max(last_ymax,ymax.max())
            else:
              xmin = xmin.min()
              xmax = xmax.max()
              ymin = ymin.min()
              ymax = ymax.max()
            last_xmin = xmin
            last_xmax = xmax
            last_ymin = ymin
            last_ymax = ymax
    
            xlab = plot_args.x_label
            ylab = plot_args.y_label
            if option.x_limits is not None:
              xmin = option.x_limits[0] 
              xmax = option.x_limits[1]
            if option.y_limits is not None:
              ymin = option.y_limits[0] 
              ymax = option.y_limits[1]
            if option.x_label is not None:
              xlab = option.x_label
            if option.y_label is not None:
              ylab = option.y_label
            if option.legend_labels is not None:
              if len(plabels) < len(option.legend_labels):
                  print("You specified more labels then there are plots")
              else:
                  for i in range(len(option.legend_labels)):
                      plabels[i] = option.legend_labels[i]
            if option.plot_size is not None:
              fig = figure(figsize=(option.plot_size[0],option.plot_size[1]))
              if not option.hide_plot:
                show(block=False)
    
            for i in range(len(x)):
              logplot(option.log_x,option.log_y,x[i],y[i],label=name+" "+plabels[i])
    
            if option.data_file_name is not None:
              output_file_temp = option.data_file_name 
              for i in range(len(x)):
                outfile_name = output_file_temp.strip()+"_"+str(name+"_"+plabels[i]).replace(" ","_").replace('/','_').replace('#','num')
                outfile =  open(outfile_name,'w')
                print("# ", xlab, ylab, file=outfile)
                for j in range(len(x[i])):
                  print('%15e  %15e' %(x[i][j], y[i][j]), file=outfile)
                print("Data written to - ", outfile_name)
                outfile.close()
      
            xlabel(xlab)
            ylabel(ylab)
            
            legend(loc='best').draw_frame(0)
            xlim(xmin,xmax)
            ylim(ymin,ymax)
            
            if not option.hide_plot:
              show(block=False)
    
            draw()
    
    
          if option.figure_name is not None:
            savefig(option.figure_name)
          
          if not option.hide_plot:
            show(block=False)
    
          option = self.get_plot_option()
          if option.background:
            figure()
          else:
            clf()
    
    def get_plot_options(self, label_string):
      '''
      Get pre-formated plotting options for the interactive ploter
       
      Input Options:
        label_string preformated string for expected data in a
        dictionary
    
      This expects a two column semicolon (;) separated text
      format string. The first column is an arbitrary string that
      will be printed by the interactive plotter as a plot the
      user can pick. The second column in a dictionary plotting
      command (more details in the examples below).
    
      examples:
        "your first fancy plot name; -sk time -dn your_dictionary_key -x your_x_data_key   -xlab "time [s]"  -y your_y_data_key  -ylab "RSS [%]";
        "your second fancy plot name; -sk cycle -dn your_dictionary_key -x bins   -xlab "bin [#]"  -y select_key  -ylab "tally_count [#]";
    
     The dictionary plotting command has some basic requirements
     include a dictionary name (-dn) the x variable key (-x), the y
     variable key (-y), the x axis lable (-xlab), and the y axis
     label (-y). There are more details about available plotting
     options in plot_dictionary.py. The "-y select_key" value is a
     magic key word that tells the interactive ploter to provide a
     list of all y_data options for the designated dictionary.
      '''
      plot_labels = []
    
      label_file = io.StringIO(label_string)
      raw = label_file.readlines()
      for line in raw:
          lines = line.strip().split(';')
          if len(lines) == 3:
            labels = []
            labels.append(lines[0])
            labels.append(self.parse_tally_plot_args(lines[1]))
            plot_labels.append(labels)
      return plot_labels
    
    def parse_tally_plot_args(self, input_string):
      '''
      Returns a set of parsed dictionary plotting options from an input_string
    
      '''
      parser = argparse.ArgumentParser(description=" Tally Plotting options ", 
        epilog =" Specify the desired plotting options ", usage='')
      parser.add_argument('-dn','--dictionary_name', dest='dictionary_name', help='dictionary that the plotting data is contained in', required=True, type=str)
      parser.add_argument('-x','--x_data', dest='x_value_name', help='dictionary data to be plotted on the x axis.', required=True)
      parser.add_argument('-y','--y_data', dest='y_value_names', help='dictionary data to be plotted on the y axis.', required=True, action='append')
      parser.add_argument('-sk','--series_key', dest='series_key', help='Series key string to access the data (i.e time or cycle)', nargs='?', required=True)
      parser.add_argument('-sv','--series_value', dest='series_value', help='Series value to plot the data at (default is the last value of the series_key data)', nargs='?', action='append', type=float, default=None)
      if hasattr(self.opppy_parser, "add_parser_args"):
          self.opppy_parser.add_parser_args(parser)
      add_plot_options(parser);
    
      return parser.parse_args(shlex.split(input_string))
    
    def run(self,input_string = None):
        if input_string:
            args = self.parser.parse_args(shlex.split(input_string))
        else:
            args = self.parser.parse_args()
        args.func(args)


