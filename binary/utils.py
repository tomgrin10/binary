import sys
from collections import OrderedDict
from typing import TypeVar, Any, List, Dict, Union, Type, Iterator

import six


class _AttributeNameGetterType(object):
    def __getattribute__(self, item):
        return item


AttributeNameGetter = _AttributeNameGetterType()


def is_dict_ordered(dict_):
    # type: (dict) -> bool
    """
    Check if the dict is ordered in the current python version.
    """

    # As of Python 3.6, for the CPython implementation of Python,
    # dictionaries remember the order of items inserted.
    # As of Python 3.7, this is no longer an implementation detail and
    # instead becomes a language feature.
    if sys.version_info[:2] >= (3, 6):
        return True

    if isinstance(dict_, OrderedDict):
        return True


_T = TypeVar('_T')


def create_obj_from_attributes(obj, attributes):
    # type: (Union[_T, Type[_T]], Dict[str, Any]) -> _T
    """
    Create or update an object with a dict of attributes.

    :param obj: Object to update or type to create an object from.
    :param attributes:
    """
    if isinstance(obj, type):
        obj_type = obj
        obj = obj_type.__new__(obj_type)

    if hasattr(obj, '__dict__'):
        obj.__dict__.update(attributes)
    # If the object has __slots__ declared for example.
    else:
        for key, value in six.iteritems(attributes):
            setattr(obj, key, value)

    return obj


def get_attributes_from_object(obj, names):
    # type: (Any, Iterator[str]) -> Dict[str, Any]
    """
    Get attributes dict from object.
    Gets only attributes in the list names and in order.

    :param obj: Object to get attributes from.
    :param names: List of attribute names.
    """
    attributes = OrderedDict()

    for name in names:
        attributes[name] = getattr(obj, name)

    return attributes
