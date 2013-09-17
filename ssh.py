#!/usr/bin/env python


"""
This is the SSH submodule for the nori library; see __main__.py for
license and usage information.


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
    The SSH functions require the paramiko module:
        https://github.com/paramiko/paramiko


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

from __future__ import print_function


#########
# add-on
#########

try:
    import paramiko
except ImportError:
    pass


###############
# this package
###############

from . import nori


########################################################################
#                              VARIABLES
########################################################################

############
# constants
############


##################
# status and meta
##################

# submodule-specific exit values
nori.exitvals['submodule']=dict(
    num=999,
    descr=(
"""
error doing submodule stuff
"""
    ),
)

# submodule-specific features
nori.supported_features['submodule'] = 'submodule stuff'
if paramiko in sys.modules:
    nori.available_features.append('submodule')


#########################
# configuration settings
#########################

#
# submodule-specific config settings
#

config_settings['submodule_setting'] = dict(
    descr=(
"""
Submodule stuff.
"""
    ),
    default='submodule stuff',
    requires='submodule',
)


#############
# hook lists
#############


############
# resources
############


########################################################################
#                               FUNCTIONS
########################################################################

#####################################
# startup and config file processing
#####################################

def validate_config():
    """
    Validate submodule-specific config settings.
    """
    pass


##################################
# SSH remote commands and tunnels
##################################

def ssh_is_supported():
    """
    Test if SSH is supported.
    Dependencies:
        modules: (paramiko), sys
    """
    return 'paramiko' in sys.modules


def check_ssh_is_supported():
    """
    If there is no SSH support, exit with an error.
    Dependencies:
        globals: INTERNAL_EXITVAL
        functions: err_exit()
        modules: paramiko, sys
    """
    if not ssh_is_supported():
        err_exit('Internal Error: SSH function called, but '
                 'there is no SSH support; exiting.',
                 INTERNAL_EXITVAL)


#
#    import paramiko, base64
#    key = paramiko.RSAKey(data=base64.decodestring('AAA...'))
#    client = paramiko.SSHClient()
#    client.get_host_keys().add('ssh.example.com', 'ssh-rsa', key)
#    client.connect('ssh.example.com', username='strongbad', password='thecheat')
#    stdin, stdout, stderr = client.exec_command('ls')
#    for line in stdout:
#        print '... ' + line.strip('\n')
#    client.close()

########################################################################
#                           RUN STANDALONE
########################################################################

def main():
    process_command_line()

if __name__ == '__main__':
    main()
