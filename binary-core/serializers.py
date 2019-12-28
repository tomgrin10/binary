import struct
from abc import ABCMeta, abstractmethod
from io import BufferedIOBase

import six
from enum import Enum
from typing import Any, Optional

from .struct_consts import (ENDIAN_NATIVE, ENDIAN_LITTLE, ENDIAN_BIG, ENDIAN_NETWORK,
                            INT8_SIGNED, INT8_UNSIGNED, INT16_SIGNED, INT16_UNSIGNED,
                            INT32_SIGNED, INT32_UNSIGNED, INT64_SIGNED, INT64_UNSIGNED,
                            FLOAT, DOUBLE)


@six.add_metaclass(ABCMeta)
class BaseSerializer(object):
    @abstractmethod
    def to_bytes(self, obj):
        # type: (Any) -> bytes
        raise NotImplementedError()

    @abstractmethod
    def from_bytes(self, bytes_stream):
        # type: (BufferedIOBase) -> Any
        raise NotImplementedError()

    @abstractmethod
    def try_get_size(self, obj=None):
        # type: (Any) -> Optional[int]
        raise NotImplementedError()


class Endian(Enum):
    Native = ENDIAN_NATIVE
    Little = ENDIAN_LITTLE
    Big = ENDIAN_BIG
    Network = ENDIAN_NETWORK


class _StructSerializer(BaseSerializer):
    __struct_format__ = NotImplemented  # type: int

    def __init__(self):
        # type: () -> None
        self.compiled_struct = struct.Struct(self.__struct_format__)

    def to_bytes(self, obj):
        # type: (Any) -> bytes
        return self.compiled_struct.pack(obj)

    def from_bytes(self, bytes_stream):
        # type: (BufferedIOBase) -> Any
        size = self.compiled_struct.size
        return self.compiled_struct.unpack_from(bytes_stream.read(size))

    def try_get_size(self, obj=None):
        # type: (Any) -> Optional[int]
        return self.compiled_struct.size


class Int8(_StructSerializer):
    __struct_format__ = INT8_SIGNED


Byte = Int8


class UInt8(_StructSerializer):
    __struct_format__ = INT8_UNSIGNED


UByte = UInt8


class Int16(_StructSerializer):
    __struct_format__ = INT16_SIGNED


Short = Int16


class UInt16(_StructSerializer):
    __struct_format__ = INT16_UNSIGNED


UShort = UInt16


class Int32(_StructSerializer):
    __struct_format__ = INT32_SIGNED


Int = Int32


class UInt32(_StructSerializer):
    __struct_format__ = INT32_UNSIGNED


UInt = UInt32


class Int64(_StructSerializer):
    __struct_format__ = INT64_SIGNED


Long = Int64


class UInt64(_StructSerializer):
    __struct_format__ = INT64_UNSIGNED


ULong = UInt64


class Float(_StructSerializer):
    __struct_format__ = FLOAT


class Double(_StructSerializer):
    __struct_format__ = DOUBLE
