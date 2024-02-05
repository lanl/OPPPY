# ---------------------------*-python-*----------------------------------------#
# file   tally.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
'''
Utilities to extract cycle tally data 

.. autosummary::

  append_tally_data
  append_tally_cycle_data
  print_pickle_tally
  print_tally_data
  append_tally_dictionary
  build_tally_dictionary_list
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
from opppy.output import *

def append_tally_data(cycle_data, data, sort_key_string):
    '''
    This function appends a dictionary of tally cycle data to an
    existing dictionary
    
    arguments:
      tally_cycle_data - python dictionary of tally data
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

    if 'tally_cycle_data' in data:
        append_tally_cycle_data(data, cycle_data, cycle_info, sort_key_string)
    else:
        data['tally_cycle_data'] = [cycle_data]
        for subkey in list(cycle_info):
          data[subkey] = [cycle_info[subkey]]


    return data

def append_tally_cycle_data(tally_data, cycle_data, cycle_info, sort_key_string):
    '''
    Append tally cycle data into the tally_data 

    arguments:
    tally_data - a Python dictionary of tally_data
    cycle_data - a Python dictionary of cycle_data
    cycle_info - a Python dictioanry of cycle_info
    sort_key_string - the string key used to access the data from cycle_info
      dictionary to sort the data
    '''
    # get the current cycle time
    time = cycle_info[sort_key_string]
    # get the list of cycle times in the tally_data
    times = tally_data[sort_key_string] 
    number_of_time_steps = len(times)
    reversed_time = reversed(times)
    for index, data_time in zip(list(range(number_of_time_steps,0,-1)),reversed_time):
        if(data_time == time):
            # replace the cycle data
            tally_data['tally_cycle_data'][-1] = cycle_data
            # replace the cycle_info data
            for subkey in list(cycle_info):
                tally_data[subkey][-1] = cycle_info[subkey]
            break
        elif(data_time > time):
            # pop the old data off the data arrays
            tally_data['tally_cycle_data'].pop(-1)
            for subkey in list(cycle_info):
                tally_data[subkey].pop(-1)
        else:
            # extend existing arrays
            tally_data['tally_cycle_data'].append(cycle_data)
            # fill the cycle_info data
            for subkey in list(cycle_info):
                tally_data[subkey].append(cycle_info[subkey])
            break



def print_pickle_tally(args):
    '''
    print_pickle_tally - 
      This function prints all relevant data in a pickle tally file
    
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
        print_tally_data(data)


def print_tally_data(data):
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
    print("This tally_data has been appended in the following order:")
    print("######################################################")
    for file_name in data['appended_files']:
        print(file_name)
    print("######################################################")

    print("This tally_data has the following dictionary items:")
    print("######################################################")
    keys = data['problem_data']['cycle_info_keys']
    print("cycle_info data:")
    for key in sorted(keys):
        print("  #_of_entries = ", len(data[key]), "\n    ","min_"+key," = ", min(data[key]), "\n    ","max_"+key," = ",max(data[key]),end='\n')
    print('')

    keys = list(data['problem_data'].keys())
    print("problem_data keys:")
    for key in sorted(keys):
        if not type(data['problem_data'][key]) is list:
            print("  "+key)
    print('')

    keys = list(data['problem_data'].keys())
    print("cycle_data keys:")
    for key in sorted(keys):
        if type(data['problem_data'][key]) is list:
            if key in 'cycle_info_keys':
                continue
            print("  dictionary - "+key)
            stride = 2
            count = 0
            subkeys = data['problem_data'][key]
            for subkey in subkeys:
                if count%stride or count==len(subkeys)-1:
                    print("    ", subkey)
                else:
                    print("    ",subkey, end='')
                count+=1
    print('')
    print("######################################################")

def append_tally_dictionary(data, output_files, opppy_parser, append_date=False, nthreads=0):
    '''
    Append tally data from a list of output_files to a user provided dictionary using a user proved
    opppy_parser. By default this function will use the multiprocessing option to parallelize the
    parsing of multiple dumps.'


    arguments:
        data opppy input dictionary to be append to (must have a 'verion' opppy key)
        output_files a list of output files to parse
        opppy_parser a user defined OPPPY tally parser for the output files
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
          thread_cycle_string_list = get_output_lines(file_name, opppy_parser.cycle_opening_string, opppy_parser.cycle_closing_string, opppy_parser.file_end_string)
          thread_data=[]
          for cycle_string in thread_cycle_string_list:
              thread_data.append(extract_cycle_data(cycle_string, opppy_parser))
          result_l[file_index] = thread_data
          
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
                       data = append_tally_data(cycle_data,data,opppy_parser.sort_key_string)
                del result_l
                del threads
    else:
      for file_name in output_files:
        cycle_string_list = get_output_lines(file_name, opppy_parser.cycle_opening_string, opppy_parser.cycle_closing_string, opppy_parser.file_end_string)
        for cycle_string in cycle_string_list:
            cycle_data = extract_cycle_data(cycle_string, opppy_parser)
            data = append_tally_data(cycle_data,data,opppy_parser.sort_key_string)
        count += 1
        progress(count,total, 'of input files read')

    print('')
    print('')
    print_tally_data(data)

def build_tally_dictionary_list(file_lists, opppy_parser, nthreads=0):
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
        append_tally_dictionary(data, output_files, opppy_parser, nthreads=nthreads)
        dictionary_data.append(data)
    
    
    return dictionary_data, dictionary_names



