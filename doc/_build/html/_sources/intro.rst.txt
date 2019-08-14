.. OPPPY documentation master file, created by
   sphinx-quickstart on Mon Feb 25 17:48:07 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. contents::
   :depth: 2
   :local:

================
Getting Started
================

The following sections provide a detailed over view of the expected data
formates used by OPPPY and how to write basic OPPPY parser classes to extract
and build python data dictionaries that can be used by the OPPPY plotting functions.

**********************
Important Data Formats
**********************

The OPPPY library provides support for three different types of output data
(cycle_data, output_data, tally_data, dump_data). The OPPPY library parses these different
data types and places them in unique Python data structures to make them easy
to plot: 

  * cycle_info - A Python dictionary with sub-dictionary data that can be used
    to sort/order 'cycle_data'

    * This is a sub-dictionary data type that is used to sort 'cycle_data'::

       cycle_info={}

       # populate some example cycle info
       cycle_info['cycle']=1
       cycle_info['time']=1.0

       print(cycle_info)

  * cycle_data (or tally_cycle_data) - A Python dictionary with sub-dictionaries the define unique cycle data.

    * This data type is used to build up the corresponding OPPPY output_data
      or tally_data types for plotting. For example here is an example of what
      cycle_data and tally_cycle_data should look like for a simple::

        import numpy

        cycle_data={}

        # populate cycle data
        cycle_info_dict={}
        cycle_info_dict['cycle'] = 1 
        cycle_info_dict['time'] = 1.0
        # there must be a 'cycle_info' dictionary used to order the cycle data 
        cycle_data['cycle_info'] = cycle_info_dcit
        time_step_dict = {}
        time_step_dict['dt'] = 0.1
        cycle_data['time_step']=time_step_dict
        n_cells_dict = {}
        n_cells_dict['ncells'] = 10
        cycle_data['cell_count']=n_cells_dict

        print(cycle_data)

        # we additionaly use tally cycle_data that is in the same formate only
        # contains arrays of data
        tally_cycle_data = {}

        # there must be a 'cycle_info' dictionary used to order the cycle data 
        cycle_info_dict = {}
        cycle_info_dict['cycle'] = 1 
        cycle_info_dict['time'] = 1.0
        tally_cycle_data['cycle_info'] = cycle_info_dict
        # load up a data dictionary
        counts_dict_1 = {}
        counts_dict_1['odd_counts'] = numpy.array([1, 3, 5, 7, 9])
        counts_dict_1['even_counts'] = numpy.array([2, 4, 6, 8, 10])
        counts_dict_1['bins'] = numpy.array([1, 2, 3, 4, 5])
        tally_cycle_data['cool_counts'] = counts_dict_1
        # there must be a 'problem_data' dictionary with cycle_info_keys and
        # subkeys associated with the cycle dictionaries
        problem_data_dict = {}
        problem_data_dict['cycle_info_keys'] = ['cycle','time']
        problem_data_dict['cool_counts'] = ['odd_counts','even_counts','bins']
        tally_cycle_data['problem_data'] = problem_data_dict
        # load up some more tally_cycle_data
        tally_cycle_data['n_odd_counts'] = sum(counts_dict_1['odd_counts'])
        tally_cycle_data['n_even_counts'] = sum(counts_dict_1['even_counts'])

        print(tally_cycle_data)

  * output_data - Time/cycle dependent scalar information (i.e. dt, total_energy, etc..)

    * This data is parsed into a Python dictionary of sub-dictionaries of
      interest. Each sub-dictionary contains a set of unique (1d) x (i.e. time or
      cycle) and y (i.e. dt or ncells) dictionaries to be used for plotting.
      The OPPPY library generally constructs this data using a series of
      'cycle_data' python dictionaries. However, for this simple example we
      will build it directly to show what the expected data structure looks
      like.  For example an output that only prints the time step size and
      number of cells every cycle could have a dictionary that looks like
      this::

        import numpy

        cycles=numpy.array([1, 2, 3, 4, 5])
        times=numpy.array([1.0, 2.0, 3.0, 4.0, 5.0])
        dt=numpy.array([0.1, 0.2, 0.3, 0.4, 0.5])
        ncells=numpy.array([10, 20, 30, 40, 50])

        # populate the time step dictionary
        time_step_subdictionary={}
        time_step_subdictionary['time']=times
        time_step_subdictionary['cycles']=cycles
        time_step_subdictionary['dt']=dt

        # populate the cell count dictionary
        cell_count_subdictionary={}
        cell_count_subdictionary['time']=times
        cell_count_subdictionary['cycles']=cycles
        cell_count_subdictionary['ncells']=ncells
        
        # populate the output dictionary
        output_data={}
        output_data['time_step']=time_step_subdictionary
        output_data['cell_count']=time_step_subdictionary

        print(output_data)

  * tally_data - Time/cycle dependent (n-dimensional) data
    
    * This data stores a dictionary of series_data that is directly associated
      with a dictionary of a list of tally_cycle_data. There are functions to
      build up a tally_data object using tally_cycle_data in opppy.tally. Here
      we will just build up a repsenative example of a tally_data object that
      can be used for plotting::

        import numpy

        # initialize the tally data dictionary
        tally_data = {}

        # there must be a 'problem_data' dictionary with cycle_info_keys and
        # subkeys associated with the cycle dictionaries 
        problem_data_dict = {}
        problem_data_dict['cycle_info_keys'] = ['cycle','time']
        problem_data_dict['cool_counts'] = ['odd_counts','even_counts','bins']
        tally_data['problem_data']=problem_data_dict

        # Here is what valid series data looks like
        tally_data['cycle'] = [1, 2] 
        tally_data['time'] = [1.0, 2.0]

        # lets build up an example tally_cycle_data list associated with the
        # series data
        tally_cycle_data_list = []

        
        # load up cycle 1 counts
        # build an example count dictionary
        counts_dict_1 = {}
        counts_dict_1['odd_counts'] = numpy.array([1, 3, 5, 7, 9])
        counts_dict_1['even_counts'] = numpy.array([2, 4, 6, 8, 10])
        counts_dict_1['bins'] = numpy.array([1, 2, 3, 4, 5])

        tally_cycle_data_1 = {}
        tally_cycle_data_1['n_odd_counts'] = sum(counts_dict_1['odd_counts'])
        tally_cycle_data_1['n_even_counts'] = sum(counts_dict_1['even_counts'])
        tally_cycle_data_1['cool_counts'] = counts_dict_1
        # append to the tally_cycle_data_list
        tally_cycle_data_list.append(tally_cycle_data_1)

        # load up cycle 2 counts
        # build an example count dictionary
        counts_dict_2 = {}
        counts_dict_2['odd_counts'] = numpy.array([11, 13, 15, 17, 19])
        counts_dict_2['even_counts'] = numpy.array([12, 14, 16, 18, 20])
        counts_dict_2['bins'] = numpy.array([1, 2, 3, 4, 5])

        tally_cycle_data_2 = {}
        tally_cycle_data_2['n_odd_counts'] = sum(counts_dict_2['odd_counts'])
        tally_cycle_data_2['n_even_counts'] = sum(counts_dict_2['even_counts'])
        tally_cycle_data_2['cool_counts'] = counts_dict_2
        # append to the tally_cycle_data_list
        tally_cycle_data_list.append(tally_cycle_data_2)

        # there must be a tally_cycle_data dictionary in every tally_data dictionary
        tally_data['tally_cycle_data'] = tally_cycle_data_list

        print(tally_data)

  * dump_data - Complete checkpoint (n-dimensional) data typically used for code restarts

    * This data is parsed into a python dictionary of sub-dictionaries
      associated with a single dump file. The sub-dictionaries are associated
      with a single dump file and contain unique arrays of values that can be
      plotted in multiple dimensions. Lets consider a two dimensional series of
      dumps::

        import numpy

        dumps = {}
        
        # build the first dump dictionary
        dump_1_dict = {}
        dump_1_dict['cycle'] = 1.0
        dump_1_dict['time'] = 1.0
        dump_1_dict['x'] = numpy.array([1, 2, 3, 1, 2, 3])
        dump_1_dict['y'] = numpy.array([1, 1, 1, 2, 2, 2])
        dump_1_dict['pressure'] = numpy.array([2, 4, 6, 8, 10, 12])
        dump_1_dict['temperature'] = numpy.array([1, 2, 3, 4, 5, 6])
        dumps['dump_1']=dump_1_dict

        # build the second dump dictionary
        dump_2_dict = {}
        dump_2_dict['cycle'] = 2.0
        dump_2_dict['time'] = 2.0
        dump_2_dict['x'] = numpy.array([1, 2, 3, 1, 2, 3])
        dump_2_dict['y'] = numpy.array([1, 1, 1, 2, 2, 2])
        dump_2_dict['pressure'] = numpy.array([3, 5, 7, 9, 11, 13])
        dump_2_dict['temperature'] = numpy.array([2, 3, 4, 5, 6, 7])
        dumps['dump_2']=dump_2_dict

        print(dumps)

