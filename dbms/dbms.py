#!/usr/bin/env python


"""
This is the DBMS submodule for the nori library; see __main__.py
for license and usage information.


DOCSTRING CONTENTS:
-------------------

1) About and Requirements
2) API Classes
3) Usage in Scripts
4) Modification Notes


1) ABOUT AND REQUIREMENTS:
--------------------------


2) API CLASSES:
---------------


3) USAGE IN SCRIPTS:
--------------------


4) MODIFICATION NOTES:
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

import getpass


###############
# this package
###############

from .. import core
from .. import ssh


########################################################################
#                              VARIABLES
########################################################################

##################
# status and meta
##################

#
# exit values
#

core.exitvals['dbms_connect'] = dict(
    num=30,
    descr=(
'''
error connecting to database
'''
    ),
)

core.exitvals['dbms_execute'] = dict(
    num=31,
    descr=(
'''
error executing a database query/command
'''
    ),
)

# supported / available features
core.supported_features['dbms'] = (
    'generic database support; subfeatures for each DBMS also required'
)
core.available_features.append('dbms')


########################################################################
#                               CLASSES
########################################################################

class DBMS(object):

    """
    This class wraps all of the DBMS functionality.

    DO NOT INSTANTIATE; USE SUBCLASSES ONLY.

    """

    #############################
    # class variables: constants
    #############################

    # what to call the DBMS; subclasses must be define this
    # (e.g.: 'MySQL')
    DBMS_NAME = ''

    # required feature(s) for config settings, etc.
    # subclasses should add to this
    REQUIRES = ['dbms']

    # local and remote ports for tunnels (remote is also for direct
    # connections); must be set by subclasses
    DEFAULT_LOCAL_PORT = None
    DEFAULT_REMOTE_PORT = None


    ###############
    # housekeeping
    ###############

    def __init__(self, prefix, delim='_'):
        """
        Populate instance variables.
        Parameters:
            prefix, delim: prefix and delimiter that start the setting
                           names to use
        """
        self.prefix = prefix
        self.delim = delim
        self.is_connected = False
        self.has_cursor = False


    #####################################
    # startup and config file processing
    #####################################

    def create_settings(self, heading='', extra_text='',
                        extra_requires=[],
                        tunnel=True if 'ssh' in core.available_features
                                    else False):

        """
        Add a block of DBMS config settings to the script.

        When modifying, remember to keep the setting_list at the bottom
        and validate_config() in sync with the config settings.

        Parameters:
            heading: if not blank, a heading entry with this value will
                     be added to the config settings
            extra_text: if not blank, this value is added to each
                        setting description (prepended with a blank
                        line; does not include the heading)
                        this is mainly intended to be used for things
                        like 'Ignored if [some setting] is False.'
            extra_requires: a list of features to be added to the
                            settings' requires attributes
            tunnel: if true, add SSH-tunnel settings

        Dependencies:
            class vars: DBMS_NAME, REQUIRES, DEFAULT_REMOTE_PORT,
                        DEFAULT_LOCAL_PORT
            instance vars: prefix, delim, tunnel_config
            config settings: [prefix+delim+:] (heading), use_ssh_tunnel,
                             protocol, host, port, socket_file, user,
                             password, pw_file, connect_db,
                             connect_options
            modules: getpass, core, ssh

        """

        pd = self.prefix + self.delim
        self.tunnel_config = tunnel

        if heading:
            core.config_settings[pd + 'heading'] = dict(
                heading=heading,
            )

        if tunnel:
            core.config_settings[pd + 'use_ssh_tunnel'] = dict(
                descr=(
'''
Use an SSH tunnel for the {0} connection (True/False)?
'''.format(self.DBMS_NAME)
                ),
                default=False,
                cl_coercer=core.str_to_bool,
                requires=['ssh'],  # see below for the rest
            )
            ssh_extra_text = ("Ignored if cfg['{0}'] is False." .
                              format(pd + 'use_ssh_tunnel'))
            if extra_text:
                ssh_extra_text += '\n\n' + extra_text
            ssh.create_ssh_settings(
                self.prefix, self.delim, extra_text=ssh_extra_text,
                extra_requires=self.REQUIRES + extra_requires,
                tunnel=True,
                default_local_port=self.__class__.DEFAULT_LOCAL_PORT,
                default_remote_port=self.__class__.DEFAULT_REMOTE_PORT)

        core.config_settings[pd + 'protocol'] = dict(
            descr=(
'''
Protocol to use for the {0} connection.

Can be:
    * 'tcp': use {1}host/port
    * 'socket': use {1}socket_file

Ignored if {1}use_ssh_tunnel is True.
'''.format(self.DBMS_NAME, pd)
            ),
            default='tcp',
            cl_coercer=str,
        )

        core.config_settings[pd + 'host'] = dict(
            descr=(
'''
Remote hostname for the {0} connection.

Ignored if {1}use_ssh_tunnel is True or if
{1}protocol is not 'tcp'.
'''.format(self.DBMS_NAME, pd)
            ),
            default='localhost',
            cl_coercer=str,
        )

        core.config_settings[pd + 'port'] = dict(
            descr=(
'''
Remote port number for the {0} connection.

Ignored if {1}use_ssh_tunnel is True or if
{1}protocol is not 'tcp'.
'''.format(self.DBMS_NAME, pd)
            ),
            # no default here; it should be set by subclasses
            cl_coercer=int,
        )

        core.config_settings[pd + 'socket_file'] = dict(
            descr=(
'''
Path to the socket file for the {0} connection.


Ignored if {1}use_ssh_tunnel is True or if
{1}protocol is not 'socket'.
'''.format(self.DBMS_NAME, pd)
            ),
            # no default here; it should be set by subclasses
            cl_coercer=str,
        )

        core.config_settings[pd + 'user'] = dict(
            descr=(
'''
Username for the {0} connection.
'''.format(self.DBMS_NAME)
            ),
            # see below for default
            cl_coercer=str,
        )
        try:
            core.config_settings[pd + 'user']['default'] = getpass.getuser()
            core.config_settings[pd + 'user']['default_descr'] = (
'''
the username the script is being run under
'''
            )
        except ImportError:
            core.config_settings[pd + 'user']['default_descr'] = (
'''
[none, because the current username could not be found]
'''
            )

        core.config_settings[pd + 'password'] = dict(
            descr=(
'''
Password for the {0} connection.

See also {1}pw_file, below.
'''.format(self.DBMS_NAME, pd)
            ),
            # no default
            cl_coercer=str,
        )

        core.config_settings[pd + 'pw_file'] = dict(
            descr=(
'''
Path to the password file for the {0} connection.

File must contain nothing but the password; leading/trailing whitespace will
be trimmed.

Ignored if {1}password is set.
'''.format(self.DBMS_NAME, pd)
            ),
            # no default
            cl_coercer=str,
        )

        core.config_settings[pd + 'connect_db'] = dict(
            descr=(
'''
Initial database for the {0} connection.
'''.format(self.DBMS_NAME)
            ),
            # no default here; it can be set by subclasses
            cl_coercer=str,
        )

        core.config_settings[pd + 'connect_options'] = dict(
            descr=(
'''
Additional options for the {0} connection.

Options must be supplied as a dict.
'''.format(self.DBMS_NAME)
            ),
            # no default here; it can be set by subclasses
        )

        setting_list = [
            'protocol', 'host', 'port', 'socket_file', 'user', 'password',
            'pw_file', 'connect_db', 'connect_options',
        ]
        if tunnel:
            setting_list += [
                'use_ssh_tunnel',
            ]
        if extra_text:
            for s_name in setting_list:
                if 'descr' in core.config_settings[pd + s_name]:
                    core.config_settings[pd + s_name]['descr'] += (
                        '\n' + extra_text
                    )
                else:
                    core.config_settings[pd + s_name]['descr'] = (
                        extra_text
                    )
        for s_name in setting_list:
            if 'requires' in core.config_settings[pd + s_name]:
                core.config_settings[pd + s_name]['requires'] += (
                    self.REQUIRES + extra_requires
                )
            else:
                core.config_settings[pd + s_name]['requires'] = (
                    self.REQUIRES + extra_requires
                )

        core.validate_config_hooks.append(self.validate_config)


    def validate_config(self):
        """
        Validate DBMS config settings.
        Only does checks that are likely to be relevant for all DBMSes;
        it's easy to be more restrictive in subclasses, but hard to be
        more lenient.
        Dependencies:
            instance vars: prefix, delim, tunnel_config
            config settings: [prefix+delim+:] use_ssh_tunnel, protocol,
                             host, port, socket_file, user, password,
                             pw_file, connect_db, connect_options
            modules: core
        """
        pd = self.prefix + self.delim
        if self.tunnel_config:
            core.setting_check_type(pd + 'use_ssh_tunnel', (bool, ))
        if not self.tunnel_config or not core.cfg[pd + 'use_ssh_tunnel']:
            if (pd + 'protocol' in core.cfg and
                  core.cfg[pd + 'protocol'] == 'tcp'):
                if pd + 'host' in core.cfg:
                    core.setting_check_not_blank(pd + 'host')
                if pd + 'port' in core.cfg:
                    core.setting_check_num(pd + 'port', 1, 65535)
            elif (pd + 'protocol' in core.cfg and
                  core.cfg[pd + 'protocol'] == 'socket'):
                if pd + 'socket_file' in core.cfg:
                    core.setting_check_not_blank(pd + 'socket_file')
        if pd + 'user' in core.cfg:
            core.setting_check_not_blank(pd + 'user')
        if pd + 'password' in core.cfg:
            core.setting_check_not_blank(pd + 'password')
        if pd + 'password' not in core.cfg and pd + 'pw_file' in core.cfg:
            core.setting_check_not_blank(pd + 'pw_file')
        if pd + 'connect_db' in core.cfg:
            core.setting_check_not_blank(pd + 'connect_db')
        if pd + 'connect_options' in core.cfg:
            core.setting_check_kwargs(pd + 'connect_options')


    #############################
    # logging and error handling
    #############################


    ###############################
    # DBMS connections and queries
    ###############################

    def connect(self):
        pass

### check socket, pw file types/access

#connect, incl. ssh
#error handling
#close, incl. auto
#exec, incl. cursor open, commit/rollback
#fetch, incl. cursor close
#
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
#pw_file default?
#connect db optional
#h/p vs socket
#
#mysql ssl
#mysql_remoteport=   (the usual port)
#
#postgres socket, ssl, etc.
