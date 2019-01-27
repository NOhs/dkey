"""Implementation file of the :any:`dkey` module."""

from warnings import warn as _warn

_warning_types = {'developer': DeprecationWarning, 'end user': FutureWarning}

_DEFAULT = object()

class deprecate_keys(dict):
    """Wrapper for dicts that allows to set certain keys as deprecated."""

    def __init__(self, dictionary, *args):
        """
        Construct the wrapper class.

        Parameters
        ----------
        dictionary: dict
            The dictionary to wrap
        *args
            Zero or more keys that should show deprecation warnings.
            Use :any:`dkey.dkey` for each key.

        Warns
        -----
        ArbitraryWarning
            If a deprecated key is used, shows a warning
            that was set for this key. (see also :any:`dkey.dkey`)

        """
        super().__init__()
        self._key_mappings = {}
        _key_mappings_new = {}
        for mapping in args:
            self._key_mappings[mapping['old key']] = mapping
            _key_mappings_new[mapping['new key']] = mapping
            if not mapping['new key'] in dictionary:
                raise ValueError(f'The new key `{mapping["new key"]}` which should replace the '
                                 +f'old key `{mapping["old key"]}` is not in the given dict.')

        for key, value in dictionary.items():
            try:
                mapping = _key_mappings_new[key]
                if not (mapping['old key'] == mapping['new key']):
                    super().__setitem__(mapping['old key'], value)
            except KeyError:
                # Not deprecated.
                pass

            super().__setitem__(key, value)

    def __getitem__(self, key):
        """
        Get the value of the item of the given key `key`.

        Warns if the given key is deprecated. If the key does not exist, it will behave
        the same as a normal dict, i.e. it will raise a :any:`KeyError`.

        Parameters
        ----------
        key
            The key for which to return the value

        Returns
        -------
        value
            The value stored for the given key

        Raises
        ------
        KeyError
            If the key is not found

        Warns
        -----
        CustomWarning
            Warns with the warning stored for the given key if the key is deprecated.

        """
        self._check_deprecated(key)

        return super().__getitem__(key)

    def __setitem__(self, key, value):
        """
        Set the value of the item of the given key `key` to `value`.

        Warns if the given key is deprecated.

        Parameters
        ----------
        key
            The key under which to store the given value
        value
            The value to store

        Warns
        -----
        CustomWarning
            Warns with the warning stored for the given key if the key is deprecated.
            Further access to the given key will not spawn additional warnings.

        """
        if self._check_deprecated(key):
            del self._key_mappings[key]

        super().__setitem__(key, value)

    def __delitem__(self, key):
        """
        Remove the item with key `key` and its associated value.

        Warns if the given key is deprecated.

        Parameters
        ----------
        key
            The key of the item which to remove.

        Raises
        ------
        KeyError
            Raises a :any:`KeyError` if the given key does not exist

        Warns
        -----
        CustomWarning
            Warns with the warning stored for the given key if the key is deprecated.
            Further access to the given key will not spawn additional warnings.

        """
        self.pop(key)

    def __contains__(self, key):
        """
        Return `True` if the given key `key` is in this dict, else `False`.

        Warns if the given key is deprecated.

        Parameters
        ----------
        key
            The key to search in this dict.

        Returns
        -------
        IsInDict : bool
            `True` if the given key is in this dict. `False`, otherwise.

        Warns
        -----
        CustomWarning
            Warns with the warning stored for the given key if the key is deprecated.

        """
        if self._check_deprecated(key):
            return True
        else:
            return super().__contains__(key)

    def __iter__(self):
        """
        Return an iterator over the keys of the dictionary.

        Warns for each deprecated item accessed.

        Returns
        -------
        Iterator : iterator
            An iterator over the wrapped dict

        Warns
        -----
        CustomWarning
            Warns whenever a deprecated item in the dict is returned. Each item
            will warn with its set warning type and message.

        """
        for key in iter(super().keys()):
            self._check_deprecated(key)
            yield key

    def clear(self):
        """
        Remove all entries from the dict.

        Will also remove all deprecation warnings and all keys.
        """
        self._key_mappings = dict()
        super().clear()

    def copy(self):
        """
        Return a shallow copy of this wrapped dict.

        Will return a wrapped dict that, as the original, will warn
        with the deprecation warnings set for this dict.

        Returns
        -------
        copy : deprecate_keys
            A shallow copy of the underlying dict and a shallow
            copy of the underlying deprecation key structure.

        """
        output = deprecate_keys(super())
        output._key_mappings = self._key_mappings.copy()

        return output

    def get(self, key, default=None):
        """
        Get the value stored under `key` or `default` if this key doesn't exist.

        This function is the same as :any:`deprecate_keys.__getitem__` except that
        it does not throw for non existing keys, but returns the given default
        value instead.

        Parameters
        ----------
        key
            The key for which to return the value
        default, optional
            The value to return, if the given key is not stored in the dict. Defaults
            to :any:`None` if not given.

        Returns
        -------
        value
            The value stored for `key` or `default` if `key` is not in the dict.

        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key, default=_DEFAULT):
        """
        Remove and return the item with key `key`.

        If the key is not in the dict and no default value is set,
        this function will raise an exception. If a default value is
        given, this value will be returned instead.

        Parameters
        ----------
        key
            The key to pop
        default : optional
            The value to return if the given `key` is not in the dict.
            If non is given, an exception is raised instead.

        Returns
        -------
        value
            The value of the key given or the given default value, or
            if no default value is given, an exception is raised.

        Raises
        ------
        KeyError
            If `key` is not in the dict and no default value is given,
            this function raises a :any:`KeyError`.

        Warns
        -----
        CustomWarning
            Warns if the popped item is a deprecated key. The deprecation
            information for this key is removed.

        """
        if self._check_deprecated(key):
            del self._key_mappings[key]

        if default is _DEFAULT:
            return super().pop(key)
        else:
            return super().pop(key, default)

    def popitem(self):
        """
        Pop an item from the dict.

        This function has the same behaviour as :any:`dict.popitem`. Therefore,
        for Python < 3.6 this function will pop an arbitrary item, whereas for
        Python >= 3.6 this function will raise the last item added to this dict.
        If the dict is empty, this function will raise a :any:`KeyError`.

        Returns
        -------
        key
            The key popped
        value
            The associated value of the popped key

        Raises
        ------
        KeyError
            If the dict is empty.

        Warns
        -----
        CustomWarning
            Warns if the popped item is a deprecated key. The deprecation
            information for this key is removed.

        """
        item = super().popitem()

        if self._check_deprecated(item[0]):
            del self._key_mappings[item[0]]

        return item

    def items(self):
        """
        Return a new view of the dictionary's items: iterator of `(key, value)` pairs.

        Works the same as the plain :any:`dict.items` function except that
        it warns about all deprecated keys contained before returning.

        Returns
        -------
        dict_items
            Basically an iterator over `(key, value)` pairs of the dict. For more information
            about dict views see: `dictionary view <https://docs.python.org/3/library/stdtypes.html#dict-views>`_

        Warns
        -----
        CustomWarning
            Warns for each deprecated item in the dictionary before returning.

        """
        for mapping in self._key_mappings:
            self._warn_deprecation(mapping)

        return super().items()

    def values(self):
        """
        Return a new view of the dictionary's values.

        Works the same as the plain :any:`dict.values` function except that
        it warns about all deprecated keys associated with returned values before returning
        the view.

        Returns
        -------
        dict_values
            Basically an iterator over the contained values of the dict. For more information
            about dict views see: `dictionary view <https://docs.python.org/3/library/stdtypes.html#dict-views>`_

        Warns
        -----
        CustomWarning
            Warns for each deprecated item in the dictionary before returning.

        """
        for mapping in self._key_mappings.values():
            self._warn_deprecation(mapping)

        return super().values()

    def keys(self):
        """
        Return a new view of the dictionary's keys.

        Works the same as the plain :any:`dict.keys` function except that
        it warns about all deprecated keys before returning the view.

        Returns
        -------
        dict_keys
            Basically an iterator over the contained keys of the dict. For more information
            about dict views see: `dictionary view <https://docs.python.org/3/library/stdtypes.html#dict-views>`_

        Warns
        -----
        CustomWarning
            Warns for each deprecated item in the dictionary before returning.

        """
        for mapping in self._key_mappings:
            self._warn_deprecation(mapping)

        return super().keys()

    def __len__(self):
        """
        Return the number of items in the dict.

        Will raise warnings, if the dict contains deprecated values. One for
        each deprecated value.

        Returns
        -------
        int
            The number of items in the dict

        Warns
        -----
        CustomWarning
            Warns for each deprecated item in the dictionary before returning.

        """
        for mapping in self._key_mappings.values():
            self._warn_deprecation(mapping)

        return super().__len__()

    def _check_deprecated(self, key):
        """
        Check if the given key is deprecated and warn if it is.

        Warns using the warning type and message stored with the key and returns True.
        Otherwise it returns False and does not warn.

        Parameters
        ----------
        key
            The key to look up in the dict of deprecated keys

        Returns
        -------
        deprecated : bool
            Whether the key is deprecated or not

        """
        try:
            mapping = self._key_mappings[key]
            self._warn_deprecation(mapping)

            return True
        except KeyError:
            return False

    def _warn_deprecation(self, mapping):
        """
        Warn with the given deprecated key mapping.

        Uses the default Python :any:`warnings.warn` function
        extracting the `'warning message'` and `'warning type'`
        from the given mapping (dict).

        Parameters
        ----------
        mapping: dict
            Dict that needs to contain the two keys `'warning message'`,
            which should be a :any:`str`, and `'warning type'` which needs
            to be a valid subclass of :any:`Exception`.

        Warns
        -----
        CustomWarning
            Warns with the given message and warning type.

        """
        _warn(mapping['warning message'], mapping['warning type'])


def dkey(*args, deprecated_in=None, removed_in=None, details=None, warning_type='developer'):
    """
    Convert a key into a deprecation lookup dict.

    To use the :any:`dkey.deprecate_keys` function it is easiest to generate
    its input with this function. This function generates:

    - A key removed deprecation warning object if one key is provided
    - A key replaced deprecation warning object if two keys are provided

    Parameters
    ----------
    *args
        One or two keys. If one key is passed, it is assumed that this
        key will be removed in the future. If two keys are passed, it is
        assumed that the second key is the replacement for the first one.
    deprecated_in : str, optional
        Version in which this key was deprecated. If given, will appear in the
        warning message.
    removed_in : str, optional
        Version in which this key will be removed and will no longer work. If given,
        will appear in the warning message.
    details : str, optional
        Will remove the default final sentence (do no longer use, or use `xxx` from now on).
    warning_type : {'developer', 'end user', ArbitraryWarning}, optional
        The warning type to use when the old key is accessed

        By default, deprecation warnings are intended for developers only which
        means a any:`DeprecationWarning` is used which isn't shown to end users.
        If it should be shown to end users, this can be done by passing 'end user'
        which will raise :any:`FutureWarning`. If you want to use your custom warning
        type this is also possible.

        .. note:: Your custom warning must work with :any:`warnings.warn`

    Returns
    -------
    dict
        A dict that can be used as a deprecated key input for :any:`dkey.deprecate_keys`.

    Raises
    ------
    ValueError
        If zero or more than two keys are passed to this function.

    """
    if len(args) == 0:
        raise ValueError('No key given')
    elif len(args) > 2:
        raise ValueError(f'More than three keys were given ({len(args)}). Maximum allowed: 2.')

    old_key = args[0]

    if len(args) == 1:
        new_key = old_key
        replace = False
    else:
        new_key = args[1]
        replace = True

    message = f'Key `{old_key}` is deprecated'
    if deprecated_in:
        message += f' since version {deprecated_in}'
    message += '.'
    if removed_in:
        message += f' It will be removed in version {removed_in}.'
    if details is None:
        if replace:
            details = f'Use `{new_key}` from now on.'
        else:
            details = 'It shouldn\'t be used anymore.'

    message += ' ' + details

    try:
        warning_type = _warning_types[warning_type]
    except KeyError:
        pass

    return {'old key': old_key, 'new key': new_key, 'warning message': message, 'warning type': warning_type}
