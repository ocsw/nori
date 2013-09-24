#!/usr/bin/env python


"""
This is the SSH submodule for the nori library; see __main__.py for
license and usage information.


DOCSTRING CONTENTS:
-------------------

1) About and Requirements
2) API Functions
3) Usage in Scripts


1) ABOUT AND REQUIREMENTS:
--------------------------

This submodule provides SSH functionality, including remote command
execution and tunnels.  It requires the 'ssh' command line utility,
which must be in the execution search path.

###TODO


2) API FUNCTIONS:
-----------------

    Startup and Config-file Processing:
    -----------------------------------

    create_ssh_settings
        Add a block of SSH config settings to the script.

    validate_ssh_config
        Validate all SSH config settings.


    SSH Remote Commands and Tunnels:
    --------------------------------

    get_ssh_cmd()
        Assemble a list containing the ssh command and its arguments.

    get_ssh_tunnel_cmd(prefix, delim='_'):
        Assemble a list containing the ssh tunnel command and its
        arguments.

    ###TODO


3) USAGE IN SCRIPTS:
--------------------

###TODO

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
import shlex

if sys.hexversion < 0x03000000:
    from types import *  # see constants, below


###############
# this package
###############

from . import core
from . import which


########################################################################
#                              VARIABLES
########################################################################

############
# constants
############

# not in the types module anymore, but more readable
if sys.hexversion >= 0x03000000:
    NoneType = type(None)


##################
# status and meta
##################

#
# exit values
#

core.exitvals['ssh_connect']=dict(
    num=20,
    descr=(
'''
error establishing SSH connection
'''
    ),
)

core.exitvals['ssh_tunnel']=dict(
    num=21,
    descr=(
'''
error establishing SSH tunnel
'''
    ),
)

# supported / available features
core.supported_features['ssh'] = 'SSH command and tunnel support'
if which.which('ssh'):
    core.available_features.append('ssh')


#########################
# configuration settings
#########################

# list of tuples: (prefix+delim, tunnel?)
# see config functions
_config_blocks = []


#############
# hook lists
#############

core.validate_config_hooks.append(lambda: validate_ssh_config())


########################################################################
#                               FUNCTIONS
########################################################################

#####################################
# startup and config file processing
#####################################

def create_ssh_settings(prefix, delim='_', heading='', extra_text='',
                        tunnel=False, default_local_port=None,
                        default_remote_port=None):

    """
    Add a block of SSH config settings to the script.

    If you're calling this function, you will almost certainly want to
    do these as well:
        core.config_settings_no_print_output_log(False)
        core.config_settings['exec_path']['no_print'] = False
        core.config_settings['print_cmds']['no_print'] = False

    When modifying, remember to keep the setting_list at the bottom and
    validate_config() in sync with the config settings.

    Parameters:
        prefix, delim: the setting names are prepended with prefix and
                       delim
        heading: if not blank, a heading entry with this value will be
                 added to the config settings
        extra_text: if not blank, this value is added to each setting
                    description (prepended with a blank line; does not
                    include the heading)
                    this is mainly intended to be used for things like
                    'Ignored if [some setting] is not True.'
        tunnel: if true, add tunnel-specific settings
        default_local_port: if tunnel is true, used as the default local
                            port number for the tunnel (and must be set)
        default_remote_port: if tunnel is true, used as the default
                             remote port number for the tunnel (and must
                             be set)

    Dependencies:
        config settings: [prefix+delim+:] (heading), ssh_host, ssh_port,
                         ssh_user, ssh_key_file, ssh_options,
                         local_host, local_port, remote_host,
                         remote_port, tun_timeout
        globals: _config_blocks
        modules: getpass, core

    """

    if heading:
        core.config_settings[prefix+delim+'heading'] = dict(
            heading=heading,
        )

    core.config_settings[prefix+delim+'ssh_host'] = dict(
        descr=(
'''
The hostname of the remote SSH host.
'''
        ),
        # no default
        cl_coercer=str,
        requires=['ssh'],
    )

    core.config_settings[prefix+delim+'ssh_port'] = dict(
        descr=(
'''
The SSH port on the remote host.
'''
        ),
        # no default
        default_descr=(
'''
the ssh utility's default (generally 22, the standard port)
'''
        ),
        cl_coercer=int,
        requires=['ssh'],
    )

    core.config_settings[prefix+delim+'ssh_user'] = dict(
        descr=(
'''
The username on the remote SSH host.
'''
        ),
        # no default
        default_descr=(
'''
the ssh utility's default (generally the username the script is run by)
'''
        ),
        cl_coercer=str,
        requires=['ssh'],
    )

    core.config_settings[prefix+delim+'ssh_key_file'] = dict(
        descr=(
'''
The path to the SSH key file.
'''
        ),
        # no default
        default_descr=(
'''
the ssh utility's default (generally ~/.ssh/id_*)
'''.format(prefix+delim)
        ),
        cl_coercer=str,
        requires=['ssh'],
    )

    core.config_settings[prefix+delim+'ssh_options'] = dict(
        descr=(
'''
The options to pass to the ssh utility.

This can be a string or a list of strings.  A string can be passed on the
command line, but this isn't recommended unless it is very simple, due to
quoting issues.
'''
        ),
        # no default
        cl_coercer=str,  # can also be a list, but not from the cli
        requires=['ssh'],
    )

    if tunnel:
        core.config_settings[prefix+delim+'local_host'] = dict(
            descr=(
'''
The hostname on the local end of the SSH tunnel.

This is generally 'localhost', but it may need to be (e.g.) '127.0.0.1'
or '::1'.
'''
            ),
            default='localhost',
            cl_coercer=str,
            requires=['ssh'],
        )

        core.config_settings[prefix+delim+'local_port'] = dict(
            descr=(
'''
The port number on the local end of the SSH tunnel.

Can be any valid unused port.
'''
            ),
            default=default_local_port,
            cl_coercer=int,
            requires=['ssh'],
        )

        core.config_settings[prefix+delim+'remote_host'] = dict(
            descr=(
'''
The hostname on the remote end of the SSH tunnel.

Connected to from the remote host.

This is generally 'localhost', but it may need to be (e.g.) '127.0.0.1'
or '::1'.  It can also be something else entirely, for example if the
purpose of the tunnel is to get through a firewall, but a connection
cannot be made directly to the necessary server.
'''
            ),
            default='localhost',
            cl_coercer=str,
            requires=['ssh'],
        )

        core.config_settings[prefix+delim+'remote_port'] = dict(
            descr=(
'''
The port number on the remote end of the SSH tunnel.
'''
            ),
            default=default_remote_port,
            cl_coercer=int,
            requires=['ssh'],
        )


        core.config_settings[prefix+delim+'tun_timeout'] = dict(
            descr=(
'''
Timeout for establishing the SSH tunnel, in seconds.

Can be None, to wait forever, or a number >= 0.
'''
            ),
            default=15,
            cl_coercer=(lambda x: None if x == 'None' or x == 'none'
                                       else int(x)),
            requires=['ssh'],
        )

    if extra_text:
        setting_list = [
            'ssh_host', 'ssh_port', 'ssh_user', 'ssh_key_file',
            'ssh_options',
        ]
        if tunnel:
            setting_list += [
                'local_host', 'local_port', 'remote_host',  'remote_port',
                'tun_timeout',
            ]
        for s_name in setting_list:
            core.config_settings[prefix+delim+s_name]['descr'] += (
                '\n' + extra_text
            )

    _config_blocks.append((prefix+delim, tunnel))


def validate_ssh_config():
    """
    Validate all SSH config settings.
    Dependencies:
        config settings: [prefix+delim+:] (heading), ssh_host, ssh_port,
                         ssh_user, ssh_key_file, ssh_options,
                         local_host, local_port, remote_host,
                         remote_port, tun_timeout
        globals: NoneType [if using Python 3], _config_blocks
        modules: types.NoneType [if using Python 2], core
    """
    for pd, tunnel in _config_blocks:
        core.setting_check_not_blank(pd+'ssh_host')
        if core.setting_is_set(pd+'ssh_port'):
            core.setting_check_num(pd+'ssh_port', 1, 65535)
        if core.setting_is_set(pd+'ssh_user'):
            core.setting_check_not_blank(pd+'ssh_user')
        if core.setting_is_set(pd+'ssh_key_file'):
            core.setting_check_file_read(pd+'ssh_key_file')
        if core.setting_is_set(pd+'ssh_options'):
            if (core.setting_check_type(pd+'ssh_options',
                                        core.STRING_TYPES + (list, ))
                  is list):
                core.setting_check_not_empty(pd+'ssh_options')
                for i, o in enumerate(core.cfg[pd+'ssh_options']):
                    core.setting_check_type((pd+'ssh_options', i),
                                            core.STRING_TYPES)
            else:
                core.setting_check_not_blank(pd+'ssh_options')
        if tunnel:
            core.setting_check_not_blank(pd+'local_host')
            core.setting_check_num(pd+'local_port', 1, 65535)
            core.setting_check_not_blank(pd+'remote_host')
            core.setting_check_num(pd+'remote_port', 1, 65535)
            if (core.setting_check_type(pd+'tun_timeout',
                                        core.NUMBER_TYPES + (NoneType, ))
                  is not NoneType):
                core.setting_check_num(pd+'tun_timeout', 0)


##################################
# SSH remote commands and tunnels
##################################

def get_ssh_cmd(prefix, delim='_'):
    """
    Assemble a list containing the ssh command and its arguments.
    For remote commands, add the remote command/argument list to the
    list returned from this function.
    See also get_ssh_tunnel_cmd().
    Parameters:
        prefix, delim: prefix and delimiter that start the setting names
    Dependencies:
        config settings: [prefix+delim+:] ssh_host, ssh_port,
                         ssh_user, ssh_key_file, ssh_options
        modules: shlex, core
    """
    cmd = ['ssh']
    if prefix+delim+'ssh_port' in core.cfg:
        cmd += ['-p', str(core.cfg[prefix+delim+'ssh_port'])]
    if prefix+delim+'ssh_key_file' in core.cfg:
        cmd += ['-i', core.cfg[prefix+delim+'ssh_key_file']]
    if prefix+delim+'ssh_options' in core.cfg:
        if isinstance(core.cfg[prefix+delim+'ssh_options'], list):
            cmd += core.cfg[prefix+delim+'ssh_options']
        else:
            cmd += shlex.split(core.cfg[prefix+delim+'ssh_options'])
    if prefix+delim+'ssh_user' in core.cfg:
        cmd += ['-l', core.cfg[prefix+delim+'ssh_user']]
    cmd.append(core.cfg[prefix+delim+'ssh_host'])
    return cmd


def get_ssh_tunnel_cmd(prefix, delim='_'):
    """
    Assemble a list containing the ssh tunnel command and its arguments.
    Parameters:
        prefix, delim: prefix and delimiter that start the setting names
    Dependencies:
        config settings: [prefix+delim+:] local_port, remote_host,
                         remote_port
        functions: get_ssh_cmd()
        modules: core
    """
    tunnel_arg = ['-L']
    tunnel_arg.append(':'.join(core.cfg[prefix+delim+'local_port'],
                               core.cfg[prefix+delim+'remote_host'],
                               core.cfg[prefix+delim+'remote_port']))
    tunnel_arg.append('-N')
    cmd = get_ssh_cmd(prefix, delim)
    return cmd[0] + tunnel_arg + cmd[1:]


########################################################################
#                           RUN STANDALONE
########################################################################

def main():
    core.process_command_line()

if __name__ == '__main__':
    main()
