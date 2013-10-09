#!/usr/bin/env python


"""
This is the SSH submodule for the nori library; see __main__.py for
license and usage information.


DOCSTRING CONTENTS:
-------------------

1) About and Requirements
2) API Classes


1) ABOUT AND REQUIREMENTS:
--------------------------

This submodule provides SSH functionality, including remote command
execution and tunnels.  It requires the 'ssh' command line utility,
which must be in the execution search path.


2) API CLASSES:
-----------------

    SSH(object)
        This class wraps all of the SSH functionality.

        Startup and Config-file Processing:
        -----------------------------------

        create_settings()
            Add a block of SSH config settings to the script.

        validate_config()
            Validate SSH config settings.


        SSH Remote Commands and Tunnels:
        --------------------------------

        get_cmd()
            Assemble a list containing the ssh command and its
            arguments.

        get_tunnel_cmd()
            Assemble a list containing the ssh tunnel command and its
            args.

        open_tunnel()
            Open an SSH tunnel, including testing and logging.

        close_tunnel()
            Close an SSH tunnel, including logging.

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
import atexit
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

# NoneType isn't in the types module anymore, but it's more readable
if sys.hexversion >= 0x03000000:
    NoneType = type(None)


##################
# status and meta
##################

#
# exit values
#

core.exitvals['ssh_connect'] = dict(
    num=20,
    descr=(
'''
error establishing SSH connection
'''
    ),
)

core.exitvals['ssh_tunnel'] = dict(
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


########################################################################
#                               CLASSES
########################################################################

class SSH(object):

    """This class wraps all of the SSH functionality."""

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


    #####################################
    # startup and config file processing
    #####################################

    def create_settings(self, heading='', extra_text='', ignore=None,
                            extra_requires=[], tunnel=False,
                            default_local_port=None,
                            default_remote_port=None):

        """
        Add a block of SSH config settings to the script.

        Makes the output log settings visible; to reverse this:
            # make output log settings invisible
            core.config_settings_no_print_output_log(True)
            core.config_settings['exec_path']['no_print'] = True
            core.config_settings['print_cmds']['no_print'] = True

        When modifying, remember to keep the setting_list at the bottom
        and validate_config() in sync with the config settings.

        Parameters:
            heading: if not blank, a heading entry with this value will
                     be added to the config settings
            extra_text: if not blank, this value is added to each
                        setting description (prepended with a blank
                        line; does not include the heading)
                        this is mainly intended to be used for things
                        like 'Ignored if [some setting] is not True.'
            ignore: if not None, a function; when this function is true,
                    don't bother validating the settings
            extra_requires: a list of features to be added to the
                            settings' requires attributes
            tunnel: if true, add tunnel-specific settings
            default_local_port: if tunnel is true, used as the default
                                local port number for the tunnel (and
                                must be set)
            default_remote_port: if tunnel is true, used as the default
                                 remote port number for the tunnel (and
                                 must be set)

        Dependencies:
            instance vars: prefix, delim, tunnel_config, ignore
            methods: validate_config()
            config settings: [prefix+delim+:] (heading), ssh_host,
                             ssh_port, ssh_user, ssh_key_file,
                             ssh_options, local_host, local_port,
                             remote_host, remote_port, tun_timeout
            globals: _config_blocks
            modules: core

        """

        # make output log settings visible
        core.config_settings_no_print_output_log(False)
        core.config_settings['exec_path']['no_print'] = False
        core.config_settings['print_cmds']['no_print'] = False

        pd = self.prefix + self.delim
        self.tunnel_config = tunnel
        self.ignore = ignore

        if heading:
            core.config_settings[pd + 'heading'] = dict(
                heading=heading,
            )

        core.config_settings[pd + 'ssh_host'] = dict(
            descr=(
'''
The hostname of the remote SSH host.
'''
            ),
            # no default
            cl_coercer=str,
        )

        core.config_settings[pd + 'ssh_port'] = dict(
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
        )

        core.config_settings[pd + 'ssh_user'] = dict(
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
        )

        core.config_settings[pd + 'ssh_key_file'] = dict(
            descr=(
'''
The path to the SSH key file.
'''
            ),
            # no default
            default_descr=(
'''
the ssh utility's default (generally ~/.ssh/id_*)
'''.format(pd)
            ),
            cl_coercer=str,
        )

        core.config_settings[pd + 'ssh_options'] = dict(
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
        )

        if tunnel:
            core.config_settings[pd + 'local_host'] = dict(
                descr=(
'''
The hostname on the local end of the SSH tunnel.

This is generally 'localhost', but it may need to be (e.g.) '127.0.0.1'
or '::1'.
'''
                ),
                default='localhost',
                cl_coercer=str,
            )

            core.config_settings[pd + 'local_port'] = dict(
                descr=(
'''
The port number on the local end of the SSH tunnel.

Can be any valid unused port.
'''
                ),
                default=default_local_port,
                cl_coercer=int,
            )

            core.config_settings[pd + 'remote_host'] = dict(
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
            )

            core.config_settings[pd + 'remote_port'] = dict(
                descr=(
'''
The port number on the remote end of the SSH tunnel.
'''
                ),
                default=default_remote_port,
                cl_coercer=int,
            )

            core.config_settings[pd + 'tun_timeout'] = dict(
                descr=(
'''
Timeout for establishing the SSH tunnel, in seconds.

Can be None, to wait forever, or a number >= 1.
'''
                ),
                default=15,
                cl_coercer=(lambda x: None if x == 'None' or x == 'none'
                                           else int(x)),
            )

        setting_list = [
            'ssh_host', 'ssh_port', 'ssh_user', 'ssh_key_file',
            'ssh_options',
        ]
        if tunnel:
            setting_list += [
                'local_host', 'local_port', 'remote_host',  'remote_port',
                'tun_timeout',
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
                    ['ssh'] + extra_requires
                )
            else:
                core.config_settings[pd + s_name]['requires'] = (
                    ['ssh'] + extra_requires
                )

        core.validate_config_hooks.append(self.validate_config)


    def validate_config(self):
        """
        Validate SSH config settings.
        Dependencies:
            instance vars: prefix, delim, ignore, tunnel_config
            config settings: [prefix+delim+:] (heading), ssh_host,
                             ssh_port, ssh_user, ssh_key_file,
                             ssh_options, local_host, local_port,
                             remote_host, remote_port, tun_timeout
            globals: NoneType [if using Python 3], _config_blocks
            modules: types.NoneType [if using Python 2], core
            Python: 2.0/3.2, for callable()
        """
        pd = self.prefix + self.delim
        if callable(self.ignore) and self.ignore():
            return
        core.setting_check_not_blank(pd + 'ssh_host')
        if core.setting_is_set(pd + 'ssh_port'):
            core.setting_check_num(pd + 'ssh_port', 1, 65535)
        if core.setting_is_set(pd + 'ssh_user'):
            core.setting_check_not_blank(pd + 'ssh_user')
        if core.setting_is_set(pd + 'ssh_key_file'):
            core.setting_check_file_read(pd + 'ssh_key_file')
        if core.setting_is_set(pd + 'ssh_options'):
            if (core.setting_check_type(pd + 'ssh_options',
                                        core.STRING_TYPES + (list, ))
                  is list):
                core.setting_check_not_empty(pd + 'ssh_options')
                for i, o in enumerate(core.cfg[pd + 'ssh_options']):
                    core.setting_check_type((pd + 'ssh_options', i),
                                            core.STRING_TYPES)
            else:
                core.setting_check_not_blank(pd + 'ssh_options')
        if self.tunnel_config:
            core.setting_check_not_blank(pd + 'local_host')
            core.setting_check_num(pd + 'local_port', 1, 65535)
            core.setting_check_not_blank(pd + 'remote_host')
            core.setting_check_num(pd + 'remote_port', 1, 65535)
            if (core.setting_check_type(pd + 'tun_timeout',
                                        core.NUMBER_TYPES + (NoneType, ))
                  is not NoneType):
                core.setting_check_num(pd + 'tun_timeout', 0)


    ##################################
    # SSH remote commands and tunnels
    ##################################

    def get_cmd(self):
        """
        Assemble a list containing the ssh command and its arguments.
        Can be used with (e.g.) core.run_command() or
        core.run_with_logging().
        For remote commands, add the remote command/argument list to the
        list returned from this function.
        See also get_ssh_tunnel_cmd().
        Dependencies:
            instance vars: prefix, delim
            config settings: [prefix+delim+:] ssh_host, ssh_port,
                             ssh_user, ssh_key_file, ssh_options
            modules: shlex, core
            external commands: ssh
        """
        pd = self.prefix + self.delim
        cmd = ['ssh']
        if pd + 'ssh_port' in core.cfg:
            cmd += ['-p', str(core.cfg[pd + 'ssh_port'])]
        if pd + 'ssh_key_file' in core.cfg:
            cmd += ['-i', core.cfg[pd + 'ssh_key_file']]
        if pd + 'ssh_options' in core.cfg:
            if isinstance(core.cfg[pd + 'ssh_options'], list):
                cmd += core.cfg[pd + 'ssh_options']
            else:
                cmd += shlex.split(core.cfg[pd + 'ssh_options'])
        if pd + 'ssh_user' in core.cfg:
            cmd += ['-l', core.cfg[pd + 'ssh_user']]
        cmd.append(core.cfg[pd + 'ssh_host'])
        return cmd


    def get_tunnel_cmd(self):
        """
        Assemble a list containing the ssh tunnel command and its args.
        Can be used with (e.g.) core.run_command() or
        core.run_with_logging(), but see open_ssh_tunnel(), below.
        Dependencies:
            instance vars: prefix, delim
            config settings: [prefix+delim+:] local_port, remote_host,
                             remote_port
            functions: get_ssh_cmd()
            modules: core
            external commands: ssh
        """
        pd = self.prefix + self.delim
        tunnel_arg = ['-L']
        tunnel_arg.append(':'.join(core.cfg[pd + 'local_port'],
                                   core.cfg[pd + 'remote_host'],
                                   core.cfg[pd + 'remote_port']))
        tunnel_arg.append('-N')
        cmd = get_ssh_cmd(prefix, delim)
        return cmd[0] + tunnel_arg + cmd[1:]


    def open_tunnel(self, descr, atexit_reg=True, use_logger=True,
                    warn_only=False,
                    exit_val=core.exitvals['ssh_tunnel']['num']):

        """
        Open an SSH tunnel, including testing and logging.

        Returns the tunnel's process object on success, otherwise False.

        Parameters:
            descr: a description of the tunnel's purpose (e.g. 'mysql
                   dumps' or 'rsync backups'); this is used in status
                   and error messages like 'running SSH tunnel for mysql
                   dumps'
            atexit_reg: if true, register a callback to kill the tunnel
                        on exit; see core.run_command()
            see core.generic_error_handler() for the rest

        Dependencies:
            instance vars: prefix, delim, descr, p_obj
            methods: get_ssh_tunnel_cmd(), close_ssh_tunnel()
            config settings: [prefix+delim+:] (remote_host),
                             (remote_port), local_host, local_port,
                             tun_timeout
            modules: (subprocess), atexit, core
            external commands: (ssh)

        """

        pd = self.prefix + self.delim
        self.descr = descr

        # log that we're running the command
        core.logging_stop_stdouterr()
        core.status_logger.info('Running SSH tunnel command for {0}...' .
                                format(descr))
        core.logging_start_stdouterr()
        core.output_logger.info('Running SSH tunnel command for {0}...' .
                                format(descr))

        # run the command and set up our own exit callback
        p = core.run_with_logging(
            'SSH tunnel for {0}'.format(descr), self.get_ssh_tunnel_cmd(),
            bg=True, atexit_register=False
        )
        self.p_obj = p
        atexit.register(self.close_ssh_tunnel)

        # test the tunnel
        waited = 0
        while True:
            # keep trying with 1-sec timeouts because the tunnel might
            # take a while to come up; if we try once with a long
            # timeout, we might catch it while it's still connecting,
            # even though it's fine
            if core.test_remote_port(descr,
                                     (core.cfg[pd + 'local_host'],
                                      core.cfg[pd + 'local_port']),
                                     timeout=1, use_logger=None,
                                     warn_only=True):
                connected = True
                break
            waited += 1

            # not working yet, but is it still running?
            if p.poll() is None:
                if waited >= core.cfg[pd + 'tun_timeout']:
                    core.kill_bg_command(p)
                    msg = ('could not establish SSH tunnel for {0} '
                           '(timed out)'.format(descr))
                    core.generic_error_handler(
                        None, msg, core.render_command_exception,
                        use_logger, warn_only, exit_val
                    )
                    connected = False
            else:  # process is already dead
                ssh_exit = p.wait()
                msg = ('could not establish SSH tunnel for {0} '
                       '(status code {1})'.format(descr, ssh_exit))
                core.generic_error_handler(
                    None, msg, core.render_command_exception, use_logger,
                    warn_only, exit_val
                )
                connected = False

        if connected:
            core.status_logger.info('SSH tunnel for {0} established.' .
                                    format(descr))
            return p
        else:
            return False


    def close_tunnel(self):
        """
        Close an SSH tunnel, including logging.
        For tunnels opened with open_ssh_tunnel().
        Can be called even if the tunnel already died / was closed / was
        killed.
        Dependencies:
            instance vars: descr, p_obj
            modules: core
        """
        ret, already = core.kill_bg_command(self.p_obj)
        if already:
            core.status_logger.info('SSH tunnel for {0} was already '
                                    'closed.'.format(self.descr))
        else:
            core.status_logger.info('SSH tunnel for {0} has been closed.' .
                                    format(self.descr))
