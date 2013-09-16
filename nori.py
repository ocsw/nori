#!/usr/bin/env python


"""
CONTENTS:
---------

    1) About and Requirements
    2) General Information
    3) Exit Values
    4) API Variables
    5) API Functions
    6) API Classes
    7) API Hooks
    8) Usage in Scripts
    9) Modification Notes


1) ABOUT AND REQUIREMENTS:
--------------------------

    This is the Nori library for wrapping scripts.  It provides tools
    such as powerful lockfile checking, logging, command-line
    processing, and config setting validation, and is particularly
    helpful for scripts that need to be run from cron with minimal
    intervention and maximal stability (although it can also be helpful
    in other cases.)

    It was originally factored out of the Aeolus backup script, then
    ported to Python; the original and the port are by Daniel Malament.

    The module requires Python 2.7/3.2, and will exit the script upon
    import (with an error message) if this requirement is not met.


2) GENERAL INFORMATION:
-----------------------

    For command-line usage information, run the module with '--help'.

    For config setting information, run the module with '-n create' or
    '-n createall'.

    For license information, run the module with 'license' or see the
    LICENSE file.

    These will also work by default in scripts that use this module, and
    will include script-specific changes.

    For more end-user information, see the USAGE file.


3) EXIT VALUES:
---------------

    0   = no error (e.g., run_every hasn't expired, or invocation was
          completed without errors)

    2   = error parsing the command line
    10  = problem with the script invocation, the config file, or a
          setting (also used in command modes like 'disable' as a
          generic error value)
    11  = previous lockfile still exists (possibly because the script
          was manually disabled)

    20  = error opening SSH tunnel

    250 = internal error; should never happen


4) API VARIABLES:
-----------------

    (Pseudo-)Constants:
    -------------------

    NO_ERROR_EXITVAL
    ARGPARSE_EXITVAL
    STARTUP_EXITVAL
    LOCKFILE_EXITVAL
    SSHTUNNEL_EXITVAL
    INTERNAL_EXITVAL
        exit values

    LF_ALERTS_SILENCED
    SCRIPT_DISABLED
        names of tempfiles stored in the lockfile directory

    FULL_DATE_FORMAT
        format for printing certain timestamps

    TASK_ARTICLE
    TASK_NAME
    TASKS_NAME
        what the script does

    SCRIPT_MODES
    SCRIPT_MODES_DESCR
        available script modes

    LICENSE
        license message

    PPS_INDENT
    PPS_WIDTH
    PPS_DEPTH
        pretty-printer settings

    NUMBER_TYPES
    STRING_TYPES
    STRINGISH_TYPES
    CONTAINER_TYPES
        type tuples

    PATH_SEP
        all path separator characters

    ZIP_SUFFIXES
        allowed suffixes for file rotation


    Resources:
    ----------

    status_logger
    alert_logger
    email_logger
    output_logger
        logger objects

    output_log_fo
        output file object


    Configuration and status:
    -------------------------

    script_name
        name of the script

    script_shortname
        name of the script without suffixes

    running_as_email
        user's local email address

    start_time
        starting timestamp

    supported_features
        dict of features supported by the module and its submodules

    available_features
        list of features actually available on the system

    config_file_header
        header for blank config files

    default_config_files
        default config-file path(s)

    config_file_paths
        paths to the user-supplied config file(s)

    config_modules
        module objects for the config file(s)

    cl_config
        names of config settings that were supplied on the command line

    cfg
        the config settings dictionary

    config_defaults_multiple
        config-setting defaults that are applied to more than one setting


    config_settings
        what config settings does this script accept?

    bogus_config
        non-existent settings that the end-user might set by accident


5) API FUNCTIONS:
-----------------

    Version check:
    -------------

    pyversion_check()
        Exit if we don't have a recent enough Python.


    Configuration and status:
    -------------------------

    config_settings_no_print_output_log()
        Turn self-documentation of the output log feature on or off.


    Variable and value manipulations:
    ---------------------------------

    char_name()
        Return the name of a character.

    type_list_string()
        Return a string containing the types listed in a tuple.

    scalar_to_tuple()
        If a value is a scalar (non-container), convert it to a tuple.

    re_repl_escape()
        Escape backreferences in a string, for the second arg of re.sub.

    str_to_bool()
        Convert a string representing a boolean to an actual boolean.


    File tests and path manipulations:
    ----------------------------------

    file_access_const()
        Return the os.*_OK constant that corresponds to a character.

    file_type_info()
        Return the stat.IS* function and name for a file type character.

    file_error_handler()
        Handle OSError/IOError exceptions with various options.

    check_file_type()
        Check if a file has the correct type.

    check_file_access()
        Check if a file is accessible.

    check_filedir_create()
        Check if we can create a file or directory.

    fix_path()
        Alter a file path, e.g. by expanding or rewriting.

    filemode()
        Reimplementation of Python 3.3's stat.filemode().

    get_file_metadata()
        Get a string with the metadata for a file.

    file_newer_than()
        Check if a file is less than num_min old.

    parentdir()
        Get the parent directory of a file or directory.

    open_create_only()
        Open a file, if and only if this causes it to be created.

    touch_file()
        Update a file's timestamp, or create it if it doesn't exist.

    rm_rf()
        Remove a file or directory, recursively if necessary.


    File rotation and pruning:
    --------------------------

    rotate_num_files()
        Rotate numbered files or directories.

    prune_num_files()
        Prune numbered files or directories by number and date.

    prune_date_files()
        Prune dated files or directories by number and date.

    prune_files()
        Wrapper: prune numbered or dated files/dirs by number and date.

    rotate_prune_output_logs()
        Rotate and prune the output logs.


    Logging and alerts:
    -------------------

    pps()
        Pretty-print a value and return it as a string.

    err_exit()
        Print a nicely-formatted message and exit.

    email_diagnostics()
      Return a diagnostic string suitable for alert/error emails.

    init_syslog()
        Set up a syslog handler and return it.

    init_logging_main()
        Initialize most of the logging.

    logging_stop_syslog()
        Turn off syslog in the loggers.

    logging_start_syslog()
        Turn on syslog in the loggers.

    logging_stop_stdouterr()
        Turn off stdout/stderr printing in the loggers.

    logging_start_stdouterr()
        Turn on stdout/stderr printing in the loggers.

    logging_email_stop_logging()
        Turn off propagation in the email logger (i.e., no actual
        logging).

    logging_email_start_logging()
        Turn on propagation in the email logger (i.e., actual logging).

    init_logging_output()
        Initialize output logging, including both logger and file
        objects.

    end_logging_output()
        Close the output log file object.

    run_with_logging()
        Run a command and log its output to the output log and stdout.


    Config setting checks and manipulations:
    ----------------------------------------

    setting_walk()
        Get the configuration (sub-)object indicated by setting_name.

    setting_is_set()
        Readability wrapper for setting_walk(): is a setting set?

    setting_is_unset()
        Readability wrapper for setting_walk(): is a setting unset?

    setting_check_is_set()
        If a config setting is not set, exit with an error.

    setting_check_one_is_set()
        At least one of a group of settings must be set, else
        error/exit.

    setting_check_type()
        If a config setting is not an allowed type, exit with an error.

    setting_check_not_empty()
        If a container-typed config setting is empty, exit with an
        error.

    setting_check_not_all_empty()
        At least one of a group of settings must be non-empty, else
        error/exit.

    setting_check_len()
        If a config setting has an invalid length, exit with an error.

    setting_check_not_blank()
        If a string-typed config setting is empty, exit with an error.

    setting_check_not_all_blank()
        At least one of a group of settings must be non-blank, else
        error/exit.

    setting_check_no_blanks()
        If a container config setting contains any blanks, error/exit.

    setting_check_no_char()
        If a config setting contains particular character(s),
        error/exit.

    setting_check_list()
        If a config setting's value is not in a list, exit with an
        error.

    setting_check_num()
        If a number-typed config setting is invalid, exit with an error.

    setting_check_file_type()
        If a file setting does not have the correct file type,
        error/exit.

    setting_check_file_access()
        If a file indicated by a setting is not accessible, error/exit.

    setting_check_file_read()
        Wrapper to check the case of a file we just need to read.

    setting_check_file_rw()
        Wrapper to check the case of a file we need to read and write.

    setting_check_dir_rwx()
        Wrapper: check a dir in which we need to create and/or rotate
        files.

    setting_check_filedir_create()
        If we won't be able to create a file or directory, error/exit.


    Status checks and modifications:
    --------------------------------

    lockfile_cleanup()
        Exit callback: clean up the lockfile.

    check_status()
        Check if the script proper should actually start running.

    render_status_messages()
        Return a string with status messages about the script.

    render_status_metadata()
        Return a string with metadata about lockfiles, semaphores, etc.

    render_status()
        Return the complete status string.

    silence_lf_alerts()
        Silence lockfile-exists alerts.

    unsilence_lf_alerts()
        Unsilence lockfile-exists alerts.

    disable_script()
        Disable the script.

    enable_script()
        (Re)-enable the script.

    clear_lockfile()
        Forcibly remove the lockfile directory.


    Startup and config file processing:
    -----------------------------------

    import_file()
        Import an arbitrary file as a module and add it to sys.modules.

    import_config_by_name()
        Import a config file (module).

    check_bogus_config()
        If there are non-existent settings set, exit with an error.

    apply_config_defaults()
        Apply defaults to the config settings, as necessary.

    apply_config_defaults_extra()
        Apply configuration defaults that are last-minute/complicated.

    validate_config()
        Validate the configuration settings.

    process_config()
        Process the config file and the settings supplied on the
        command line.

    render_config()
        Return a string containing the current config settings.

    log_cl_config()
        Log the config file paths, CWD, and settings given on the
        command line.

    create_blank_config_files()
        Create blank config files, or print blank config to stdout.

    create_arg_parser()
        Create and return the command-line-argument parser.

    license_mode()
        Print a license message to stderr.

    config_mode()
        Wrapper for render_config() to add blank lines.

    status_mode()
        Wrapper for render_status() to add blank lines.

    statusall_mode()
        Wrapper for render_status(True) to add blank lines.

    createfull_mode()
        Wrapper for create_blank_config_files(True).

    run_mode()
        Do the actual business of the script.

    process_command_line()
        Process the command-line arguments and do mode-dependent
        actions.


    Database calls and manipulations:
    ---------------------------------

    ###TODO


    Backups and file syncing:
    --------------------------

    ###TODO


6) API CLASSES:
---------------

    SMTPDiagHandler(logging.handlers.SMTPHandler)
        Override SMTPHandler to add diagnostics to the email.


7) API HOOKS:
-------------

    render_status_messages_hook()
        Change/add to status messages returned by
        render_status_messages().

    render_status_metadata_hook()
        Change/add to metadata returned by render_status_metadata().

    apply_config_defaults_hook()
        Override/add to last-minute defaults applied by
        apply_config_defaults().

    validate_config_hook()
        Add config-setting validations to validate_config().

    process_config_hook()
        Override/add to process_config() initializations.

    create_arg_parser_hook()
        Override/add to command-line parser returned by
        create_arg_parser().

    run_mode_hook()
        Supply a task for the script, as performed by run_mode().

    mode_callbacks_hook()
        Change/add to mode_callbacks dictionary used by
        process_command_line().


8) USAGE IN SCRIPTS:
--------------------

    (These are some pointers for using this module; however, there are
    many things left out.  See the comments and docstrings, below, for
    more information.)

    To use this module to wrap a task, the minimum setup that should be
    done is as follows:
        * redefine TASK_ARTICLE, TASK_NAME, and TASKS_NAME
        * redefine LICENSE
        * add to config_settings, as necessary, and define
          validate_config_hook()
        * define run_mode_hook()

    In most cases, these will also be necessary:
        * add more *_EXITVAL constants
        * redefine default_config_files
        * copy and edit/expand the USAGE file, replacing 'nori' with the
          name of the script

    To use the output log feature:
        * run config_settings_no_print_output_log(False)
        * set these (in most cases):
          config_settings['exec_path']['no_print'] = False
          config_settings['print_cmds']['no_print'] = False

    To add command-line modes:
        * add to / redefine SCRIPT_MODES and SCRIPT_MODES_DESCR
        * define mode_callbacks_hook()


9) MODIFICATION NOTES:
----------------------

    Settings:
    ---------

    Any change to the setting variables (additions, deletions, name
    changes, type changes, etc.) must be reflected in the following, as
    appropriate:
        config_settings, _config_settings_extra(), bogus_config,
        apply_config_defaults_extra(), and validate_config()


    Files:
    ------

    All files in the lockfile directory should have constants for their
    names, and be listed in render_status_metadata().


    Exit values:
    ------------

    The exit values must be kept in sync with the list in this
    docstring.

"""


########################################################################
#                             MAIN IMPORTS
########################################################################

from __future__ import print_function

import sys
import atexit
import os
import shutil
import socket
import errno
import getpass
import stat
import time
import logging
import logging.handlers
import copy
import subprocess
import re
import pprint
from pprint import pprint as pp  # for debugging
from types import *
import collections
import operator

if sys.hexversion < 0x03040000:
    import imp  # see import_file()

try:
    from StringIO import StringIO  # Python 2.x
except ImportError:
    from io import StringIO  # Python 3.x

try:
    import pwd  # Unix
except ImportError:
    pass

try:
    import grp  # Unix
except ImportError:
    pass

### see also deferred imports, after the version check ###


########################################################################
#                               VARIABLES
########################################################################

#####################
# (pseudo-)constants
#####################

#
# These can actually be redefined if necessary by scripts that use this
# library (before using them!), but most of them aren't ordinarily
# intended to be.  The ones that SHOULD be redefined are noted.
#

# exit values; see the module's docstring for details
# (when modifying: keep the numbers in sync with the docstring)
NO_ERROR_EXITVAL = 0
ARGPARSE_EXITVAL = 2  # hardcoded in the argparse module
STARTUP_EXITVAL = 10
LOCKFILE_EXITVAL = 11
SSHTUNNEL_EXITVAL = 20
INTERNAL_EXITVAL = 250

# names of tempfiles stored in the lockfile directory
LF_ALERTS_SILENCED = 'lf_alerts_silenced'
SCRIPT_DISABLED = 'script_disabled'

# for printing timestamps
FULL_DATE_FORMAT = '%a %b %d %H:%M:%S %Z %Y'

# what the script does, used in various messages;
# these SHOULD be changed by scripts that use this module
#   TASK_ARTICLE: the article to use with TASK_NAME, such as 'a' or
#                 'an'; this is used in messages like 'a backup is
#                 probably running'
#   TASK_NAME: a description of the script's purpose, such as 'backup';
#              this is used in messages like 'after the current backup
#              finishes'
#   TASKS_NAME: the plural of TASK_NAME, used in messages like 'backups
#               have been disabled'
TASK_ARTICLE = 'a'
TASK_NAME = 'script invocation'
TASKS_NAME = 'script invocations'

# available script modes; see create_arg_parser()
SCRIPT_MODES = ['license', 'config', 'settings', 'status', 'statusall',
                'silence', 'unsilence', 'stop', 'disable', 'start',
                'enable', 'clearlock', 'unlock', 'create', 'createfull',
                'run', ]
SCRIPT_MODES_DESCR = ('''
available modes:
  'license': a license message is printed

  'config' or 'settings': the current config settings are printed

  'status': the current status, including timestamps, is printed
  'statusall': temp files mainly relevant for debugging are also
  included (if applicable)

  'silence': alerts about the lockfile existing are silenced until
  either they are unsilenced, or the lockfile is no longer present

  'unsilence': alerts about the lockfile existing are re-enabled

  'stop' or 'disable': {2} are disabled until 'start' or 'enable'
  is used

  'start' or 'enable': {2} are re-enabled

  'clearlock' or 'unlock': the lockfile is forcibly removed; only use
  this if you're sure {0} {1} isn't currently running!

  'create': a config file template is printed (all settings, in logical
  order, commented out so that the default values will be used unless
  otherwise specified)

      If -f is given, the config file is output to the supplied path,
      but only if the file does not already exist.  If -n is given, the
      blank config is printed to stdout.  If neither -f nor -n is given,
      the default config file is used (see above).

      NOTE: the final component of the path given to -f cannot be a symlink,
      even if it points to a non-existent location.  Paths on NFS mounts may
      be problematic.

  'createfull': like 'create', but includes a description of each
  setting, as well as the default (if any)

  'run': run normally (the default)''' .
                     format(TASK_ARTICLE, TASK_NAME, TASKS_NAME))

