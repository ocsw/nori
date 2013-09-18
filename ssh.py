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
execution and tunnels.  It requires the paramiko module:
    https://github.com/paramiko/paramiko


2) API FUNCTIONS:
-----------------

    Startup and config file processing:
    -----------------------------------

    create_ssh_settings
        Add a block of SSH config settings to the script.

    validate_config
        Validate all SSH config settings.


    SSH remote commands and tunnels:
    --------------------------------

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

import sys
import getpass
from types import *
from pprint import pprint as pp  # for debugging


#########
# add-on
#########

try:
    import paramiko
except ImportError:
    pass  # see the status and meta variables section


###############
# this package
###############

from . import nori


########################################################################
#                              VARIABLES
########################################################################

##################
# status and meta
##################

#
# exit values
#

nori.exitvals['ssh_connect']=dict(
    num=20,
    descr=(
"""
error establishing SSH connection (including timeouts)
"""
    ),
)

nori.exitvals['ssh_host_key']=dict(
    num=21,
    descr=(
"""
host key problem while establishing SSH connection
"""
    ),
)

nori.exitvals['ssh_auth']=dict(
    num=22,
    descr=(
"""
authentication problem while establishing SSH connection
"""
    ),
)

nori.exitvals['ssh_command']=dict(
    num=23,
    descr=(
"""
error running remote command over SSH
"""
    ),
)

nori.exitvals['ssh_tunnel']=dict(
    num=24,
    descr=(
"""
error establishing SSH tunnel
"""
    ),
)

# supported / available features
nori.supported_features['ssh'] = 'SSH command and tunnel support'
if 'paramiko' in sys.modules:
    nori.available_features.append('ssh')


#########################
# configuration settings
#########################

# list of tuples: (prefix + delim, tunnel?)
# see config functions
_config_blocks = []


#############
# hook lists
#############

nori.validate_config_hooks.append(lambda: validate_config())


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
        globals: _config_blocks
        modules: getpass, nori

    """

    if heading:
        nori.config_settings[prefix + delim + 'heading'] = dict(
            heading=heading,
        )

    nori.config_settings[prefix + delim + 'ssh_host'] = dict(
        descr=(
"""
The hostname of the remote SSH host.
"""
        ),
        # no default
        cl_coercer=str,
        requires=['ssh'],
    )

    nori.config_settings[prefix + delim + 'ssh_port'] = dict(
        descr=(
"""
The SSH port on the remote host.
"""
        ),
        default=22,
        default_descr=(
"""
22 (the standard port)
"""
        ),
        cl_coercer=int,
        requires=['ssh'],
    )

    nori.config_settings[prefix + delim + 'ssh_user'] = dict(
        descr=(
"""
Username on the remote SSH host.
"""
        ),
        default=getpass.getuser(),
        default_descr=(
"""
the username the script is run by
"""
        ),
        cl_coercer=str,
        requires=['ssh'],
    )

    nori.config_settings[prefix + delim + 'ssh_key_file'] = dict(
        descr=(
"""
The path to the SSH key file.
"""
        ),
        default=None,
        default_descr=(
"""
any key available through an SSH agent, or ~/.ssh/id_rsa, or
~/.ssh/id_dsa, (in that order), subject to the values of the
{0}ssh_allow_agent and {0}ssh_look_for_keys settings
""".format(prefix + delim)
        ),
        cl_coercer=str,
        requires=['ssh'],
    )

    nori.config_settings[prefix + delim + 'ssh_allow_agent'] = dict(
        descr=(
"""
Look for an SSH agent if a key file is not supplied?

Can be True or False.
"""
        ),
        default=True,
        cl_coercer=lambda x: str_to_bool(x),
        requires=['ssh'],
    )

    nori.config_settings[prefix + delim + 'ssh_look_for_keys'] = dict(
        descr=(
"""
Look for ~/.ssh/id_rsa and ~/.ssh/id_dsa if a key file is not supplied?