These Python data structures can then be plotted using OPPPY plotting tools. 

*****************************
User defined OPPPY parsers
*****************************

The OPPPY library provides a set of functions to make building these Python
data (output_data, tally_data, dump_data) structures easier. To make this tool
flexible enough to accommodate any unique output type it requires users to
define unique opppy_parsers for their projects. There are two types of
opppy_parsers (cycle_string_parsers and dump_parsers).

cycle_string_parser - 
============================================

This user defined python parser class requires 5 main python attributes:
  * A python string called 'sort_key_string' to sort the data based on the
    dictionary values in the 'cycle_info' sub-dictionary available in every
    'cycle_data' dictionary.
  * A python string called 'cycle_opening_string' to indicate how a cycle string begins
  * A python string called 'cycle_ending_string' to indicate how a cycle string ends
  * A python string called 'file_end_string' to indicate the successful end of a file

    * This can be defaulted to file_end_string=None which assumes all
      valid cycles end with a 'cycle_end_string'

  * An associated python function called 'parse_cycle_string' that takes a
    full cycle string and generates a 'cycle_data' dictionary (defined in the
    Important Data Formats section).  
    
    * This function takes a python 'cycle_string' as input. 
    * this function returns either a 'cycle_data' python dictionary

      * The cycle_data must contain a 'cycle_info' sub-dictionary with a data value
        corresponding to the 'sort_key_string' defined by the user.

