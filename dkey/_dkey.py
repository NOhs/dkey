'''
'''

from warnings import warn as _warn

_warning_types = {'developer': DeprecationWarning, 'end user': FutureWarning}

class deprecate_keys(dict):
    '''
    If keys appear twice, the latter will remain!
    '''
    def __init__(self, dictionary, *args, warning_type='developer'):
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
            details = ''

    message += ' ' + details

    try:
        warning_type = _warning_types[warning_type]
    except KeyError:
        pass

    return {'old key': old_key, 'new key': new_key, 'warning message': message, 'warning type': warning_type}
