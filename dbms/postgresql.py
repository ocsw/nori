#!/usr/bin/env python


"""
This is the PostgreSQL submodule for the nori library; see __main__.py
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
    import psycopg2
except ImportError:
    pass  # see the status and meta variables section

#import psycopg2.extensions
#psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
#psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
#DEC2FLOAT = psycopg2.extensions.new_type(
#    psycopg2.extensions.DECIMAL.values,
#    'DEC2FLOAT',
#    lambda value, curs: float(value) if value is not None else None)
#psycopg2.extensions.register_type(DEC2FLOAT)


###############
# this package
###############

from .. import core
from .dbms import DBMS


########################################################################
#                              VARIABLES
########################################################################

##################
# status and meta
##################

# supported / available features
core.supported_features['dbms.postgresql'] = 'PostgreSQL support'
if 'psycopg2' in sys.modules:
    core.available_features.append('dbms.postgresql')


########################################################################
#                               CLASSES
########################################################################

class PostgreSQL(DBMS):

    """This class adapts the DBMS functionality to PostgreSQL."""

    #############################
    # class variables: constants
    #############################

    # what to call the DBMS
    DBMS_NAME = 'PostgreSQL'

    # required feature(s) for config settings, etc.
    REQUIRES = DBMS.REQUIRES + ['dbms.postgresql']

    # local and remote ports for tunnels (remote is also for direct
    # connections)
    DEFAULT_LOCAL_PORT = 6432
    DEFAULT_REMOTE_PORT = 5432

    # where to look for the socket file, to set the default
    SOCKET_SEARCH_PATH = [
        '/var/run/mysqld/mysqld.sock',
        '/tmp/mysql.sock',
    ]


    #####################################
    # startup and config file processing
    #####################################

    def create_settings(self, heading='', extra_text='',
                        extra_requires=[],
                        tunnel=True if 'ssh' in core.available_features
                                    else False):

        """
        Add a block of DBMS config settings to the script.

        Parameters:
            see DBMS.create_settings()

        Dependencies:
            class vars: DEFAULT_REMOTE_PORT, SOCKET_SEARCH_PATH
            instance vars: prefix, delim
            config settings: [prefix+delim+:] port, socket_file
            modules: core, dbms.DBMS

        """

        # first do the generic stuff
        DBMS.create_settings(self, heading, extra_text, extra_requires,
                             tunnel)

        pd = self.prefix + self.delim

        # fix some defaults
        core.config_settings[pd + 'port']['default'] = (
            MySQL.DEFAULT_REMOTE_PORT
        )
        for f in MySQL.SOCKET_SEARCH_PATH:
            if (core.check_file_type(f, 'MySQL socket', type_char='s',
                                follow_links=True, must_exist=True,
                                use_logger=None, warn_only=True) and
                  core.check_file_access(f, 'MySQL socket', file_rwx='rw',
                                    use_logger=None, warn_only=True)):
                core.config_settings[pd + 'socket_file']['default'] = f
                break

        if tunnel:
            # make output log settings visible
            core.config_settings_no_print_output_log(False)
            core.config_settings['exec_path']['no_print'] = False
            core.config_settings['print_cmds']['no_print'] = False


    def validate_config(self):
        """
        Validate DBMS config settings.
        Only does checks that aren't done in DBMS.validate_config().
        Dependencies:
            instance vars: prefix, delim, tunnel_config
            config settings: [prefix+delim+:] use_ssh_tunnel, protocol,
                             host, port, socket_file
            modules: core, dbms.DBMS
        """
        pd = self.prefix + self.delim
        if not self.tunnel_config or not core.cfg[pd + 'use_ssh_tunnel']:
            core.setting_check_list(pd + 'protocol', ['tcp', 'socket'])
            if core.cfg[pd + 'protocol'] == 'tcp':
                core.setting_check_is_set(pd + 'host')
                core.setting_check_is_set(pd + 'port')
            elif core.cfg[pd + 'protocol'] == 'socket':
                core.setting_check_is_set(pd + 'socket_file')
        DBMS.validate_config(self)
