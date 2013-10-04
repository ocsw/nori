#!/usr/bin/env python


"""
This is the MySQL submodule for the nori library; see __main__.py
for license and usage information.


DOCSTRING CONTENTS:
-------------------

1) About and Requirements
2) API Classes


1) ABOUT AND REQUIREMENTS:
--------------------------


2) API CLASSES:
---------------

"""


########################################################################
#                               IMPORTS
########################################################################

#########
# system
#########

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from pprint import pprint as pp  # for debugging

import sys


#########
# add-on
#########

try:
    import mysql.connector
except ImportError:
    pass  # see the status and meta variables section


###############
# this package
###############

from .. import core
from . import dbms


########################################################################
#                              VARIABLES
########################################################################

##################
# status and meta
##################

# supported / available features
core.supported_features['dbms.mysql'] = 'MySQL support'
if 'mysql.connector' in sys.modules:
    core.available_features.append('dbms.mysql')


########################################################################
#                               CLASSES
########################################################################

class MySQL(dbms.DBMS):

    """This class adapts the DBMS functionality to MySQL."""

    ##################
    # class variables
    ##################

    # what to call the DBMS
    DBMS_NAME = 'MySQL'

    # required feature(s) for config settings, etc.
    REQUIRES = super(MySQL).REQUIRES + ['dbms.mysql']


    #####################################
    # startup and config file processing
    #####################################




#warnings
#errors, incl. strings
#pooling
#dicts
#conversion, incl. unicode
#buffering?
#autocommit
#
#which package
#
#connect
#error handling
#close, incl. auto
#exec, incl. cursor open, commit/rollback
#fetch, incl. cursor close