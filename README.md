# dkey - deprecating dict keys

This module provides a thin wrapper that can be used to set certain keys in dictionaries as deprecated.
If you have e.g. a function that returns a dict, you can wrap it to declare certain keys as deprecated, which is not
possible with the default `dict` implementation.

## Usage example

### Replacing or removing keys

```python
from dkey import deprecate_keys

def customer_info():
  # old version
  # return {
  #    'name': 'Smith',
  #    'age': 24,
  #    'cleartext password': 'password'
  # }
  # new version, 'name' does not have to appear anymore in the dict
  return deprecate_keys(
    {
        'first name': 'Adam',
        'last name': 'Smith',
        'age': 24
    },
    dkey('name', 'last name'),
    dkey('cleartext password',))

def my_func():
    customer = customer_info()

    # Worked with the old version, will warn to use 'last name' in the future
    # and will return 'last name' which is the replacement for 'name'
    print(customer['name'])

    # Worked with the old version, will warn that in future release
    # 'cleartext password' will no longer be available
    print(customer['cleartext password'])
```

Several things are done here:

- To ensure nothing breaks, access to the new dict with the old key still works
- For key replacements, old keys are simply mapped to the new object (no duplication
  is created)
- For key removals, old keys will raise a warning but are still in the dict
- To ensure developers are made aware of the deprecation a `DeprecationWarning` is
  raised which automatically tells which old key to replace with what, or which
  key is no longer available.

## Customisation and configuration

To give more specialised warning messages or to indicate since when this function is deprecated, etc. please
have a look at the documentation website which explains all available options:

[Documentation](https://dkey.readthedocs.io/)

## Limitations

- No deprecation warnings can be generated to indicate that the number of entries of the dict has change.
- No automatic docstring changes are possible at the moment