# the license message; this constant is what is printed by the 'license'
# mode of the script, so it SHOULD be changed by scripts that use this
# module (the text below is the license for this library)
LICENSE = '''
Except as otherwise noted in the source code:

Copyright 2013 Daniel Malament.  All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN
NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# for pps() pretty-printer
PPS_INDENT = 1
PPS_WIDTH = 76
PPS_DEPTH = None

# see variable/value and config setting functions
if sys.hexversion < 0x03000000:
    NUMBER_TYPES = (int, float, long)  # not complex
    STRING_TYPES = (basestring, )  # tuple so we can add to it
    STRINGISH_TYPES = (basestring, bytearray, buffer)
    CONTAINER_TYPES = (list, tuple, xrange, set, frozenset, dict,
                       collections.ItemsView, collections.KeysView,
                       collections.ValuesView)
else:
    NUMBER_TYPES = (int, float)  # not complex
    STRING_TYPES = (str, )  # tuple so we can add to it
    STRINGISH_TYPES = (str, bytes, bytearray)
    CONTAINER_TYPES = (list, tuple, range, set, frozenset, dict,
                       collections.ItemsView, collections.KeysView,
                       collections.ValuesView)

# all path separator characters, to account for, e.g., Windows accepting
# both '/' and '\'; see validate_config()
PATH_SEP = os.sep + ('/' if os.name == 'nt' else '')

# internal, see file/path functions
# set third tuple value to False for lookup-only
# (i.e., use for going from character to tuple, but not the reverse)
_FILE_TYPE_FUNCS = {
    '-': (stat.S_ISREG, 'regular file', True),
    # f is non-standard, but clearer
    'f': (stat.S_ISREG, 'regular file', False),
    'd': (stat.S_ISDIR, 'directory', True),
    'l': (stat.S_ISLNK, 'symbolic link', True),
    'b': (stat.S_ISBLK, 'block device', True),
    'c': (stat.S_ISCHR, 'character device', True),
    'p': (stat.S_ISFIFO, 'named pipe (FIFO)', True),
    's': (stat.S_ISSOCK, 'socket', True),
}
if sys.hexversion >= 0x03040000:
    _FILE_TYPE_FUNCS += {
        'w': (stat.S_ISWHT, 'whiteout', True),
        'D': (stat.S_ISDOOR, 'door', True),
        'P': (stat.S_ISPORT, 'event port', True),
    }

# see file rotation functions
ZIP_SUFFIXES = ['.gz', '.bz2', '.lz', '.xz', ]


############
# resources
############

#
# These are listed here just for centralization purposes;
# they are intended to be constant once initialized.
#

# see logging functions
status_logger = None
alert_logger = None
email_logger = None
output_logger = None
output_log_fo = None

# internal, see logging functions
_syslog_handler = None
_stdout_handler = None
_stderr_handler = None


### see also the configuration section, below ###


########################################################################
#                             VERSION CHECK
########################################################################

def pyversion_check(two_ver, three_ver):

    """
    Exit if we don't have a recent enough Python.

    Parameters:
        two_ver: minimum version of Python 2.x (e.g., 7)
        three_ver: minimum version of Python 3.x (e.g., 2)

        If either is negative, don't allow 2.x/3.x.

    Dependencies:
        globals: INTERNAL_EXITVAL, STARTUP_EXITVAL
        modules: sys

    """

    # sanity check
    if two_ver < 0 and three_ver < 0:
        print('\nInternal Error: Python 2.x and 3.x are both '
              'disallowed; exiting.\n',
              file=sys.stderr)
        sys.exit(INTERNAL_EXITVAL)

    # build version string
    ver_string = '\nError: This script requires Python version '
    if two_ver >= 0:
        ver_string += '2.' + str(two_ver) + '+'
    if three_ver >= 0:
        if two_ver >= 0:
            ver_string += ' or '
        ver_string += '3.' + str(three_ver) + '+'
    else:
        ver_string += ' (not including 3.x)'
    ver_string += '; exiting.\n'

    # check all cases
    if (
        (sys.version_info[0] < 2)  # 0.x or 1.x
        or
        (two_ver < 0 and sys.version_info[0] == 2)  # 2.x not allowed
        or
        (two_ver >= 0 and sys.version_info[0] == 2 and
         sys.version_info[1] < two_ver)  # 2.x < two_ver
        or
        (three_ver < 0 and sys.version_info[0] == 3)  # 3.x not allowed
        or
        (three_ver >= 0 and sys.version_info[0] == 3 and
         sys.version_info[1] < three_ver)  # 3.x < three_ver
       ):
        print(ver_string, file=sys.stderr)
        sys.exit(STARTUP_EXITVAL)

# call with the minimums for the imports and code below
pyversion_check(7, 2)


########################################################################
#                           DEFERRED IMPORTS
########################################################################

####################
# version-dependent
####################

import collections  # OrderedDict requires 2.7/3.1
import argparse  # requires 2.7/3.2
import importlib  # requires 2.7/3.1


########################################################################
#                       CONFIGURATION AND STATUS
########################################################################

############
# variables
############

# get the name of the script from the invocation;
# this isn't 100% reliable, so it should really be (re)set
# by scripts that use this module
script_name = os.path.basename(sys.argv[0])

# remove .py, etc. from the script name for use in messages
# and filenames
script_shortname = re.sub('\.py.?$', '', script_name)

# get the user's local email address
# uses environment variables, so it's not totally safe;
# better to set the address explicitly whereever it's needed
# (e.g., don't use the default alert_emails_from/alert_emails_to
# settings)
running_as_email = getpass.getuser() + '@' + socket.getfqdn()

# starting timestamp (see run_mode(); listed here for centralization)
start_time = None

# dict of supported features
# format: 'feature_name': 'feature_description'
# see also available_features, below, and the section on submodules in
# the module docstring, above
supported_features = {}

# list of available features
# if a feature name is in the list, it is actually available on the
# system, not just supported by the module
# see also supported_features and the section on submodules in the
# module docstring, above
available_features = []

# used by create_blank_config_files()
config_file_header = ('# {0} config settings' .
                      format(script_shortname))
config_file_header = ('{0}\n{1}\n{0}\n' .
                      format('#' * (len(config_file_header) + 1),
                             config_file_header))

# default config-file path(s), in case none are specified;
# scripts that use this module way want to change this
default_config_files = ['/etc/{0}/{0}.conf'.format(script_shortname)]

# paths to the user-supplied config file(s), if any;
# see process_command_line()
config_file_paths = None

# module objects for the config file(s); see import_config_by_name()
config_modules = []

# names of config settings that were supplied on the command line;
# see process_config()
cl_config = []

# the config settings dict itself; see import_config_by_name()
cfg = {}

#
# config-setting defaults that are applied to more than one setting
#
# for example, you might have a timeout setting that applies to multiple
# database connections; you can centralize it here as something like
# config_defaults_multiple['database_timeout'] and then use it below, in
# config_settings
#
config_defaults_multiple = dict(
)

#
# what config settings does this script accept?
#
# (listed in logical order, which is preserved by using OrderedDict;
# see render_config())
#
# this is a dictionary; the keys are setting names, and the values
# are dictionaries containing these keys:
#
#   descr: a description of the setting, used by
#          create_blank_config_files(full=True) (with leading and
#          trailing whitespace removed); should be supplied for all
#          settings, but won't cause an error if omitted
#          note: this will have '# ' prepended to each line; format
#          accordingly
#
#   default: the default value of the setting, applied if it is unset;
#            can be omitted
#
#   default_descr: a string description of the default; if this is
#                  present, it will be used by
#                  create_blank_config_files(full=True)
#                  (with leading and trailing whitespace removed)
#                  in place of the actual default
#                  note: this will have '# Default: ' prepended to the
#                  first line, and '# ' to the rest; format accordingly
#
#   cl_coercer: a function that can take a value passed on the command
#               line (as a string) and generate a value for the config
#               setting (possibly raising a ValueError exception);
#               if omitted, the setting cannot be supplied on the
#               command line
#               notes:
#                 - conversion is safest with scalar (non-container)
#                   values, so this is usually str, int, etc.
#                 - see also str_to_bool(), which should be used for
#                   boolean values
#                 - to refer to functions that haven't been defined yet,
#                   use this trick: cl_coercer=lambda x: str_to_bool(x)
#
#   renderer: a function to use for printing the value of the setting;
#             if omitted, pps() is used
#
#   requires: a list of supported features that must be available if
#             this setting is set; see supported_features,
#             available_features, and the section on submodules in the
#             module docstring, above
#
#   no_print: if present and true, this setting will be omitted by
#             render_config() and create_blank_config_files();
#             this is especially useful for settings that don't apply
#             to a particular script, but need to be left in the code
#             so as not to break anything (for example, this is often
#             the case with output_log*, so those settings have this set
#             by default; see also
#             config_settings_no_print_output_log())
#
#   heading: if this is present, the element represents a section
#            heading for render_config() and
#            create_blank_config_files(), not an actual setting;
#            the value of this key is the heading string
#
config_settings = collections.OrderedDict()
# if we put the values in the constructor, they are added to kwargs and
# lose their order, so we have to be more verbose

config_settings['housekeeping_heading'] = dict(
    heading='Housekeeping',
)

config_settings['exec_path'] = dict(
    descr=(
"""
Search path for executables.

Typical safe value:
'/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin'

If unset, the system default will be used.
"""
    ),
    # no default
    cl_coercer=str,
    no_print=True,  # only needed w/ext cmds
)

config_settings['umask'] = dict(
    descr=(
"""
File-creation umask value.

Generally 077 (more secure, but less accessible), or 022 (more
accessible, but less secure; not necessarily a good idea); 077 is
strongly recommended.

If unset, the system default will be used.
"""
    ),
    # no default
    cl_coercer=lambda x: int(x, base=8),
    renderer=oct,
)

config_settings['print_cmds'] = dict(
    descr=(
"""
For important external commands, print the commands themselves?
Environment variables added to the commands are also printed, one per line.

For example:

    Running command:
    'ls' '-l' 'nori.py'
    with environment additions:
    A='B'
    PATH='/bin/:/usr/bin/'

Commands printed are script-dependent.

Can be True or False.
"""
    ),
    default=False,
    cl_coercer=lambda x: str_to_bool(x),
    no_print=True,
)

config_settings['debug'] = dict(
    descr=(
"""
Debug the script?

If True, messages of DEBUG priority and above are processed;
if False, only INFO or above.
"""
    ),
    default=False,
    cl_coercer=lambda x: str_to_bool(x),
)

config_settings['status_heading'] = dict(
    heading='Status checks',
)

config_settings['run_every'] = dict(
    descr=(
"""
How often to allow the script to run {0} {1}, in minutes.

The script is designed to be able run fairly frequently from cron (e.g.,
every hour) and to determine for itself when to actually perform
{0} {1}; this is so that {2} will eventually
be done even on systems that aren't always on.

Alternatively, if this is set to 0, no check will be performed, and
{0} {1} will be attempted every time the script is run.
Otherwise, {0} {1} will only be attempted if this amount
of time has passed since the last {1} was started
(see last_started_file, below).
""".format(TASK_ARTICLE, TASK_NAME, TASKS_NAME)
    ),
    default=0,
    cl_coercer=int,
)

config_settings['last_started_file'] = dict(
    descr=(
"""
Path to the last-started timestamp file.

The timestamp is updated when {0} {1} actually starts.

The script uses this for the run_every check, and it can also be used
by other scripts (e.g., to check if {2} haven't been run
for a while)

_Not_ ignored, even if run_every is 0.
""".format(TASK_ARTICLE, TASK_NAME, TASKS_NAME)
    ),
    default=('/var/log/' + script_shortname + '.started'),
    cl_coercer=str,
)

config_settings['lockfile'] = dict(
    descr=(
"""
Path to the lockfile.

(Actually a directory for technical reasons, and since we have it,
we can put temp files in it.)
"""
    ),
    default=('/var/run/' + script_shortname + '.lock'),
    cl_coercer=str,
)

config_settings['if_running'] = dict(
    descr=(
"""
If the script has passed the run_every check, but the previous
{0} is still running or was interrupted
(i.e., the lockfile is still present):

* It will send an alert to the alert_emails_to address(es).
* It will send further alerts every if_running minutes, unless
  if_running is 0 or the alerts are silenced.
  (run '{1} --help' for more information on silencing alerts)
* Either way, it will send an alert when it next successfully starts,
  so you know that the previous {0} finally finished, and the
  next one has begun.
""".format(TASK_NAME, script_name)
    ),
    default=120,
    default_descr=(
"""
120 (2 hours)
"""
    ),
    cl_coercer=int,
)

config_settings['lockfile_alert_file'] = dict(
    descr=(
"""
Path to the alert-timestamp file (used to track if_running).

_Not_ ignored, even if if_running is 0.
"""
    ),
    # default is cfg['lockfile'] + '.alert', applied at the last minute;
    # see apply_config_defaults_extra()
    default_descr=(
"""
cfg['lockfile'] + '.alert'
(e.g., if lockfile is set to '/var/run/{0}.lock', lockfile_alert_file
will default to '/var/run/{0}.lock.alert'
""".format(script_shortname)
    ),
    cl_coercer=str,
)

config_settings['logging_heading'] = dict(
    heading='Alerts and logging',
)

config_settings['send_alert_emails'] = dict(
    descr=(
"""
Send email for alerts/errors?  (True/False)
"""
    ),
    default=True,
    cl_coercer=lambda x: str_to_bool(x),
)

config_settings['alert_emails_from'] = dict(
    descr=(
"""
Address to send email alerts/errors from.

Ignored if send_alert_emails is False.
"""
    ),
    default=running_as_email,
    default_descr=(
"""
the local email address of the user running the script
(i.e., [user]@[hostname], where [user] is the current user and [hostname]
is the local hostname)
"""
    ),
    cl_coercer=str,
)

config_settings['alert_emails_to'] = dict(
    descr=(
"""
Where to send email alerts/errors.

This must be a list of strings (even if there is only one address).

Ignored if send_alert_emails is False.
"""
    ),
    default=[running_as_email],
    default_descr=(
"""
a list containing the local email address of the user running
the script (i.e., [user]@[hostname], where [user] is the current user
and [hostname] is the local hostname)
"""
    ),
)

config_settings['alert_emails_subject'] = dict(
    descr=(
"""
The subject line of alert/error emails.

Ignored if send_alert_emails is False.
"""
    ),
    default=(script_shortname + ' alert on ' + socket.getfqdn()),
    default_descr=(
"""
'{0} alert on [hostname]', where [hostname] is the local
hostname
""".format(script_shortname)
    ),
    cl_coercer=str,
)

config_settings['alert_emails_host'] = dict(
    descr=(
"""
The SMTP server via which email alerts will be sent.

This can be a string containing the hostname, or a tuple of the
hostname and the port number.

Ignored if send_alert_emails is False.
"""
    ),
    default='localhost',
)

config_settings['alert_emails_cred'] = dict(
    descr=(
"""
The credentials to be used with the alert_emails_host.

This can be None or a tuple containing the username and password.

Ignored if send_alert_emails is False.
"""
    ),
    default=None,
)

config_settings['alert_emails_sec'] = dict(
    descr=(
"""
The SSL/TLS options to be used with the alert_emails_host.

This can be None, () for plain SSL/TLS, a tuple containing only
the path to a key file, or a tuple containing the paths to the key
and certificate files.

Ignored if send_alert_emails is False.
"""
    ),
    default=None,
)

config_settings['quiet'] = dict(
    descr=(
"""
Suppress most printed output?

This includes all intentional output to stdout/stderr, including
warning and alert messages for known error conditions.

Setting this to True is the recommended mode for 'silent running' of
the script.

Can be True or False.
"""
    ),
    default=False,
    cl_coercer=lambda x: str_to_bool(x),
)

config_settings['use_syslog'] = dict(
    descr=(
"""
Log messages to syslog?

Can be True or False.
"""
    ),
    default=True,
    cl_coercer=lambda x: str_to_bool(x),
)

config_settings['syslog_addr'] = dict(
    descr=(
"""
Where to send syslog messages.

This can be a string containing the path to the syslog socket file, or
a tuple containing the hostname and port (usually 514; available as
logging.handlers.SYSLOG_UDP_PORT).

Ignored if use_syslog is False.
"""
    ),
    # see _config_settings_extra()
    default_descr=(
"""
if either '/dev/log' or '/var/run/syslog' works, it is used;
otherwise, ('localhost', logging.handlers.SYSLOG_UDP_PORT)
"""
    ),
)

config_settings['syslog_sock_type'] = dict(
    descr=(
"""
What kind of socket to use for syslog.

This can be socket.SOCK_DGRAM for UDP (the default), or
socket.SOCK_STREAM for TCP.

Ignored if use_syslog is False.
"""
    ),
    default=socket.SOCK_DGRAM,
    # see also _config_settings_extra()
    default_descr=(
"""
socket.SOCK_DGRAM, unless '/dev/log' or '/var/run/syslog' is
found, and is found to require socket.SOCK_STREAM
"""
    ),
)

config_settings['syslog_fac'] = dict(
    descr=(
"""
The syslog facility to use.

Allowed values:
    'auth' 'authpriv' 'cron' 'daemon' 'ftp' 'kern' 'lpr' 'mail' 'news'
    'syslog' 'user' 'uucp' 'local0' 'local1' 'local2' 'local3' 'local4'
    'local5' 'local6' 'local7'
and their corresponding numerical constants.

See the syslog and/or Python documentation (logging.handlers) for more
information.

Ignored if use_syslog is False.
"""
    ),
    default='daemon',
    cl_coercer=str,
)

config_settings['syslog_tag'] = dict(
    descr=(
"""
An identifier to add to each message logged to syslog.

This is typically the name of the script.

Ignored if use_syslog is False.
"""
    ),
    default=script_shortname,
    cl_coercer=str,
)

config_settings['status_log'] = dict(
    descr=(
"""
The path to the status log.

This gets a copy of all intentional script output except what goes in
the output log.  Messages are appended; this file is not rotated.

If set to None, no status log will be used.
"""
    ),
    default=('/var/log/' + script_shortname + '.log'),
    cl_coercer=str,
)

config_settings['output_log'] = dict(
    descr=(
"""
The path to the output log.

Depending on the script, this log gets a copy of the output of various
external commands, plus a few timestamps and diagnostics.

If output_log_layout is 'date', the filename will have output_log_sep and
a date string appended to it (see output_log_sep and output_log_date).

Output logs may be compressed in place by any utility that uses any of
the following suffixes, without disrupting the script:
{0}

If set to None, no output log will be used.
""".format(ZIP_SUFFIXES)
    ),
    default=('/var/log/' + script_shortname + '-output.log'),
    cl_coercer=str,
    no_print=True,
)

config_settings['output_log_layout'] = dict(
    descr=(
"""
The file layout to use for the output logs.

Available options:
    'append': append to a single file, with no rotation
    'number': log to numbered files (lower number = more recent, most
              recent has no number)
    'date': log to date-suffixed files (all suffixed, including the most
            recent; see output_log_date)

For example, if output_log is '{0}.log', output_log_layout is 'number',
and output_log_sep is '.', the second-most-recent file will be named
'{0}.log.1'.

Ignored if output_log is None.
""".format(script_name)
    ),
    default='number',
    cl_coercer=str,
    no_print=True,
)

config_settings['output_log_sep'] = dict(
    descr=(
"""
The separator to use before number/date suffixes in output log names.

This may not include path-separator characters ('{0}'; all directories
in the path must be in the output_log setting).  However, it may be more
than one character, or blank.

Ignored if output_log is None or output_log_layout is 'append'.
""".format(PATH_SEP)
    ),
    default='.',
    cl_coercer=str,
    no_print=True,
)

config_settings['output_log_date'] = dict(
    descr=(
"""
The date format string for output log names.

Recommended value: '%Y%m%d', or '%Y%m%d%H' if {0} are run
more than once a day.

(See http://docs.python.org/2/library/time.html#time.strftime
for the format of this value.)

Dates refer to when the script starts; all files created during a given
run of the script will have the same date suffix.

This may not include path-separator characters ('{1}'; all directories
in the path must be in the output_log setting).  However, it may be blank.

Ignored if output_log is None or output_log_layout is not 'date'.
""".format(TASKS_NAME, PATH_SEP)
    ),
    default='%Y%m%d',
    cl_coercer=str,
    no_print=True,
)

config_settings['output_log_num'] = dict(
    descr=(
"""
Number of output logs to keep, including the current one.

A value of 0 means no number limit (but there may still be a date limit;
see output_log_days).

Note: this applies to both 'number' and 'date' values of output_log_layout.

Ignored if output_log is None or output_log_layout is 'append'.
"""
    ),
    default=0,
    cl_coercer=int,
    no_print=True,
)

config_settings['output_log_days'] = dict(
    descr=(
"""
Days worth of output logs to keep.

A value of 0 means no days limit (but there may still be a number limit;
see output_log_num).

Logs this many days old or older are removed.

(Specifically, 1 day = a full 24 hours; if you run the script once a day,
and set output_log_days to 1, the log from the previous run will be newer
than 24 hours by however long the script took to run, and it will be saved.)

Note: this applies to both 'number' and 'date' values of output_log_layout.

Ignored if output_log is None or output_log_layout is 'append'.
"""
    ),
    default=14,
    cl_coercer=int,
    no_print=True,
)

#
# non-existent settings that the end-user might set by accident,
# e.g. because they are similar to other settings, or because
# they exist for some DBMSes and not others
#
# top-level settings are already handled, so this should contain only
# tuples matching sub-settings (e.g., ('alert_emails_sec', 3));
# see the note about setting_names in the config functions section
#
# see also check_bogus_config()
#
bogus_config = [
]


############
# functions
############

def _config_settings_extra():

    """
    Fix up config settings that are platform-dependent or complicated.

    In a function for namespace cleanliness; called immediately.

    Dependencies:
        globals: config_settings
        modules: os, stat, socket, errno, logging.handlers

    """

    ### syslog_addr, syslog_sock_type ###

    found_it = False

    if hasattr(socket, 'AF_UNIX'):
        for sock_path in ['/dev/log', '/var/run/syslog']:
            try:
                st_mode = os.stat(sock_path)[0]
            except OSError:
                continue
            if stat.S_ISSOCK(st_mode):
                try:
                    s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                    s.connect(sock_path)
                except IOError as e:
                    if e.errno == errno.EPROTOTYPE:
                        try:
                            s = socket.socket(socket.AF_UNIX,
                                              socket.SOCK_STREAM)
                            s.connect(sock_path)
                        except IOError:
                            continue
                         # looks like this needs to be SOCK_STREAM
                         # instead
                        config_settings['syslog_sock_type']['default'] = (
                            socket.SOCK_STREAM
                        )
                    continue
                s.close()
                found_it = True
                config_settings['syslog_addr']['default'] = sock_path
                break

    if not found_it:
        config_settings['syslog_addr']['default'] = (
            ('localhost', logging.handlers.SYSLOG_UDP_PORT)
        )

_config_settings_extra()


def config_settings_no_print_output_log(no_print):
    """
    Turn self-documentation of the output log feature on or off.
    Parameters:
        no_print: desired value of the no_print attribute of the
                  output_log* settings (see notes on config_settings,
                  above)
    Dependencies:
        globals: config_settings['output_log*']
    """
    config_settings['output_log']['no_print'] = no_print
    config_settings['output_log_layout']['no_print'] = no_print
    config_settings['output_log_sep']['no_print'] = no_print
    config_settings['output_log_date']['no_print'] = no_print
    config_settings['output_log_num']['no_print'] = no_print
    config_settings['output_log_days']['no_print'] = no_print


########################################################################
#                               FUNCTIONS
########################################################################


### see also the version check and configuration sections, above ###


###################################
# variable and value manipulations
###################################

def char_name(c):
    """
    Return the name of a character.
    Specifically, returns a descriptive name instead of whitespace.
    No type checking is done.
    Parameters:
        c: a string containing the character
    """
    cnames = {
        ' ': 'space',
        '\t': 'tab',
        '\n': 'newline',
        '\r': 'carriage return',
        '\f': 'formfeed',
        '\v': 'vertical tab',
        '\b': 'backspace',
        '\a': 'bell',
    }
    return cnames[c[0]] if c[0] in cnames else c[0]


def type_list_string(tt):
    """
    Return a string containing the types listed in a tuple.
    See *_TYPES, under constants.
    Parameters:
        tt: the tuple of types to stringify
    Dependencies:
        functions: pps()
    """
    return ' '.join(map(pps, tt))


def scalar_to_tuple(v):
    """
    If a value is a scalar (non-container), convert it to a tuple.
    Parameters:
        v: the value to check
    Dependencies:
        globals: CONTAINER_TYPES
    """
    return v if isinstance(v, CONTAINER_TYPES) else (v, )


def re_repl_escape(s):
    """
    Escape backreferences in a string, for the second arg of re.sub().
    Parameters:
        s: the string to escape
    Dependencies:
        modules: re
    """
    return re.sub(r'\\([1-9][0-9]?)', r'\\\\\1', s)


def str_to_bool(s):
    """
    Convert a string representing a boolean to an actual boolean.
    Allows multiple formats; intended for command-line processing.
    Raises a ValueError exception if the string cannot be parsed.
    Parameters:
        s: the string to convert
    """
    if s.lower() == 'true': return True
    if s.lower() == 'false': return False
    if s.lower() == 'on': return True
    if s.lower() == 'off': return False
    if s.lower() == 'yes': return True
    if s.lower() == 'no': return False
    if s == '1': return True
    if s == '0': return False
    raise ValueError


####################################
# file tests and path manipulations
####################################

def file_access_const(c):
    """
    Return the os.*_OK constant that corresponds to a character.
    If the character isn't recognized, returns None.
    Parameters:
        c: a string containing the character
    Dependencies:
        modules: os
    """
    a_char = {
        'f': os.F_OK,
        'r': os.R_OK,
        'w': os.W_OK,
        'x': os.X_OK,
    }
    if c[0] in a_char:  # add [0] in case a longer string is passed
        return a_char[c[0]]
    return None


def file_type_info(c):
    """
    Return the stat.IS* function and name for a file type character.
    If the character isn't recognized, or corresponds to a function
    that isn't available in the version of Python running the script,
    returns (None, None, None).
    Parameters:
        c: a string containing the character
    Dependencies:
        globals: _FILE_TYPE_FUNCS
      modules: stat
    """
    if c[0] in _FILE_TYPE_FUNCS:  # add [0] in case more is passed
        return _FILE_TYPE_FUNCS[c[0]]
    return (None, None, None)


def file_error_handler(e, verb, file_label, file_path, must_exist=True,
                       use_logger=False, warn_only=False,
                       exit_val=STARTUP_EXITVAL):

    """
    Handle OSError/IOError exceptions with various options.

    If it returns, returns False (but see must_exist, below).

    Parameters:
        e: the exception object
        verb: a string describing the action that failed (e.g., 'stat',
              'remove')
        file_label: a string describing the file the exception was
                    related to
        file_path: the path to the file/directory the exception was
                   related to
        must_exist: if false, and if the exception was because of a
                    non-existent file, the exception is ignored and the
                    function returns None
        use_logger: if None, no messages are logged/printed
                    if callable, is called with a message string and
                    warn_only
                    if true, the email logger is used
                    if false, messages are printed to stderr
        warn_only: if true, this is treated as a warning, not an error
                   (which changes the messages logged/printed and
                   prevents exiting the script)
        exit_val: the value to exit the script with; if this is None,
                  the function doesn't actually exit the script

    Dependencies:
        globals: email_logger, STARTUP_EXITVAL
        functions: pps(), err_exit()
        modules: sys, errno

    """

    # allowed to not exist?
    if (e.errno == errno.ENOENT) and (not must_exist):
        return None

    # warning/error
    if warn_only:
        warn_msg = ('Warning: could not {0} {1} ({2}).\n'
                    'Details: [Errno {3}] {4}' .
                     format(verb, file_label, pps(file_path), e.errno,
                            e.strerror))

        if use_logger is None:
            pass  # no messages
        elif callable(use_logger):
            use_logger(warn_msg, warn_only)
        elif use_logger:
            email_logger.warn(warn_msg)
        else:
            print('\n{0}\n'.format(warn_msg), file=sys.stderr)

        return False

    else:  # not warn_only
        err_msg = ('Error: could not {0} {1} ({2}); exiting.\n'
                   'Details: [Errno {3}] {4}' .
                   format(verb, file_label, pps(file_path), e.errno,
                          e.strerror))

        if use_logger is None:
            pass  # no messages
        elif callable(use_logger):
            use_logger(err_msg, warn_only)
        elif use_logger:
            email_logger.error(err_msg)
        else:
            err_exit(err_msg, exit_val)

        if exit_val is not None:
            sys.exit(exit_val)
        return False


def check_file_type(file_path, file_label, type_char='f', follow_links=True,
                    must_exist=True, use_logger=False, warn_only=False,
                    exit_val=STARTUP_EXITVAL):

    """
    Check if a file has the correct type.

    For purposes of this function, 'file' includes directories,
    symlinks, etc.

    Parameters:
        file_path: the path to the file to check
        type_char: a string containing characters corresponding to file
                   types (see _FILE_TYPE_FUNCS, under constants); if
                   this contains an illegal value, the script will exit
                   with an internal error
        follow_links: if true, the function will operate on the target
                      of a symlink, not the link itself
        must_exist: determines what happens if the file doesn't exist:
                    if true, it will be treated as an error
                    if false, it will be ignored (i.e., treated as a
                    success of the check)
        see file_error_handler() for the rest

    Dependencies:
        globals: email_logger, STARTUP_EXITVAL, INTERNAL_EXITVAL
        functions: fix_path(), file_error_handler(), file_type_info(),
                   pps(), err_exit()
        modules: os, stat, sys

    """

    # follow links?
    if follow_links:
        stat_func = os.stat
    else:
        stat_func = os.lstat

    # file exists / is accessible?
    try:
        st_mode = stat_func(fix_path(file_path))[0]
    except OSError as e:
        if file_error_handler(e, 'stat', file_label, file_path, must_exist,
                              use_logger, warn_only, exit_val) is None:
            return True

    # file type?
    for t_char in type_char:
        t_func, t_name, unused = file_type_info(t_char)
        if t_func is None:
            err_exit(
'''Internal Error: type_char contains an illegal value ({0})
in check_file_type(); call was (in expanded notation):


