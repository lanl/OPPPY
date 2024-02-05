# ---------------------------*-python-*----------------------------------------#
# file   output.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
'''
Utilities to extract cycle data from outputs

.. autosummary::

  append_cycle_data
  append_data
  print_pickle_data
  print_dictionary_data
  get_output_lines
  extract_cycle_data
  append_output_dictionary
'''

#----------------------------------------------------------#
#  The main code for generating an output pickle file
#----------------------------------------------------------#

import sys
import io
import os
import math
import platform
import numpy as np
import pickle
if "linux" in platform.system().lower(): 
    from multiprocessing import Process, Manager, cpu_count
else:
    # Protect against multiprocessing fork issue on Windows and Mac
    from multiprocess import Process, Manager, cpu_count

from opppy.version import __version__
from opppy.progress import *

def append_cycle_data(cycle_data, data, sort_key_string):
    '''
    This function appends a dictionary of cycle data to an
    existing dictionary
    
    arguments:
      cycle_data - python dictionary of cycle data
      data - python dictionary of data 
      sort_key_string - string used to access the sorting data in the 'cycle_info' dictionary
    
    Output:
      data - python dictionary of appended data
    '''
    try:
        cycle_info = cycle_data.pop('cycle_info') 
        cycle_value = cycle_info[sort_key_string]
    except:
        print("Error: No cycle info was found")
        sys.exit(0)

    # Check that the problem data for the cycle matches the current data
    # problem data.
    if 'problem_data' in data:
        problem_data = data.pop('problem_data')
        cycle_problem_data = cycle_data.pop('problem_data')
        for key in list(cycle_problem_data.keys()):
            if key in problem_data:
                if isinstance(cycle_problem_data[key],(list,tuple,np.ndarray)):
                    if len(problem_data[key]) != len(cycle_problem_data[key]):
                        print("Error: Problem data doesn't match")
                        print("len(previous_problem_data[", key, "] --", len(problem_data[key]))
                        print("len(cycle_problem_data[", key, "] --", len(cycle_problem_data[key]))
                        sys.exit(0)
                    for index, problem_value, cycle_value in zip(list(range(len(problem_data[key]))), problem_data[key], cycle_problem_data[key]):
                      if (problem_value != cycle_value):
                        print("Error: Problem data doesn't match")
                        print("previous_problem_data[", key, "][",index,"] --", problem_value)
                        print("cycle_problem_data[", key, "][",index,"] --", cycle_value)
                        sys.exit(0)
                elif problem_data[key] != cycle_problem_data[key]:
                    print("Error: Problem data doesn't match")
                    print("previous_problem_data = ", key, "--", problem_data[key])
                    print("cycle_problem_data = ", key, "--", cycle_problem_data[key])
                    sys.exit(0)
            else:
               problem_data[key] = cycle_problem_data[key]
        data['problem_data'] = problem_data
    else:
        if ('problem_data' in cycle_data):
            data['problem_data'] = cycle_data.pop('problem_data')

    for key in list(cycle_data.keys()):
        if not bool(cycle_data[key]):
            continue
        elif key in data:
            dict_data = data.pop(key)
            cycle_dict_data = cycle_data.pop(key)
            data[key] = append_data(dict_data, cycle_dict_data, cycle_info, sort_key_string)
        elif cycle_data[key]:
            data[key] = cycle_data[key]
            # make the sub array data a list so we can append it later
            for subkey in list(data[key].keys()):
                data[key][subkey] = [data[key][subkey]]
            for subkey in list(cycle_info):
                data[key][subkey] = [cycle_info[subkey]]
    return data



def append_data(data, cycle_data, cycle_info, sort_key_string):
    '''
    This function appends the cycle OPPPY data into an existing
    data dictionary based on the current cycle and time.
    
    arguments:
      data - python dictionary of data 
      cycle_data - python dictionary of cycle data
      cycle_info - python dictionary of cycle info (i.e. time and cycle)
      sort_key_string - key string used to access the cycle_info data value to sort the data
    
    Output:
      data - python dictionary of appended data
    '''
    time = cycle_info[sort_key_string]
    last_time = data[sort_key_string][-1]
    # pop off any old data 
    if(time<=last_time):
        reversed_time = reversed(data[sort_key_string])
        dict_keys = list(data.keys())
        for data_time in reversed_time:
            if(data_time >= time):
                # pop the old data off the data arrays
                for key in dict_keys:
                    data[key].pop(-1)
            else:
                break

    # Now the data array is clean of duplicate data we can do a simple append
    # extend existing arrays
    for key in data.keys():
        data[key].append(0)
    # fill the cycle_info data
    for subkey in list(cycle_info):
        data[subkey][-1] = cycle_info[subkey]
    # filly the cycle data 

    cycle_keys = list(cycle_data.keys())
    for key in cycle_keys:
        if key in data:
            data[key][-1] = cycle_data[key]
        else:
            # Backfill missing data with zeros
            data[key] = [0]*len(data[sort_key_string])
            data[key][-1] = cycle_data[key]
    return data


