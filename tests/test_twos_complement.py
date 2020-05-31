import pytest

from nommy import Data

# Useful for making the test cases:
# https://www.exploringbinary.com/twos-complement-converter/


@pytest.mark.parametrize(
    'size, bytestr, expected_sign, expected', [
    ],
)
def test_twos_complement(size, bytestr, expected_sign, expected):
    data = Data(bytestr)
    arr = bytearray(data.bytes)
    sign = data._twos_complement(arr, size)
    assert sign == expected_sign
    assert arr == bytearray(expected)