cycle_tally_parser - 
============================================

This user defined python parser class requires 5 main python attributes:
  * A python string called 'sort_key_string' to sort the data based on the
    dictionary values in the 'cycle_info' sub-dictionary available in every
    'tally_cycle_data' dictionary.
  * A python string called 'cycle_opening_string' to indicate how a cycle string begins
  * A python string called 'cycle_ending_string' to indicate how a cycle string ends
  * A python string called 'file_end_string' to indicate the successful end of a file

    * This can be defaulted to file_end_string=None which assumes all
      valid cycles end with a 'cycle_end_string'

  * An associated python function called 'parse_cycle_string' that takes a
    full cycle string and generates a 'cycle_tally_data' dictionary (defined in
    the Important Data Formats section).  
    
    * This function takes a python 'cycle_string' as input. 
    * this function returns either a 'tally_cycle_data' python dictionary

      * This tally_cycle_data contains an arbitrary number of tally data dictionaries.
      * The tally_cycle_data must contain a 'cycle_info' sub-dictionary with a data value
        corresponding to the 'sort_key_string' defined by the user.
      * The tally_cycle_data must contain a 'problem_data' dictionary that
        contains a 'cycle_info_keys' dictionary entry with a list of valid
        'sort_key_strings'. 'problem_data' also must contain a dictionary entry
        for every corresponding tally data dictionary. This 'problem_data'
        dictionary entry must contain a list of sub associated with the
        corresponding tally data dictionary.