check_file_type(file_path={1}, file_label={2}, type_char={3},
                follow_links={4}, must_exist={5}, use_logger={6},
                warn_only={7}, exit_val={8})

Exiting.''' .
                     format(*map(pps, [t_char, file_path, file_label,
                                       type_char, follow_links, must_exist,
                                       use_logger, warn_only, exit_val])),
                     INTERNAL_EXITVAL
            )
        if t_func(st_mode):
            return True

    # try to give info while being clear
    # (to the user; the code, OTOH...)
    if warn_only:
        if len(type_char) == 1:
            warn_str = ('Warning: {0} ({1}) is not a {2}{3}.' .
                        format(file_label, pps(file_path), t_name,
                               ' or a symlink to one' if follow_links
                                                      else ''))
        else:
            warn_str = ('Warning: {0} ({1}) is not an allowed file type '
                        '({2}){3}.' .
                        format(file_label, pps(file_path), t_name,
                               '\nor a symlink to one' if follow_links
                                                       else ''))

        if use_logger is None:
            pass  # no messages
        elif callable(use_logger):
            use_logger(warn_str, warn_only)
        elif use_logger:
            email_logger.warn(warn_str)
        else:
            print('\n{0}\n'.format(warn_str), file=sys.stderr)

        return False

    else:  # not warn_only
        if len(type_char) == 1:
            err_str = ('Error: {0} ({1}) is not a {2}{3}; exiting.' .
                 format(file_label, pps(file_path), t_name,
                        ' or a symlink to one' if follow_links else ''))
        else:
            err_str = ('Error: {0} ({1}) is not an allowed file type '
                       '({2}){3}; exiting.' .
                       format(file_label, pps(file_path), t_name,
                              '\nor a symlink to one' if follow_links
                                                      else ''))

        if use_logger is None:
            pass  # no messages
        elif callable(use_logger):
            use_logger(err_str, warn_only)
        elif use_logger:
            email_logger.error(err_str)
        else:
            err_exit(err_str, exit_val)

        if exit_val is not None:
            sys.exit(exit_val)
        return False


def check_file_access(file_path, file_label, file_rwx='r', use_logger=False,
                      warn_only=False, exit_val=STARTUP_EXITVAL):

    """
    Check if a file is accessible.

    For purposes of this function, 'file' includes directories,
    symlinks, etc.

    If the file doesn't exist, the check will fail.

    Parameters:
        file_path: the path to the file to check
        file_rwx: a string containing characters indicating which types
                  of access to check: 'r' (read), 'w' (write), and/or
                  'x' (execute, or search if the file is a directory)
                  if blank, access is not checked; if this contains an
                  illegal value, the script will exit with an internal
                  error
        see file_error_handler() for the rest

    Dependencies:
        globals: email_logger, STARTUP_EXITVAL, INTERNAL_EXITVAL
        functions: fix_path(), file_access_const(),
                   file_error_handler(), pps(), err_exit()
        modules: os, sys

    """

    # check if the file doesn't exist, so we can say that instead of
    # multiple r/w/x failure messages;
    # while we're at it, remove any other 'f's that might have been in
    # file_rwx
    file_rwx = 'f' + file_rwx.replace('f', '')

    # file existence / access?
    for a_char in file_rwx:
        # os.*_OK constant
        a_const = file_access_const(a_char)
        if a_const is None:
            err_exit(
'''Internal Error: file_rwx contains an illegal value ({0})
in check_file_access(); call was (in expanded notation):


check_file_access(file_path={1}, file_label={2}, file_rwx={3},
                  use_logger={4}, warn_only={5}, exit_val={6})

Exiting.''' .
                     format(*map(pps, [a_char, file_path, file_label,
                                       file_rwx, use_logger, warn_only,
                                       exit_val])),
                     INTERNAL_EXITVAL
            )

        # check access
        try:
            access_ret = os.access(fix_path(file_path), a_const)
        except (OSError, IOError) as e:
            # the documentation doesn't really say anything about
            # exceptions, and I can't produce one, but I've seen
            # examples online, so...
            # (must_exist=True)
            if (file_error_handler(e, 'check access to', file_label,
                                   file_path, True, use_logger, warn_only,
                                   exit_val)
                  is None):
                return False

        # each failure is different
        if not access_ret:
            # doesn't exist?
            if a_char == 'f':
                if warn_only:
                    warn_msg = ('Warning: {0} ({1}) does not exist.' .
                                format(file_label, pps(file_path)))

                    if use_logger is None:
                        pass  # no messages
                    elif callable(use_logger):
                        use_logger(warn_msg, warn_only)
                    elif use_logger:
                        email_logger.warn(warn_msg)
                    else:
                        print('\n{0}\n'.format(warn_msg), file=sys.stderr)

                    return False

                else:  # not warn_only
                    err_msg = ('Error: {0} ({1}) does not exist; exiting.' .
                     format(file_label, pps(file_path)))

                    if use_logger is None:
                        pass  # no messages
                    elif callable(use_logger):
                        use_logger(err_msg, warn_only)
                    elif use_logger:
                        email_logger.error(err_msg)
                    else:
                        err_exit(err_msg, exit_val)

                    if exit_val is not None:
                        sys.exit(exit_val)
                    return False

            # r/w/x strings
            err_word = {
                'r': 'readable',
                'w': 'writable',
                'x': 'executable',
            }
            if a_char == 'x' and os.path.isdir(fix_path(file_path)):
                err_word['x'] = 'searchable'

            # r/w/x messages
            if warn_only:
                warn_msg = ('Warning: {0} ({1}) is not {2}.' .
                            format(file_label, pps(file_path),
                                   err_word[a_char]))

                if use_logger is None:
                    pass  # no messages
                elif callable(use_logger):
                    use_logger(warn_msg, warn_only)
                elif use_logger:
                    email_logger.warn(warn_msg)
                else:
                    print('\n{0}\n'.format(warn_msg), file=sys.stderr)

                return False

            else:  # not warn_only
                err_msg = ('Error: {0} ({1}) is not {2}; exiting.' .
                           format(file_label, pps(file_path),
                                  err_word[a_char]))

                if use_logger is None:
                    pass  # no messages
                elif callable(use_logger):
                    use_logger(err_msg, warn_only)
                elif use_logger:
                    email_logger.error(err_msg)
                else:
                    err_exit(err_msg, exit_val)

                if exit_val is not None:
                    sys.exit(exit_val)
                return False

    # success
    return True


def check_filedir_create(file_path, file_label, create_type='f',
                         need_rotation=False, use_logger=False,
                         warn_only=False, exit_val=STARTUP_EXITVAL):

    """
    Check if we can create a file or directory.

    Specifically: this is for files/directories we're going to be
    touching, writing to, creating, and/or rotating (but not necessarily
    reading), such as output logs.

    If the file/directory exists, then:
        - If create_type is 'f', it must be a file or a symlink to one,
          and it must be writable.
        - If create_type is 'd', it must be a directory or a symlink to
          one and it must be writable and searchable (for creating
          files).
    Regardless, the parent directory must exist, be a directory or a
    symlink to one, and be writable and searchable; if need_rotation
    is true, it must also be readable.

    Parameters:
        file_path: the path to the file/directory to check
        create_type: what we want to be able to create: 'f' (file) or
                     'd' (directory); if this contains an illegal value,
                     the script will exit with an internal error
        need_rotation: if true, the parent directory of file_path must
                       be readable (see above)
        see file_error_handler() for the rest

    Dependencies:
        globals: INTERNAL_EXITVAL
        functions: fix_path(), check_file_type(), check_file_access(),
                   parentdir(), pps()
        modules: os

    """

    # sanity check
    if create_type != 'f' and create_type != 'd':
        err_exit(
'''Internal Error: create_type contains an illegal value ({0})
in check_filedir_create(); call was (in expanded notation):

check_filedir_create(file_path={1}, file_label={2}, create_type={3},
                     need_rotation={4}, use_logger={5}, warn_only={6},
                     exit_val={7})

