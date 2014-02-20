#!/usr/bin/env python


"""
This is the collections submodule for the nori library; see __main__.py
for license and usage information.


DOCSTRING CONTENTS:
-------------------

    1) About and Requirements
    2) API Classes


1) ABOUT AND REQUIREMENTS:
--------------------------

    This submodule provides wrappers for Python's collections classes,
    with expanded functionality.  So far, only OrderedDict is included.


2) API CLASSES:
---------------

    OrderedDict(collections.OrderedDict)
        Adds more insertion functionality to OrderedDict.

        insert_before()
            Insert before a given key.

        insert_after()
            Insert after a given key.

"""


########################################################################
#                             MAIN IMPORTS
########################################################################

#########
# system
#########

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from pprint import pprint as pp  # for debugging


###############
# this package
###############

from . import core


########################################################################
#                         PYTHON VERSION CHECK
########################################################################

# minimum versions for the imports and code below
core.pyversion_check(7, 1)


########################################################################
#                           DEFERRED IMPORTS
########################################################################

import collections as _collections  # OrderedDict requires 2.7/3.1


########################################################################
#                               CLASSES
########################################################################

class OrderedDict(_collections.OrderedDict):

    """Adds more insertion functionality to OrderedDict."""

    def insert_before(self, existing_key, new_key, new_value):
        """
        Insert before a given key.
        If the key is not present, the new key is appended.
        If the new key is already present, the value is updated.
        Parameters:
            existing_key: the key to insert before
            new_key: the key to insert
            new_value: the value to insert
        """
        if existing_key not in self or new_key in self:
            self.update([(new_key, new_value)])
            return
        new_items = []
        for (k, v) in self.items():
            if k == existing_key:
                new_items.append((new_key, new_value))
            new_items.append((k, v))
        self.clear()
        self.update(new_items)


    def insert_after(self, existing_key, new_key, new_value):
        """
        Insert after a given key.
        If the key is not present, the new key is appended.
        If the new key is already present, the value is updated.
        Parameters:
            existing_key: the key to insert after
            new_key: the key to insert
            new_value: the value to insert
        """
        if existing_key not in self or new_key in self:
            self.update([(new_key, new_value)])
            return
        new_items = []
        for (k, v) in self.items():
            new_items.append((k, v))
            if k == existing_key:
                new_items.append((new_key, new_value))
        self.clear()
        self.update(new_items)
