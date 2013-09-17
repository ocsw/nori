#!/usr/bin/env python


"""
This is the SSH submodule for the nori library; see __main__.py for
license and usage information.


DOCSTRING CONTENTS:
-------------------


Requirements
API Variables
API Functions
API Classes
usage
Modification Notes


1) REQUIREMENTS:
----------------

    The SSH functions require the paramiko module:
        https://github.com/paramiko/paramiko

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

nori.supported_features['ssh'] = 'ssh stuff'
nori.available_features.append('ssh')

###TODO: supported_features, available_features,
###config_settings (generator)? incl. requires
###setting hooks
###exitval(s), USAGE


nori.exitvals['ssh_tunnel']=dict(
    num=20,
    descr=(
"""
error opening SSH tunnel
"""
    ),
)

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
