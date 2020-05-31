from .exceptions import NommyLShiftError, NommyChompBitsError

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

    def chomp_to_bitarray(self, size):
        bits = []
        for chomped in range(size):
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

    def chomp_to_bytearray(self, size):
        bit_arr = self.chomp_to_bitarray(size)
        byte_arr = bytearray()
        while bit_arr:
            last = bit_arr[-8:]
            bit_arr = bit_arr[:-8]
            byte_arr.append(self._convert_bitarray_be(last))
        return byte_arr[::-1]

    def _extract_sign_from_bytearray(self, arr, size):
        """
        Not used yet. Two's complement not implemented.
        """
        # If it's size 9, then you might have 0x01ff, signed -255.
        # That first byte is 0x01. 9 % 8 == 1.
        # If it's size 10, then you might have 0x03ff.
        # That first byte is 0b0011. 10 % 8 == 2.
        # For size 11, 0x07ff would be 0111.1111.1111, % 8 == 3...
        mod = size % 8
        # _BIT_MASK key, to get which bit it is.
        # If it was the 3rd bit, like size 11 % 3, then the key would be
        # 5, or 8 - mod.
        # If mod is 0, then it's the 8th bit and the key should be 0.
        if mod == 0:
            key = 0
        else:
            key = 8 - mod
        the_bit, mask = _BIT_MASK[key]
        # Get the signbit.
        signbit = bool(arr[0] & the_bit)
        # Mask it out.
        arr[0] &= mask
        return -1 if signbit else 1

    def _twos_complement(self, arr, size):
        raise NotImplementedError()
        sign = self._extract_sign_from_bytearray(arr, size)
        return sign

    def chomp_bits(self, size, endian='le'):
        arr = self.chomp_to_bytearray(size)
        sign = 1
        # TODO add signed logic and `signed` keyword.
        # if signed:
        #     sign = self._twos_complement(arr, size)
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
