"""Module containing tools to deprecate the use of selected keys in a given dictionary.

This module provides:

deprecate_keys
==============
Class to wrap a dict to deprecate some keys in it.

dkey
====
Function to generate deprecated keys.

__version__
===========
A string indicating which version of dkey is currently used.

version_info
============
A tuple containing the currently used version.

"""
from ._dkey import deprecate_keys as deprecate_keys
from ._dkey import dkey as dkey

from pbr.version import VersionInfo

_v = VersionInfo('mgen').semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()