dump_parser - 
============================================

This user defined python parser class requires 1 main python
attributes:
  * An associated python function called 'build_data_dictionary' that builds a
    'dump_data' dictionary from a user provided filename.

    * This function takes a string 'filename' used to open the dump file to be parsed
    * This function takes an optional list of 'dump_keys' string used to
      extract a subset of user defined data from the dump file
    * This function returns a 'dump_data' dictionary for plotting.


***************************************
Building OPPPY Python Data Dictionaries
***************************************

Example: Building an output_data dictionary
============================================

In this example we will build up an example output_data dictionary using an
example user defined opppy_parser.

For demonstrative purposes we define a set of simple output text files.

output_example1.txt:

.. include:: ../tests/output_example1.txt
   :literal:

output_example2.txt:

.. include:: ../tests/output_example2.txt
   :literal:

output_example3.txt:

.. include:: ../tests/output_example3.txt
   :literal:

Given this simple output formate we can define the following example ('cycle_string_parser') OPPPY
output parser my_test_opppy_parser.py

.. include:: ../tests/my_test_opppy_parser.py
   :literal:

We can now build output_data dictionary using the opppy.output functions and plot the results using opppy.plot_dictionary functions:

.. include:: ../tests/test_dict_plotting.py
   :literal:



Example: Building a dump_data dictionary
========================================

For demonstrative purposes we define a simple set of dump files in text format:

example_dump.txt

.. include:: ../tests/example_dump.txt
   :literal:

example_dump2.txt

.. include:: ../tests/example_dump2.txt
   :literal:

example_dump3.txt

.. include:: ../tests/example_dump3.txt
   :literal:

Given this simple dump formate we can define the following example
('dump_parser') OPPPY dump parser my_test_opppy_dump_parser.py

.. include:: ../tests/my_test_opppy_dump_parser.py
   :literal:

We can now build up data_dump dictionary using the opppy.dump_utils functions and plot the data using the opppy.plot_dump_dictionary:

.. include:: ../tests/test_dump_ploter.py
   :literal:

Example: Building a tally_data dictionary
========================================

For demonstrative purposes we define a simple set of tally files in text format:

example_tally1.txt

.. include:: ../tests/example_tally1.txt
   :literal:

example_tally2.txt

.. include:: ../tests/example_tally2.txt
   :literal:

example_tally3.txt

.. include:: ../tests/example_tally3.txt
   :literal:

Given this simple dump formate we can define the following example
('tally_parser') OPPPY tally parser my_test_opppy_tally_parser.py

.. include:: ../tests/my_test_opppy_tally_parser.py
   :literal:

We can now build up data_dump dictionary using the opppy.dump_utils functions and plot the data using the opppy.plot_dump_dictionary:

.. include:: ../tests/test_tally_plotting.py
   :literal:

************************************************
Building an Interactive Commandline OPPPY Ploter
************************************************

OPPPY provides some useful interactive plotting functions (see
opppy.interactive_utils) to build a user defined command line based plotting
tool with pre-formatted plots.  To demonstrate this capability we will build an
example command line plotter using the example user defined OPPPY parsers
above.

.. include:: ../tests/my_interactive_parser.py
   :literal:

Using the example files above this example interactive parsing tool can be used:
* build up python Pickle data files for rapid repeated plotting or alternative
  python scripting 
* directly plot data either from a pickle file or directly parsing data files
* interactive plotting based on a pre-defined plotting command  

The following simple 'input_scripts' are used for the interactive examples shown below:

interactive_input.txt

.. include:: ../tests/interactive_input.txt
   :literal:


interactive_tally_input.txt

.. include:: ../tests/interactive_tally_input.txt
   :literal:

Example of using the interactive user defined command line parser:

.. include:: ../tests/test_interactive.py
   :literal:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
