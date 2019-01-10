import warnings

from nose.tools import with_setup

from dkey import deprecate_keys, dkey

def setup_check_all_warnings():
    warnings.simplefilter("always")

@with_setup(setup_check_all_warnings)
def test_empty_mapping():
    my_dict = deprecate_keys({'a': 12})

    with warnings.catch_warnings(record=True) as w:
        my_dict['a']
        assert len(w) == 0

@with_setup(setup_check_all_warnings)
def test_replacing():
    my_dict = deprecate_keys({'b': 12}, dkey('a', 'b'))
    with warnings.catch_warnings(record=True) as w:
        my_dict['b']
        my_dict['a']
        assert len(w) == 1

@with_setup(setup_check_all_warnings)
def test_removing():
    my_dict = deprecate_keys({'a': 12}, dkey('a'))
    with warnings.catch_warnings(record=True) as w:
        my_dict['a']
        assert len(w) == 1
