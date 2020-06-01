import struct
from functools import partial
from collections import namedtuple

from .exceptions import NommyUnpackError, NommyFieldError
from .data import Data


def _make_parser(unpack_str, size):

    def _parser(data):
        try:
            val = struct.unpack(unpack_str, data.bytes[:size])[0]
            data << size * 8
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
_le_u = {8: le_u8, 16: le_u16, 32: le_u32, 64: le_u64}
_le_i = {8: le_i8, 16: le_i16, 32: le_i32, 64: le_i64}
_be_u = {8: be_u8, 16: be_u16, 32: be_u32, 64: be_u64}
_be_i = {8: be_i8, 16: be_i16, 32: be_i32, 64: be_i64}


def string(size):

    if size is None:
        def _parser(data):
            s = ''
            while data.bytes[0] != 0:
                s += chr(data.bytes[0])
                data << 8
            data << 8
            return s
    else:
        def _parser(data):
            val = data.bytes[:size].decode('utf8')
            data << size * 8
            return val
    return _parser


def pascal_string(data):
    ln = data.bytes[0]
    val = data.bytes[1:ln + 1].decode('utf8')
    data << (ln + 1) * 8
    return val


def flag(data):
    return bool(data.chomp_bits(1))


def le_u(size):
    if size in _le_u:
        return _le_u[size]

    def _parser(data):
        return data.chomp_bits(size, endian='le')

    return _parser


def be_u(size):
    if size in _be_u:
        return _be_u[size]

    def _parser(data):
        return data.chomp_bits(size, endian='be')

    return _parser


# TODO add signed logic for le/be functions.
'''
def le_i(size):

    def _parser(data):
        return data.chomp_bits(size, endian='le', signed=True)

    return _parser


def be_i(size):

    def _parser(data):
        return data.chomp_bits(size, endian='be', signed=True)

    return _parser
'''


class repeating:
    """
    This allows you to have a list of a repeating parser, based on the count
    specified by the value in `field_name`.
    """

    def __init__(self, parse_func, field):
        self._parse_func = parse_func
        self.field = field
        self.count = None

    def parse(self, data, **kwargs):
        val = []
        if not isinstance(self.count, int):
            raise NommyFieldError(
                f'couldnt get count from field {self.field!r}: {self.count!r}'
            )
        for _ in range(self.count):
            val.append(self._parse_func(data))
        return val

    def load(self, values):
        if self.field not in values:
            raise NommyFieldError(
                f'dont have field {self.field!r} in parsed values: {values!r}'
            )
        self.count = values[self.field]
        if not isinstance(self.count, int):
            raise NommyFieldError(
                f'couldnt get count from field {self.field!r}: {self.count!r}'
            )
        return


def _parse(cls, _bytes):
    values = {}
    data = Data(_bytes)
    for name, pfunc in cls._parsers.items():
        # If it's a class, or a enum.le_enum, etc.
        if hasattr(pfunc, 'load'):
            pfunc.load(values)
        if hasattr(pfunc, 'parse'):
            pfunc = partial(pfunc.parse)
        try:
            val = pfunc(data)
        except NommyUnpackError as e:
            raise NommyUnpackError(
                f'failed to unpack {name} from bytes {data.bytes!r}: {e}'
            )
        values[name] = val
    return cls(**values), data.bytes


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
