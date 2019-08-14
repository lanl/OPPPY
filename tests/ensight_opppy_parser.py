#!/usr/bin/env python
# ---------------------------*-python-*----------------------------------------#
# file   ensight_opppy_parser.py
# author mathew cleveland
# date   March 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
import sys
import os

sys.path.append('..')

import unittest
from test import support
import shlex
import numpy as np

from opppy.interactive_utils import *
from opppy.plotting_help import *


'''
OPPPY ensight dump parsing class
'''
class ensight_opppy_dump_parser():
    '''
    OPPPY dump parser for ensight files
    '''
    def append_case_dictionary(self, dump_dictionary, case_filename, dump_keys=None):
      # initialize the cycle parsing data
      self.case_filename = case_filename

      # get geometry file name
      case_lines = open(self.case_filename,'r').readlines()
      found = False
      for line in case_lines:
        if "model:" in line:
          self.geom_filename = os.path.dirname(self.case_filename) + "/" +  line.split(': ')[-1].strip('\n')
          found = True
          break
      if not found:
        print("Could not find geometry file")
        sys.exit(0)

      valid_geom_list = ['quad4']
      geom_lines = open(self.geom_filename).readlines()
      found = False
      valid_geom = ''
      for valid_geom in valid_geom_list:
          if any([valid_geom in line for line in geom_lines]):
              found = True
              break
      # Check valid geometry file
      if not found:
        print("Unsupported geometry type specifed in ",self.geom_filename)
        sys.exit(0)

      # extract case file data
      data = {}
      keys = []
      data_files = []
      times = []
      filename_int_count = 0
      number_of_steps = 0
      filename_start_number = 0
      filename_increment = 0
      read_key = False
      read_time = False
      read_time_values = False
      for line in case_lines:
          if "TIME" in line and len(line)==5:
              read_time = True
          if "VARIABLE" in line and len(line)==9:
              read_key = True
              continue
          if len(line) == 1:
              read_key = False
              read_time = False
          if read_key:
              key = line.strip('\n').split()[4]
              if dump_keys is not None:
                  if key in dump_keys:
                      keys.append(key)
              else:
                keys.append(key)
              filename_int_count = len(line.strip('\n').split()[-1])-len(line.strip('\n').split()[-1].strip('*'))
              shortname = line.strip('\n').split()[-1].strip('*')
              data_files.append(os.path.dirname(self.case_filename) + "/" + shortname )
          elif read_time:
              if "number of steps" in line:
                  number_of_steps = int(line.split()[-1])
              elif "filename start number" in line:
                  filename_start_number = int(line.split()[-1])
              elif "filename increment" in line:
                  filename_increment = int(line.split()[-1])
              elif "time values" in line:
                  read_time_values = True
                  continue
              if read_time_values:
                  times.append(float(line))


      if number_of_steps is not len(times):
          print("Number of steps does not patch number of time points in case file")
          sys.exit(0)

      # extract geometry data
      read_coord = False
      read_cell = False
      part_count = 0
      coord_num = 0
      coord_count = -1
      cell_num = 0
      cell_count = -1
      cell_ids = []
      cell_coords = []
      coord_ids = []
      coord_x = []
      coord_y = []
      coord_z = []
      for line in geom_lines:
          if "part" in line:
              part_count += 1
              if part_count is not 1:
                  print("Error: multiple parts found in geom file (this is currently not supported by this OPPPY parser")
                  sys.exit(0)
          if "coordinates" in line:
              read_coord = True
              continue
          if read_coord:
            if coord_count == -1:
              coord_num = int(line)
              coord_count += 1
            elif coord_count < coord_num:
              coord_ids.append(int(line))
              coord_count += 1
            elif coord_count < coord_num*2:
              coord_x.append(float(line))
              coord_count += 1
            elif coord_count < coord_num*3:
              coord_y.append(float(line))
              coord_count += 1
            elif coord_count < coord_num*4:
              coord_z.append(float(line))
              coord_count += 1
            else:
              read_coord = False
          if valid_geom in line:
              read_cell = True
              continue
          if read_cell:
              if cell_count == -1:
                  cell_num = int(line)
                  cell_count += 1
              elif cell_count < cell_num:
                  cell_ids.append(float(line))
                  cell_count += 1
              elif cell_count < cell_num*2:
                  cell_coords.append(str_vector_to_int_vector(line.strip('\n').split()))
                  cell_count += 1
              else:
                  read_cell = False

      # calculate average cell position
      ave_x = []
      ave_y = []
      ave_z = []
      for coords in cell_coords:
        ave_x.append(sum([coord_x[coord_id-1] for coord_id in coords])/len(coords))
        ave_y.append(sum([coord_y[coord_id-1] for coord_id in coords])/len(coords))
        ave_z.append(sum([coord_z[coord_id-1] for coord_id in coords])/len(coords))
     
      # build up the data dictionary
      dumpname_prefix = os.path.split(self.case_filename)[-1].split('.')[0]
      for filenumber, time in zip(range(filename_start_number, number_of_steps, filename_increment), times):
        data = {}
        dumpname = dumpname_prefix + '.{:0{prec}d}'.format(filenumber, prec=filename_int_count)
        # skip previously append dumps
        if dumpname in dump_dictionary.keys():
            continue
        data['time'] = np.array([time])
        data['x'] = np.array(ave_x)
        data['y'] = np.array(ave_y)
        data['z'] = np.array(ave_z)
        for key, datafile_prefix in zip(keys, data_files):
            datafile = datafile_prefix + '{:0{prec}d}'.format(filenumber, prec=filename_int_count)
            datalines = open(datafile,'r').readlines()
            values = []
            readvalues = False
            for line in datalines:
                if valid_geom in line:
                    readvalues = True
                    continue
                if readvalues:
                    values.append(float(line))
            data[key]=np.array(values)
        dump_dictionary[dumpname]=data

      return dump_dictionary


'''
This is an interactive OPPPY parser for ensight dump flies
'''
parser = argparse.ArgumentParser(description="Interactive Ensight parser for fancy plotting")
parser.add_argument('-t','--times', dest='times', help='Time value to plot the data at (default is the last value of the time data in the case file)', nargs='?', type=float, default=None)

# initialize the dump parser
opppy_dump_parser = ensight_opppy_dump_parser()

# setup the interactive dump parser
parser.set_defaults(func=parser.parse_args)

d_parser = interactive_dump_parser(opppy_dump_parser, parser)

args = parser.parse_args()
args.func(args)