Can be True or False.
"""
        ),
        default=True,
        cl_coercer=lambda x: str_to_bool(x),
        requires=['ssh'],
    )

#set_combine_stderr(self, combine)
#Set whether stderr should be combined into stdout on this channel.

#set_name(self, name)
#Set a name for this channel.

#setblocking(self, blocking)
#Set blocking or non-blocking mode of the channel: if blocking is 0, the
#channel is set to non-blocking mode; otherwise it's set to blocking mode.

#settimeout(self, timeout)
#Set a timeout on blocking read/write operations.


###TODO password auth?  password for key?
###TODO host key policy / files
#    nori.config_settings[prefix + delim + 'ssh_'] = dict(
#        descr=(
#"""
#"""
#        ),
#        default=,
#        cl_coercer=str,
#        requires=['ssh'],
#    )

    nori.config_settings[prefix + delim + 'ssh_compress'] = dict(
        descr=(
"""
Use SSH compression?

Can be True or False.
"""
        ),
        default=False,
        cl_coercer=lambda x: str_to_bool(x),
        requires=['ssh'],
    )

    nori.config_settings[prefix + delim + 'ssh_timeout'] = dict(
        descr=(
"""
Timeout for establishing the SSH connection, in seconds.

Can be None, to wait forever.
"""
        ),
        default=15,
        cl_coercer=lambda x: None if x == 'None' or x == 'none' else int(x),
        requires=['ssh'],
    )

    if tunnel:
        nori.config_settings[prefix + delim + 'local_host'] = dict(
            descr=(
"""
The hostname on the local end of the SSH tunnel.

This is generally 'localhost', but it may need to be (e.g.) '127.0.0.1'
or '::1'.
"""
            ),
            default='localhost',
            cl_coercer=str,
            requires=['ssh'],
        )

        nori.config_settings[prefix + delim + 'local_port'] = dict(
            descr=(
"""
The port number on the local end of the SSH tunnel.

Can be any valid unused port.
"""
            ),
            default=default_local_port,
            cl_coercer=int,
            requires=['ssh'],
        )

        nori.config_settings[prefix + delim + 'remote_host'] = dict(
            descr=(
"""
The hostname on the remote end of the SSH tunnel.

Connected to from the remote host.

This is generally 'localhost', but it may need to be (e.g.) '127.0.0.1'
or '::1'.  It can also be something else entirely, for example if the
purpose of the tunnel is to get through a firewall, but a connection
cannot be made directly to the necessary server.
"""
            ),
            default='localhost',
            cl_coercer=str,
            requires=['ssh'],
        )

        nori.config_settings[prefix + delim + 'remote_port'] = dict(
            descr=(
"""
The port number on the remote end of the SSH tunnel.
"""
            ),
            default=default_remote_port,
            cl_coercer=int,
            requires=['ssh'],
        )

    if extra_text:
        setting_list = [
            'ssh_host', 'ssh_port', 'ssh_user', 'ssh_key_file',
            'ssh_allow_agent', 'ssh_look_for_keys', 'ssh_compress',
            'ssh_timeout',
        ]
        if tunnel:
            setting_list += [
                'local_host', 'local_port', 'remote_host',  'remote_port',
            ]
        for s_name in setting_list:
            nori.config_settings[prefix + delim + s_name]['descr'] += (
                '\n' + extra_text
            )

    _config_blocks.append((prefix + delim, tunnel))


def validate_config():
    """
    Validate all SSH config settings.
    Dependencies:
        globals: _config_blocks
        modules: types, nori
    """
    for pd, tunnel in _config_blocks:
        nori.setting_check_not_blank(pd + 'ssh_host')
        nori.setting_check_num(pd + 'ssh_port', 1, 65535)
        nori.setting_check_not_blank(pd + 'ssh_user')
        nori.setting_check_file_read(pd + 'ssh_key_file')
        nori.setting_check_type(pd + 'ssh_allow_agent', bool)
        nori.setting_check_type(pd + 'ssh_look_for_keys', bool)
        nori.setting_check_type(pd + 'ssh_compress', bool)
        if (nori.setting_check_type(pd + 'ssh_timeout',
                                    nori.NUMBER_TYPES + (NoneType, ))
              is not NoneType):
            nori.setting_check_num(pd + 'ssh_timeout', 0)
        if tunnel:
            nori.setting_check_not_blank(pd + 'local_host')
            nori.setting_check_num(pd + 'local_port', 1, 65535)
            nori.setting_check_not_blank(pd + 'remote_host')
            nori.setting_check_num(pd + 'remote_port', 1, 65535)


##################################
# SSH remote commands and tunnels
##################################

# error handler

#    if 'ssh' not in nori.available_features:
#        nori.err_exit('Internal Error: SSH function called, but '
#                      'there is no SSH support; exiting.',
#                      nori.exitvals['internal']['num'])


#    client = paramiko.SSHClient()
#    client.load_system_host_keys()
#    client.connect('ssh.example.com', username='strongbad', password='thecheat')
#    stdin, stdout, stderr = client.exec_command('ls')
#    for line in stdout:
#        print '... ' + line.strip('\n')
#    client.close()


########################################################################
#                           RUN STANDALONE
########################################################################

def main():
    nori.process_command_line()

if __name__ == '__main__':
    main()