Exiting.''' .
                 format(*map(pps, [create_type, file_path, file_label,
                                   create_type, need_rotation, use_logger,
                                   warn_only, exit_val])),
                 INTERNAL_EXITVAL
        )

    # file/directory type and access
    if os.path.exists(fix_path(file_path)):
        t = check_file_type(file_path, file_label, create_type,
                            follow_links=True, must_exist=False,
                            use_logger=use_logger, warn_only=warn_only,
                            exit_val=exit_val)
        if not t:
            return t
        a = check_file_access(file_path, file_label,
                              'w' if create_type == 'f' else 'wx',
                              use_logger, warn_only, exit_val)
        if not a:
            return a

    # parent directory type and access
    p_dir = parentdir(file_path)
    t = check_file_type(p_dir, file_label + "'s parent directory", 'd',
                        follow_links=True, must_exist=True,
                        use_logger=use_logger, warn_only=warn_only,
                        exit_val=exit_val)

    if not t:
        return t
    a = check_file_access(p_dir, file_label + "'s parent directory",
                          'rwx' if need_rotation else 'wx',
                          use_logger, warn_only, exit_val)
    if not a:
        return a

    # success
    return True


def fix_path(p):
    """
    Alter a file path, e.g. by expanding or rewriting.
    Currently, only does ~-expansion, but can be overridden to do
    virtually anything, such as invisibly rewriting all file accesses
    to a different base directory or mount point (although that's a bad
    idea, of course).
    Wrap the parameters of all calls to open(), os.*(), etc. in this
    function unless you're sure it's not necessary.
    Parameters:
        p: the path to fix
    Dependencies:
        modules: os
    """
    return os.path.expanduser(p)


def filemode(mode):

    """
    Reimplementation of Python 3.3's stat.filemode().

    (Use that instead if available.)

    Parameters:
        mode: mode value from os.stat(), os.fstat(), or os.lstat()

    Dependencies:
        globals: _FILE_TYPE_FUNCS
        modules: stat

    """

    mode_chars = []

    # get the file type character
    mode_chars.append('?')
    for c, t in _FILE_TYPE_FUNCS.items():
        if not t[2]:  # skip lookup-only values
            continue
        if t[0](mode):
            mode_chars[0] = c
            break

    # get the mode characters
    mode_chars.append('r' if mode & stat.S_IRUSR else '-')
    mode_chars.append('w' if mode & stat.S_IWUSR else '-')
    mode_chars.append('x' if mode & stat.S_IXUSR else '-')
    mode_chars.append('r' if mode & stat.S_IRGRP else '-')
    mode_chars.append('w' if mode & stat.S_IWGRP else '-')
    mode_chars.append('x' if mode & stat.S_IXGRP else '-')
    mode_chars.append('r' if mode & stat.S_IROTH else '-')
    mode_chars.append('w' if mode & stat.S_IWOTH else '-')
    mode_chars.append('x' if mode & stat.S_IXOTH else '-')
    if mode & stat.S_ISUID:
        mode_chars[3] = 's' if mode & stat.S_IXUSR else 'S'
    if mode & stat.S_ISGID:
        mode_chars[6] = 's' if mode & stat.S_IXGRP else 'S'
    if mode & stat.S_ISVTX:
        mode_chars[9] = 't' if mode & stat.S_IXGRP else 'T'

    return ''.join(mode_chars)


def get_file_metadata(file_path, if_noent=None):

    """
    Get a string with the metadata for a file.

    For purposes of this function, 'file' includes directories,
    symlinks, etc.

    Format is similar to 'ls -l':
        mode links owner group size mtime name

    Does not follow symlinks.

    Returns if_noent if the file doesn't exist; may raise an OSError for
    other error conditions.

    Parameters:
        file_path: path to the file
        if_noent: value to return if the file doesn't exist

    Dependencies:
        functions: fix_path(), filemode() [if Python <3.3]
        modules: os, errno, sys, pwd [optional], grp [optional], time
        Python: 3.3 for stat.filemode() [optional]

    """

    # get metadata
    try:
        (st_mode, unused, unused, st_nlink, st_uid,
         st_gid, st_size, unused, st_mtime, unused) = (
            os.lstat(fix_path(file_path)))
    except OSError as e:
        if e.errno == errno.ENOENT:
            return '(none)'
        else:
            raise

    # get mode string
    if sys.hexversion >= 0x03030000:
        st_mode_str = stat.filemode(st_mode)
    else:
        st_mode_str = filemode(st_mode)

    # get username from uid
    if 'pwd' in sys.modules:
        st_uid_str = pwd.getpwuid(st_uid)[0]
    else:
        st_uid_str = str(st_uid)

    # get group name from gid
    if 'grp' in sys.modules:
        st_gid_str = grp.getgrgid(st_gid)[0]
    else:
        st_gid_str = str(st_gid)

    # size string; size doesn't really make sense for all file types
    if st_mode_str[0] in ['-', 'f', 'd', 'l']:
        st_size_str = str(st_size)
    else:
        st_size_str = '-'

    # get date string
    if (time.time() - st_mtime) > (60 * 60 * 24 * 182.5):  # 6 months
        st_mtime_str = time.strftime('%b %d %Y', time.localtime(st_mtime))
    else:
        st_mtime_str = time.strftime('%b %d %H:%M',
                                     time.localtime(st_mtime))

    # join what we have so far
    metadata_str = ' '.join([st_mode_str, str(st_nlink), st_uid_str,
                             st_gid_str, st_size_str, st_mtime_str,
                             file_path])

    # if it's a link, get the target
    if st_mode_str[0] == 'l':
        metadata_str += ' -> ' + os.readlink(fix_path(file_path))

    return metadata_str


def file_newer_than(file_path, num_min):
    """
    Check if a file is less than num_min old.
    May raise an OSError.
    Parameters:
        file_path: path to the file
        num_min: number of minutes; can be a float
    Dependencies:
        functions: fix_path()
        modules: os, time
    """
    st_mtime = os.stat(fix_path(file_path))[8]
    return ((time.time() - st_mtime) < (num_min * 60))


def parentdir(file_path):

    """
    Get the parent directory of a file or directory.

    Goes by the path alone, so it doesn't follow symlinks.

    This function is not the same as os.path.dirname(); for example,
    dirname will not give us the correct answer for any of:
        . ./ .. ../

    Note: still doesn't always correctly handle paths starting with /
    and containing . or .., e.g., parentdir('/foo/..')

    Dependencies:
        modules: re

    """

    # remove trailing /'s
    parentdir = re.sub('/*$', '', file_path)

    # are there no /'s left?
    if parentdir.find('/') == -1:
        if parentdir == '':
            return '/'  # it was /, and / is its own parent
        if parentdir == '.':
            return '..'
        if parentdir == '..':
            return '../..'
        return '.'

    # remove the last component of the path
    parentdir = re.sub('/*[^/]*$', '', parentdir)
    if parentdir == '':
        return '/'

    return parentdir

#print(parentdir('//'))                   # /
#print(parentdir('//foo'))                # /
#print(parentdir('//foo//'))              # /
#print(parentdir('//foo//bar'))           # //foo
#print(parentdir('//foo//bar//'))         # //foo
#print(parentdir('//foo//bar//baz'))      # //foo//bar
#print(parentdir('//foo//bar//baz//'))    # //foo//bar
#print(parentdir('.'))                    # ..
#print(parentdir('.//'))                  # ..
#print(parentdir('.//foo'))               # .
#print(parentdir('.//foo//'))             # .
#print(parentdir('.//foo//bar'))          # .//foo
#print(parentdir('.//foo//bar//'))        # .//foo
#print(parentdir('.//foo//bar//baz'))     # .//foo//bar
#print(parentdir('.//foo//bar//baz//'))   # .//foo//bar
#print(parentdir('..'))                   # ../..
#print(parentdir('..//'))                 # ../..
#print(parentdir('..//foo'))              # ..
#print(parentdir('..//foo//'))            # ..
#print(parentdir('..//foo//bar'))         # ..//foo
#print(parentdir('..//foo//bar//'))       # ..//foo
#print(parentdir('..//foo//bar//baz'))    # ..//foo//bar
#print(parentdir('..//foo//bar//baz//'))  # ..//foo//bar
#print(parentdir('foo'))                  # .
#print(parentdir('foo//'))                # .
#print(parentdir('foo//bar'))             # foo
#print(parentdir('foo//bar//'))           # foo
#print(parentdir('foo//bar//baz'))        # foo//bar
#print(parentdir('foo//bar//baz//'))      # foo//bar


def open_create_only(file_path):
    """
    Open a file, if and only if this causes it to be created.
    The final component of the path may not be a symlink, even if it
    points to a non-existent location.
    Paths on NFS mounts may cause problems; see the documentation for
    the open() function in your system libraries.  Specifially, the
    Linux man page says that this is only supported with NFSv3+ and
    kernel 2.6+, and that there is a race condition otherwise.  (The
    race condition may or may not be a big deal, depending on the
    context.)
    May raise an OSError exception.
    Parameters:
        file_path: the path to the file to create; see above
    Dependencies:
        functions: fix_path()
        modules: os
    """
    # use os.open() to avoid a race condition
    return os.fdopen(os.open(fix_path(file_path),
                             os.O_CREAT | os.O_EXCL | os.O_RDWR),
                     'a+')


def touch_file(file_path, file_label, times=None, use_logger=False,
               warn_only=False, exit_val=STARTUP_EXITVAL):
    """
    Update a file's timestamp, or create it if it doesn't exist.
    Also works on existing directories.
    Parameters:
        file_path: the file to touch
        see file_error_handler() for the rest
    Dependencies:
        globals: STARTUP_EXITVAL
        functions: fix_path(), file_error_handler()
        modules: sys, os
    """
    try:
        if sys.hexversion >= 0x03030000:
            with os.open(fix_path(file_path), os.O_APPEND) as f:
                os.utime(f.fileno() if os.utime in os.supports_fd
                                    else fix_path(file_path),
                         times)
        elif os.path.isdir(file_path):
            # minor race condition here
            os.utime(fix_path(file_path), times)
        else:
            with open(fix_path(file_path), 'a'):
                # minor race condition here
                os.utime(fix_path(file_path), times)
    except OSError as e:
        # must_exist=True
        file_error_handler(e, 'touch', file_label, file_path, True,
                           use_logger, warn_only, exit_val)


def rm_rf(rm_path, file_label, must_exist=False, use_logger=False,
          warn_only=False, exit_val=STARTUP_EXITVAL):
    """
    Remove a file or directory, recursively if necessary.
    Parameters:
        rm_path: the file/directory to remove
        see file_error_handler() for the rest
    Dependencies:
        functions: fix_path(), file_error_handler()
        modules: os, shutil
    """
    if os.path.isdir(fix_path(rm_path)):
        try:
            shutil.rmtree(os.path.realpath(fix_path(rm_path)), False)
        except OSError as e:
            file_error_handler(e, 'remove', file_label, rm_path, must_exist,
                               use_logger, warn_only, exit_val)
    else:
        try:
            os.unlink(fix_path(rm_path))
        except OSError as e:
            file_error_handler(e, 'remove', file_label, rm_path, must_exist,
                               use_logger, warn_only, exit_val)


############################
# file rotation and pruning
############################

def rotate_num_files(dir_path, prefix, sep, suffix,
                     exit_val=STARTUP_EXITVAL):

    """
    Rotate numbered files or directories.

    Files/directories can optionally have any of the suffixes in
    ZIP_SUFFIXES following the suffix parameter.

    Parameters:
        dir_path: the directory containing the files/directories to
                  rotate
        prefix: file/directory name up to the number, not including any
                trailing separator
        sep: separator before the number (not in prefix because the most
             recent file won't have a separator or a number)
        suffix: suffix after the number, including any leading
                separator; cannot begin with a number
        exit_val: value to exit the script with on error

    Dependencies:
        globals: email_logger, STARTUP_EXITVAL, ZIP_SUFFIXES
        functions: fix_path(), pps()
        modules: re, os, operator, sys

    """

    # get a list of matching files in dir_path, along with their
    # file numbers, sorted in reverse numerical order
    f_list = []
    r = re.compile('^' +
                   re.escape(prefix + sep) + '([0-9]+)' +
                   re.escape(suffix) +
                   '(|' + '|'.join(map(re.escape, ZIP_SUFFIXES)) + ')' +
                   '$')
    try:
        for f in os.listdir(fix_path(dir_path)):
            res = r.search(f)
            if res:
                f_list.append((f, int(res.group(1))))
    except OSError as e:
        email_logger.error('Error: could not list directory {0}; exiting.\n'
                           'Details: [Errno {1}] {2}' .
                           format(pps(dir_path), e.errno, e.strerror))
        sys.exit(exit_val)
    f_list.sort(None, operator.itemgetter(1), True)

    # move to the new numbers
    for ft in f_list:
        new_name = re.sub('^' + re.escape(prefix + sep) + '([0-9]+)',
                          re_repl_escape(prefix + sep) + str(ft[1] + 1),
                          ft[0])
        try:
            os.rename(fix_path(os.path.join(dir_path, ft[0])), new_name)
        except OSError as e:
            email_logger.error('Error: could not rename file/directory '
                               '({0} -> {1});\nexiting.\n'
                               'Details: [Errno {1}] {2}' .
                               format(pps(os.path.join(dir_path, ft[0])),
                                      pps(new_name), e.errno, e.strerror))
            sys.exit(exit_val)

    # handle the most recent file (no separator or number)
    f_list = []
    r = re.compile('^' +
                   re.escape(prefix + suffix) +
                   '(|' + '|'.join(map(re.escape, ZIP_SUFFIXES)) + ')' +
                   '$')
    try:
        f_list = [f for f in os.listdir(fix_path(dir_path))
                    if r.search(f)]
    except OSError as e:
        email_logger.error('Error: could not list directory {0}; exiting.\n'
                           'Details: [Errno {1}] {2}' .
                           format(pps(dir_path), e.errno, e.strerror))
        sys.exit(exit_val)
    for f in f_list:
        new_name = re.sub('^' + re.escape(prefix + suffix),
                          re_repl_escape(prefix + sep + '1' + suffix),
                          f)
        try:
            os.rename(fix_path(os.path.join(dir_path, f)), new_name)
        except OSError as e:
            email_logger.error('Error: could not rename file/directory '
                               '({0} -> {1});\nexiting.\n'
                               'Details: [Errno {1}] {2}' .
                               format(pps(os.path.join(dir_path, f)),
                                      pps(new_name), e.errno, e.strerror))
            sys.exit(exit_val)


def prune_num_files(dir_path, prefix, sep, suffix, num_f, days_f,
                    exit_val=STARTUP_EXITVAL):

    """
    Prune numbered files or directories by number and date.

    Files/directories can optionally have any of the suffixes in
    ZIP_SUFFIXES
    following the suffix parameter.

    Parameters:
        dir_path: the directory containing the files/directories to
                  rotate
        prefix: file/directory name up to the number, not including any
                trailing separator
        sep: separator before the number (not in prefix because the most
             recent file won't have a separator or a number)
        suffix: suffix after the number, including any leading
                separator; cannot begin with a number
        num_f: number of files to keep, including the current
               (un-numbered) one; 0 = unlimited
        days_f: number of days worth of files to keep; 0 = unlimited
        exit_val: value to exit the script with on error

    Dependencies:
        globals: email_logger, STARTUP_EXITVAL, ZIP_SUFFIXES
        functions: fix_path(), pps(), file_newer_than(), rm_rf()
        modules: re, os, sys

    """

    # anything to do?
    if not num_f and not days_f:
        return

    # get a list of matching files in dir_path, along with their
    # file numbers
    f_list = []
    r = re.compile('^' +
                   re.escape(prefix + sep) + '([0-9]+)' +
                   re.escape(suffix) +
                   '(|' + '|'.join(map(re.escape, ZIP_SUFFIXES)) + ')' +
                   '$')
    try:
        for f in os.listdir(fix_path(dir_path)):
            res = r.search(f)
            if res:
                f_list.append((f, int(res.group(1))))
    except OSError as e:
        email_logger.error('Error: could not list directory {0}; exiting.\n'
                           'Details: [Errno {1}] {2}' .
                           format(pps(dir_path), e.errno, e.strerror))
        sys.exit(exit_val)

    # delete files
    for ft in f_list:
        # by number
        if num_f and (ft[1] >= num_f):
            rm_rf(os.path.join(dir_path, ft[0]), 'file/directory',
                  must_exist=False, use_logger=True, warn_only=False,
                  exit_val=exit_val)
            continue

    # by date
        if days_f:
            try:
                # 1440 = min per day
                nt = file_newer_than(os.path.join(dir_path, ft[0]),
                                     (days_f * 1440))
            except OSError as e:
                email_logger.error('Error: could not stat file/directory '
                                   '{0}; exiting.\n'
                                   'Details: [Errno {1}] {2}' .
                                   format(pps(os.path.join(dir_path,
                                                           ft[0])),
                                          e.errno, e.strerror))
                sys.exit(exit_val)
            if not nt:
                rm_rf(os.path.join(dir_path, ft[0]), 'file/directory',
                      must_exist=False, use_logger=True, warn_only=False,
                      exit_val=exit_val)


def prune_date_files(dir_path, prefix, sep, suffix, num_f, days_f,
                     exit_val=STARTUP_EXITVAL):

    """
    Prune dated files or directories by number and date.

    Files/directories can optionally have any of the suffixes in
    ZIP_SUFFIXES following the suffix parameter.

    Note: the 'current' file must exist before calling this function, so
    that it can be counted.

    Also, because we can't make any assumptions about the format of the
    date string, this function can be over-broad in the files it looks
    at; make sure there are no files that match
    ^[prefix][sep].*[suffix][zip]?$
    except for the desired ones.

    Parameters:
        dir_path: the directory containing the files/directories to
                  rotate
        prefix: file/directory name up to the date, not including any
                trailing separator
        sep: separator before the date
        suffix: suffix after the date, including any leading separator
        num_f: number of files to keep, including the current one;
               0 = unlimited
        days_f: number of days worth of files to keep; 0 = unlimited
        exit_val: value to exit the script with on error

    Dependencies:
        globals: email_logger, STARTUP_EXITVAL, ZIP_SUFFIXES
        functions: fix_path(), pps(), rm_rf()
        modules: re, os, time, operator, sys

    """

    # anything to do?
    if not num_f and not days_f:
        return

    # get a list of matching files in dir_path
    f_list = []
    r = re.compile('^' +
                   re.escape(prefix + sep) + '.*' + re.escape(suffix) +
                   '(|' + '|'.join(map(re.escape, ZIP_SUFFIXES)) + ')' +
                   '$')
    try:
        f_list = [(f, 0) for f in os.listdir(fix_path(dir_path))
                         if r.search(f)]
    except OSError as e:
        email_logger.error('Error: could not list directory {0}; exiting.\n'
                           'Details: [Errno {1}] {2}' .
                           format(pps(dir_path), e.errno, e.strerror))
        sys.exit(exit_val)

    # stat the files, get dates
    f_remain = []
    for ft in f_list:
        try:
            st_mtime = os.stat(fix_path(os.path.join(dir_path, ft[0])))[8]
        except OSError as e:
            email_logger.error('Error: could not stat file/directory {0}; '
                               'exiting.\nDetails: [Errno {1}] {2}' .
                               format(pps(os.path.join(dir_path, ft[0])),
                                      e.errno, e.strerror))
            sys.exit(exit_val)
        # delete by date
        if ((time.time() - st_mtime) >= (days_f * 86400)):  # secs/day
            rm_rf(os.path.join(dir_path, ft[0]), 'file/directory',
                  must_exist=False, use_logger=True, warn_only=False,
                  exit_val=exit_val)
        else:
            f_remain.append(ft)

    # delete by number
    f_remain.sort(None, operator.itemgetter(1), False)
    for i, ft in enumerate(f_remain):
        if i >= num_f:
            rm_rf(os.path.join(dir_path, ft[0]), 'file/directory',
                  must_exist=False, use_logger=True, warn_only=False,
                  exit_val=exit_val)


def prune_files(layout, dir_path, prefix, sep, suffix, num_f, days_f,
                exit_val=STARTUP_EXITVAL):
    """
    Wrapper: prune numbered or dated files/dirs by number and date.
    Files/directories can optionally have any of the suffixes in
    ZIP_SUFFIXES following the suffix parameter.
    Parameters:
        layout: the layout type (see below)
        see prune_num_files() and prune_days_files() for the rest
    Dependencies:
        functions: prune_num_files(), prune_days_files()
    """
    if layout == 'single' or layout == 'singledir' or layout == 'append':
        # not generally called for these, but here for future use / FTR
        pass  # nothing to do
    elif layout == 'number' or layout == 'numberdir':
        prune_num_files(dir_path, prefix, sep, suffix, num_f, days_f,
                        exit_val)
    elif layout == 'date' or layout == 'datedir':
        prune_date_files(dir_path, prefix, sep, suffix, num_f, days_f,
                         exit_val)


def rotate_prune_output_logs():

    """
    Rotate and prune the output logs.

    Files can optionally have any of the suffixes in ZIP_SUFFIXES
    following the suffix parameter.

    Dependencies:
        config settings: output_log, output_log_layout, output_log_sep,
                         output_log_num, output_log_days
        globals: cfg, status_logger, STARTUP_EXITVAL
        functions: rotate_num_files, prune_files(), parentdir()

    """

    # no logs?
    if not cfg['output_log']:
        status_logger.info('Output logging is off; not rotating logs.')
        return

    # appending to one log?
    if cfg['output_log_layout'] == 'append':
        status_logger.info('Output logs are being appended to a single '
                           'file; not rotating logs.')
        return

    status_logger.info('Rotating logs...')

    # rotate
    if cfg['output_log_layout'] == 'number':
        rotate_num_files(parentdir(cfg['output_log']), cfg['output_log'],
                         cfg['output_log_sep'], '', STARTUP_EXITVAL)

    # prune
    prune_files(cfg['output_log_layout'], parentdir(cfg['output_log']),
                cfg['output_log'], cfg['output_log_sep'], '',
                cfg['output_log_num'], cfg['output_log_days'],
                STARTUP_EXITVAL)


########################################################################
# logging and alerts: email, stdout/err, syslog, status log, output log
########################################################################

def pps(to_print):
    """
    Pretty-print a value and return it as a string.
    Especially useful because it will use single- or double-quotes
    as necessary depending on the contents.
    Dependencies:
        globals: PPS_INDENT, PPS_WIDTH, PPS_DEPTH
        modules: StringIO.StringIO / io.StringIO, pprint
    """
    sio = StringIO()
    pprint.pprint(to_print, stream=sio, indent=PPS_INDENT, width=PPS_WIDTH,
                  depth=PPS_DEPTH)
    s = sio.getvalue().strip()
    sio.close()
    return s


def err_exit(msg, exit_val):
    """
    Print a nicely-formatted message and exit.
    msg should _not_ end with \n.
    In general, this function should only be used for errors which might
    happen before the config file has been imported and the logger
    objects have been initialized.
    Parameters:
        msg: the message to print
        exit_val: the value to exit the script with; if this is None,
                  don't actually exit
    Dependencies:
        modules: sys
    """
    print('\n' + msg + '\n', file=sys.stderr)
    if exit_val is not None:
        sys.exit(exit_val)


def email_diagnostics():
    """
    Return a diagnostic string suitable for alert/error emails.
    This is a sample that can be used as-is or overridden by redefining
    this function.
    Dependencies:
        functions: render_config()
    """
    return ('\n\n' + render_config() + '\n\n' + render_status(full=True))


class SMTPDiagHandler(logging.handlers.SMTPHandler):

    """Override SMTPHandler to add diagnostics to the email."""

    def emit(self, record):
        """
        Add diagnostics to the message, and log that an email was sent.
        Dependencies:
            config settings: alert_emails_to
            globals: cfg, alert_logger
            functions: email_diagnostics()
            modules: copy
        """
        # use a copy so the parent loggers won't see the changed message
        r = copy.copy(record)
        if r.msg[-1] != '\n':
            r.msg += '\n'
        r.msg += email_diagnostics()
        super(SMTPDiagHandler, self).emit(r)
        alert_logger.info('Alert email sent to {0}.' .
                          format(cfg['alert_emails_to']))


def init_syslog():

    """
    Set up a syslog handler and return it.

    This is a helper function for init_logging().

    Dependencies:
        config settings: syslog_addr, syslog_sock_type, syslog_fac,
                         syslog_tag
        globals: cfg
        modules: sys, logging, logging.handlers
        Python: 2.7/3.2, for SysLogHandler(socktype)

    """

    if sys.hexversion >= 0x03040000 and cfg['syslog_tag'] != '':
        slh = logging.handlers.SysLogHandler(
                  address=cfg['syslog_addr'],
                  socktype=cfg['syslog_sock_type'],
                  facility=cfg['syslog_fac'],
                  ident=cfg['syslog_tag']
              )
    else:
        slh = logging.handlers.SysLogHandler(
                  address=cfg['syslog_addr'],
                  socktype=cfg['syslog_sock_type'],
                  facility=cfg['syslog_fac']
              )
        syslog_formatter = logging.Formatter(cfg['syslog_tag'] +
                                             '[%(process)d]: %(message)s')
        slh.setFormatter(syslog_formatter)

    return slh


def init_logging_main():

    """
    Initialize most of the logging.

    Includes email, stdout/err, syslog, and/or status log.  See
    init_logging_output() for the output log.

    status_logger and alert_logger both log to the status log (with a
    prefix including the date and process ID) and to syslog.
    status_logger also outputs to stdout, and alert_logger to stderr.
    email_logger sends an email including additional diagnostics and
    hands off the message to alert_logger.

    See logging_stop_stdouterr(), logging_start_stdouterr(),
    logging_email_stop_logging(), and logging_email_start_logging() for
    ways to temporarily change the logging methods.

    Note: syslog may turn control characters into octal, including
    whitespace (e.g., newline -> #012).

    Dependencies:
        config settings: debug, send_alert_emails, alert_emails_from,
                         alert_emails_to, alert_emails_subject,
                         alert_emails_host, alert_emails_cred,
                         alert_emails_sec, quiet, use_syslog, status_log
        globals: cfg, status_logger, alert_logger, email_logger,
                 _syslog_handler, _stdout_handler, _stderr_handler,
                 FULL_DATE_FORMAT, STARTUP_EXITVAL
        functions: init_syslog(), err_exit()
        classes: SMTPDiagHandler
        modules: logging, logging.handlers, sys
        Python: 2.7+/3.x, for SMTPHandler(secure)

    """

    global status_logger, alert_logger, email_logger
    global _syslog_handler, _stdout_handler, _stderr_handler

    # common to status messages and alerts/errors
    base_logger = logging.getLogger(__name__)

    # debug? this value will be used for child loggers as well
    if cfg['debug']:
        base_logger.setLevel(logging.DEBUG)
    else:
        base_logger.setLevel(logging.INFO)

    # status log
    if cfg['status_log']:
        try:
            status_log_handler = logging.FileHandler(cfg['status_log'], 'a')
        except IOError as e:
            err_exit('Error: could not open the status log ({0}); '
                     'exiting.\nDetails: [Errno {1}] {2}' .
                     format(pps(cfg['status_log']), e.errno, e.strerror),
                     STARTUP_EXITVAL)
        status_log_formatter = (
        logging.Formatter('%(asctime)s [%(process)d]: %(message)s',
                          FULL_DATE_FORMAT))
        # (syslog uses %e instead of %d, but it's less portable)
        status_log_handler.setFormatter(status_log_formatter)
        base_logger.addHandler(status_log_handler)

    #syslog
    if cfg['use_syslog']:
        _syslog_handler = init_syslog()
        base_logger.addHandler(_syslog_handler)

    # specific to status messages
    status_logger = logging.getLogger(__name__ + '.status')
    # stdout
    if not cfg['quiet']:
        _stdout_handler = logging.StreamHandler(sys.stdout)
        status_logger.addHandler(_stdout_handler)

    # specific to alerts/errors; use when you don't want email
    alert_logger = logging.getLogger(__name__ + '.alert')
    # stderr
    if not cfg['quiet']:
        _stderr_handler = logging.StreamHandler(sys.stderr)
        alert_logger.addHandler(_stderr_handler)

    # email; use this for most alerts/errors
    email_logger = logging.getLogger(__name__ + '.alert.email')
    if cfg['send_alert_emails']:
        email_handler = SMTPDiagHandler(cfg['alert_emails_host'],
                                        cfg['alert_emails_from'],
                                        cfg['alert_emails_to'],
                                        cfg['alert_emails_subject'],
                                        cfg['alert_emails_cred'],
                                        cfg['alert_emails_sec'])
    else:
        # if we turn off propagation temporarily (see
        # logging_email_stop_logging()), we will get errors unless
        # there's a handler
        email_handler = logging.NullHandler()
    email_logger.addHandler(email_handler)


def logging_stop_syslog():
    """
    Turn off syslog in the loggers.
    Useful when you need to log something sensitive; remember that
    syslog frequently goes to a world-readable file!
    Call logging_start_stdouterr() when done.
    Dependencies:
        globals: base_logger, _syslog_handler
        modules: logging
    """
    base_logger.removeHandler(_syslog_handler)


def logging_start_syslog():
    """
    Turn on syslog in the loggers.
    See logging_stop_syslog().
    Dependencies:
        globals: base_logger, _syslog_handler
        modules: logging
    """
    base_logger.addHandler(_syslog_handler)


def logging_stop_stdouterr():
    """
    Turn off stdout/stderr printing in the loggers.
    Useful when you need to log something that doesn't need to be
    printed.
    Call logging_start_stdouterr() when done.
    Dependencies:
        globals: status_logger, alert_logger, _stdout_handler,
                 _stderr_handler
        modules: logging
    """
    status_logger.removeHandler(_stdout_handler)
    alert_logger.removeHandler(_stderr_handler)


def logging_start_stdouterr():
    """
    Turn on stdout/stderr printing in the loggers.
    See logging_stop_stdouterr().
    Dependencies:
        globals: status_logger, alert_logger, _stdout_handler,
                 _stderr_handler
        modules: logging
    """
    status_logger.addHandler(_stdout_handler)
    alert_logger.addHandler(_stderr_handler)


def logging_email_stop_logging():
    """
    Turn off propagation in the email logger (i.e., no actual logging).
    Useful if you need to send an email with the same settings but
    without logging or printing.
    Call logging_email_start_logging() when done.
    WARNING: the current implementation is not thread-safe.
    Dependencies:
        globals: email_logger
        modules: logging
    """
    email_logger.propagate = False


def logging_email_start_logging():
    """
    Turn on propagation in the email logger (i.e., actual logging).
    See logging_email_stop_logging().
    WARNING: the current implementation is not thread-safe.
    Dependencies:
        globals: email_logger
        modules: logging
    """
    email_logger.propagate = True


def init_logging_output():

    """
    Initialize output logging, including both logger and file objects.

    The output log is for output from external programs; see, e.g.,
    run_with_logging().  See init_logging_main() for the rest of the
    logging.

    output_logger logs to the output log and stdout.  output_log_fo is a
    file object attached to the output log, and is used by (e.g.)
    run_with_logging().

    Dependencies:
        config settings: output_log, output_log_layout, output_log_sep,
                         output_log_date, (output_log_num),
                         (output_log_days)
        globals: cfg, output_logger, output_log_fo, email_logger,
                 start_time, STARTUP_EXITVAL, FULL_DATE_FORMAT
        functions: fix_path(), rotate_prune_output_logs(), pps(),
                   end_logging_output
        modules: logging, sys, os, time, atexit

    """

    global output_logger, output_log_fo, _stdout_handler

    # assemble the complete path, including datestring if applicable
    if cfg['output_log']:
        output_log_path = cfg['output_log']
        if cfg['output_log_layout'] == 'date':
            output_log_path += (cfg['output_log_sep'] +
                                time.strftime(cfg['output_log_date'],
                                              time.localtime(start_time)))
        # needed for prune_date_files(), for pruning by number
        touch_file(output_log_path, 'the output log', None, use_logger=True,
                   warn_only=False, exit_val=STARTUP_EXITVAL)

    # rotate and prune output logs
    # (also tests in case there is no output log, and prints status
    # accordingly)
    rotate_prune_output_logs()

    # output logger object
    # the actual output will be sent with the file object (below);
    # this is for adding things like pre- and post-run status messages
    output_logger = logging.getLogger(__name__ + '.output')
    output_logger.propagate = False
    output_logger.addHandler(_stdout_handler)
    if cfg['output_log']:
        try:
            output_handler = logging.FileHandler(cfg['output_log'])
        except IOError as e:
            email_logger.error('Error: could not open the output log '
                               '({0}); exiting.\nDetails: [Errno {1}] {2}' .
                               format(pps(cfg['output_log']), e.errno,
                                      e.strerror))
            sys.exit(STARTUP_EXITVAL)
        output_logger.addHandler(output_handler)

    # output log file object, for use by (e.g.) run_with_logging()
    try:
        # appending is always safe / the right thing to do, because
        # either the file won't exist, or it will have been moved out of
        # the way by the rotation - except in one case:
        # if we're using a date layout, and the script has been run more
        # recently than the datestring allows for, we should append so
        # as not to lose information
        output_log_fo = open(fix_path(cfg['output_log'])
                                 if cfg['output_log']
                                 else os.devnull,
                             'a')
    except IOError as e:
        email_logger.error('Error: could not open the output log ({0}); '
                           'exiting.\nDetails: [Errno {1}] {2}' .
                           format(pps(cfg['output_log'])
                                      if cfg['output_log']
                                      else os.devnull,
                                  e.errno, e.strerror))
        sys.exit(STARTUP_EXITVAL)

    # automatically close on exit
    # (should be done anyway, but we'll be thorough)
    atexit.register(end_logging_output)


def end_logging_output():
    """
    Close the output log file object.
    Dependencies:
        globals: output_log_fo
    """
    output_log_fo.close()


def run_with_logging(cmd_descr, cmd, include_stderr=True, env_add=None,
                     **kwargs):

    """
    Run a command and log its output to the output log and stdout.

    Returns the exit value of the command.

    May raise exceptions: OSError or ValueError.

    Parameters:
        cmd_descr: a string describing the command, used in messages
                   like 'starting rsync backup'
        cmd: a list containing the command and its arguments
        include_stderr: if true, include stderr in the output (but on
                        stdout)
        env_add: if not None, a dictionary of keys and values to add to
                 the environment in which the command will run; this is
                 added to the current environment if there is no env
                 argument or if env is None, or to the env argument if
                 it is not None
                 * keys that already exist in the target environment
                   will be overridden
                 * values must be strings, or a TypeError will be raised
        kwargs: passed to subprocess.Popen(); but see env_add

    Dependencies:
        config_settings: print_cmds
        globals: cfg, output_logger, output_log_fo, status_logger,
                 FULL_DATE_FORMAT
        functions: pps()
        modules: copy, os, time, operator, subprocess, threading, sys

    """

    # set up the environment
    if env_add is not None:
        if 'env' not in kwargs or kwargs['env'] is None:
            kwargs['env'] = copy.copy(os.environ).update(env_add)
        else:
            kwargs['env'].update(env_add)

    # log the starting time
    output_logger.info('Starting {0} {1}.' .
                       format(cmd_descr,
                              time.strftime(FULL_DATE_FORMAT,
                                            time.localtime())))

    # print the command
    if cfg['print_cmds']:
        cmd_msg = 'Running command:\n'
        cmd_msg += ' '.join(map(pps, cmd)) + '\n'
        if env_add is not None:
            cmd_msg += 'with environment additions:\n'
            for k, v in sorted(env_add.items(),
                               key=operator.itemgetter(0)):
                cmd_msg += k + '=' + pps(v) + '\n'
        print(cmd_msg.strip(), file=output_log_fo)  # no stdout yet
        status_logger.info(cmd_msg.strip())

    # run the command;
    # redirect stderr so we get everything in the same order as we would
    # on the command line
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT
                                if include_stderr else None,
                         **kwargs)

    # get the output
    for line in iter(p.stdout.readline, ''):
        output_log_fo.write(line)
        sys.stdout.write(line)

    # log the ending time
    output_logger.info('{0} finished {1}.' .
                       format(cmd_descr.capitalize(),
                              time.strftime(FULL_DATE_FORMAT,
                                            time.localtime())))

    # get the exit value
    return p.wait()


#
# see also rotate_prune_output_logs()
#


##########################################
# config setting checks and manipulations
##########################################

#
# ### setting_names ###
#
# For the functions below, setting_name can be either a string which is
# an index into cfg, or else a tuple containing recursive indexes into
# cfg; for example, ('alert_emails_host', 1) would test the port number
# of the alert_emails_host setting (cfg['alert_emails_host'][1]),
# assuming it's a tuple.
#
# In setting-checking functions, if the indexed setting doesn't exist
# (e.g., if alert_emails_host is a string containing a hostname), it is
# considered a failure of the check, and causes the script to exit with
# an error, unless otherwise specified.  Settings should be have
# defaults applied, and/or be checked for existence, before calling
# these.
#
# Examples:
#
# allowed to be either unset or a string:
#   setting_is_unset('s_name') or setting_check_type('s_name', str)
#
# allowed to be either a non-blank string or a tuple containing a
# non-blank string and an integer between 1 and 65535:
#   t = setting_check_type('s_name', (str, tuple))
#   if t == str: setting_check_not_blank('s_name')
#   if t == tuple: (setting_check_not_blank(('s_name', 0)) and
#                   setting_check_int(('s_name', 0), 1, 65535))
#


def setting_walk(setting_name):

    """
    Get the configuration (sub-)object indicated by setting_name.

    Returns a tuple containing 4 elements:
        0: True (if the object is found) or False (if it isn't)
        1: the object (if found) or None (if not)
        2: the full path to the object (a string such as
           cfg['name1']['name2'])
        3: a path indicating how far the search got; if the object was
           not found, this path will stop at the last found component,
           otherwise it will be the same as [2]

    Note that None can also be a legitimate object value, so don't use
    [1] to test for the existence of the object.

    Parameters:
        setting_name: see note, above

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg
        functions: scalar_to_tuple(), pps()

    """

    # if setting_name isn't a tuple, make it one
    setting_name = scalar_to_tuple(setting_name)

    # create the full path string
    full_path = 'cfg'
    for ind in setting_name:
        full_path += '[' + pps(ind) + ']'

    # walk the tree
    obj = cfg
    real_path = 'cfg'
    for ind in setting_name:
        try:
            obj = obj[ind]
        except (NameError, IndexError, KeyError, AttributeError, TypeError):
            return (False, None, full_path, real_path)
        real_path += '[' + pps(ind) + ']'
    return (True, obj, full_path, real_path)


def setting_is_set(setting_name):
    """
    Readability wrapper for setting_walk(): is a setting set?
    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg
        functions: setting_walk()
    """
    return setting_walk(setting_name)[0]


def setting_is_unset(setting_name):
    """
    Readability wrapper for setting_walk(): is a setting unset?
    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg
        functions: setting_walk()
    """
    return not setting_walk(setting_name)[0]


def setting_check_is_set(setting_name):

    """
    If a config setting is not set, exit with an error.

    If the setting is set, returns a tuple containing the setting object
    and the full path to the object (see setting_walk()).

    Parameters:
        setting_name: see note, above

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, STARTUP_EXITVAL
        functions: setting_walk(), err_exit()

    """

    ret, obj, full_path, real_path = setting_walk(setting_name)
    if not ret:
        # you should be walking down the tree in order, so everything
        # up to the last component should exist; we won't complicate
        # things by including the real_path
        err_exit('Error: setting {0} is not set; exiting.' .
                 format(pps(full_path)),
                 STARTUP_EXITVAL)
    return (obj, full_path)


def setting_check_one_is_set(setting_name_list):

    """
    At least one of a group of settings must be set, else error/exit.

    Otherwise, returns a tuple containing the first setting object found
    and the full path to the object (see setting_walk()).

    Parameters:
        setting_name_list: a list or tuple of setting_names; see note,
                           above

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, STARTUP_EXITVAL
        functions: setting_walk(), pps(), err_exit()

    """

    setting_paths = []
    for setting_name in setting_name_list:
        ret, obj, full_path, real_path = setting_walk(setting_name)
        setting_paths.append(full_path)
        if ret:
            return (obj, full_path)

    err_exit('Error: at least one of the following must be set:\n'
             '{0}\nExiting.' .
             format('\n'.join(setting_paths)),
             STARTUP_EXITVAL)


def setting_check_type(setting_name, type_tuple):

    """
    If a config setting is not an allowed type, exit with an error.

    If the setting is an allowed type, returns the matching type.

    The existence of the setting is checked.

    Parameters:
        setting_name: see note, above
        type_tuple: a type or tuple of types, which can be either from
                    the types module, or class objects (built-in or
                    user-defined); in both cases, instances of
                    subclasses will also be allowed
                    illegal values in this list will cause the script to
                    exit with an internal error

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, STARTUP_EXITVAL, INTERNAL_EXITVAL
        functions: setting_check_is_set(), pps(), scalar_to_tuple(),
                   type_list_string(), err_exit()

    """

    # walk the tree and make sure it's set
    obj, obj_path = setting_check_is_set(setting_name)

    # if type_tuple isn't a tuple, make it one
    type_tuple = scalar_to_tuple(type_tuple)

    # isinstance() could check them all at once, but then we can't tell
    # which type matched
    for t in type_tuple:
        try:
            if isinstance(obj, t):
                return t
        except TypeError:
            err_exit('Internal Error: type_tuple contains an illegal value '
                     '({0})\nin setting_check_type(); call was '
                     '(in expanded notation):\n'
                     'setting_check_type({1}, {2})\n'
                     'Exiting.' .
                     format(*map(pps, [t, setting_name, type_tuple])),
                     INTERNAL_EXITVAL)

    # nope, it's not an allowed type
    if len(type_tuple) == 1:
        err_exit('Error: {0} must be of type {1}; exiting.' .
                 format(obj_path, pps(type_tuple[0])),
                 STARTUP_EXITVAL)
    else:
        err_exit('Error: {0} must have one of the following types:\n{1}\n'
                 'Exiting.' .
                 format(obj_path, type_list_string(type_tuple)),
                 STARTUP_EXITVAL)


def setting_check_not_empty(setting_name):

    """
    If a container-typed config setting is empty, exit with an error.

    Otherwise, returns a tuple containing the setting object and the
    full path to the object (see setting_walk()).

    The existence and type of the setting are checked.

    See CONTAINER_TYPES, under constants.

    Parameters:
        setting_name: see note, above

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, CONTAINER_TYPES, STARTUP_EXITVAL
        functions: setting_check_is_set(), setting_check_type(),
                   err_exit()

    """

    # walk the tree and make sure it's set
    obj, obj_path = setting_check_is_set(setting_name)

    # check the type
    setting_check_type(setting_name, CONTAINER_TYPES)

    # empty?
    if not obj:
        err_exit('Error: {0} may not be empty; exiting.'.format(obj_path),
                 STARTUP_EXITVAL)

    return (obj, obj_path)


def setting_check_not_all_empty(setting_name_list):

    """
    At least one of a group of settings must be non-empty, else e/e.

    Otherwise, returns a tuple containing the first non-empty setting
    object found and the full path to the object (see setting_walk()).

    The existence and types of the (existent) settings are checked.
    Non-existent settings do not cause an error, but non-container-typed
    settings do.

    See CONTAINER_TYPES, under constants.

    Parameters:
        setting_name_list: a list or tuple of setting_names; see note,
                           above

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, CONTAINER_TYPES, STARTUP_EXITVAL
        functions: setting_walk(), setting_check_type(), err_exit()

    """

    setting_paths = []
    found_one = False

    for setting_name in setting_name_list:
        ret, obj, full_path, real_path = setting_walk(setting_name)
        setting_paths.append(full_path)
        if ret:
            setting_check_type(setting_name, CONTAINER_TYPES)
            if (not found_one) and obj:
                to_return = (obj, full_path)
                found_one = True

    if found_one:
        return to_return
    else:
        err_exit('Error: at least one of the following must be non-empty:\n'
                 '{0}\nExiting.' .
                 format('\n'.join(setting_paths)),
                 STARTUP_EXITVAL)


def setting_check_len(setting_name, min_len, max_len):

    """
    If a config setting has an invalid length, exit with an error.

    Otherwise, returns a tuple containing the setting object and the
    full path to the object (see setting_walk()).

    Works on container- or stringish-typed settings.  The existence and
    type of the setting are checked.

    See CONTAINER_TYPES and STRINGISH_TYPES, under constants.

    Parameters:
        setting_name: see note, above
        min_len: None, or a minimum allowed length (inclusive)
        max_len: None, or a maximum allowed length (inclusive)

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, CONTAINER_TYPES, STRINGISH_TYPES, STARTUP_EXITVAL
        functions: setting_check_is_set(), setting_check_type(), pps(),
                   err_exit()

    """

    # walk the tree and make sure it's set
    obj, obj_path = setting_check_is_set(setting_name)

    # check the type
    t = setting_check_type(setting_name, CONTAINER_TYPES + STRINGISH_TYPES)

    # len(obj) < min_len?  len(obj) > max_len?
    if ((min_len is not None and len(obj) < min_len) or
          (max_len is not None and len(obj) > max_len)):
        if t in CONTAINER_TYPES:
            err_exit('Error: {0} contains an invalid number of elements '
                     '({1}); exiting.'.format(obj_path, pps(len(obj))),
                     STARTUP_EXITVAL)
        else:
            err_exit('Error: {0} is an invalid length ({1}); '
                     'exiting.'.format(obj_path, pps(len(obj))),
                     STARTUP_EXITVAL)

    return (obj, obj_path)


def setting_check_not_blank(setting_name, ish=False):

    """
    If a string-typed config setting is empty, exit with an error.

    Otherwise, returns a tuple containing the setting object and the
    full path to the object (see setting_walk()).

    The existence and type of the setting are checked.

    Parameters:
        setting_name: see note, above
        ish: if true, string-like but non-string types are allowed
             (see STRINGISH_TYPES, under constants)

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, STRING_TYPES, STRINGISH_TYPES, STARTUP_EXITVAL
        functions: setting_check_is_set(), setting_check_type(),
                   err_exit()

    """

    # walk the tree and make sure it's set
    obj, obj_path = setting_check_is_set(setting_name)

    # check the type
    setting_check_type(setting_name,
                       STRINGISH_TYPES if ish else STRING_TYPES)

    # blank?
    if not obj:
        err_exit('Error: {0} may not be blank; exiting.'.format(obj_path),
                 STARTUP_EXITVAL)

    return (obj, obj_path)


def setting_check_not_all_blank(setting_name_list, ish=False):

    """
    At least one of a group of settings must be non-blank, else e/e.

    Otherwise, returns a tuple containing the first non-blank setting
    object found and the full path to the object (see setting_walk()).

    The existence and types of the (existent) settings are checked.
    Non-existent settings do not cause an error, but non-string-typed
    settings do.

    Parameters:
        setting_name_list: a list or tuple of setting_names; see note,
                           above
        ish: if true, string-like but non-string types are allowed
             (see STRINGISH_TYPES, under constants)

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, STRING_TYPES, STRINGISH_TYPES, STARTUP_EXITVAL
        functions: setting_walk(), setting_check_type(), err_exit()

    """

    setting_paths = []
    found_one = False

    for setting_name in setting_name_list:
        ret, obj, full_path, real_path = setting_walk(setting_name)
        setting_paths.append(full_path)
        if ret:
            setting_check_type(setting_name,
                               STRINGISH_TYPES if ish else STRING_TYPES)
            if (not found_one) and obj:
                to_return = (obj, full_path)
                found_one = True

    if found_one:
        return to_return
    else:
        err_exit('Error: at least one of the following must be non-blank:\n'
                 '{0}\nExiting.' .
                 format('\n'.join(setting_paths)),
                 STARTUP_EXITVAL)


def setting_check_no_blanks(setting_name, ish=False):

    """
    If a container config setting contains any blanks, error/exit.

    Otherwise, returns a tuple containing the setting object and the
    full path to the object (see setting_walk()).

    The existence and type of the container are checked, but only the
    types of the container's contents are checked.  If the container
    can't be empty, see setting_check_not_empty().

    See CONTAINER_TYPES, under constants.

    Parameters:
        setting_name: see note, above
        ish: if true, string-like but non-string types are allowed
             (see STRINGISH_TYPES, under constants)

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, CONTAINER_TYPES, STRING_TYPES, STRINGISH_TYPES,
                 STARTUP_EXITVAL
        functions: setting_check_is_set(), setting_check_type(),
                   err_exit()

    """

    # walk the tree and make sure it's set
    obj, obj_path = setting_check_is_set(setting_name)

    # check the container type
    setting_check_type(setting_name, CONTAINER_TYPES)

    # blanks?
    for subobj in obj:
        if not isinstance(subobj, STRINGISH_TYPES if ish else STRING_TYPES):
            err_exit('Error: {0} contains a non-string; Exiting.' .
                     format(obj_path),
                     STARTUP_EXITVAL)
        if not subobj:
            err_exit('Error: {0} contains a blank string; Exiting.' .
                     format(obj_path),
                     STARTUP_EXITVAL)

    return (obj, obj_path)


def setting_check_no_char(setting_name, char, ish=False):

    """
    If a config setting contains particular character(s), error/exit.
    (Setting must be string-typed.)

    Otherwise, returns a tuple containing the setting object and the
    full path to the object (see setting_walk()).

    The existence and type of the setting are checked.

    Parameters:
        setting_name: see note, above
        char: a string containing the illegal character, or a tuple of
              such strings
        ish: if true, string-like but non-string types are allowed
             (see STRINGISH_TYPES, under constants)

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, STRING_TYPES, STRINGISH_TYPES, STARTUP_EXITVAL
        functions: setting_check_is_set(), setting_check_type(),
                   scalar_to_tuple(), char_name(), err_exit()

    """

    # walk the tree and make sure it's set
    obj, obj_path = setting_check_is_set(setting_name)

    # check the type
    setting_check_type(setting_name,
                       STRINGISH_TYPES if ish else STRING_TYPES)

    # if char isn't a tuple, make it one
    char = scalar_to_tuple(char)

    # char in string?
    for c in char:
        if c in obj:
            err_exit('Error: {0} may not contain {1} characters; exiting.' .
                     format(obj_path, pps(char_name(c))),
                     STARTUP_EXITVAL)

    return (obj, obj_path)


def setting_check_list(setting_name, list_vals):

    """
    If a config setting's value is not in a list, exit with an error.

    Otherwise, returns a tuple containing the setting object and the
    full path to the object (see setting_walk()).

    The existence of the setting is checked.

    Parameters:
        setting_name: see note, above
        list_vals: a list (or tuple) containing the allowed values
                   of the setting

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg
        functions: setting_check_is_set()

    """

    # walk the tree and make sure it's set
    obj, obj_path = setting_check_is_set(setting_name)

    # in the list?
    if obj not in list_vals:
        err_exit('Error: invalid setting for {0} ({1}); exiting.' .
                 format(obj_path, pps(obj)),
                 STARTUP_EXITVAL)

    return (obj, obj_path)


def setting_check_num(setting_name, min_val=None, max_val=None):

    """
    If a number-typed config setting is invalid, exit with an error.

    Otherwise, returns a tuple containing the setting object and the
    full path to the object (see setting_walk()).

    The existence and type of the setting are checked.

    See NUMBER_TYPES, under constants.

    Parameters:
        setting_name: see note, above
        min_val: None, or a minimum allowed value (inclusive)
        max_val: None, or a maximum allowed value (inclusive)

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, NUMBER_TYPES
        functions: setting_check_is_set(), setting_check_type()

    """

    # walk the tree and make sure it's set
    obj, obj_path = setting_check_is_set(setting_name)

    # check the type
    setting_check_type(setting_name, NUMBER_TYPES)

    # obj < min_val?  obj > max_val?
    if ((min_val is not None and obj < min_val) or
          (max_val is not None and obj > max_val)):
        err_exit('Error: invalid setting for {0} ({1}); exiting.' .
                 format(obj_path, pps(obj)),
                 STARTUP_EXITVAL)

    return (obj, obj_path)


def setting_check_file_type(setting_name, type_char='f', follow_links=True):

    """
    If a file setting does not have the correct file type, error/exit.

    Otherwise, returns a tuple containing the setting object and the
    full path to the object (see setting_walk()).

    For purposes of this function, 'file' includes directories,
    symlinks, etc.

    The existence and (string) type of the setting are checked, and the
    setting may not be blank.  The file must exist.

    Parameters:
        setting_name: see note, above
        see check_file_access() for the others

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, STARTUP_EXITVAL
        functions: setting_check_not_blank(), check_file_type()

    """

    # check for setting existence, type, and non-blankness
    obj, obj_path = setting_check_not_blank(setting_name)

    # check file type
    check_file_type(obj, obj_path, type_char, follow_links, must_exist=True,
                    use_logger=False, warn_only=False,
                    exit_val=STARTUP_EXITVAL)

    return (obj, obj_path)


def setting_check_file_access(setting_name, file_rwx='r'):

    """
    If a file indicated by a setting is not accessible, error/exit.

    Otherwise, returns a tuple containing the setting object and the
    full path to the object (see setting_walk()).

    The existence and (string) type of the setting are checked, and the
    setting may not be blank.  The file must exist.

    Parameters:
        setting_name: see note, above
        file_rwx: see check_file_access()

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, STARTUP_EXITVAL
        functions: setting_check_not_blank(), check_file_access()

    """

    # check for setting existence, type, and non-blankness
    obj, obj_path = setting_check_not_blank(setting_name)

    # check for access
    check_file_access(obj, obj_path, file_rwx, use_logger=False,
                      warn_only=False, exit_val=STARTUP_EXITVAL)

    return (obj, obj_path)


def setting_check_file_read(setting_name):
    """
    Wrapper to check the case of a file we just need to read.
    Setting must be a non-blank string.  File must exist, be a regular
    file or a symlink to one, and be readable.
    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg
        functions: setting_check_file_type(),
                   setting_check_file_access()
    """
    setting_check_file_type(setting_name, 'f')
    return setting_check_file_access(setting_name, 'r')


def setting_check_file_rw(setting_name):
    """
    Wrapper to check the case of a file we need to read and write.
    Setting must be a non-blank string.  File must exist, be a regular
    file or a symlink to one, and be readable and writable.
    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg
        functions: setting_check_file_type(),
                   setting_check_file_access()
    """
    setting_check_file_type(setting_name, 'f')
    return setting_check_file_access(setting_name, 'rw')


def setting_check_dir_rwx(setting_name):
    """
    Wrapper: check a dir in which we need to create and/or rotate files.
    Setting must be a non-blank string.  Directory must exist, be a
    directory or a symlink to one, and have full permissions (r for
    rotation, wx for creating files).
    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg
        functions: setting_check_file_type(),
                   setting_check_file_access()
    """
    setting_check_file_type(setting_name, 'd')
    return setting_check_file_access(setting_name, 'rwx')


def setting_check_filedir_create(setting_name, create_type='f',
                                 need_rotation=False):

    """
    If we won't be able to create a file or directory, error/exit.

    Otherwise, returns a tuple containing the setting object and the
    full path to the object (see setting_walk()).

    Specifically: this is for files/directories we're going to be
    touching, writing to, creating, and/or rotating (but not necessarily
    reading), such as output logs.

    The existence and (string) type of the setting are checked, and the
    setting may not be blank.

    See check_filedir_create() for details.

    Parameters:
        setting_name: see note, above
        see check_filedir_create() for the others

    Dependencies:
        config settings: (contents of setting_name)
        globals: cfg, STARTUP_EXITVAL
        functions: setting_check_not_blank(), check_filedir_create()

    """

    # check for setting existence, type, and non-blankness
    obj, obj_path = setting_check_not_blank(setting_name)

    # check for creation
    check_filedir_create(obj, obj_path, create_type, need_rotation,
                         use_logger=False, warn_only=False,
                         exit_val=STARTUP_EXITVAL)

    return (obj, obj_path)


##################################
# status checks and modifications
##################################

def lockfile_cleanup():
    """
    Exit callback: clean up the lockfile.
    Removes the lockfile unless the SCRIPT_DISABLED semaphore exists.
    Dependencies:
        config settings: lockfile
        globals: cfg, SCRIPT_DISABLED
        functions: fix_path()
        modules: os, shutil
    """
    # If the file exists, a disable command must have been run while we
    # were running; leave the lockfile dir alone, so future invocations
    # will be disabled.
    if not os.path.isfile(fix_path(os.path.join(cfg['lockfile'],
                                                SCRIPT_DISABLED))):
        # By the time we run this, we won't really be able to rely on
        # any of the logging, and we might be in the middle of a signal
        # handler, so ignore errors.  The next time the script is
        # invoked, it will complain that the lockfile directory exists,
        # so we'll know something went wrong.
        shutil.rmtree(os.path.realpath(fix_path(cfg['lockfile'])), True)


def check_status():

    """
    Check if the script proper should actually start running.

    * Has cfg['run_every'] passed?
    * Does cfg['lockfile'] already exist?
    * Send alerts about it if necessary.
    * Has the script been disabled?

    Dependencies:
        config settings: run_every, last_started_file, lockfile,
                         if_running, lockfile_alert_file
        globals: cfg, status_logger, alert_logger, email_logger,
                 TASK_NAME, TASKS_NAME, NO_ERROR_EXITVAL,
                 STARTUP_EXITVAL, LOCKFILE_EXITVAL, LF_ALERTS_SILENCED,
                 SCRIPT_DISABLED
        functions: fix_path(), file_newer_than(),
                   logging_email_stop_logging(),
                   logging_email_start_logging(), pps(),
                   lockfile_cleanup()
        modules: sys, atexit, os, errno

    """

    if cfg['run_every'] == 0:
        status_logger.info('Interval checking has been disabled; '
                           'continuing.')
    else:
        # has it been long enough since the script was last started
        # (sucessfully)?
        #
        # if cfg['last_started_file'] exists and is newer than
        # cfg['run_every'], exit
        try:
            nt = file_newer_than(cfg['last_started_file'], cfg['run_every'])
        except OSError as e:
            if e.errno == errno.ENOENT:
                nt = False  # no last_started_file == not newer than
            else:
                email_logger.error(
                    "Error: could not stat cfg['last_started_file'] ({0}); "
                    "exiting.\nDetails: [Errno {1}] {2}" .
                    format(pps(cfg['last_started_file']), e.errno,
                           e.strerror)
                )
                sys.exit(STARTUP_EXITVAL)
        if nt:
            status_logger.info('{0} interval has not expired; exiting.' .
                               format(TASK_NAME.capitalize()))
            sys.exit(NO_ERROR_EXITVAL)
        else:
            status_logger.info('{0} interval has expired; continuing.' .
                               format(TASK_NAME.capitalize()))

    # did the previous run finish?
    #
    # EAFP is Pythonic to begin with, but it's essential here, because
    # we need to use a single call to check and create the lock
    try:
        os.mkdir(cfg['lockfile'])
    except OSError as e:
        if e.errno != errno.EEXIST:
            email_logger.error(
                'Error: could not create the lockfile directory ({0}); '
                'exiting.\nDetails: [Errno {1}] {2}' .
                format(pps(cfg['lockfile']), e.errno,
                       e.strerror)
            )
            # not LOCKFILE_EXITVAL because it's not about locking, it's
            # about the path or the filesystem or whatever
            sys.exit(STARTUP_EXITVAL)

        else:  # lockfile exists already
            # is it because we disabled the script?
            if os.path.exists(fix_path(os.path.join(cfg['lockfile'],
                                                    SCRIPT_DISABLED))):
                alert_logger.error('{0} have been manually disabled; '
                                   'exiting.' .
                                   format(TASKS_NAME.capitalize()))
            else:
                alert_logger.error(
                    'Could not create the lockfile directory\n'
                    '(previous {0} still running or failed?); exiting.' .
                    format(TASK_NAME.capitalize())
                )
            # don't actually exit yet

            # send the initial alert email
            # (email only; we already logged it)
            if not os.path.exists(fix_path(cfg['lockfile_alert_file'])):
                # first, touch the semaphore
                touch_file(cfg['lockfile_alert_file'],
                           "cfg['lockfile_alert_file']",
                           None, use_logger=True, warn_only=False,
                           exit_val=None)
                           # don't exit yet, we're already about to exit

                # send the email and exit
                logging_email_stop_logging()
                if os.path.exists(fix_path(os.path.join(cfg['lockfile'],
                                                        SCRIPT_DISABLED))):
                    email_logger.error('{0} have been manually disabled; '
                                       'exiting.' .
                                       format(TASKS_NAME.capitalize()))
                else:
                    email_logger.error(
                        'Could not create the lockfile directory\n'
                        '(previous {0} still running or failed?); '
                        'exiting.' .
                        format(TASK_NAME.capitalize())
                    )
                logging_email_start_logging()
                sys.exit(LOCKFILE_EXITVAL)

            # but what about subsequent emails?

            # if cfg['if_running']==0, log it but don't send email
            if cfg['if_running'] == 0:
                alert_logger.error('if_running == 0; no email sent.')
                sys.exit(LOCKFILE_EXITVAL)

            # if alerts have been silenced, log it but don't send email
            # (and don't bother checking timestamps)
            if os.path.exists(fix_path(os.path.join(cfg['lockfile'],
                                                    LF_ALERTS_SILENCED))):
                alert_logger.error('Alerts have been silenced; '
                                   'no email sent.')
                sys.exit(LOCKFILE_EXITVAL)

            # if cfg['lockfile_alert_file'] is newer than
            # cfg['if_running'], log it but don't send email
            try:
                nt = file_newer_than(cfg['lockfile_alert_file'],
                                     cfg['if_running'])
            except OSError:
                email_logger.error(
                    "Error: could not stat "
                    "cfg['lockfile_alert_file'] ({0}); exiting.\n"
                    "Details: [Errno {1}] {2}" .
                    format(pps(cfg['lockfile_alert_file']), e.errno,
                           e.strerror)
                )
                sys.exit(STARTUP_EXITVAL)
            if nt:
                alert_logger.error('Alert interval has not expired; '
                                   'no email sent.')
                sys.exit(LOCKFILE_EXITVAL)

            # touch the semaphore
            touch_file(cfg['lockfile_alert_file'],
                       "cfg['lockfile_alert_file']",
                       None, use_logger=True, warn_only=False,
                       exit_val=None)
                       # don't exit yet, we're already about to exit

            # send another alert email
            # (email only; we already logged it)
            logging_email_stop_logging()
            if os.path.exists(fix_path(os.path.join(cfg['lockfile'],
                                                    SCRIPT_DISABLED))):
                email_logger.error('{0} have been manually disabled; '
                                   'exiting.' .
                                   format(TASKS_NAME.capitalize()))
            else:
                email_logger.error(
                    'Could not create the lockfile directory\n'
                    '(previous {0} still running or failed?); exiting.' .
                    format(TASK_NAME.capitalize())
                )
            logging_email_start_logging
            sys.exit(LOCKFILE_EXITVAL)

    # ok, got the lock

    # register callback to remove the lockfile on exit
    atexit.register(lockfile_cleanup)

    # clear lock-alert status
    try:
        os.unlink(fix_path(cfg['lockfile_alert_file']))
    except OSError as e:
        if e.errno != errno.ENOENT:
            email_logger.error(
                "Error: could not remove cfg['lockfile_alert_file'] ({0}); "
                "exiting.\n"
                "Details: [Errno {1}] {2}" .
                format(pps(cfg['lockfile_alert_file']), e.errno,
                       e.strerror)
            )
            sys.exit(STARTUP_EXITVAL)
        else:  # it didn't exist, ignore
            pass
    else:  # it did exist, tell the user
        email_logger.info('Lockfile created; '
                          'cancelling previous alert status.')


def render_status_messages(full=False):

    """
    Return a string with status messages about the script.

    The messages can be changed or added to by redefining this function
    or by defining render_status_messages_hook(), which must take the
    message string and the full flag, and return a message string.

    Parameters:
        full: if true, include less-useful (e.g., debugging) info

    Dependencies:
        config settings: last_started_file, lockfile,
                         lockfile_alert_file
        hooks: render_status_messages_hook
        globals: cfg, LF_ALERTS_SILENCED, SCRIPT_DISABLED, TASK_NAME,
                 TASKS_NAME
        functions: fix_path()
        modules: os

    """

    msg = (
'''-------
Status:
-------

