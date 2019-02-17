"""Test module testing all features of dkey."""

import warnings
import unittest
from contextlib import contextmanager
import re
from subprocess import check_output, STDOUT, CalledProcessError
import sys
from tempfile import NamedTemporaryFile

from dkey import deprecate_keys, dkey

class dkey_test_case(unittest.TestCase):
    def test_number_of_keys_incorrect(self):
        with self.assertRaises(ValueError):
            dkey()

        with self.assertRaises(ValueError):
            dkey('a', 'b', 'c')

class deprecate_keys_test_case(unittest.TestCase):
    @contextmanager
    def assertNotWarns(self, warning):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            yield
            if len(w) > 0:
                self.assertNotEqual(w[0].category, warning)
            else:
                self.assertTrue(True)

    @contextmanager
    def assertWarnsHere(self, warning):
        with self.assertWarns(warning) as w:
            yield

        self.assertIn('test_dkey.py', w.filename)

    def get_key_assertions(self):
        return ((key, self.assertWarnsHere if self.is_deprecated(key) else self.assertNotWarns) for key in (x[0] for x in self.example_case['items']))

    def is_deprecated(self, key):
        return (key == self.example_case['removed key']) or (key == self.example_case['replaced key'][0])

    def setUp(self):
        self.example_case = {'items': (('a', 12), ('b', 13), ('c', 13), ('d', 14)), 'removed key': 'a', 'replaced key': ('b', 'c'), 'no key': 'f', 'default value': 100}

        self.regular_dict = dict(self.example_case['items'])

        items_for_dkey = (item for item in self.example_case['items'] if item[0] != self.example_case['replaced key'][0])
        dkeys = [dkey(self.example_case['removed key']), dkey(*self.example_case['replaced key'])]
        self.deprecated_dict = deprecate_keys(dict(items_for_dkey), *dkeys)

    def _refill_dict(self):
        for key, val in self.example_case['items']:
            self.deprecated_dict[key] = val

    def test_wrong_new_key(self):
        with self.assertRaises(ValueError):
            deprecate_keys({'a': 12}, dkey('b', 'c'))

        with self.assertRaises(ValueError):
            deprecate_keys({'a': 12}, dkey('b'))

    def test_empty_mapping(self):
        my_dict = deprecate_keys({'a': 12})
        warnings.simplefilter("always")
        with warnings.catch_warnings(record=True) as w:
            self.assertEqual(12, my_dict['a'])
            self.assertEqual(len(w), 0)

    def test_pop(self):
        for key, assertion in self.get_key_assertions():
            with assertion(DeprecationWarning):
                val = self.deprecated_dict.pop(key)
            self.assertEqual(self.regular_dict.pop(key), val)

        self.assertEqual(len(self.regular_dict), len(self.deprecated_dict))

        with self.assertNotWarns(DeprecationWarning):
            self._refill_dict()

        with self.assertRaises(KeyError):
            self.deprecated_dict.pop(self.example_case['no key'])

    def test_pop_default(self):
        for key, assertion in self.get_key_assertions():
            with assertion(DeprecationWarning):
                val = self.deprecated_dict.pop(key, self.example_case['default value'])
            self.assertEqual(self.regular_dict.pop(key, self.example_case['default value']), val)

        self.assertEqual(len(self.regular_dict), len(self.deprecated_dict))

        with self.assertNotWarns(DeprecationWarning):
            self._refill_dict()

        with self.assertNotWarns(DeprecationWarning):
            self.assertEqual(self.deprecated_dict.pop(self.example_case['no key'], self.example_case['default value']), self.regular_dict.pop(self.example_case['no key'], self.example_case['default value']))

    def test_popitem(self):
        num_deprecations = 0
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            while self.deprecated_dict:
                l = len(w)
                dep_item = self.deprecated_dict.popitem()
                self.assertEqual(dep_item, self.regular_dict.popitem())
                if self.is_deprecated(dep_item[0]):
                    self.assertEqual(len(w), l + 1)
                    num_deprecations = num_deprecations + 1

        with self.assertNotWarns(DeprecationWarning):
                self._refill_dict()

    def test_clear(self):
        with self.assertNotWarns(DeprecationWarning):
            self.deprecated_dict.clear()
            self._refill_dict()

    def test_del(self):
        for key, assertion in self.get_key_assertions():
            with assertion(DeprecationWarning):
                del self.deprecated_dict[key]
            with self.assertRaises(KeyError):
                del self.deprecated_dict[key]

        with self.assertNotWarns(DeprecationWarning):
            self._refill_dict()

    def _test_in(self, dictionary):
        for key, assertion in self.get_key_assertions():
            with assertion(DeprecationWarning):
                self.assertTrue(key in dictionary)

        with self.assertNotWarns(DeprecationWarning):
            self.assertFalse(self.example_case['no key'] in dictionary)

    def test_in(self):
        self._test_in(self.deprecated_dict)

    def test_iter(self):
        num_deprecations = 0
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            for key in self.deprecated_dict:
                if self.is_deprecated(key):
                    self.assertEqual(len(w), num_deprecations + 1)
                    num_deprecations = len(w)

    def test_copy(self):
        dict_copy = self.deprecated_dict.copy()
        self._test_in(dict_copy)

    def test_get(self):
        for key, assertion in self.get_key_assertions():
            with assertion(DeprecationWarning):
                val = self.deprecated_dict.get(key)
            self.assertEqual(self.regular_dict.get(key), val)

        with self.assertNotWarns(DeprecationWarning):
            self.assertEqual(self.regular_dict.get(self.example_case['no key']), self.deprecated_dict.get('no key'))

    def test_get_default(self):
        for key, assertion in self.get_key_assertions():
            with assertion(DeprecationWarning):
                val = self.deprecated_dict.get(key, self.example_case['default value'])
            self.assertEqual(self.regular_dict.get(key, self.example_case['default value']), val)

        with self.assertNotWarns(DeprecationWarning):
            self.assertEqual(self.deprecated_dict.get(self.example_case['no key'], self.example_case['default value']), self.regular_dict.get(self.example_case['no key'], self.example_case['default value']))

    def test_replacing(self):
        with self.assertWarnsRegex(DeprecationWarning, f'Key `{self.example_case["replaced key"][0]}` is deprecated. Use `{self.example_case["replaced key"][1]}` from now on.'):
            self.assertEqual(self.deprecated_dict[self.example_case['replaced key'][0]], self.regular_dict[self.example_case['replaced key'][0]])

        with self.assertNotWarns(DeprecationWarning):
            self.assertEqual(self.deprecated_dict[self.example_case['replaced key'][1]], self.regular_dict[self.example_case['replaced key'][1]])

    def test_removing(self):
        with self.assertWarnsRegex(DeprecationWarning, f'Key `{self.example_case["removed key"][0]}` is deprecated. It shouldn\'t be used anymore.'):
            self.assertEqual(self.deprecated_dict[self.example_case['removed key']], self.regular_dict[self.example_case['removed key']])

    def test_setitem(self):
        for key, assertion in self.get_key_assertions():
            with assertion(DeprecationWarning):
                self.deprecated_dict[key] = self.example_case['default value']

            with self.assertNotWarns(DeprecationWarning):
                self.deprecated_dict[key] = self.example_case['default value']

    def test_items(self):
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(self.deprecated_dict.items(), self.regular_dict.items())

    def test_values(self):
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(set(self.deprecated_dict.values()), set(self.regular_dict.values()))

    def test_keys(self):
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(self.deprecated_dict.keys(), self.regular_dict.keys())

    def test_equality(self):
        with self.assertWarns(DeprecationWarning):
            self.assertTrue(self.deprecated_dict == self.regular_dict)

        with self.assertWarns(DeprecationWarning):
            self.assertTrue(self.deprecated_dict == self.deprecated_dict)

        with self.assertWarns(DeprecationWarning):
            self.assertTrue(self.regular_dict == self.deprecated_dict)

    def test_inequality(self):
        with self.assertWarns(DeprecationWarning):
            self.assertFalse(self.deprecated_dict != self.regular_dict)

        with self.assertWarns(DeprecationWarning):
            self.assertFalse(self.deprecated_dict != self.deprecated_dict)

        with self.assertWarns(DeprecationWarning):
            self.assertFalse(self.regular_dict != self.deprecated_dict)

    def test_custom_warning_type(self):
        my_dict = deprecate_keys({'a': 12}, dkey('a', warning_type=UserWarning))
        with self.assertWarns(UserWarning):
            self.assertEqual(my_dict['a'], 12)

    def test_end_user_warning(self):
        my_dict = deprecate_keys({'a': 12}, dkey('a', warning_type='end user'))
        with self.assertWarns(FutureWarning):
            self.assertEqual(my_dict['a'], 12)

    def test_developer_warning(self):
        my_dict = deprecate_keys({'a': 12}, dkey('a', warning_type='developer'))
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(my_dict['a'], 12)

    def test_deprecated_in(self):
        version = '1.81.1'
        my_dict = deprecate_keys({'a': 12}, dkey('a', deprecated_in=version))
        with self.assertWarnsRegex(DeprecationWarning, f'Key `a` is deprecated since version {version}. It shouldn\'t be used anymore.'):
            self.assertEqual(my_dict['a'], 12)

    def test_removed_in(self):
        version = '2.0'
        my_dict = deprecate_keys({'a': 12}, dkey('a', removed_in=version))
        with self.assertWarnsRegex(DeprecationWarning, f'Key `a` is deprecated. It will be removed in version {version}. It shouldn\'t be used anymore.'):
            self.assertEqual(my_dict['a'], 12)

    def test_added_details(self):
        details = 'Get rid of it!'
        my_dict = deprecate_keys({'a': 12}, dkey('a', details=details))
        with self.assertWarnsRegex(DeprecationWarning, details):
            self.assertEqual(my_dict['a'], 12)
