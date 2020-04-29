import warnings
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from io import BytesIO
from typing import Any, TypeVar, Union, Type, Dict, Callable

import six

from binary.serializers import BaseSerializer, UInt16, Int32
from binary.utils import AttributeNameGetter, is_dict_ordered, _T, create_obj_from_attributes, \
    get_attributes_from_object


__all__ = ['Binary']


class SerializersNotOrderedWarning(UserWarning):
    pass


@six.add_metaclass(ABCMeta)
class ExternalBinary(object):
    pass  # TODO


@six.add_metaclass(ABCMeta)
class Binary(object):
    @abstractmethod
    def serialize(self):
        # type: (Any) -> Dict[Any, BaseSerializer]
        """
        Implement this function to declare a serializer for each field.

        In python 3.6+ (dict is ordered by default):

        >>> return {
        >>>     self.a: UInt16,
        >>>     self.b: Int32
        >>> }

        Other versions:

        >>> return OrderedDict([
        >>>     (self.a, UInt16),
        >>>     (self.b, Int32)
        >>> ])
        """
        pass

    @classmethod
    def _get_serializers(cls):
        # type: () -> Dict[str, BaseSerializer]
        serializers = cls.serialize(AttributeNameGetter)

        if not is_dict_ordered(serializers):
            warnings.warn(
                "The serialize method returns an unordered dict. \n"
                "Use OrderedDict instead of a regular dict.",
                SerializersNotOrderedWarning)

        return serializers

    class _ToBytesDescriptor(object):
        @staticmethod
        def to_bytes(binary_class, obj):
            # type: (Type[Binary], Any) -> bytes
            serializers = binary_class._get_serializers()
            return _object_to_bytes(obj, serializers)

        def __get__(self, instance, type_):
            # If called by a class
            if instance is None:
                return lambda obj: self.to_bytes(type_, obj)

            # If called by an instance
            else:
                return lambda: self.to_bytes(type_, instance)

    # Declare this function twice for type hinting
    def to_bytes(self):
        # type: (Any) -> bytes
        pass

    # noinspection PyRedeclaration
    to_bytes: Callable[[], bytes] = _ToBytesDescriptor()

    _T = TypeVar('_T')

    class _FromBytesDescriptor(object):
        @staticmethod
        def from_bytes(binary_class, obj, bytes_):
            # type: (Type[Binary], Any) -> bytes
            serializers = binary_class._get_serializers()
            return _object_to_bytes(obj, serializers)

        def __get__(self, instance, type_):
            # If called by a class
            if instance is None:
                return lambda obj: self.to_bytes(type_, obj)

            # If called by an instance
            else:
                return lambda: self.to_bytes(type_, instance)

    def from_bytes(self, bytes_):
        # type: (Any, bytes) -> _T
        pass


def _attributes_to_bytes(byte_stream, serializers, attributes):
    # type: (BytesIO, Dict[str, BaseSerializer], Dict[str, Any]) -> None
    for attr_name, serializer in six.iteritems(serializers):
        attr_value = attributes[attr_name]
        byte_stream.write(serializer.to_bytes(attr_value))


def _object_to_bytes(obj, serializers):
    # type: (Any, Dict[str, BaseSerializer]) -> bytes
    stream = BytesIO()
    attributes = get_attributes_from_object(obj, six.iterkeys(serializers))
    _attributes_to_bytes(stream, serializers, attributes)
    return stream.getvalue()


def _from_bytes(byte_stream, attributes_to_serializers):
    # type: (BytesIO, Dict[str, BaseSerializer]) -> Dict[str, Any]
    attributes_to_values = OrderedDict()

    for attribute, serializer in six.iteritems(attributes_to_serializers):
        attributes_to_values[attribute] = serializer.from_bytes(byte_stream)

    return attributes_to_serializers


def from_bytes(obj, bytes_):
    # type: (Union[_T, Type[_T]], bytes) -> _T
    byte_stream = BytesIO(bytes_)

    serialize_func = six.get_method_function(obj.__serialize__)
    attributes_to_serializers = serialize_func(AttributeNameGetter)
    attributes_to_values = _from_bytes(byte_stream, attributes_to_serializers)

    return create_obj_from_attributes(obj, attributes_to_values)
