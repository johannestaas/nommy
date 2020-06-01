import struct
from functools import partial
from collections import namedtuple

from .exceptions import NommyUnpackError, NommyFieldError, NommyDataError
from .data import Data


def _make_parser(unpack_str, size):

    def _parser(data, **kwargs):
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
        def _parser(data, **kwargs):
            s = ''
            while data.bytes[0] != 0:
                s += chr(data.bytes[0])
                data << 8
            data << 8
            return s
    else:
        def _parser(data, **kwargs):
            val = data.bytes[:size].decode('utf8')
            data << size * 8
            return val
    return _parser


def pascal_string(data, **kwargs):
    ln = data.bytes[0]
    val = data.bytes[1:ln + 1].decode('utf8')
    data << (ln + 1) * 8
    return val


def flag(data, **kwargs):
    return bool(data.chomp_bits(1))


def le_u(size):
    if size in _le_u:
        return _le_u[size]

    def _parser(data, **kwargs):
        return data.chomp_bits(size, endian='le')

    return _parser


def be_u(size):
    if size in _be_u:
        return _be_u[size]

    def _parser(data, **kwargs):
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
    _is_parser = True

    def __init__(self, parse_func_or_cls, field):
        self.field = field
        if getattr(parse_func_or_cls, '_is_parser', False):
            self._parse_cls = parse_func_or_cls
            self._parse_func = parse_func_or_cls.parse
        else:
            self._parse_cls = None
            self._parse_func = parse_func_or_cls

    def _get_count_from_values(self, values):
        if '.' in self.field:
            fields = self.field.split('.')
            try:
                count = values[fields[0]]
            except KeyError:
                raise NommyFieldError(
                    f'couldnt get field {fields[0]!r} from {values!r}'
                )
            for fld in fields[1:]:
                if not hasattr(count, fld):
                    raise NommyFieldError(f'{count!r} has no field {fld!r}')
                count = getattr(count, fld)
        else:
            try:
                count = values[self.field]
            except KeyError:
                raise NommyFieldError(
                    f'couldnt get field {self.field!r} from {values!r}'
                )
        if not isinstance(count, int):
            raise NommyFieldError(
                f'couldnt get count from field {self.field!r}: {count!r}'
            )
        return count

    def parse(self, data, values=None, parent=None, **kwargs):
        values = values or {}
        count = self._get_count_from_values(values)
        val = []
        for _ in range(count):
            result = self._parse_func(data, values=values, **kwargs)
            # Would have `rest` in there as well.
            if self._parse_cls:
                result = result[0]
            val.append(result)
        return val


class repeating_until_null:
    """
    This will keep parsing until it hits a null byte.
    """
    _is_parser = True

    def __init__(self, parse_func_or_cls):
        if getattr(parse_func_or_cls, '_is_parser', False):
            self._parse_cls = parse_func_or_cls
            self._parse_func = parse_func_or_cls.parse
        else:
            self._parse_cls = None
            self._parse_func = parse_func_or_cls

    def parse(self, data, values=None, parent=None, **kwargs):
        values = values or {}
        val = []
        while data.bytes[0:1] != b'\0':
            result = self._parse_func(data, values=values, **kwargs)
            # Would have `rest` in there as well.
            if self._parse_cls:
                result = result[0]
            val.append(result)
        data.chomp_bits(8)
        return val


def _parse(cls, _bytes, values=None, parent=None, **kwargs):
    nt_values = {}
    values = values or {}
    if isinstance(_bytes, Data):
        data = _bytes
    elif isinstance(_bytes, (bytes, bytearray)):
        data = Data(_bytes)
    else:
        raise NommyDataError(f'unknown datatype: {_bytes!r}')
    for name, parse_cls_or_func in cls._parsers.items():
        # If it's a class, or a enum.le_enum, etc.
        if getattr(parse_cls_or_func, '_is_parser', False):
            pcls = parse_cls_or_func
            pfunc = pcls.parse
        else:
            pcls = None
            pfunc = parse_cls_or_func
        try:
            val = pfunc(data, values=values, parent=cls, **kwargs)
        except NommyUnpackError as e:
            raise NommyUnpackError(
                f'failed to unpack {name} from bytes {data.bytes!r}: {e}'
            )
        nt_values[name] = val
        values[name] = val
    if parent:
        return cls(**nt_values)
    else:
        return cls(**nt_values), data.bytes


def parser(cls):
    parts = cls.__annotations__
    parsers = {}
    for key, val in parts.items():
        parsers[key] = val
        if getattr(val, '_is_parser', False):
            val._is_subparser = True
    new = namedtuple(
        cls.__name__,
        list(parts.keys()),
    )
    new._is_parser = True
    new._is_subparser = False
    new._parsers = parsers
    new.parse = partial(_parse, new)
    return new
