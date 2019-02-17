*********************
Configuration Options
*********************

To deprecate a key in a dict, it has to be wrapped using :any:`dkey.deprecate_keys`.
``dkey`` offers two different ways to deprecate a key. Either, the key is deprecated
as it will be replace by a different one, or it will be removed completely in the future.
In both scenarios it is important, that during the deprecation period, the old keys
must still work the same way as before.

Removing a key
==============

To deprecate a key and warn that it will be removed in the future, you wrap
your dict using :any:`dkey.deprecate_keys` and pass it the deprecated key
using :any:`dkey.dkey`::

    from dkey import deprecate_keys, dkey

    def customer_info():
        return deprecate_keys({
                'name': 'Smith',
                'age': 24,
                'cleartext password': 'password'
            },
            dkey('cleartext password'))

Should someone now try to access the ``cleartext password`` key, a :any:`DeprecationWarning`
is generated::

    print(customer_info()['cleartext password'])
    # Wil warn with a DeprecationWarning:
    # Key `cleartext password` is deprecated. It shouldn't be used anymore.

An automatically generated deprecation warning is used that warns developers
to no longer use this key in the future.

.. note::

    A :any:`DeprecationWarning` is only shown when you set your warning filters appropriately.
    For other warning types that are shown by default, check :ref:`this section <label_custom_warning>`.

Replacing a key
===============

Another scenario you might run into is that you want to rename a key (for various reasons), and again
you want to give people time to adapt. For this you can do the following::

    from dkey import deprecate_keys, dkey

    def customer_info():
        return deprecate_keys({
                'first name': 'Adam',
                'last name': 'Smith',
                'age': 24,
            },
            dkey('name', 'last name'))

Again we use the :any:`deprecate_keys` function. This time we pass two string to :any:`dkey.dkey`: The old
key and the new key people should be using. Both keys will point to the same object.
The result is again a warning if people use the old key::

    print(customer['name'])
    # Wil raise a DeprecationWarning:
    # Key `name` is deprecated. Use `first name` from now on.

And again an automatically generated deprecation warning is used that also informs developers
about which key to use instead.

More configuration options
==========================

In case the default way warnings are generated are not what you need, :any:`dkey` offers
several ways to customise how deprecated keys are treated:

- A version number can be given to indicate since when a key is deprecated
- A version number can be given to indicate when a key is definitively removed
- A custom message can be given to add more information about why the change happend and how to adapt
- A custom warning type can be given to align the deprecation warnings to an existing project

Version numbers
---------------

If you have a well organised code project, you will normally also want to communicate since when a feature is
deprecated and when it finally will be removed. You can pass those details to :any:`dkey.dkey`::

    from dkey import deprecate_keys, dkey

    def customer_info():
        return deprecate_keys({
                'first name': 'Adam',
                'last name': 'Smith',
                'age': 24,
            },
            dkey('name', 'last name', deprecated_in='1.1.12', removed_in='2.0.0'))

Which will result in the warning:

    Key `name` is deprecated since version 1.1.12. It will be removed in version 2.0.0.
    Use `first name` from now on.

Custom message
--------------

Sometimes, changes are not as simple as `a` was replaced with `b`. In these scenarios,
you can provide a custom message with more information::

    def customer_info():
        return deprecate_keys({
                'first name': 'Adam',
                'last name': 'Smith',
                'age': 24,
            },
            dkey('name', 'last name',
                details='`name` has been replaced by the two keys `first name` and `last name`.'))

Which will result in the warning:

    Key `name` is deprecated.
    `name` has been replaced by the two keys `first name` and `last name`.

.. _label_custom_warning:

Custom warning type
-------------------

By default, a :any:`DeprecationWarning` is used. This warning does not appear for end users. If you have
deprecation warnings that are actually meant for end users and not just for developers, you can change
the warning type::

    from dkey import deprecate_keys, dkey

    def customer_info():
        return deprecate_keys({
                'name': 'Smith',
                'age': 24,
                'cleartext password': 'password'
            },
            dkey('cleartext password', warning_type='end user'))

Which will generate a :any:`FutureWarning`. :any:`FutureWarning` is a warning type that is shown
to end users by default. If you want to show your own warning type, this is also possible.
Just hand your warning type to ``warning_type`` instead of the string `'end user'` and it
will be used to spawn the warning::

    from dkey import deprecate_keys, dkey

    class UltimateWarning(FutureWarning):
        pass

    def customer_info():
        return deprecate_keys({
                'name': 'Smith',
                'age': 24,
                'cleartext password': 'password'
            },
            dkey('cleartext password', warning_type=UltimateWarning))

.. note::

    In order for your custom warning type to work it has to be compatible with the :any:`warnings.warn`
    function.



Limitations
-----------

- No automatic doc-string adaptations are possible as of now

.. automodule:: dkey
