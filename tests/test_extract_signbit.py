import pytest

from nommy import Data


@pytest.mark.parametrize(
    'size, bytestr,expected_sign,expected', [
        (8, b'\xff', -1, [0x7f]),
        (8, b'\x80', -1, [0x00]),
        (8, b'\x7f', 1, [0x7f]),
        (8, b'\x70', 1, [0x70]),
        (8, b'\xf0', -1, [0x70]),
        (16, b'\x80\x00', -1, [0x00, 0x00]),
        (16, b'\xff\xff', -1, [0x7f, 0xff]),
        (16, b'\x7f\x00', 1, [0x7f, 0xff]),
        (16, b'\x7f\xff', 1, [0x7f, 0xff]),
        (16, b'\x7f\x0f', 1, [0x7f, 0x0f]),
        (4, b'\xff', -1, [0x7f]),
        (4, b'\x7f', 1, [0x7f]),
        (3, b'\xff', -1, [0x7f]),
        (3, b'\x7f', 1, [0x7f]),
        (32, b'\xff\x12\x34\x56', -1, [0x7f, 0x12, 0x34, 0x56]),
        (32, b'\x7f\x12\x34\x56', 1, [0x7f, 0x12, 0x34, 0x56]),
    ],
)
def test_extract_signbit_ff(size, bytestr, expected_sign, expected):
    data = Data(bytestr)
    arr = bytearray(data.bytes)
    sign = data._extract_sign_from_bytearray(arr, size)
    assert sign == expected_sign
    assert arr == bytearray(expected)
