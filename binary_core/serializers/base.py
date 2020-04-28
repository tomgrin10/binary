from abc import ABCMeta, abstractmethod
from io import BytesIO

import six
from typing import Any, Optional

__all__ = ['BaseSerializer']


@six.add_metaclass(ABCMeta)
class BaseSerializer(object):
    @abstractmethod
    def to_bytes(self, obj):
        # type: (Any) -> bytes
        raise NotImplementedError()

    @abstractmethod
    def from_bytes(self, bytes_stream):
        # type: (BytesIO) -> Any
        raise NotImplementedError()

    @abstractmethod
    def try_get_size(self, obj=None):
        # type: (Any) -> Optional[int]
        raise NotImplementedError()