'''
          )

    if not os.path.exists(fix_path(cfg['last_started_file'])):
        msg += ('No last-started file; '
                'this {0} appears to have never been run.\n' .
                format(TASK_NAME))

    if os.path.exists(fix_path(cfg['lockfile'])):
        msg += ('Lockfile directory exists; a {0} may be in progress.\n' .
                format(TASK_NAME))
    else:
        msg += ('No lockfile directory found; {0} are enabled but not '
                'in progress.\n' .
                format(TASKS_NAME))

    if os.path.exists(fix_path(cfg['lockfile_alert_file'])):
        msg += ('Alertfile exists; a running {0} prevented a new one '
                'from starting.\n' .
                format(TASK_NAME))

    if os.path.exists(fix_path(os.path.join(cfg['lockfile'],
                                            LF_ALERTS_SILENCED))):
        msg += 'Lockfile alerts have been silenced.\n'

    if os.path.exists(fix_path(os.path.join(cfg['lockfile'],
                                            SCRIPT_DISABLED))):
        msg += ('{0} have been disabled (but the last one may still '
                'be running).\n' .
                format(TASKS_NAME.capitalize()))

    # hook for adding more messages
    if ('render_status_messages_hook' in globals() and
          callable(render_status_messages_hook)):
        msg = render_status_messages_hook(msg, full)

    return msg


def render_status_metadata(full=False):

    """
    Return a string with metadata about lockfiles, semaphores, etc.

    The metadata can be changed or added to by redefining this function
    or by defining render_status_metadata_hook(), which must take the
    message string and the full flag, and return a message string.

    Parameters:
        full: if true, include less-useful (e.g., debugging) info

    Dependencies:
        config settings: last_started_file, lockfile,
                         lockfile_alert_file
        hooks: render_status_metadata_hook
        globals: cfg, LF_ALERTS_SILENCED, SCRIPT_DISABLED
        functions: get_file_metadata()
        modules: os

    """

    msg = (
'''------------------------------
Timestamps and other metadata:
------------------------------

