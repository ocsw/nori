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
import atexit


###############
# this package
###############

from .. import core
from ..ssh import SSH


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
error connecting to or disconnecting from a database;
also used for cursors
'''
    ),
)

core.exitvals['dbms_execute'] = dict(
    num=31,
    descr=(
'''
error executing a database query/command/function
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

    # module object containing connect(), etc.
    MODULE = None

    # local and remote ports for tunnels (remote is also for direct
    # connections); must be set by subclasses
    DEFAULT_LOCAL_PORT = None
    DEFAULT_REMOTE_PORT = None

    # where to look for the socket file, to set the default
    # format can vary by subclass (e.g., files vs. directories)
    SOCKET_SEARCH_PATH = []


    ################################
    # class variables: housekeeping
    ################################

    # these are used to keep track of all connections/cursors for last-
    # minute cleanup; see close_conns() and close_cursors()
    # NOTE: * do not override them in subclasses
    #       * refer to them with DBMS.var
    atexit_close_conns_registered = False
    atexit_close_cursors_registered = False
    open_conns = []  # actually contains DBMS objects with open conns
    open_cursors = []    # actually contains tuples: (DBMS obj, cur obj)


    ###############
    # housekeeping
    ###############

    def __init__(self, prefix, delim='_', err_use_logger=True,
                 err_warn_only=False, err_no_exit=False,
                 warn_use_logger=True, warn_warn_only=True,
                 warn_no_exit=False):
        """
        Populate instance variables.
        See also save_err_warn() / restore_err_warn().
        Parameters:
            prefix, delim: prefix and delimiter that start the setting
                           names to use
            err_no_exit: if True, don't exit the script on DBMS / tunnel
                         errors (assuming warn_only is False; this is
                         the equivalent of passing exit_val=None to
                         core.generic_error_handler())
            warn_no_exit: like err_no_exit, but for DBMS warnings
            see core.generic_error_handler() for the rest;
                err_* apply to DBMS errors, and warn_* apply to DBMS
                warnings
                note that if warn_warn_only is False, warnings will be
                treated as errors
        """
        self.prefix = prefix
        self.delim = delim
        self.err_use_logger = err_use_logger
        self.err_warn_only = err_warn_only
        self.err_no_exit = err_no_exit
        self.warn_use_logger = warn_use_logger
        self.warn_warn_only = warn_warn_only
        self.warn_no_exit = warn_no_exit
        self.conn = None
        self.cur = None


    @classmethod
    def close_conns(cls):
        """
        Close all DBMS connections.
        NOTE: * do not override in subclasses
              * call with DBMS.close_conns()
        Dependencies:
            class vars: open_conns
            instance methods: close()
        """
        for dbms in cls.open_conns:
            dbms.close()


    @classmethod
    def close_cursors(cls):
        """
        Close all DBMS cursors.
        NOTE: * do not override in subclasses
              * call with DBMS.close_cursors()
        Dependencies:
            class vars: open_cursors
            instance methods: close_cursor()
        """
        for (dbms, cur) in cls.open_cursors:
            dbms.close_cursor(cur)


    #####################################
    # startup and config file processing
    #####################################

    def create_settings(self, heading='', extra_text='', ignore=None,
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
            ignore: if not None, a function; when this function is true,
                    don't bother validating the settings
            extra_requires: a list of features to be added to the
                            settings' requires attributes
            tunnel: if true, add SSH-tunnel settings

        Dependencies:
            class vars: DBMS_NAME, REQUIRES, DEFAULT_REMOTE_PORT,
                        DEFAULT_LOCAL_PORT
            instance vars: prefix, delim, tunnel_config, ignore, ssh
            methods: _ignore_ssh_settings, settings_extra_text(),
                     validate_config(), populate_conn_args()
            config settings: [prefix+delim+:] (heading), use_ssh_tunnel,
                             protocol, host, port, socket_file, user,
                             password, pw_file, connect_db,
                             connect_options, cursor_options
            modules: getpass, core, ssh.SSH

        """

        pd = self.prefix + self.delim
        self.tunnel_config = tunnel
        self.ignore = ignore

        if heading:
            core.config_settings[pd + 'heading'] = dict(
                heading=heading,
            )

        if tunnel:
            core.config_settings[pd + 'use_ssh_tunnel'] = dict(
                descr=(
'''
Use an SSH tunnel for the {0} connection (True/False)?

If True, specify the host in {0}_ssh_host and the port in
{0}_remote_port instead of {0}_host and
{0}_port.
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
            self.ssh = SSH(self.prefix, self.delim)
            self.ssh.create_settings(
                extra_text=ssh_extra_text,
                ignore=self._ignore_ssh_settings,
                extra_requires=(self.REQUIRES + extra_requires),
                tunnel=True,
                default_local_port=self.DEFAULT_LOCAL_PORT,
                default_remote_port=self.DEFAULT_REMOTE_PORT
            )

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

Recommended filename: '/etc/{1}/{2}.pw'.

Ignored if {3}password is set.
'''.format(self.DBMS_NAME, core.script_shortname, self.prefix, pd),
            ),

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
            default={},
        )

        core.config_settings[pd + 'cursor_options'] = dict(
            descr=(
'''
Additional options for creating {0} cursors.

Options must be supplied as a dict.
'''.format(self.DBMS_NAME)
            ),
            default={},
        )

        setting_list = [
            'protocol', 'host', 'port', 'socket_file', 'user', 'password',
            'pw_file', 'connect_db', 'connect_options', 'cursor_options',
        ]
        if tunnel:
            setting_list += [
                'use_ssh_tunnel',
            ]
        if extra_text:
            self.settings_extra_text(setting_list, extra_text)
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
        core.process_config_hooks.append(self.populate_conn_args)


    def _ignore_ssh_settings(self):
        """
        If true, ignore the SSH config settings.
        Dependencies:
            instance vars: prefix, delim
            config settings: [prefix+delim+:] use_ssh_tunnel
            modules: core
        """
        pd = self.prefix + self.delim
        return not core.cfg[pd + 'use_ssh_tunnel']


    def settings_extra_text(self, setting_list, extra_text):
        """
        Add extra text to config setting descriptions.
        Pulled out for use by subclasses that replace descriptions.
        Parameters:
            setting_list: a list of settings to modify
            extra_text: if not blank, added to the descriptions of the
                        settings in setting_list (preceded by a blank
                        line)
                        this is mainly intended to be used for things
                        like 'Ignored if [some setting] is False.'
        Dependencies:
            instance vars: prefix, delim
            modules: core
        """
        pd = self.prefix + self.delim
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


    def validate_config(self):
        """
        Validate DBMS config settings.
        Only does checks that are likely to be relevant for all DBMSes;
        it's easy to be more restrictive in subclasses, but hard to be
        more lenient.
        Dependencies:
            instance vars: ignore, prefix, delim, tunnel_config
            config settings: [prefix+delim+:] use_ssh_tunnel, protocol,
                             host, port, socket_file, user, password,
                             pw_file, connect_db, connect_options,
                             cursor_options
            modules: core
            Python: 2.0/3.2, for callable()
        """
        if callable(self.ignore) and self.ignore():
            return
        pd = self.prefix + self.delim
        if self.tunnel_config:
            core.setting_check_type(pd + 'use_ssh_tunnel', (bool, ))
        if not self.tunnel_config or not core.cfg[pd + 'use_ssh_tunnel']:
            if (pd + 'protocol' not in core.config_settings or
                  (pd + 'protocol' in core.cfg and
                   core.cfg[pd + 'protocol'] == 'tcp')):
                if pd + 'host' in core.cfg:
                    core.setting_check_not_blank(pd + 'host')
                if pd + 'port' in core.cfg:
                    core.setting_check_num(pd + 'port', 1, 65535)
            elif (pd + 'protocol' not in core.config_settings or
                  (pd + 'protocol' in core.cfg and
                   core.cfg[pd + 'protocol'] == 'socket')):
                if pd + 'socket_file' in core.cfg:
                    core.setting_check_file_rw(pd + 'socket_file')
        if pd + 'user' in core.cfg:
            core.setting_check_not_blank(pd + 'user')
        if pd + 'password' in core.cfg:
            core.setting_check_not_blank(pd + 'password')
        if pd + 'password' not in core.cfg and pd + 'pw_file' in core.cfg:
            core.setting_check_file_read(pd + 'pw_file')
        if pd + 'connect_db' in core.cfg:
            core.setting_check_not_blank(pd + 'connect_db')
        if pd + 'connect_options' in core.cfg:
            core.setting_check_kwargs(pd + 'connect_options')
        if pd + 'cursor_options' in core.cfg:
            core.setting_check_kwargs(pd + 'cursor_options')


    def populate_conn_args(self):
        """
        Turn the config settings into a dictionary of connection args.
        Dependencies:
            instance vars: prefix, delim, tunnel_config, conn_args
            methods: read_password_file()
            config_settings: [prefix+delim+:] use_ssh_tunnel,
                             local_host, local_port, protocol, host,
                             port, socket_file, user, password, pw_file,
                             connect_db, connect_options
            modules: core
        """
        pd = self.prefix + self.delim
        self.conn_args = {}
        if self.tunnel_config and core.cfg[pd + 'use_ssh_tunnel']:
            self.conn_args['host'] = core.cfg[pd + 'local_host']
            self.conn_args['port'] = core.cfg[pd + 'local_port']
        else:
            if (pd + 'protocol' not in core.config_settings or
                  (pd + 'protocol' in core.cfg and
                   core.cfg[pd + 'protocol'] == 'tcp')):
                if pd + 'host' in core.cfg:
                    self.conn_args['host'] = core.cfg[pd + 'host']
                if pd + 'port' in core.cfg:
                    self.conn_args['port'] = core.cfg[pd + 'port']
            elif (pd + 'protocol' not in core.config_settings or
                  (pd + 'protocol' in core.cfg and
                   core.cfg[pd + 'protocol'] == 'socket')):
                if pd + 'socket_file' in core.cfg:
                    self.conn_args['unix_socket'] = (
                        core.cfg[pd + 'socket_file']
                    )
        if pd + 'user' in core.cfg:
            self.conn_args['user'] = core.cfg[pd + 'user']
        if pd + 'password' in core.cfg:
            self.conn_args['password'] = core.cfg[pd + 'password']
        elif pd + 'pw_file' in core.cfg:
            self.conn_args['password'] = self.read_password_file()
        if pd + 'connect_db' in core.cfg:
            self.conn_args['database'] = core.cfg[pd + 'connect_db']
        if pd + 'connect_options' in core.cfg:
            self.conn_args.update(core.cfg[pd + 'connect_options'])


    def read_password_file(self):
        """
        Get and the password from the password file.
        Dependencies:
            instance vars: prefix, delim
            config_settings: [prefix+delim+:] pw_file
            modules: core
        """
        pd = self.prefix + self.delim
        try:
            with open(core.fix_path(core.cfg[pd + 'pw_file']), 'r') as pf:
                return pf.read().strip()
        except IOError as e:
            core.file_error_handler(
                e, 'read', 'password file', cfg[pd + 'pw_file'],
                must_exist=True, use_logger=True, warn_only=False,
                exit_val=core.exitvals['startup']['num']
            )


    #############################
    # logging and error handling
    #############################

    def error_handler(self, e, err_verb, warn_verb, exit_val):

        """
        Handle DBMS exceptions with various options.

        If it returns, returns False.

        Parameters:
            err_verb: a string describing the action that failed, for
                      errors (e.g., 'connect to')
            warn_verb: a string describing the action that failed, for
                       warnings (e.g., 'connecting to')
            see core.generic_error_handler() for the rest

        Dependencies:
            class vars: DBMS_NAME, MODULE
            instance vars: prefix, delim, err_use_logger, err_warn_only,
                           err_no_exit, warn_use_logger, warn_warn_only,
                           warn_no_exit
            methods: render_exception()
            modules: (contents of MODULE), core

        """

        pd = self.prefix + self.delim

        if isinstance(e, self.MODULE.Warning):
            use_logger = self.warn_use_logger
            warn_only = self.warn_warn_only
            exit_val=None if self.warn_no_exit else exit_val
        if isinstance(e, self.MODULE.Error):
            use_logger = self.err_use_logger
            warn_only = self.err_warn_only
            exit_val=None if self.err_no_exit else exit_val

        if warn_only:
            msg = ('problem {0} {1} DBMS '
                   '(config prefix/delim {2})' .
                   format(warn_verb, self.DBMS_NAME, core.pps(pd)))
        else:
            msg = ('could not {0} {1} DBMS '
                   '(config prefix/delim {2})' .
                   format(err_verb, self.DBMS_NAME, core.pps(pd)))

        return core.generic_error_handler(
            e, msg, self.render_exception, use_logger, warn_only, exit_val
        )


    def render_exception(self, e):
        """
        Return a formatted string for a DBMS-related exception.
        Parameters:
            e: the exception to render
        """
        return 'Details: {0}'.format(e)


    def save_err_warn(self):
        """
        Save the err.* and warn.* settings before temporary changes.
        Dependencies:
            instance vars: err_use_logger, err_warn_only, err_no_exit,
                           warn_use_logger, warn_warn_only,
                           warn_no_exit, err_use_logger_saved,
                           err_warn_only_saved, err_no_exit_saved,
                           warn_use_logger_saved, warn_warn_only_saved,
                           warn_no_exit_saved
        """
        self.err_use_logger_saved = self.err_use_logger
        self.err_warn_only_saved = self.err_warn_only
        self.err_no_exit_saved = self.err_no_exit
        self.warn_use_logger_saved = self.warn_use_logger
        self.warn_warn_only_saved = self.warn_warn_only
        self.warn_no_exit_saved = self.warn_no_exit


    def restore_err_warn(self):
        """
        Restore the err.* and warn.* settings after temporary changes.
        Dependencies:
            instance vars: err_use_logger, err_warn_only, err_no_exit,
                           warn_use_logger, warn_warn_only,
                           warn_no_exit, err_use_logger_saved,
                           err_warn_only_saved, err_no_exit_saved,
                           warn_use_logger_saved, warn_warn_only_saved,
                           warn_no_exit_saved
        """
        self.err_use_logger = self.err_use_logger_saved
        self.err_warn_only = self.err_warn_only_saved
        self.err_no_exit = self.err_no_exit_saved
        self.warn_use_logger = self.warn_use_logger_saved
        self.warn_warn_only = self.warn_warn_only_saved
        self.warn_no_exit = self.warn_no_exit_saved
        del(self.err_use_logger_saved)
        del(self.err_warn_only_saved)
        del(self.err_no_exit_saved)
        del(self.warn_use_logger_saved)
        del(self.warn_warn_only_saved)
        del(self.warn_no_exit_saved)


    def wrap_call(self, func, err_verb, warn_verb, *args, **kwargs):
        """
        Wrap a DBMS function call in error handling.
        Returns a tuple: (success?, function_return_value)
        Parameters:
            func: the function to wrap
            args/kwargs: arguments to pass to the function
            see error_handler() for the rest
        Dependencies:
            class vars: MODULE
            instance vars: err_warn_only
            methods: error_handler()
            modules: (module containing func), core
        """
        core.status_logger.debug('Calling DBMS function {0} with '
                                 'args:\n{1}\nand kwargs:\n{2}' .
                                 format(func, args, kwargs))
        err = False
        try:
            ret = func(*args, **kwargs)
        except (self.MODULE.Warning, self.MODULE.Error) as e:
            self.error_handler(
                e, err_verb, warn_verb,
                core.exitvals['dbms_execute']['num']
            )
            if isinstance(e, self.MODULE.Error) and not self.err_warn_only:
                err = True
        return (not err, ret)


    ###############################
    # DBMS connections and queries
    ###############################

    def connect(self):

        """
        Connect to the DBMS, including any SSH tunnel.

        Returns False on error, otherwise True.

        Dependencies:
            class vars: DBMS_NAME, MODULE,
                        atexit_close_conns_registered, open_conns
            instance vars: prefix, delim, tunnel_config, ssh, conn_args,
                           conn, err_use_logger, err_warn_only,
                           err_no_exit
            methods: close_conns(), error_handler()
            config settings: [prefix+delim+:] use_ssh_tunnel
            modules: atexit, (contents of MODULE), core, (ssh.SSH)

        """

        pd = self.prefix + self.delim

        # SSH tunnel
        if self.tunnel_config and core.cfg[pd + 'use_ssh_tunnel']:
            if self.err_no_exit:
                # atexit_reg = True, exit_val = None
                self.ssh.open_tunnel(self.DBMS_NAME + ' connection',
                                     True, self.err_use_logger,
                                     self.err_warn_only, None)
            else:
                # atexit_reg = True
                self.ssh.open_tunnel(self.DBMS_NAME + ' connection',
                                     True, self.err_use_logger,
                                     self.err_warn_only)

        # DBMS connection
        core.status_logger.info(
            'Connecting to {0} DBMS (config prefix/delim {1})...' .
            format(self.DBMS_NAME, core.pps(pd))
        )
        try:
            self.conn = self.MODULE.connect(**self.conn_args)
        except (self.MODULE.Warning, self.MODULE.Error) as e:
            self.error_handler(e, 'connect to', 'connecting to',
                               core.exitvals['dbms_connect']['num'])
            if isinstance(e, self.MODULE.Error):
                self.conn = None
                self.ssh.close_tunnel()
                return False
        if self not in DBMS.open_conns:
            DBMS.open_conns.append(self)
        if not DBMS.atexit_close_conns_registered:
            atexit.register(DBMS.close_conns)
            DBMS.atexit_close_conns_registered = True
        core.status_logger.info('{0} connection established.' .
                                format(self.DBMS_NAME))
        return True


    def close(self, force_no_exit=True):

        """
        Close the DBMS connection, including any SSH tunnel.

        Returns False on error, otherwise True.

        Parameters:
            force_no_exit: if True, don't exit on errors/warnings,
                           regardless of the values of err_no_exit and
                           warn_no_exit

        Dependencies:
            class vars: DBMS_NAME, MODULE, open_conns
            instance vars: prefix, delim, tunnel_config, ssh, conn, cur,
                           err_warn_only, err_no_exit, warn_no_exit
            methods: close_cursor(), save_err_warn(),
                     restore_err_warn(), error_handler()
            config settings: [prefix+delim+:] use_ssh_tunnel
            modules: (contents of MODULE), core, (ssh.SSH)

        """

        pd = self.prefix + self.delim

        # main cursor, if any
        if self.cur is not None:
            self.close_cursor(None, force_no_exit)

        # DBMS connection
        err = False
        if self.conn is None:
            core.status_logger.info(
                '{0} connection (config prefix/delim {1})\n'
                'was already closed.' .
                format(self.DBMS_NAME, core.pps(pd))
            )
        else:
            try:
                self.conn.close()
            except (self.MODULE.Warning, self.MODULE.Error) as e:
                if force_no_exit:
                    self.save_err_warn()
                    self.err_no_exit = True
                    self.warn_no_exit = True
                self.error_handler(e, 'close connection to',
                                   'closing connection to',
                                   core.exitvals['dbms_connect']['num'])
                if force_no_exit:
                    self.restore_err_warn()
                if (isinstance(e, self.MODULE.Error) and
                      not self.err_warn_only):
                    err = True
            self.conn = None
            if self in DBMS.open_conns:
                DBMS.open_conns.remove(self)
            if not err:
                core.status_logger.info(
                    '{0} connection (config prefix/delim {1})\n'
                    'has been closed.' .
                    format(self.DBMS_NAME, core.pps(pd))
                )

        # SSH tunnel
        if self.tunnel_config and core.cfg[pd + 'use_ssh_tunnel']:
            self.ssh.close_tunnel()

        return not err


    def cursor(self, main=True):

        """
        Get a cursor for the DBMS connection.

        Returns the cursor object, or None on error.

        Parameters:
            main: if True, treat this as the "main" cursor: store it in
                  the object and use it by default in other methods

        Dependencies:
            class vars: DBMS_NAME, MODULE,
                        atexit_close_cursors_registered, open_cursors
            instance vars: prefix, delim, conn, cur
            methods: close_cursors(), error_handler()
            config settings: [prefix+delim+:] cursor_options
            modules: atexit, (contents of MODULE), core

        """

        pd = self.prefix + self.delim

        try:
            cur = self.conn.cursor(**core.cfg[pd + 'cursor_options'])
        except (self.MODULE.Warning, self.MODULE.Error) as e:
            self.error_handler(e, 'get cursor for', 'getting cursor for',
                               core.exitvals['dbms_connect']['num'])
            if isinstance(e, self.MODULE.Error):
                cur = None

        if main:
            self.cur = cur
        if cur:
            if main:
                if (self, None) not in DBMS.open_cursors:
                    DBMS.open_cursors.append((self, None))
            else:
                if (self, cur) not in DBMS.open_cursors:
                    DBMS.open_cursors.append((self, cur))
            if not DBMS.atexit_close_cursors_registered:
                atexit.register(DBMS.close_cursors)
                DBMS.atexit_close_cursors_registered = True
            core.status_logger.debug('Got {0}{1} cursor.' .
                                     format('main ' if main else '',
                                            self.DBMS_NAME))

        return cur


    def close_cursor(self, cur=None, force_no_exit=True):

        """
        Close the DBMS cursor.

        Can be called more than once for the "main" cursor, but calling
        on an already-closed non-main cursor will cause an error.

        Returns False on error, otherwise True.

        Parameters:
            cur: the cursor to close; if None, the "main" cursor is
                 closed
            force_no_exit: if True, don't exit on errors/warnings,
                           regardless of the values of err_no_exit and
                           warn_no_exit

        Dependencies:
            class vars: DBMS_NAME, MODULE, open_cursors
            instance vars: prefix, delim, cur, err_warn_only,
                           err_no_exit, warn_no_exit
            methods: save_err_warn(), restore_err_warn(),
                     error_handler()
            modules: (contents of MODULE), core

        """

        pd = self.prefix + self.delim

        main_str = 'main ' if cur is None else ''

        if cur is None and self.cur is None:
            core.status_logger.debug(
                'Main {0} cursor (config prefix/delim {1})\n'
                'was already closed.' .
                format(self.DBMS_NAME, core.pps(pd))
            )
            return True

        err = False
        try:
            if cur is None:
                self.cur.close()
            else:
                cur.close()
        except (self.MODULE.Warning, self.MODULE.Error) as e:
            if force_no_exit:
                self.save_err_warn()
                self.err_no_exit = True
                self.warn_no_exit = True
            self.error_handler(
                e, 'close {0}cursor for'.format(main_str),
                'closing {0}cursor for'.format(main_str),
                core.exitvals['dbms_connect']['num']
            )
            if force_no_exit:
                self.restore_err_warn()
            if (isinstance(e, self.MODULE.Error) and
                  not self.err_warn_only):
                err = True
        if cur is None:
            self.cur = None
            if (self, None) in DBMS.open_cursors:
                DBMS.open_cursors.remove((self, None))
        else:
            cur = None
            if (self, cur) in DBMS.open_cursors:
                DBMS.open_cursors.remove((self, cur))
        if not err:
            core.status_logger.debug(
                '{0}{1} cursor (config prefix/delim {2})\n'
                'has been closed.' .
                format(main_str.capitalize(), self.DBMS_NAME, core.pps(pd))
            )

        return not err


    def execute(self, cur, query, *param):
        """
        Wrapper: execute a DBMS query.
        Returns False on error, otherwise True.
        Parameters:
            cur: the cursor to use; if None, the "main" cursor is used
            query/param: the query and its parameters
        Dependencies:
            instance vars: cur
            methods: wrap_call()
            modules: (cur's module)
        """
        cur = cur if cur else self.cur
        return self.wrap_call(cur.execute, 'execute query on',
                              'executing query on', query,
                              *param)[0]


#log status
#
#err vars in docs
#redo-config func
#
#exec, incl. cursor open, commit/rollback
#   'execute query on'
#fetch, incl. cursor close, incl. auto
#   'retrieve data from'
#change db
#get db list
#   run a get-database-list command
#   (may not be possible/straightforward for all DBMSes)
#      MySQL:
#        "SHOW DATABASES;"
#      PostgreSQL:
#        "SELECT datname FROM pg_catalog.pg_database;"
#
#warnings
#pooling
#dicts
#conversion, incl. unicode
#buffering?
#autocommit
#
#which package
