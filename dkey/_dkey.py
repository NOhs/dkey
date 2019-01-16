from warnings import warn as _warn

_warning_types = {'developer': DeprecationWarning, 'end user': FutureWarning}

class deprecate_keys(dict):
    '''
    Wrapper for dicts that allows to set certain keys as deprecated.

    Attributes
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
    '''

    def __init__(self, dictionary, *args):
        super().__init__(dictionary)
        self._key_mappings = {}
        for mapping in args:
            self._key_mappings[mapping['old key']] = mapping

    def __getitem__(self, key):
        key = self._check_deprecated(key)
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        key = self._check_deprecated(key)
        return super().__setitem__(key, value)

    def _check_deprecated(self, key):
        '''Checks if the given key is in the dict of deprecated keys. If it is
        it warns and returns the appropriate new key. Which is in case of a
        removal the old key, and in case of a replacement the new key.

        Parameters
        ----------
        key
            The key to look up in the dict of deprecated keys

        Returns
        -------
        key
            The old key, if the key will be removed at some point. The new
            key if the key has a replacement.
        '''
        try:
            mapping = self._key_mappings[key]
            _warn(mapping['warning message'], mapping['warning type'])
            key = mapping['new key']
        except KeyError:
            pass

        return key


def dkey(*args, deprecated_in=None, removed_in=None, details=None, warning_type='developer'):
    '''Function that converts a key into a deprecation lookup dict.

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
    '''

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