last_started_file:
{0}

lockfile:
{1}

lockfile_alert_file:
{2}

lfalertssilenced:
{3}

scriptdisabled:
{4}''' .
           format(get_file_metadata(cfg['last_started_file'], '(none)'),
                  get_file_metadata(cfg['lockfile'], '(none)'),
                  get_file_metadata(cfg['lockfile_alert_file'], '(none)'),
                  get_file_metadata(os.path.join(cfg['lockfile'],
                                                 LF_ALERTS_SILENCED),
                                    '(none)'),
                  get_file_metadata(os.path.join(cfg['lockfile'],
                                                 SCRIPT_DISABLED),
                                    '(none)'))
          )

    # hook for adding more metadata
    if ('render_status_metadata_hook' in globals() and
          callable(render_status_metadata_hook)):
        msg = render_status_metadata_hook(msg, full)

    return msg


def render_status(full=False):
    """
    Return the complete status string.
    Doesn't print surrounding blank lines; add them if necessary in
    context.
    Parameters:
        full: if true, include less-useful (e.g., debugging) info
    """
    return (render_status_messages(full) + '\n\n' +
            render_status_metadata(full))


#
# Note: the functions below are meant to be run from manual command line
# modes, not autonomous operation; they only log actual status changes.
#


def silence_lf_alerts():

    """
    Silence lockfile-exists alerts.

    Dependencies:
        config settings: lockfile
        globals: cfg, status_logger, NO_ERROR_EXITVAL, STARTUP_EXITVAL,
                 LF_ALERTS_SILENCED
        functions: fix_path(), logging_stop_stdouterr(),
                   logging_start_stdouterr(), log_cl_config(), pps(),
                   err_exit()
        modules: sys, os

    """

    # lockfile exists?
    if not os.path.exists(fix_path(cfg['lockfile'])):
        print("\nLockfile directory doesn't exist; nothing to silence.\n")
        sys.exit(STARTUP_EXITVAL)

    # alerts already silenced?
    if os.path.exists(fix_path(os.path.join(cfg['lockfile'],
                                            LF_ALERTS_SILENCED))):
        print('\nLockfile alerts were already silenced.\n')
        sys.exit(STARTUP_EXITVAL)

    # touch the semaphore;
    # using a file in the lockfile dir means that we automatically
    # get the silencing cleared when the lockfile is removed
    touch_file(os.path.join(cfg['lockfile'], LF_ALERTS_SILENCED),
               'the semaphore file', None, use_logger=False,
               warn_only=False, exit_val=STARTUP_EXITVAL)

    # print and log status, separately
    print('\nLockfile alerts have been silenced.\n')
    logging_stop_stdouterr()
    log_cl_config()  # to help interpret the status message
    status_logger.info('Lockfile alerts have been silenced for '
                       'lockfile {0}.'.format(pps(cfg['lockfile'])))
    logging_start_stdouterr()


def unsilence_lf_alerts():

    """
    Unsilence lockfile-exists alerts.

    Dependencies:
        config settings: lockfile
        globals: cfg, status_logger, NO_ERROR_EXITVAL, STARTUP_EXITVAL,
                 LF_ALERTS_SILENCED
        functions: fix_path(), logging_stop_stdouterr(),
                   logging_start_stdouterr(), log_cl_config(), pps(),
                   err_exit()
        modules: sys, os, errno

    """

    # alerts already unsilenced, or no lockfile?
    if not os.path.exists(fix_path(os.path.join(cfg['lockfile'],
                                                LF_ALERTS_SILENCED))):
        print('\nLockfile alerts were already unsilenced.\n')
        sys.exit(STARTUP_EXITVAL)

    # remove the semaphore
    try:
        os.unlink(fix_path(os.path.join(cfg['lockfile'],
                                        LF_ALERTS_SILENCED)))
    except OSError as e:
        if e.errno != errno.ENOENT:
            err_exit('\nError: could not remove the semaphore file ({0}); '
                     'exiting.\nDetails: [Errno {1}] {2}\n' .
                     format(pps(os.path.join(cfg['lockfile'],
                                             LF_ALERTS_SILENCED)),
                            e.errno, e.strerror),
                     STARTUP_EXITVAL)
        else:  # it didn't exist, ignore
            pass

    # print and log status, separately
    print('\nLockfile alerts have been unsilenced.\n')
    logging_stop_stdouterr()
    log_cl_config()  # to help interpret the status message
    status_logger.info('Lockfile alerts have been unsilenced for '
                       'lockfile {0}.'.format(pps(cfg['lockfile'])))
    logging_start_stdouterr()


def disable_script():

    """
    Disable the script.

    Dependencies:
        config settings: lockfile
        globals: cfg, status_logger, TASK_ARTICLE, TASK_NAME,
                 TASKS_NAME, NO_ERROR_EXITVAL, STARTUP_EXITVAL,
                 SCRIPT_DISABLED
        functions: fix_path(), logging_stop_stdouterr(),
                   logging_start_stdouterr(), log_cl_config(), pps(),
                   err_exit()
        modules: sys, os, errno

    """

    # script already disabled?
    if os.path.exists(fix_path(os.path.join(cfg['lockfile'],
                                            SCRIPT_DISABLED))):
        print('\n{0} were already disabled.\n' .
              format(TASKS_NAME.capitalize()))
        sys.exit(STARTUP_EXITVAL)

    # lockfile exists?
    if os.path.exists(fix_path(cfg['lockfile'])):
        print('\nThe lockfile directory exists; {0} {1} is probably '
              'running.\n'
              'The disable command will take effect after the current {1} '
              'finishes.'.format(TASK_ARTICLE, TASK_NAME))  # no \n

    # touch the semaphore
    try:
        # first make sure the lockfile directory exists
        os.mkdir(fix_path(os.path.join(cfg['lockfile'])))
    except OSError as e:
        if e.errno != errno.EEXIST:
            err_exit('\nError: could not create the lockfile directory '
                     '({0}); exiting.\nDetails: [Errno {1}] {2}\n' .
                     format(pps(cfg['lockfile']), e.errno, e.strerror),
                     STARTUP_EXITVAL)
        else:  # it existed already
            pass
    touch_file(os.path.join(cfg['lockfile'], SCRIPT_DISABLED),
               'the semaphore file', None, use_logger=False,
               warn_only=False, exit_val=STARTUP_EXITVAL)

    # print and log status, separately
    print('\n{0} have been disabled; remember to re-enable them later!\n' .
          format(TASKS_NAME.capitalize()))
    logging_stop_stdouterr()
    log_cl_config()  # to help interpret the status message
    status_logger.info('{0} have been disabled; lockfile is {1}.' .
                       format(TASKS_NAME.capitalize(),
                              pps(cfg['lockfile'])))
    logging_start_stdouterr()


def enable_script():

    """
    (Re)-enable the script.

    Dependencies:
        config settings: lockfile
        globals: cfg, status_logger, TASK_ARTICLE, TASK_NAME,
                 TASKS_NAME, NO_ERROR_EXITVAL, STARTUP_EXITVAL,
                 SCRIPT_DISABLED
        functions: fix_path(), logging_stop_stdouterr(),
                   logging_start_stdouterr(), log_cl_config(), pps(),
                   err_exit()
        modules: sys, os, errno

    """

    # script already enabled?
    if not os.path.exists(fix_path(os.path.join(cfg['lockfile'],
                                                SCRIPT_DISABLED))):
        print('\n{0} were already enabled.\n' .
              format(TASKS_NAME.capitalize()))
        sys.exit(STARTUP_EXITVAL)

    # remove the semaphore
    try:
        os.unlink(fix_path(os.path.join(cfg['lockfile'], SCRIPT_DISABLED)))
    except OSError as e:
        if e.errno != errno.ENOENT:
            err_exit('\nError: could not remove the semaphore file ({0}); '
                     'exiting.\nDetails: [Errno {1}] {2}\n' .
                     format(pps(os.path.join(cfg['lockfile'],
                                             SCRIPT_DISABLED)),
                            e.errno, e.strerror),
                     STARTUP_EXITVAL)
        else:  # it didn't exist, ignore
            pass

    # print and log status, separately
    print('\n{0} have been re-enabled.\n'
          '\nIf {1} {2} is not currently running, you should now remove the'
          '\nlockfile with the unlock command.\n' .
          format(TASKS_NAME.capitalize(), TASK_ARTICLE, TASK_NAME))
    logging_stop_stdouterr()
    log_cl_config()  # to help interpret the status message
    status_logger.info('{0} have been re-enabled; lockfile is {1}.' .
                       format(TASKS_NAME.capitalize(),
                              pps(cfg['lockfile'])))
    logging_start_stdouterr()


def clear_lockfile():

    """
    Forcibly remove the lockfile directory.

    Dependencies:
        config settings: lockfile
        globals: cfg, status_logger, TASK_ARTICLE, TASK_NAME,
                 NO_ERROR_EXITVAL, STARTUP_EXITVAL
        functions: fix_path(), logging_stop_stdouterr(),
                   logging_start_stdouterr(), log_cl_config(), pps(),
                   err_exit()
        modules: sys, os, shutil, errno

    """

    # lockfile already removed?
    if not os.path.exists(fix_path(cfg['lockfile'])):
        print('\nThe lockfile directory has already been removed.\n')
        sys.exit(STARTUP_EXITVAL)

    # are you sure?
    yn = raw_input("\nWARNING: the lockfile directory should only be "
                   "removed if you're sure that\n{0} {1} is not currently "
                   "running.\n"
                   "Continue (y/n)? " .
                   format(TASK_ARTICLE, TASK_NAME))
    if yn.lower() != 'y':
        print('\nExiting.\n')
        sys.exit(NO_ERROR_EXITVAL)

    # remove the lockfile
    try:
        shutil.rmtree(os.path.realpath(fix_path(cfg['lockfile'])), False)
    except OSError as e:
        if e.errno != errno.ENOENT:
            err_exit('Error: could not remove the lockfile directory '
                     '({0}); exiting.\nDetails: [Errno {1}] {2}' .
                     format(pps(cfg['lockfile']), e.errno, e.strerror),
                     STARTUP_EXITVAL)
        else:  # it didn't exist, ignore
            pass

    # print and log status, separately
    print('\nThe lockfile directory ({0}) has been removed.\n' .
          format(pps(cfg['lockfile'])))
    logging_stop_stdouterr()
    log_cl_config()  # to help interpret the status message
    status_logger.info('Lockfile directory {0} has been manually removed.' .
                       format(pps(cfg['lockfile'])))
    logging_start_stdouterr()


#####################################
# startup and config file processing
#####################################

def import_file(file_path):

    """
    Import an arbitrary file as a module and add it to sys.modules.

    Returns a tuple containing the module name and the module object.

    Does not use sys.path or the relative import syntax, and allows
    filenames to contain any character.

    If using a version of Python prior to 2.7/3.2 which does not have
    universal newlines support, the file must use Unix newlines.
    Versions prior to 2.7/3.2 may also require that the file end with a
    newline.

    May raise exceptions: OSError, IOError, SyntaxError, or TypeError.

    Parameters:
        file_path: the path to the file to import

    Dependencies:
        functions: fix_path()
        modules: re, os, sys, imp [if using Python <3.4],
                 types.ModuleType [if using Python 3.4+]
        Python: 2.7/3.2 [depending on the contents of the file; see
                above]

    """

    # shorter, cleaner name for the module
    mod_name = re.sub('\.py.?$', '', os.path.basename(fix_path(file_path)))
    mod_name = re.sub('[^A-Za-z0-9_]', '_', mod_name)

    # module object
    if sys.hexversion < 0x03040000:
        module = imp.new_module(mod_name)
    else:
        module = ModuleType(mod_name)

    # note: can't supply a file directly to exec in Python3
    exec(compile(open(file_path, 'U').read(), file_path, 'exec'),
         module.__dict__)
    sys.modules[mod_name] = module

    return (mod_name, module)


def import_config_by_name(file_path):
    """
    Import a config file (module).
    Parameters:
        mod_path: the path to the config file
    Dependencies:
        globals: config_modules, cfg, STARTUP_EXITVAL
        functions: import_file(), pps(), err_exit()
    """
    global config_modules, cfg
    try:
        c_mod_name, c_mod = import_file(file_path)
    except (OSError, IOError) as e:
        err_exit('Error: could not read config file {0}; exiting.\n'
                 'Details: [Errno {1}] {2}' .
                 format(pps(file_path), e.errno, e.strerror),
                 STARTUP_EXITVAL)
    except (SyntaxError, TypeError) as e:
        err_exit('Error: could not process config file {0}; exiting.\n'
                 'Details: {1}'.format(pps(file_path), e),
                 STARTUP_EXITVAL)
    config_modules.append(c_mod)
    cfg.update(c_mod.cfg)


def check_bogus_config():

    """
    If there are non-existent settings set, exit with an error.

    Dependencies:
        globals: cfg, config_settings, bogus_config, STARTUP_EXITVAL
        functions: setting_walk(), pps(), err_exit()

    """

    # check for bogus top-level settings
    for setting in cfg:
        if (setting not in config_settings or
              'heading' in config_settings[setting]):
            err_exit("Warning: cfg['{0}'] is set (to {1}), "
                     "but there is no such setting." .
                     format(setting, pps(cfg[setting])),
                     STARTUP_EXITVAL)

    # look for specific sub-settings
    for bogus in bogus_config:
        ret, obj, full_path, real_path = setting_walk(bogus)
        if ret:
            err_exit('Warning: {0} is set (to {1}), '
                     'but there is no such setting.' .
                     format(full_path, pps(obj)),
                     STARTUP_EXITVAL)


def apply_config_defaults():

    """
    Apply defaults to the config settings, as necessary.

    Dependencies:
        config settings: (most of them)
        globals: config_settings, cfg
        functions: apply_config_defaults_extra()

    """

    # first do the straightforward ones
    for s_name, s_dict in config_settings.items():
        if (s_name not in cfg and 'default' in s_dict and
              'heading' not in s_dict):
            cfg[s_name] = s_dict['default']

    # then do the last-minute/complicated ones
    apply_config_defaults_extra()


def apply_config_defaults_extra():

    """
    Apply configuration defaults that are last-minute/complicated.
    In particular, this is the place for defaults that depend on the
    values supplied for other settings.

    To change or add to the extra setting defaults, either redefine this
    function, or define apply_config_defaults_hook(), which takes no
    arguments.

    Dependencies:
        config settings: lockfile_alert_file, lockfile
        hooks: apply_config_defaults_hook()
        globals: cfg

    """

    # lockfile_alert_file
    if 'lockfile_alert_file' not in cfg:
        cfg['lockfile_alert_file'] = cfg['lockfile'] + '.alert'

    # hook for adding more defaults
    if ('apply_config_defaults_hook' in globals() and
          callable(apply_config_defaults_hook)):
        apply_config_defaults_hook()


def check_config_requirements():
    """
    If settings require unavailable features, exit with an error.
    Dependencies:
        globals: supported_features, available_features,
                 config_settings, cfg, STARTUP_EXITVAL
        functions: pps(), err_exit()
    """
    for s_name, s_dict in config_settings.items():
        if 'requires' in s_dict and s_dict['requires'] and s_name in cfg:
            for feature in s_dict['requires']:
                if feature not in available_features:
                    msg = ('Error: setting cfg[{0}] is set (to {1}), '
                           'but it requires\n'
                           'the {2} feature, which is not available '
                           'on this system.' .
                           format(*map(pps, [s_name, cfg[s_name],
                                             feature])))
                    if (feature in supported_features and
                          supported_features[feature]):
                        msg += ('\nFeature description: {0}' .
                                format(supported_features[feature]))
                    err_exit(msg, STARTUP_EXITVAL)


def validate_config():

    """
    Validate the configuration settings.

    To change or add to the validation, either redefine this function,
    or define validate_config_hook(), which takes no arguments.

    Dependencies:
        config settings: (all of them)
        hooks: validate_config_hook()
        globals: cfg, STRING_TYPES, PATH_SEP
        functions: setting_check_type(), setting_check_num(),
                   setting_check_filedir_create(),
                   setting_check_not_blank(), setting_check_no_blanks(),
                   setting_check_len(), setting_check_file_read(),
                   setting_check_file_type(),
                   setting_check_file_access(), setting_check_list(),
                   setting_check_no_char()
        modules: socket

    """

    # validate the settings that are already available
    if 'exec_path' in cfg:
        setting_check_type('exec_path', STRING_TYPES)
    if 'umask' in cfg:
        setting_check_num('umask', 0, 511)  # 511 = 0o777
    setting_check_type('debug', bool)
    setting_check_num('run_every', 0)
    setting_check_filedir_create('last_started_file', 'f')
    setting_check_filedir_create('lockfile', 'd')
    setting_check_num('if_running', 0)
    setting_check_filedir_create('lockfile_alert_file', 'f')
    setting_check_type('send_alert_emails', bool)
    if cfg['send_alert_emails']:
        setting_check_not_blank('alert_emails_from')
        setting_check_type('alert_emails_to', list)
        setting_check_no_blanks('alert_emails_to')
        setting_check_type('alert_emails_subject', STRING_TYPES)
        if setting_check_type('alert_emails_host',
                              STRING_TYPES + (tuple, )) == tuple:
            setting_check_len('alert_emails_host', 2, 2)
            setting_check_not_blank(('alert_emails_host', 0))
            setting_check_num(('alert_emails_host', 1), 1, 65535)
        else:
            setting_check_not_blank('alert_emails_host')
        if (setting_check_type('alert_emails_cred', (NoneType, tuple))
              is not NoneType):
            setting_check_len('alert_emails_cred', 2, 2)
            setting_check_no_blanks('alert_emails_cred')
        if (setting_check_type('alert_emails_sec', (NoneType, tuple))
              is not NoneType):
            setting_check_len('alert_emails_sec', 0, 2)
            for i, f in enumerate(cfg['alert_emails_sec']):
                setting_check_file_read(('alert_emails_sec', i))
    setting_check_type('quiet', bool)
    setting_check_type('use_syslog', bool)
    if cfg['use_syslog']:
        if setting_check_type('syslog_addr',
                              STRING_TYPES + (tuple, )) == tuple:
            setting_check_len('syslog_addr', 2, 2)
            setting_check_not_blank(('syslog_addr', 0))
            setting_check_num(('syslog_addr', 1), 1, 65535)
        else:
            setting_check_file_type('syslog_addr', 's')
            setting_check_file_access('syslog_addr', 'w')
        setting_check_list('syslog_sock_type', [socket.SOCK_DGRAM,
                                                socket.SOCK_STREAM])
        sl_class = logging.handlers.SysLogHandler  # for readability
        # encodePriority() doesn't do enough checking (e.g., it will
        # allow any integer), so just use the list from the
        # documentation
        setting_check_list(
            'syslog_fac',
            [
                'auth', sl_class.LOG_AUTH,
                'authpriv', sl_class.LOG_AUTHPRIV,
                'cron', sl_class.LOG_CRON,
                'daemon', sl_class.LOG_DAEMON,
                'ftp', sl_class.LOG_FTP,
                'kern', sl_class.LOG_KERN,
                'lpr', sl_class.LOG_LPR,
                'mail', sl_class.LOG_MAIL,
                'news', sl_class.LOG_NEWS,
                'syslog', sl_class.LOG_SYSLOG,
                'user', sl_class.LOG_USER,
                'uucp', sl_class.LOG_UUCP,
                'local0', sl_class.LOG_LOCAL0,
                'local1', sl_class.LOG_LOCAL1,
                'local2', sl_class.LOG_LOCAL2,
                'local3', sl_class.LOG_LOCAL3,
                'local4', sl_class.LOG_LOCAL4,
                'local5', sl_class.LOG_LOCAL5,
                'local6', sl_class.LOG_LOCAL6,
                'local7', sl_class.LOG_LOCAL7,
            ]
        )
        setting_check_type('syslog_tag', STRING_TYPES)
    setting_check_type('status_log', STRING_TYPES + (NoneType, ))
    if cfg['status_log']:
        setting_check_filedir_create('status_log', 'f')
    setting_check_type('output_log', STRING_TYPES + (NoneType, ))
    if cfg['output_log']:
        setting_check_filedir_create('output_log', 'f', need_rotation=True)
        setting_check_list('output_log_layout',
                           ['append', 'number', 'date'])
        setting_check_no_char('output_log_sep', PATH_SEP)
        setting_check_not_blank('output_log_date', PATH_SEP)
        setting_check_no_char('output_log_date', PATH_SEP)
        if cfg['output_log_layout'] != 'append':
            setting_check_num('output_log_num', 0)
            setting_check_num('output_log_days', 0)

    # hook for adding more validation
    if ('validate_config_hook' in globals() and
          callable(validate_config_hook)):
        validate_config_hook()


def process_config(arg_ns):

    """
    Process the config file and settings supplied on the command line.
    Includes applying defaults, checking requirements, validating values,
    and initializing loggers (main and output).

    To add initializations, define process_config_hook(), which takes no
    arguments.

    Parameters:
        arg_ns: the Namespace object returned by an argument parser
                (see create_arg_parser() and process_command_line())

    Dependencies:
        config settings: exec_path, umask
        hooks: process_config_hook()
        globals: cfg, config_file_paths, cl_config, config_settings,
                 STARTUP_EXITVAL
        functions: import_config_by_name(), check_bogus_config(),
                   apply_config_defaults(), validate_config(),
                   init_logging_main(), init_logging_output(), pps(),
                   err_exit()
        modules: argparse, os
        Python: 2.7/3.2, for argparse

    """

    global cl_config

    # config_file_paths is set in process_command_line() because it
    # might be needed before this function is called

    # import the config files
    if config_file_paths is not None:
        for cfp in config_file_paths:
            if not cfp:
                err_exit('Error: config file paths may not be empty '
                         'strings; exiting', STARTUP_EXITVAL)
            check_file_type(cfp, 'config file', 'f', follow_links=True,
                            must_exist=True, use_logger=False,
                            warn_only=False, exit_val=STARTUP_EXITVAL)
            check_file_access(cfp, 'config file', 'r', use_logger=False,
                              warn_only=False, exit_val=STARTUP_EXITVAL)
            import_config_by_name(cfp)

    # process settings supplied on the command line;
    # be defensive in case the args were changed
    if hasattr(arg_ns, 'o') and arg_ns.o is not None:
        for [s_name, s_val] in arg_ns.o:
            if (s_name not in config_settings or
                  'heading' in config_settings[s_name]):
                err_exit('Error: non-existent setting {0} was supplied '
                         'on the command line.\nExiting.' .
                         format(pps(s_name)),
                         STARTUP_EXITVAL)
            if ('cl_coercer' not in config_settings[s_name] or
                  not callable(config_settings[s_name]['cl_coercer'])):
                err_exit('Error: setting {0} may not be supplied on the '
                         'command line.\nExiting.'.format(pps(s_name)),
                         STARTUP_EXITVAL)
            try:
                cfg[s_name] = config_settings[s_name]['cl_coercer'](s_val)
            except ValueError:
                err_exit('Error: invalid value for setting {0} ({1}); '
                         'exiting.' .
                         format(s_name, pps(s_val)), STARTUP_EXITVAL)
            cl_config.append(s_name)

    # check for bogus settings
    check_bogus_config()

    # apply defaults, check requirements, and validate
    apply_config_defaults()
    check_config_requirements()
    validate_config()

    # now that the settings are complete, initialize things
    # based on them
    init_logging_main()
    if 'exec_path' in cfg:
        os.environ['PATH'] = cfg['exec_path']
    if 'umask' in cfg:
        os.umask(cfg['umask'])

    # hook for adding more initializations
    if ('process_config_hook' in globals() and
          callable(process_config_hook)):
        process_config_hook()


def render_config():

    """
    Return a string containing the current config settings.
    Also includes config file names and CWD.

    Doesn't print surrounding blank lines; add them if necessary in
    context.

    Dependencies:
        config settings: (all)
        globals: cfg, config_settings, config_file_paths
        modules: os

    """

    def render_config_file_paths():
        """
        Render the list of config files.
        Could probably be inlined, but this is clearer.
        """
        if config_file_paths is None:
            return 'Config file: (none)'
        if len(config_file_paths) == 1:
            return 'Config file: {0}'.format(config_file_paths[0])
        return ('Config files: ' +
                '\n              '.join(config_file_paths))

    def render_settings():
        """Render all of the actual settings."""
        msg = ''
        for s_name, s_dict in config_settings.items():
            if 'no_print' in s_dict and s_dict['no_print']:
                continue
            if 'heading' in s_dict:
                msg += '\n' + s_dict['heading'] + ':\n'
                continue
            if s_name in cfg:
                if 'renderer' in s_dict and callable(s_dict['renderer']):
                    msg += ("cfg['" + s_name + "'] = " +
                            s_dict['renderer'](cfg[s_name]) + "\n")
                else:
                    msg += ("cfg['" + s_name + "'] = " +
                            pps(cfg[s_name]) + "\n")
            else:
                msg += "cfg['" + s_name + "'] is not set\n"
        return msg.strip()

    return (
'''-----------------
Current Settings:
-----------------

