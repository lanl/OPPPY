#!/usr/bin/env python
# ---------------------------*-python-*----------------------------------------#
# file   my_interactive_parser.py
# author mathew cleveland
# date   February 2019
# note   Copyright (C) 2019, Los Alamos National Security, LLC.
#        All rights reserved.
# -----------------------------------------------------------------------------#
import sys

sys.path.append('..')

import unittest
from test import support
import shlex

from opppy.interactive_utils import *

'''
This is an example interactive parser that can be build up with OPPPY
'''
parser = argparse.ArgumentParser(description="Interactive test parser for fancy plotting")
subparser = parser.add_subparsers(help='options')

# import the test parser
from my_test_opppy_parser import my_test_opppy_parser

# initialize the output parser
opppy_parser = my_test_opppy_parser()

option_string = ''
option_string = option_string + 'Plot Density; -dn density -x time -xlab "time [s]"  -y select_key  -ylab "Density";\n'
option_string = option_string + 'Plot Test Data 1; -dn test_data1 -x time -xlab "time [s]"  -y test_data1          -ylab "Test Data 1";\n'
option_string = option_string + 'Plot Test Data 2; -dn test_data1 -x time -xlab "time [s]"  -y test_data2          -ylab "Test Data 2";\n'

# setup the interactive output parser
output_parser = subparser.add_parser("output", help='Interactive output parser')
output_parser.set_defaults(func=output_parser.parse_args)
o_parser = interactive_output_parser(opppy_parser, option_string, output_parser)


# initialize the dump parser
from my_test_opppy_dump_parser import my_test_opppy_dump_parser

# initialize the dump parser
opppy_dump_parser = my_test_opppy_dump_parser()

# setup the interactive dump parser
dump_parser = subparser.add_parser("dump", help='Interactive dump parser')
dump_parser.set_defaults(func=dump_parser.parse_args)

d_parser = interactive_dump_parser(opppy_dump_parser, dump_parser)

# initialize the hdf parser
from my_test_opppy_hdf_parser import my_test_opppy_hdf_parser

# initialize the dump parser
opppy_hdf_parser = my_test_opppy_hdf_parser()

# setup the interactive dump parser
hdf_parser = subparser.add_parser("hdf", help='Interactive hdf parser')
hdf_parser.set_defaults(func=hdf_parser.parse_args)

h_parser = interactive_dump_parser(opppy_hdf_parser, hdf_parser)

# initialize the output parser
from my_test_opppy_tally_parser import my_test_opppy_tally_parser

# initialize the output parser
opppy_tally_parser = my_test_opppy_tally_parser()


tally_string = ''
tally_string = tally_string + 'Plot Cool Counts; -sk time -dn cool_counts -x bins -xlab "bin [#]"  -y select_key  -ylab "Counts [#]";\n'
tally_string = tally_string + 'Plot Odd Counts; -sk cycle -dn cool_counts -x bins -xlab "bin [#]"  -y odd_counts  -ylab "Counts [#]";\n'
tally_string = tally_string + 'Plot Even Counts; -sk time -dn cool_counts -x bins -xlab "bin [#]"  -y even_counts  -ylab "Counts [#]";\n'


# setup the interactive tally parser
tally_parser = subparser.add_parser("tally", help='Interactive tally parser')
tally_parser.set_defaults(func=tally_parser.parse_args)
t_parser = interactive_tally_parser(opppy_tally_parser, tally_string, tally_parser)





args = parser.parse_args()
args.func(args)
