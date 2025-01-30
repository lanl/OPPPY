# a simple example opppy dump parser
import sys
import re
from numpy import *

sys.path.append('..')

from opppy.plotting_help import *

class my_test_opppy_dump_parser():
    '''
    An example OPPPY dump parser that can extract data from a simple ASCII dump file
    '''
    def __init__(self):
      # initialize the cycle parsing data
      print("Initializing my_test_opppy_dump_parser")

    def build_data_dictionary(self, filename, dump_keys=None):
        dump_file = open(filename,'r')    
        lines = dump_file.readlines()
        data = {}
        keys = []
        if dump_keys:
            keys = dump_keys
        else:
            for line in lines:
                if "keys" in line and not dump_keys:
                    keys = line.strip('\n').split(' ')[1:]
                    break

        data = {}
        for line in lines:
            for key in keys:
                if key in line and len(key) is len(line.split(':')[0]):
                    data[key] = array(str_vector_to_float_vector(line.strip('\n').split(' ')[1:]))


        # build xy_verts for 2d mesh plotting example
        if 'x' in data and 'y' in data:
            xy_verts = []
            for x, y in zip(data['x'], data['y']):
                xy_verts.append([[x-0.5,y-0.5],[x+0.5,y-0.5],[x+0.5,y+0.5],[x-0.5,y+0.5]])
            data['xy_verts'] = xy_verts

        return data
        