def print_pickle_data(args):
    '''
    print_pickle_data - 
      This function prints all relevant data in a pickle file
    
      arguments:
        args - argeparse data structure with pickle name info
    '''
    file_list = []
    for sublist in args.pickle_files:
      for item in sublist:
        file_list.append(item)
    # load data from the pickle
    pickle_data=[]
    pickle_names=[]
    for pickle_file_name in file_list:
        pickle_names.append(pickle_file_name.split('/')[-1])
        pickle_data.append(pickle.load(open(pickle_file_name,'rb')))

    for data, name in zip(pickle_data, pickle_names):
        print("######################################################")
        print("#############    Data for ", name, "  #################")
        print_dictionary_data(data)


def print_dictionary_data(data):
    '''
    print_dictionary_data - 
      List the data available in the python dictionary
    
      arguments:
       data - python dictionary data to be read
    '''
    print("######################################################")
    print("##      Built with: OPPPY " +data['version']+ '     ##')
    print("######################################################")
    print("#############     APPEND FILE HISTORY      ###########")
    print("######################################################")
    print("This pickle has been appended in the following order:")
    print("######################################################")
    for file_name in data['appended_files']:
        print(file_name)
    print("######################################################")

    print("This pickle has the following dictionary items:")
    print("######################################################")
    for key in list(data.keys()):
        if key == 'appended_files' or key == 'version':
            continue
        print(key,":", end='\n  ')
        if 'time' in data[key] and len(data[key]['time'])>0:
            print("#_of_entries = ", len(data[key]['time']), "\n  min_time =", min(data[key]['time']), "\n  max_time = ",max(data[key]['time']),end='\n  ')
        keys = list(data[key].keys())
        print("keys:")
        stride = 2
        count = 0
        for key in sorted(keys):
            if count%stride or count==len(keys)-1:
                print("    ", key)
            else:
                print("    ",key, end='')
            count+=1
        print('')
    print("######################################################")


 
def get_output_lines(filename,opening_string,closing_string, file_end_string=None):
    '''
    Chunk the output file into "cycle strings" (recursive sets of data in a
    file isolated by an opening and closing string.

    arguments:
        filename a string designated the file that should be read
        opening_string a string designated the beginning of cycle data
        closing_string a string designated the end of cycle data
        file_end_string a string that tells the parser the output file completed without error. The goal of this is to prevent parsing of incomplete cycle data.

    and example text::
        
        This example data file will be broken up based on multiple cycles

        #cycle 1
        some data here 
        
        #cycle 2
        some more data here

        #end of file 
        
    This function would parse this deck into two cycle strings if called like this::

        >> get_output_liens(my_example_file, "#cycle","#cycle", "#end of file") 

    would split the data up into the flowing list::

        ["#cycle 1\nsome data here\n\n","#cycle 2\nsome more data here"]

    '''
    output = []
    output_file = open(filename,'r')
    raw = output_file.readlines()
    cycle_lines = []
    temp_lines = ''
    reading_cycle = False
    for line in raw:
      if not reading_cycle and opening_string in str(line) :
          reading_cycle = True
      elif reading_cycle and closing_string in str(line):
          # catch the special exception when the line is a return character
          if closing_string == '\n' and len(line) != 1:
              temp_lines += line
              continue
          reading_cycle = False
          if opening_string in str(line):
           # push the buffer into the cycle lines 
            reading_cycle = True
            cycle_lines.append(temp_lines)
            temp_lines = ''
          else:
           # push the buffer into the cycle lines 
            cycle_lines.append(temp_lines+line)
           # include this line into the buffer
            temp_lines = ''
           # skip the append because this line was included in the buffer
            continue 
      # append the line to the buffer
      elif file_end_string is not None and file_end_string in str(line):
            cycle_lines.append(temp_lines+line)
            cycle_lines[-1] += line
            temp_lines = ''
            break 
      if reading_cycle:
        temp_lines += line
    output_file.close()
    return cycle_lines
 

