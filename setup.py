#!/usr/bin/env python
# ============================================================================
# \file   setup.py
# \author M.A. Cleveland
# \date   Feb 2018
# \note   Copyright (C) 2018 Los Alamos National Security, LLC.
#         All Rights Reserved.
# ============================================================================
#
# OPTIONS:
#    build    Provide python library and scripts in the build directory
#    install  Provide python library and scripts as part of a release.
#    --build-lib=<dir> provide libraries and python files at <dir>
#    --home=<dir>      install libraries and python files at <dir>
#
# TYPICAL USE:
#
# python setup.py build --build-lib="${CMAKE_CURRENT_BINARY_DIR}/build/lib/"
# python setup.py install --home="${CMAKE_INSTALL_PREFIX}"
#
##---------------------------------------------------------------------------##

from opppy.version import __version__
try:
    from setuptools import setup
except ImportError:
    try:
        from setuptools.core import setup
    except ImportError:
        from distutils.core import setup

setup(name='opppy',
      version=__version__,
      description='Output Parse-Pickle-Plot Python (OPPPY) library',
      author='Mathew Cleveland',
      author_email='cleveland@lanl.gov',
      url='https://gitlab.lanl.gov/chaos/opppy',
      packages=['opppy'])

##---------------------------------------------------------------------------##
# End of file
##---------------------------------------------------------------------------##
