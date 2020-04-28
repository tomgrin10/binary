import struct
from io import BufferedIOBase

from enum import Enum
from typing import Any, Optional

from binary_core.serializers import BaseSerializer
from binary_core.struct_consts import (
    ENDIAN_NATIVE, ENDIAN_LITTLE, ENDIAN_BIG, ENDIAN_NETWORK, INT8_SIGNED,
    INT8_UNSIGNED, INT16_SIGNED, INT16_UNSIGNED, INT32_SIGNED, INT32_UNSIGNED,
    INT64_SIGNED, INT64_UNSIGNED, FLOAT, DOUBLE
)

__all__ = ['Endian', 'Int8', 'UInt8', 'Int16', 'UInt16', 'Int32', 'UInt32',
           'Int64', 'UInt64', 'Float', 'Double', 'Byte', 'UByte', 'Short',
           'UShort', 'Int', 'UInt', 'Long', 'ULong']


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


class UInt8(_StructSerializer):
    __struct_format__ = INT8_UNSIGNED


class Int16(_StructSerializer):
    __struct_format__ = INT16_SIGNED


class UInt16(_StructSerializer):
    __struct_format__ = INT16_UNSIGNED


class Int32(_StructSerializer):
    __struct_format__ = INT32_SIGNED


class UInt32(_StructSerializer):
    __struct_format__ = INT32_UNSIGNED


class Int64(_StructSerializer):
    __struct_format__ = INT64_SIGNED


class UInt64(_StructSerializer):
    __struct_format__ = INT64_UNSIGNED


class Float(_StructSerializer):
    __struct_format__ = FLOAT


class Double(_StructSerializer):
    __struct_format__ = DOUBLE


Byte = Int8
UByte = UInt8
Short = Int16
UShort = UInt16
Int = Int32
UInt = UInt32
Long = Int64
ULong = UInt64