def extract_cycle_data(cycle_string, my_opppy_parser):
    '''
    This function takes a list of cycle data strings and extracts
    them using a user supplied opppy_parser. The extracted data is
    placed in dictionary format. 

    arguments:
      my_opppy_parser is a simple user defined python class with a parser function that returns a cycle dictionary. The dictionary must contain a "problem_data" dictionary with a cycle and time dictionary. The remaining dictionary items can should be packed such they can be appended to an overaching dictionary.
      cycle_string a cycle string extracted from the output file.
    '''
    if type(cycle_string) is not str:
      print("cycle_string object is not a list")
      print(type(cycle_string))
      print(cycle_string)
      sys.exit(0)
    if not hasattr(my_opppy_parser, "parse_cycle_string"):
      print("my_opppy_parser does not have a parse_cycle_string function")
      sys.exit(0)

    cycle_dictionary = my_opppy_parser.parse_cycle_string(cycle_string)

    return cycle_dictionary

def append_output_dictionary(data, output_files, opppy_parser, append_date=False, nthreads=0):
    '''
    Append output data from a list of output_files to a user provided dictionary using a user proved
    opppy_parser. By default this function will use the multiprocessing option to parallelize the
    parsing of multiple dumps. The parallel parsing can be disabled by setting
    the environment variable 'OPPPY_USE_THREADS=False'


    arguments:
        data opppy input dictionary to be append to (must have a 'verion' opppy key)
        output_files a list of output files to parse
        opppy_parser a user defined OPPPY parser for the output files
        append_date bool to specify if the data should be appended to the file
            name for tracking purposes 
    '''
    if not 'version' in data or not (data['version'] == __version__):
      print('')
      print("Error: data dictionary does not match this version of OPPPY")
      if 'version' in data:
        print("data dictionary was build with version", data['version'])
      else:
        print("This data dictionary has no version")
      print("This version of OPPPY is ", __version__)
      sys.exit(0)
    time = ''
    if append_date:
      time = time+'.'+datetime.datetime.now().strftime ("%Y%m%d%H%M%S")
    for file_name in output_files:
      if 'appended_files' in data:
          data['appended_files'].append(file_name.split('/')[-1]+time)
      else:
          data['appended_files'] = [file_name.split('/')[-1]+time]

    count = 0
    total = len(output_files) 
    print('')
    print("Number of files to be read: ", total)
    nthreads = cpu_count() if nthreads < 0 else nthreads
    if(nthreads>0):
      def thread_all(file_name, file_index, result_l):
          thread_cycle_string_list = get_output_lines(file_name, opppy_parser.cycle_opening_string,
                 opppy_parser.cycle_closing_string, opppy_parser.file_end_string);
          thread_data = []
          for cycle_string in thread_cycle_string_list:
                thread_data.append(extract_cycle_data(cycle_string, opppy_parser))
          result_l[file_index]=thread_data
      print("Number of threads used for processing: ",nthreads)
      for stride in range(math.ceil(float(total)/float(nthreads))):
          files = output_files[nthreads*stride:min(nthreads*(stride+1),len(output_files))]
          with Manager() as manager:
                result_l = manager.list(range(len(files)))
                threads = []
                for file_index, file_name in enumerate(files):
                    thread = Process(target=thread_all, args=(file_name, file_index, result_l,))
                    thread.start()
                    threads.append(thread)
                for thread in threads:
                    thread.join()
                    count += 1
                    progress(count,total, 'of input files read')
                for file_data in result_l:
                    for cycle_data in file_data:
                        data = append_cycle_data(cycle_data,data,opppy_parser.sort_key_string)
                del result_l
                del threads
    else:
      for file_name in output_files:
        cycle_string_list = get_output_lines(file_name, opppy_parser.cycle_opening_string, opppy_parser.cycle_closing_string, opppy_parser.file_end_string)
        for cycle_string in cycle_string_list:
            cycle_data = extract_cycle_data(cycle_string, opppy_parser)
            data = append_cycle_data(cycle_data,data,opppy_parser.sort_key_string)
        count += 1
        progress(count,total, 'of input files read')

    print('')
    print('')
    print_dictionary_data(data)

def build_output_dictionary_list(file_lists, opppy_parser, nthreads):
    '''
    append_pickle - 
      This function generates a opppy output dictionary
      data from an output file.
    
      args:
        args - Parsed input arguments
    '''
    dictionary_data = []
    dictionary_names = []
    for output_files in file_lists:
        # add a data name to go with the data sets
        dictionary_names.append(output_files[0])
        # build a new dictionary
        data = {}
        data['version'] = __version__
        append_output_dictionary(data, output_files, opppy_parser, nthreads=nthreads)
        dictionary_data.append(data)
    
    
    return dictionary_data, dictionary_names



