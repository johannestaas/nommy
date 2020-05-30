import struct
from functools import partial
from collections import namedtuple

from .exceptions import NommyUnpackError


class Data:

    def __init__(self, _bytes):
        self._bytes = _bytes
        self._chomped_bits = 0

    def chomp_bits(self, count):
        pass

    @property
    def bytes(self):
        if self._chomped_bits != 0:
            self.lshift(self._chomped_bits)
        return self._bytes

    def lshift(self, size):
        if self._chomped_bits == 0:
            if size % 8 == 0:
                self._bytes = self._bytes[size // 8:]
            else:
                pass
        else:
            pass


def string(size):

    def _parser(data):
        val = data.bytes[:size].decode('utf8')
        data.lshift(size * 8)
        return val

    return _parser


def flag(_bytes):

    def _parser(_bytes):
        return ..., ...

    return _parser


def _make_parser(unpack_str, size):

    def _parser(data):
        try:
            val = struct.unpack(unpack_str, data.bytes[:size])[0]
            data.lshift(size * 8)
        except struct.error as e:
            raise NommyUnpackError(e)
        return val

    return _parser


char = _make_parser('c', 1)
le_u8 = _make_parser('<B', 1)
be_u8 = _make_parser('>B', 1)
le_i8 = _make_parser('<b', 1)
be_i8 = _make_parser('>b', 1)
bool8 = _make_parser('?', 1)
le_u16 = _make_parser('<H', 2)
be_u16 = _make_parser('>H', 2)
le_i16 = _make_parser('<h', 2)
be_i16 = _make_parser('>h', 2)
le_u32 = _make_parser('<I', 4)
be_u32 = _make_parser('>I', 4)
le_i32 = _make_parser('<i', 4)
be_i32 = _make_parser('>i', 4)
le_u64 = _make_parser('<Q', 8)
be_u64 = _make_parser('>Q', 8)
le_i64 = _make_parser('<q', 8)
be_i64 = _make_parser('>q', 8)
le_float16 = _make_parser('<e', 2)
be_float16 = _make_parser('>e', 2)
le_float32 = _make_parser('<f', 4)
be_float32 = _make_parser('>f', 4)
le_float64 = _make_parser('<d', 8)
be_float64 = _make_parser('>d', 8)


def _parse(cls, _bytes):
    vals = {}
    data = Data(_bytes)
    for name, pfunc in cls._parsers.items():
        try:
            val = pfunc(data)
        except NommyUnpackError as e:
            raise NommyUnpackError(
                f'failed to unpack {name} from bytes {data.bytes!r}: {e}'
            )
        vals[name] = val
    return cls(**vals), data.bytes


def parser(cls):
    parts = cls.__annotations__
    parsers = {}
    for key, val in parts.items():
        parsers[key] = val
    new = namedtuple(
        cls.__name__,
        list(parts.keys()),
    )
    new._parsers = parsers
    new.parse = partial(_parse, new)
    return new
