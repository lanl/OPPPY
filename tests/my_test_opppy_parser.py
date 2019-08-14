# a simple example opppy parser
import re

class my_test_opppy_parser():
    '''
    An example OPPPY parser that can extract simple cycle string
    data and return a cycle dictionary
    '''
    def __init__(self):
      # initialize the cycle parsing data
      self.sort_key_string = 'time'
      self.cycle_opening_string = "#"
      self.cycle_closing_string = "#"
      self.file_end_string = None
      print("Initializing my_test_opppy_parser")

    def parse_cycle_string(self,cycle_string):
      # return dictionary of dictionaries 
      data_dict = {}
      # initial internal dictionaries
      problem_data_dict = {}
      cycle_info = {}
      test_data1 = {}
      test_data2 = {}
      back_fill_data = {}
      density_data = {}
      for string in cycle_string.splitlines():
        if "cycle" in string:
          cycle = int(string.replace('# cycle ',''))
          cycle_info['cycle'] = cycle
          data_dict['cycle_info'] = cycle_info 
        if "time" in string:
          time = float(string.replace('time ',''))
          cycle_info['time'] = time
          data_dict['cycle_info'] = cycle_info
        if "test_data1" in string:
          split_string = string.split('=')
          test_data1[split_string[0]] = float(split_string[1])
          data_dict["test_data1"] = test_data1
        if "test_data2" in string:
          split_string = string.split('=')
          test_data2[split_string[0]] = float(split_string[1])
          data_dict["test_data2"] = test_data2
        if "back_fill_data" in string:
          split_string = string.split('=')
          back_fill_data[split_string[0]] = float(split_string[1])
          data_dict["back_fill_data"] = back_fill_data
        if "density" in string:
            density = float(string.split('=')[-1]) 
            mat = re.split(r'[(|)]',string)[1]
            density_data[mat] = density

      # append dictionary with multiple entries
      data_dict['density'] = density_data




      return data_dict
        
