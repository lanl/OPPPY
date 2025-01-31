# a simple example opppy tally parser
import sys
import re
from numpy import array

sys.path.append('..')

from opppy.plotting_help import *

class my_test_opppy_tally_parser():
    '''
    An example OPPPY parser that can extract simple cycle string
    data and return a cycle tally dictionary
    '''
    def __init__(self):
      # initialize the cycle parsing data
      self.sort_key_string = 'cycle'
      self.cycle_opening_string = "cycle"
      self.cycle_closing_string = "\n"
      self.file_end_string = None
      print("Initializing my_test_opppy_tally_parser")

    def add_parser_args(self, parser):
        parser.add_argument('-ppt', '--pre_parser_test', dest="pre_parser_test", nargs="?", default=None)

    def pre_parse(self, args):
        if(args.pre_parser_test is not None):
            print("pre_parse hook works: args.pre_parser_test")
        else:
            print("pre_parse hook works: None")


    def parse_cycle_string(self,cycle_string):
      cycle_data_keys = ['bins','odd_counts','even_counts']
      cycle_info_keys = ['time', 'cycle']
      # return dictionary of dictionaries 
      data_dict = {}
      problem_data_dict = {}
      problem_data_dict['cycle_info_keys'] = cycle_info_keys
      problem_data_dict['cool_counts'] = cycle_data_keys
      cycle_info = {}
      # initial internal dictionaries
      counts = {}

      # parse string and build up dictionaries
      for line in cycle_string.splitlines():
           # get cycle info
            for key in cycle_info_keys:
                if key in line and len(key) is len(line.split(':')[0]):
                    cycle_info[key] = float(line.split(':')[-1])
            # get tally info
            for key in cycle_data_keys:
                if key in line and len(key) is len(line.split(':')[0]):
                    counts[key] = array(str_vector_to_float_vector(line.strip('\n').split(' ')[1:]))
                    # add the total counts for this cycle
                    if 'counts' in line:
                        data_dict["n_"+key] = sum(counts[key])

                    # store problem data
                    if key is 'bins':
                        problem_data_dict[key] = array(str_vector_to_float_vector(line.strip('\n').split(' ')[1:]))
                        problem_data_dict['number_of_bins'] = len(problem_data_dict[key])
       
    
      # append the sub-dictionaries
      data_dict['problem_data'] = problem_data_dict
      data_dict['cycle_info'] = cycle_info
      data_dict['cool_counts'] = counts

      return data_dict

    def post_parse(self, args, data):
       print("Post Parse Test Data keys: ",data.keys())


