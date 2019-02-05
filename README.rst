****************************
DKey - Deprecating Dict Keys
****************************

.. image:: https://travis-ci.org/NOhs/dkey.svg?branch=master
    :target: https://travis-ci.org/NOhs/dkey
    :alt: travis

.. image:: https://coveralls.io/repos/github/NOhs/dkey/badge.svg?branch=master
    :target: https://coveralls.io/github/NOhs/dkey?branch=master
    :alt: coveralls

.. image:: https://readthedocs.org/projects/dkey/badge/?version=latest
    :target: https://dkey.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs

.. image:: https://badge.fury.io/py/dkey.svg
    :target: https://badge.fury.io/py/dkey
    :alt: PyPI

.. image:: https://img.shields.io/badge/License-MIT-brightgreen.svg
    :target: https://opensource.org/licenses/MIT
    :alt: license: MIT

.. image:: https://api.codacy.com/project/badge/Grade/24cc8c86e18b44d2b3cb14270bca97bb
    :target: https://www.codacy.com/app/NOhs/dkey?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NOhs/dkey&amp;utm_campaign=Badge_Grade
    :alt: codacy

.. image:: https://requires.io/github/NOhs/dkey/requirements.svg?branch=master
     :target: https://requires.io/github/NOhs/dkey/requirements/?branch=master
     :alt: requires.io

The ``dkey`` module allows you to deprecate the use of selected keys in a given dictionary thus making API changes involving
dictionaries less disruptive. To learn more about how to use it head over to the `Documentation <https://dkey.readthedocs.io/>`_.

============
Installation
============

To install this package simply use pip::

    pip install dkey

=============
Usage example
=============

Let's say we have a dict with an old key that we want to replace with a new one.


.. image:: https://raw.githubusercontent.com/nohs/dkey/master/img/usage.gif
