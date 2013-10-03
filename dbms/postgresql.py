#!/usr/bin/env python


"""
This is the DBMS submodule for the nori library; see __main__.py
for license and usage information.


DOCSTRING CONTENTS:
-------------------

1) About and Requirements
2) API Variables
3) API Functions
4) API Classes
5) Usage in Scripts
6) Modification Notes


1) ABOUT AND REQUIREMENTS:
--------------------------


2) API VARIABLES:
-----------------


3) API FUNCTIONS:
-----------------


4) API CLASSES:
---------------


5) USAGE IN SCRIPTS:
--------------------


6) MODIFICATION NOTES:
----------------------

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
    import paramiko
except ImportError:
    pass  # see the status and meta variables section

import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)

warnings
errors, incl. strings
pooling
dicts
conversion, incl. unicode
buffering?
autocommit

which package
features

connect
error handling
close, incl. auto
exec, incl. cursor open, commit/rollback
fetch, incl. cursor close

###############
# this package
###############

from .. import core


########################################################################
#                         PYTHON VERSION CHECK
########################################################################

# minimum versions for the imports and code below
pyversion_check(7, 2)


########################################################################
#                              VARIABLES
########################################################################

############
# constants
############


##################
# status and meta
##################

# submodule-specific exit values
core.exitvals['submodule'] = dict(
    num=999,
    descr=(
'''
error doing submodule stuff
'''
    ),
)

# submodule-specific features
core.supported_features['submodule'] = 'submodule stuff'
if 'paramiko' in sys.modules:
    core.available_features.append('submodule')


#########################
# configuration settings
#########################

#
# submodule-specific config settings
#

if 'submodule' in core.available_features:
    core.config_settings['submodule_heading'] = dict(
        heading='Submodule',
    )

    core.config_settings['submodule_setting'] = dict(
        descr=(
'''
Submodule stuff.
'''
        ),
        default='submodule stuff',
        requires=['submodule'],
    )


#############
# hook lists
#############


############
# resources
############


########################################################################
#                               FUNCTIONS
########################################################################

#####################################
# startup and config file processing
#####################################

def validate_config():
    """
    Validate submodule-specific config settings.
    """
    pass


####################
# [submodule stuff]
####################


