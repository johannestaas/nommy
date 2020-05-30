import struct
from functools import partial
from collections import namedtuple

from .exceptions import NommyUnpackError


class Data:

    def __init__(self, _bytes):
        self._bytes = _bytes
        self._chomped_bits = 0

    def chomp_bits(self, count):
        first = self._bytes[0]


def string(size):

    def _parser(byts):
        return byts[:size].decode('utf8'), byts[size:]

    return _parser


def flag(byts):

    def _parser(byts):
        return ..., ...

    return _parser


def _make_parser(unpack_str, size):

    def _parser(byts):
        try:
            val = struct.unpack(unpack_str, byts[0:size])[0]
        except struct.error as e:
            raise NommyUnpackError(e)
        return val, byts[size:]

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


def _parse(cls, byts):
    vals = {}
    for name, pfunc in cls._parsers.items():
        try:
            val, byts = pfunc(byts)
        except NommyUnpackError as e:
            raise NommyUnpackError(
                f'failed to unpack {name} from byts {byts!r}: {e}'
            )
        vals[name] = val
    return cls(**vals), byts


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


@parser
class Example:
    header: string(4)
    name: string(5)
    some_byte: le_u8


print(repr(Example.parse(
    b'BUZZjohanA'
)[0]))