(List includes settings that are currently ignored, and may not be valid.)

{0}
CWD: {1}

{2}''' .
            format(render_config_file_paths(), os.getcwd(),
                   render_settings())
           )


def log_cl_config():

    """
    Log the config file paths, CWD, and settings from the command line.

    Dependencies:
        config settings: (any that can be passed on the command line)
        globals: status_logger, config_file_paths, cl_config, cfg,
                 config_settings
        functions: pps()
        modules: os

    """

    # log the list of config files
    if config_file_paths is None:
        status_logger.info('Config file: (none)')
    if len(config_file_paths) == 1:
        status_logger.info('Config file: {0}'.format(config_file_paths[0]))
    else:
        status_logger.info('Config files: {0}'.format(config_file_paths[0]))
        for cfp in config_file_paths[1:]:
            status_logger.info('              ' + cfp)

    # log the current working directory
    status_logger.info('CWD: ' + os.getcwd())

    # log the actual command-line settings
    if not cl_config:
        status_logger.info('No settings passed on the command line.')
    else:
        status_logger.info('Settings passed on the command line:')
        for s_name, s_dict in config_settings.items():
            if (s_name in cl_config and s_name in cfg and
                  'heading' not in s_dict):
                if 'renderer' in s_dict and callable(s_dict['renderer']):
                    status_logger.info("cfg['" + s_name + "'] = " +
                                       s_dict['renderer'](cfg[s_name]))
                else:
                    status_logger.info("cfg['" + s_name + "'] = " +
                                       pps(cfg[s_name]))


def create_blank_config_files(full=False):

    """
    Create blank config files, or print blank config to stdout.

    Files must not exist already.

    Parameters:
        full: if true, include a description of each setting, as well as
              the default (if any)

    Dependencies:
        globals: config_file_paths, config_settings, STARTUP_EXITVAL
        functions: open_create_only(), pps(), err_exit()
        modules: sys, errno, re

    """

    msg = ''

    if not full:
        for s_name, s_dict in config_settings.items():
            if 'no_print' in s_dict and s_dict['no_print']:
                continue
            if 'heading' in s_dict:
                msg += '\n\n### {0} ###\n\n'.format(s_dict['heading'])
                continue
            msg += "#cfg['" + s_name + "'] = \n"

    else:  # full=True
        for s_name, s_dict in config_settings.items():
            if 'no_print' in s_dict and s_dict['no_print']:
                continue
            if 'heading' in s_dict:
                msg += ('\n{0}\n{1}\n{0}\n\n' .
                        format('#' * (len(s_dict['heading']) + 3),
                               '# ' + s_dict['heading']))
                continue
            msg += '#\n'
            if 'descr' in s_dict and s_dict['descr'].strip():
                msg += re.sub('^', '# ', s_dict['descr'].strip(),
                              flags=re.MULTILINE) + '\n'
                msg += '#\n'
            if 'default_descr' in s_dict:
                msg += re.sub('^', '# ',
                              'Default: ' + s_dict['default_descr'].strip(),
                              flags=re.MULTILINE) + '\n'
            elif 'default' in s_dict:
                msg += '# Default: ' + pps(s_dict['default']) + '\n'
            else:
                msg += '# No default.\n'
            msg += '#\n'
            msg += "###cfg['" + s_name + "'] = \n"
            msg += '\n'

    msg = config_file_header + '\n' + msg.strip()

    try:
        if config_file_paths is None:
            print(msg, file=sys.stdout)
        else:
            for cfp in config_file_paths:
                # see open_create_only() and SCRIPT_MODES_DESCR for
                # warnings
                with open_create_only(cfp) as cf_obj:
                    print(msg, file=cf_obj)
    except (OSError, IOError) as e:
        if (e.errno == errno.EEXIST):
            err_exit('Error: specified config file {0} already exists; '
                     'exiting.'.format(pps(cfp)), STARTUP_EXITVAL)
        else:
            if config_file_paths is None:
                # should never happen, but...
                err_exit('Error printing blank config file; exiting.\n'
                         'Details: [Errno {0}] {1}' .
                         format(e.errno, e.strerror),
                         STARTUP_EXITVAL)
            else:
                err_exit('Error creating blank config file {0}; exiting.\n'
                         'Details: [Errno {1}] {2}' .
                         format(pps(cfp), e.errno, e.strerror),
                         STARTUP_EXITVAL)


def create_arg_parser():

    """
    Create and return the command-line-argument parser.

    To change the arguments the script takes, either redefine this
    function, or define create_arg_parser_hook(), which must take and
    return an ArgumentParser object.

    See also process_command_line().

    Dependencies:
        hooks: create_arg_parser_hook()
        globals: script_name, SCRIPT_MODES, SCRIPT_MODES_DESCR
        modules: argparse
        Python: 2.7/3.2, for argparse

    """

    # create the default config file message at the last minute,
    # in case the list was changed
    default_config_files_descr = ('If neither -n nor -f is given, '
                                  'the following will be tried:\n{0}' .
                                  format('\n'.join(default_config_files)))

    # the arguments we have so far
    arg_parser = argparse.ArgumentParser(
        prog=script_name,
        description=default_config_files_descr,
        epilog=SCRIPT_MODES_DESCR,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    cfg_arg_group = arg_parser.add_mutually_exclusive_group()
    cfg_arg_group.add_argument(
        '-n', action='store_true', dest='no_config_files',
        help='use no config file'
    )
    cfg_arg_group.add_argument(
        '-f', action='append', dest='config_file_paths',
        help=('config file paths; can be used more than once')
    )
    arg_parser.add_argument(
        '-o', nargs=2, metavar=('SETTING', 'VALUE'), action='append',
        help='set a config setting'
    )
    arg_parser.add_argument(
         'mode', nargs='?', choices=SCRIPT_MODES, action='store',
         default='run', metavar='MODE',
         help='mode in which to run the script; see below'
    )

    # hook for adding more arguments
    if ('create_arg_parser_hook' in globals() and
          callable(create_arg_parser_hook)):
        arg_parser = create_arg_parser_hook(arg_parser)

    return arg_parser


def license_mode():
    """
    Print a license message to stderr.
    Dependencies:
        globals: LICENSE
        modules: sys
    """
    print(LICENSE, file=sys.stderr)


def config_mode():
    """Wrapper for render_config() to add blank lines."""
    print('\n' + render_config() + '\n')


def status_mode():
    """Wrapper for render_status() to add blank lines."""
    print('\n' + render_status() + '\n')


def statusall_mode():
    """Wrapper for render_status(True) to add blank lines."""
    print('\n' + render_status(True) + '\n')


def createfull_mode():
    """Wrapper for create_blank_config_files(True)."""
    create_blank_config_files(True)


def run_mode():

    """
    Do the actual business of the script.

    To supply a task for the script to do, this function can be
    redefined, or you can define run_mode_hook(), which takes no
    arguments.

    Dependencies:
        config settings: last_started_file
        globals: status_logger, output_logger, start_time, cfg,
                 TASK_NAME, FULL_DATE_FORMAT, STARTUP_EXITVAL
        hooks: run_mode_hook()
        functions: log_cl_config(), check_status(),
                   init_logging_output(), touch_file()
        modules: time

    """

    global start_time

    # log enough so that the config files plus the logs will tell us
    # everything we need to know about this invocation
    # (but don't log all the settings for space and readability reasons)
    log_cl_config()

    # make sure we're clear to keep going
    check_status()

    # get the starting timestamp; can be used for comparisons and
    # filenames, including the output logs
    start_time = time.time()

    # set up the output logger in case we need it, and rotate the logs
    init_logging_output()

    # log that we're starting the task
    status_logger.info('Starting {0}.'.format(TASK_NAME))
    touch_file(cfg['last_started_file'], "cfg['last_started_file']", None,
               use_logger=True, warn_only=False, exit_val=STARTUP_EXITVAL)
    output_logger.info('{0} started {1}.' .
                       format(TASK_NAME.capitalize(),
                              time.strftime(FULL_DATE_FORMAT,
                                            time.localtime())))

    # hook for supplying a task
    if ('run_mode_hook' in globals() and
          callable(run_mode_hook)):
        run_mode_hook()
    else:
        status_logger.warning('Warning: no task supplied; '
                              'not doing anything.')

    # log that we've finished the task
    status_logger.info('{0} finished.'.format(TASK_NAME.capitalize()))
    output_logger.info('{0} finished {1}.' .
                       format(TASK_NAME.capitalize(),
                              time.strftime(FULL_DATE_FORMAT,
                                            time.localtime())))


def process_command_line():

    """
    Process the command-line arguments and do mode-dependent actions.

    To change the modes the script offers, change SCRIPT_MODES and
    SCRIPT_MODES_DESCR and define mode_callbacks_hook(), which must take
    and return the mode_callbacks dict.

    Dependencies:
        hooks: mode_callbacks_hook()
        globals: config_file_paths, default_config_files,
                 NO_ERROR_EXITVAL
        functions: license_mode(), config_mode(), status_mode(),
                   statusall_mode(), silence_lf_alerts(),
                   unsilence_lf_alerts(), disable_script(),
                   enable_script(), clear_lockfile(),
                   create_blank_config_files(), createfull_mode(),
                   run_mode(), create_arg_parser(), process_config()
        modules: argparse, sys
        Python: 2.7/3.2, for argparse

    """

    global config_file_paths

    # mode callback dict
    #
    # format is:
    # 'mode': (function, requires_config_files_to_be_processed_first?)
    mode_callbacks = {
        'license': (license_mode, False),
        'config': (config_mode, True),
        'settings': (config_mode, True),
        'status': (status_mode, True),
        'statusall': (statusall_mode, True),
        'silence': (silence_lf_alerts, True),
        'unsilence': (unsilence_lf_alerts, True),
        'stop': (disable_script, True),
        'disable': (disable_script, True),
        'start': (enable_script, True),
        'enable': (enable_script, True),
        'clearlock': (clear_lockfile, True),
        'unlock': (clear_lockfile, True),
        'create': (create_blank_config_files, False),
        'createfull': (createfull_mode, False),
        'run': (run_mode, True),
    }

    # hook for adding/changing callbacks
    if ('mode_callbacks_hook' in globals() and
          callable(mode_callbacks_hook)):
        mode_callbacks = mode_callbacks_hook(mode_callbacks)

    # parse the command line
    arg_ns = create_arg_parser().parse_args()

    # get the config file paths;
    # be defensive in case the args were changed
    if (hasattr(arg_ns, 'config_file_paths') and
          arg_ns.config_file_paths is not None):
        config_file_paths = arg_ns.config_file_paths
    elif hasattr(arg_ns, 'no_config_files') and arg_ns.no_config_files:
        config_file_paths = None
    else:
        config_file_paths = default_config_files

    # get the script mode; be defensive in case the args were changed
    mode = arg_ns.mode if hasattr(arg_ns, 'mode') else 'run'

    # first deal with the modes that don't require processing the
    # config file or command-line settings
    if not mode_callbacks[mode][1]:
        mode_callbacks[mode][0]()
        sys.exit(NO_ERROR_EXITVAL)

    # process the config file and command-line settings
    process_config(arg_ns)

    # deal with the rest of the modes
    mode_callbacks[mode][0]()
    sys.exit(NO_ERROR_EXITVAL)


###################################
# database calls and manipulations
###################################

###TODO


###########################
# backups and file syncing
###########################

###TODO


########################################################################
#                           RUN STANDALONE
########################################################################

def main():
    process_command_line()

if __name__ == '__main__':
    main()
