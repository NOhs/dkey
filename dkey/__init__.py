"""Module containing tools to deprecate the use of selected keys in a given dictionary.

This module provides:

deprecate_keys
==============
Class to wrap a dict to deprecate some keys in it.

dkey
====
Function to generate deprecated keys.

"""
from ._dkey import deprecate_keys as deprecate_keys
from ._dkey import dkey as dkey
