*******************************
Behaviour of wrapped dictionary
*******************************

There are different ways items can be accessed in dicts. :any:`dkey` tries to
find the best warning solution for each case.

Single item access
==================

When accessing a single item in a dict, :any:`dkey` warns only, when the associated
key is deprecated. So if key `A` is deprecated, all of these operation warn::

    my_dict['A']
    my_dict['A'] = 12
    my_dict.get('A')
    del my_dict['A']
    my_dict.pop('A')

Setting or removing a deprecated (key,value) pair will also remove the warning::

    my_dict['A'] = 12  # warns
    my_dict['A']       # does not warn

This is to make sure that warnings do not propagate completely out of context.

Multi item access
=================

Due to the special view classes dict uses to give access to its internal structure
via the functions :any:`dict.values`, :any:`dict.keys`, and :any:`dict.items`,
these functions return *all* warnings directly when called. For all other functions
like normal iteration::

    for key in my_dict: # warns when key is 'A'
        print(key)

or :any:`dict.popitem`, the warning is instead generated, when the deprecated element
is accessed.