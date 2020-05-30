import struct
from functools import partial
from collections import namedtuple

from .exceptions import (
    NommyUnpackError, NommyLShiftError, NommyChompBitsError,
)

# For getting a bit at a point, and masking out the rest.
_BIT_MASK = {
    0: (0b10000000, 0b01111111),
    1: (0b01000000, 0b10111111),
    2: (0b00100000, 0b11011111),
    3: (0b00010000, 0b11101111),
    4: (0b00001000, 0b11110111),
    5: (0b00000100, 0b11111011),
    6: (0b00000010, 0b11111101),
    7: (0b00000001, 0b11111110),
}


class Data:

    def __init__(self, _bytes):
        self._bytes = bytearray(_bytes)
        self._chomped_bits = 0

    def _reset_chomped_bits(self):
        # If we go up to 8, we can just shift our data over by a byte.
        if self._chomped_bits == 8:
            self << 8
            # Now we have 0 chomped bits again.
            self._chomped_bits = 0

    def _convert_bitarray_be(self, arr):
        bit_str = ''.join(str(x) for x in arr)
        return int('0b' + bit_str, 2)

    def chomp_to_bitarray(self, count):
        bits = []
        for chomped in range(count):
            if not self._bytes:
                raise NommyChompBitsError(f'no more data: {self._bytes!r}')
            byt = self._bytes[0]
            mask, rem_mask = _BIT_MASK[self._chomped_bits]
            bit = int(bool(byt & mask))
            bits.append(bit)
            self._bytes[0] &= rem_mask
            self._chomped_bits += 1
            self._reset_chomped_bits()
        return bits

    def chomp_to_bytearray(self, count):
        bit_arr = self.chomp_to_bitarray(count)
        byte_arr = bytearray()
        while bit_arr:
            last = bit_arr[-8:]
            bit_arr = bit_arr[:-8]
            byte_arr.append(self._convert_bitarray_be(last))
        return byte_arr[::-1]

    def chomp_bits(self, count, endian='le', signed=False):
        arr = self.chomp_to_bytearray(count)
        sign = 1
        # Get the sign of the leftmost bit.
        if signed:
            sign = -1 if bool(0x80 & arr[0]) else 1
            arr[0] = arr[0] & 0x7f
        if len(arr) == 1:
            return arr[0] * sign
        if endian == 'be':
            arr = arr[::-1]
        val = 0
        for i, b in enumerate(arr):
            val += b * 256**i
        return val * sign

    @property
    def bytes(self):
        return bytes(self._bytes)

    def __lshift__(self, size):
        if size % 8 == 0:
            self._bytes = self._bytes[size // 8:]
        else:
            raise NommyLShiftError(f'cant lshift unless multiple of 8: {size}')


def string(size):

    def _parser(data):
        val = data.bytes[:size].decode('utf8')
        data << size * 8
        return val

    return _parser


def flag(data):
    return bool(data.chomp_bits(1))


def le_u(size):

    def _parser(data):
        return data.chomp_bits(size, endian='le', signed=False)

    return _parser


def be_u(size):

    def _parser(data):
        return data.chomp_bits(size, endian='be', signed=False)

    return _parser


def le_i(size):

    def _parser(data):
        return data.chomp_bits(size, endian='le', signed=True)

    return _parser


def be_i(size):

    def _parser(data):
        return data.chomp_bits(size, endian='be', signed=True)

    return _parser


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
