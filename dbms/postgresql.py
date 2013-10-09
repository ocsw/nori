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

    # module object containing connect(), etc.
    MODULE = psycopg2

    # local and remote ports for tunnels (remote is also for direct
    # connections)
    DEFAULT_LOCAL_PORT = 6432
    DEFAULT_REMOTE_PORT = 5432

    # where to look for the socket file, to set the default
    # this is a list of directories (without trailing /)
    SOCKET_SEARCH_PATH = ['/tmp', '/var/run/postgresql', '/var/run']


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
            class vars: DBMS_NAME, DEFAULT_REMOTE_PORT
            instance vars: prefix, delim
            methods: settings_extra_text(),
                     apply_config_defaults_extra()
            config settings: [prefix+delim+:] use_ssh_tunnel, protocol,
                             host, port, socket_file, connect_db
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
    sslmode
    sslcompression
    sslcert
    sslkey
    sslrootcert
    sslcrl
See the {0} documentation for more information.
'''.format(self.DBMS_NAME, pd)
        )

        #
        # PostgreSQL combines tcp and socket into host
        #

        del(core.config_settings[pd + 'protocol'])

        core.config_settings[pd + 'host']['descr'] = (
'''
Hostname or socket directory for the {0} connection.

If this doesn't start with '/', it will be treated as a remote hostname
to connect to via TCP.

If it does start with '/', it will be treated as the directory containing
the Unix socket file.  The file used will be 'HOST/.s.PGSQL.PORT', where
HOST and PORT are the given settings.

Note: there is apparently no way, with {0}, to specify a
relative directory or the full name of the socket file, or to use
anything other than a port number as the suffix.

Ignored if {1}use_ssh_tunnel is True.
'''.format(self.DBMS_NAME, pd)
        )
        # default is set in apply_config_defaults_extra()

        core.config_settings[pd + 'port']['descr'] = (
'''
Port number for the {0} connection.

Used for both TCP and socket connections; see {0}_host.

Ignored if {1}use_ssh_tunnel is True.
'''.format(self.DBMS_NAME, pd)
        )
        core.config_settings[pd + 'port']['default'] = (
            self.DEFAULT_REMOTE_PORT
        )

        del(core.config_settings[pd + 'socket_file'])

        # PostgreSQL requires a connection DB
        core.config_settings[pd + 'connect_db']['descr'] = (
'''
Initial database for the {0} connection.

{0} requires a database to connect to even for commands that
don't use any (such as getting the list of databases).
'''.format(self.DBMS_NAME)
        )
        core.config_settings[pd + 'connect_db']['default'] = 'postgres'

        # fix up descriptions we replaced
        if extra_text:
            setting_list = ['use_ssh_tunnel', 'host', 'port', 'connect_db']
            self.settings_extra_text(setting_list, extra_text)

        core.apply_config_defaults_hooks.append(
            self.apply_config_defaults_extra
        )


    def apply_config_defaults_extra(self):

        """
        Apply configuration defaults that are last-minute/complicated.

        Dependencies:
            class vars: SOCKET_SEARCH_PATH
            instance vars: prefix, delim
            config settings: [prefix+delim+:] host, port, remote_port
            modules: core

        """

        pd = self.prefix + self.delim

        # pd + 'host': first try to find a socket, then fall back to TCP
        for d in self.SOCKET_SEARCH_PATH:
            f = d + '/.s.PGSQL.' + str(core.cfg[pd + 'port'])
            if (core.check_file_type(f, 'PostgreSQL socket', type_char='s',
                                follow_links=True, must_exist=True,
                                use_logger=None, warn_only=True) and
                  core.check_file_access(f, 'PostgreSQL socket',
                                         file_rwx='rw', use_logger=None,
                                         warn_only=True)):
                core.config_settings[pd + 'host']['default'] = f
                break
        if pd + 'host' not in core.config_settings:
            core.config_settings[pd + 'host']['default'] = '127.0.0.1'

        # pd + 'port', pd + 'remote_port': clarify default
        for s_name in [pd + 'port', pd + 'remote_port']:
            if (s_name in core.config_settings and
                  core.config_settings[s_name]['default'] == 5432):
                core.config_settings[s_name]['default_descr'] = (
                    '5432 (the standard port)'
                )


    def validate_config(self):
        """
        Validate DBMS config settings.
        Only does checks that aren't done in DBMS.validate_config().
        Dependencies:
            instance vars: ignore, prefix, delim, tunnel_config
            config settings: [prefix+delim+:] use_ssh_tunnel, host, port,
                             connect_db
            modules: core, dbms.DBMS
            Python: 2.0/3.2, for callable()
        """
        if callable(self.ignore) and self.ignore():
            return
        pd = self.prefix + self.delim
        if not self.tunnel_config or not core.cfg[pd + 'use_ssh_tunnel']:
            core.setting_check_not_blank(pd + 'host')
            if core.cfg[pd + 'host'][0] == '/':
                core.setting_check_dir_search(pd + 'host')
            core.setting_check_is_set(pd + 'port')
        core.setting_check_is_set(pd + 'connect_db')
        DBMS.validate_config(self)
