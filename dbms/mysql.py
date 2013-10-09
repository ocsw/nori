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
from .dbms import DBMS


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

class MySQL(DBMS):

    """This class adapts the DBMS functionality to MySQL."""

    #############################
    # class variables: constants
    #############################

    # what to call the DBMS
    DBMS_NAME = 'MySQL'

    # required feature(s) for config settings, etc.
    REQUIRES = DBMS.REQUIRES + ['dbms.mysql']

    # module object containing connect(), etc.
    MODULE = mysql.connector

    # local and remote ports for tunnels (remote is also for direct
    # connections)
    DEFAULT_LOCAL_PORT = 4306
    DEFAULT_REMOTE_PORT = 3306

    # where to look for the socket file, to set the default
    # this is a list of file paths, not directories
    SOCKET_SEARCH_PATH = [
        '/var/run/mysqld/mysqld.sock',
        '/tmp/mysql.sock',
    ]


    #####################################
    # startup and config file processing
    #####################################

    def create_settings(self, heading='', extra_text='', ignore=None,
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
            methods: settings_extra_text(),
                     apply_config_defaults_extra()
            config settings: [prefix+delim+:] use_ssh_tunnel, port,
                             socket_file
            modules: core, dbms.DBMS

        """

        # first do the generic stuff
        DBMS.create_settings(self, heading, extra_text, ignore,
                             extra_requires, tunnel)

        pd = self.prefix + self.delim

        # add notes about SSL
        core.config_settings[pd + 'use_ssh_tunnel']['descr'] = (
'''
Use an SSH tunnel for the {0} connection (True/False)?

If True, specify the host in {0}_ssh_host and the port in
{0}_remote_port instead of {0}_host and
{0}_port.

Note: to use {0}'s SSL support, you will need to add the
necessary options to {1}connect_options:
    ssl_ca
    ssl_cert
    ssl_key
    ssl_verify_cert
See the {0} documentation for more information.
'''.format(self.DBMS_NAME, pd)
        )

        #
        # fix some defaults
        #

        core.config_settings[pd + 'host']['default'] = (
            '127.0.0.1'  # mysql.connector default
        )

        core.config_settings[pd + 'port']['default'] = (
            self.DEFAULT_REMOTE_PORT
        )
        for f in self.SOCKET_SEARCH_PATH:
            if (core.check_file_type(f, 'MySQL socket', type_char='s',
                                follow_links=True, must_exist=True,
                                use_logger=None, warn_only=True) and
                  core.check_file_access(f, 'MySQL socket', file_rwx='rw',
                                    use_logger=None, warn_only=True)):
                core.config_settings[pd + 'socket_file']['default'] = f
                break

        # fix up descriptions we replaced
        if extra_text:
            setting_list = ['use_ssh_tunnel']
            self.settings_extra_text(setting_list, extra_text)

        core.apply_config_defaults_hooks.append(
            self.apply_config_defaults_extra
        )


    def apply_config_defaults_extra(self):

        """
        Apply configuration defaults that are last-minute/complicated.

        Dependencies:
            instance vars: prefix, delim
            config settings: [prefix+delim+:] port, remote_port
            modules: core

        """

        pd = self.prefix + self.delim

        # pd + 'port', pd + 'remote_port': clarify default
        for s_name in [pd + 'port', pd + 'remote_port']:
            if (s_name in core.config_settings and
                  core.config_settings[s_name]['default'] == 3306):
                core.config_settings[s_name]['default_descr'] = (
                    '3306 (the standard port)'
                )


    def validate_config(self):
        """
        Validate DBMS config settings.
        Only does checks that aren't done in DBMS.validate_config().
        Dependencies:
            instance vars: ignore, prefix, delim, tunnel_config
            config settings: [prefix+delim+:] use_ssh_tunnel, protocol,
                             host, port, socket_file
            modules: core, dbms.DBMS
        """
        if callable(self.ignore) and self.ignore():
            return
        pd = self.prefix + self.delim
        if not self.tunnel_config or not core.cfg[pd + 'use_ssh_tunnel']:
            core.setting_check_list(pd + 'protocol', ['tcp', 'socket'])
            if core.cfg[pd + 'protocol'] == 'tcp':
                core.setting_check_is_set(pd + 'host')
                core.setting_check_is_set(pd + 'port')
            elif core.cfg[pd + 'protocol'] == 'socket':
                core.setting_check_is_set(pd + 'socket_file')
        DBMS.validate_config(self)
