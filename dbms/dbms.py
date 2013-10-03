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
#if 'paramiko' in sys.modules:
#    core.available_features.append('submodule')


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
#                               CLASSES
########################################################################
########################################################################
#                        FUNCTIONS AND CLASSES
########################################################################

class DBMS(object):

    """This class wraps all of the DBMS functionality."""

    ##################
    # class variables
    ##################

    # what to call the DBMS; subclasses must be define this
    # (e.g.: 'MySQL')
    DBMS_NAME = ''

    # required feature(s) for config settings, etc.
    # subclasses should add to this
    REQUIRES = ['dbms']


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
            class vars: DBMS_NAME, REQUIRES
            instance vars: prefix, delim, tunnel_config
            config settings: [prefix+delim+:] (heading), use_ssh_tunnel,
                             user, password, pw_file, host, port,
                             socket_file, connect_db, connect_options
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
                ssh_extra_text += '\n' + extra_text
            ssh.create_ssh_settings(
                self.prefix, self.delim, extra_text=ssh_extra_text,
                extra_requires=self.REQUIRES + extra_requires,
                tunnel=True
            )
            # we don't set default_local_port or default_remote_port
            # here; subclasses must change the defaults in
            # core.config_settings

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

See also {1}, below.
'''.format(self.DBMS_NAME, pd + 'pw_file')
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

Ignored if {1} is set.
'''.format(self.DBMS_NAME, pd + 'password')
            ),
            # no default
            cl_coercer=str,
        )

        core.config_settings[pd + 'host'] = dict(
            descr=(
'''
Remote hostname for the {0} connection.
'''.format(self.DBMS_NAME)
            ),
            default='localhost',
            cl_coercer=str,
        )

        core.config_settings[pd + 'port'] = dict(
            descr=(
'''
Remote port number for the {0} connection.
'''.format(self.DBMS_NAME)
            ),
            # no default here; it should be set by subclasses
            cl_coercer=int,
        )

        core.config_settings[pd + 'socket_file'] = dict(
            descr=(
'''
Path to the socket file for the {0} connection.

Ignored if {1} or {2} are set.
'''.format(self.DBMS_NAME, pd + 'host', pd + 'port')
            ),
            # no default here; it should be set by subclasses
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
            'user', 'password', 'pw_file', 'host', 'port',
            'socket_file', 'connect_db', 'connect_options',
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


    def validate_config():
        """
        Validate DBMS config settings.
        Only does checks that are likely to be relevant for all DBMSes;
        it's easy to be more restrictive in subclasses, but hard to be
        more lenient.
        Dependencies:
            instance vars: prefix, delim, tunnel_config
            config settings: [prefix+delim+:] use_ssh_tunnel,
                             user, password, pw_file, host, port,
                             socket_file, connect_db, connect_options
            modules: core
        """
        pd = self.prefix + self.delim
        if self.tunnel_config:
            core.setting_check_type(pd + 'use_ssh_tunnel', (bool, ))
        if pd + 'user' in core.cfg:
            core.setting_check_not_blank(pd + 'user')
        if pd + 'password' in core.cfg:
            core.setting_check_not_blank(pd + 'password')
        if pd + 'pw_file' in core.cfg:
            core.setting_check_not_blank(pd + 'pw_file')
        if pd + 'host' in core.cfg:
            core.setting_check_not_blank(pd + 'host')
        if pd + 'port' in core.cfg:
            core.setting_check_num(pd + 'port', 1, 65535)
        if pd + 'socket_file' in core.cfg:
            core.setting_check_not_blank(pd + 'socket_file')
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

#connect, incl. ssh
#error handling
#close, incl. auto
#exec, incl. cursor open, commit/rollback
#fetch, incl. cursor close
#
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
#features
#
#pw_file default?
#connect db optional
#h/p vs socket
#
#mysql ssl
#
#        If you're calling this function, you will almost certainly want to
#        do these as well:
#            core.config_settings_no_print_output_log(False)
#            core.config_settings['exec_path']['no_print'] = False
#            core.config_settings['print_cmds']['no_print'] = False
#
####mysql_localhost=  # defaults to "127.0.0.1"
####mysql_localport=  # defaults to "4306"
####mysql_remoteport=  # defaults to "3306" (the usual port)
#postgres socket, ssl, etc.
#port, socket defaults
