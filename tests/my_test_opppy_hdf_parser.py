# a simple example opppy hdf parser
import sys
import re
import h5py
from numpy import *

sys.path.append('..')

from opppy.plotting_help import *

class my_test_opppy_hdf_parser():
    '''
    An example OPPPY dump parser that can extract data from a simple ASCII dump file
    '''
    def __init__(self):
      # initialize the cycle parsing data
      print("Initializing my_test_opppy_hdf_parser")

    def build_data_dictionary(self, filename, dump_keys=None):
        hdf_file = h5py.File(filename, "r")
        data = {}
        keys = hdf_file.keys()

        print(keys)
        data = {}
        for key in keys:
            print(key)
            print(hdf_file)
            print(hdf_file[key])
            print(hdf_file[key])
            data[key] = hdf_file[key][:]

        hdf_file.close()

        return data
        

