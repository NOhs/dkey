import warnings

from nose.tools import with_setup, eq_, assert_raises

from dkey import deprecate_keys, dkey

def setup_check_all_warnings():
    warnings.simplefilter("always")

@with_setup(setup_check_all_warnings)
def test_empty_mapping():
    my_dict = deprecate_keys({'a': 12})

    with warnings.catch_warnings(record=True) as w:
        my_dict['a']
        eq_(len(w), 0)

@with_setup(setup_check_all_warnings)
def test_replacing():
    my_dict = deprecate_keys({'b': 12}, dkey('a', 'b'))
    with warnings.catch_warnings(record=True) as w:
        my_dict['b']
        eq_(len(w), 0)
    with warnings.catch_warnings(record=True) as w:
        my_dict['a']
        eq_(len(w), 1)
        eq_(w[0].category, DeprecationWarning)
        eq_(str(w[0].message), 'Key `a` is deprecated. Use `b` from now on.')

@with_setup(setup_check_all_warnings)
def test_removing():
    my_dict = deprecate_keys({'a': 12}, dkey('a'))
    with warnings.catch_warnings(record=True) as w:
        my_dict['a']
        eq_(len(w), 1)
        eq_(w[0].category, DeprecationWarning)
        eq_(str(w[0].message), 'Key `a` is deprecated. It shouldn\'t be used anymore.')

@with_setup(setup_check_all_warnings)
def test_setitem():
    my_dict = deprecate_keys({'a': 12}, dkey('a'))
    with warnings.catch_warnings(record=True) as w:
        my_dict['a'] = 100
        eq_(len(w), 1)
        eq_(w[0].category, DeprecationWarning)
        eq_(str(w[0].message), 'Key `a` is deprecated. It shouldn\'t be used anymore.')

@with_setup(setup_check_all_warnings)
def test_custom_warning():
    my_dict = deprecate_keys({'a': 12}, dkey('a', warning_type=UserWarning))
    with warnings.catch_warnings(record=True) as w:
        my_dict['a']
        eq_(len(w), 1)
        eq_(w[0].category, UserWarning)
        eq_(str(w[0].message), 'Key `a` is deprecated. It shouldn\'t be used anymore.')

@with_setup(setup_check_all_warnings)
def test_end_user_warning():
    my_dict = deprecate_keys({'a': 12}, dkey('a', warning_type='end user'))
    with warnings.catch_warnings(record=True) as w:
        my_dict['a']
        eq_(len(w), 1)
        eq_(w[0].category, FutureWarning)
        eq_(str(w[0].message), 'Key `a` is deprecated. It shouldn\'t be used anymore.')

@with_setup(setup_check_all_warnings)
def test_developer_warning():
    my_dict = deprecate_keys({'a': 12}, dkey('a', warning_type='developer'))
    with warnings.catch_warnings(record=True) as w:
        my_dict['a']
        eq_(len(w), 1)
        eq_(w[0].category, DeprecationWarning)
        eq_(str(w[0].message), 'Key `a` is deprecated. It shouldn\'t be used anymore.')

def test_deprecated_in():
    my_dict = deprecate_keys({'a': 12}, dkey('a', deprecated_in='1.81.1'))
    with warnings.catch_warnings(record=True) as w:
        my_dict['a']
        eq_(len(w), 1)
        eq_(w[0].category, DeprecationWarning)
        eq_(str(w[0].message), 'Key `a` is deprecated since version 1.81.1. It shouldn\'t be used anymore.')

def test_removed_in():
    my_dict = deprecate_keys({'a': 12}, dkey('a', removed_in='2.0'))
    with warnings.catch_warnings(record=True) as w:
        my_dict['a']
        eq_(len(w), 1)
        eq_(w[0].category, DeprecationWarning)
        eq_(str(w[0].message), 'Key `a` is deprecated. It will be removed in version 2.0. It shouldn\'t be used anymore.')

def test_added_details():
    my_dict = deprecate_keys({'a': 12}, dkey('a', details='Get rid of it!'))
    with warnings.catch_warnings(record=True) as w:
        my_dict['a']
        eq_(len(w), 1)
        eq_(w[0].category, DeprecationWarning)
        eq_(str(w[0].message), 'Key `a` is deprecated. Get rid of it!')

def test_number_of_keys_incorrect():
    with assert_raises(ValueError):
        dkey()

    with assert_raises(ValueError):
        dkey('a', 'b', 'c')