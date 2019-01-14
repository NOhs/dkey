from warnings import warn as _warn

_warning_types = {'developer': DeprecationWarning, 'end user': FutureWarning}

class deprecate_keys(dict):
    '''
    Wrapper for dicts that allow to set certain keys as deprecated.

    Attributes
    ----------
    dictionary: dict
        The dictionary to wrap
    *args
        Zero or more keys that should raise deprecation warnings.
        Use :any:`dkey.dkey` for each key.

    Warns
    -----
    ArbitraryWarning
        If a deprecated key is used, raises a warning
        that was set for this key. (see also :any:`dkey.dkey`)
    '''

    def __init__(self, dictionary, *args):
        super().__init__(dictionary)
        self._key_mappings = {}
        for mapping in args:
            self._key_mappings[mapping['old key']] = mapping

    def __getitem__(self, key):
        try:
            mapping = self._key_mappings[key]
            _warn(mapping['warning message'], mapping['warning type'])
            key = mapping['new key']
        except KeyError:
            pass

        return super().__getitem__(key)


def dkey(*args, deprecated_in=None, removed_in=None, details=None, warning_type='developer'):
    '''Function that converts a key into a deprecation lookup dict.

    To use the :any:`dkey.deprecate_keys` functions it is easiest to generate
    the input with this function. This function generates:

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
        By default, deprecation warnings are intended for developers only which
        means a any:`DeprecationWarning` is used which isn't shown to end users
        in default setups. If it should be shown to end users, this can be done
        by passing 'end user' which will raise :any:`FutureWarning`. If you want
        to use your custom warning type this is also possible.

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
            details = f' Please use `{new_key}` from now on.'
        else:
            details = ' Please do no longer use it.'

    message += ' ' + details

    try:
        warning_type = _warning_types[warning_type]
    except KeyError:
        pass

    return {'old key': old_key, 'new key': new_key, 'warning message': message, 'warning type': warning_type}
