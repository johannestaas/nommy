import pytest

from nommy import parser, repeating, le_u8, le_u16, be_u32


@parser
class ArrayOfValues:
    byte_ct: le_u8
    half_ct: le_u8
    dword_ct: le_u8
    byte_arr: repeating(le_u8, 'byte_ct')
    half_arr: repeating(le_u16, 'half_ct')
    dword_arr: repeating(be_u32, 'dword_ct')


@pytest.mark.parametrize(
    'bytestr, exp_bytes, exp_halfs, exp_dwords, exp_rest', [
        (b'\0\0\0', [], [], [], b''),
        (b'\0\0\0somestuff\0here', [], [], [], b'somestuff\0here'),
        (b'\1\0\0\xff', [255], [], [], b''),
        (b'\0\1\0\x01\xff', [], [0xff01], [], b''),
        (b'\0\0\1\x01\x02\x03\x04   ', [], [], [0x01020304], b'   '),
        (
            (
                b'\3\3\3'
                b'\x00\x01\xff'
                b'\x01\x00\xff\x01\xcc\xdd'
                b'\x01\x00\x00\x00\xcc\xdd\xee\xff\x7f\x00\x00\xff'
                b'thisistherest'
            ),
            [0x0, 0x1, 0xff],
            [0x0001, 0x01ff, 0xddcc],
            [0x01000000, 0xccddeeff, 0x7f0000ff],
            b'thisistherest',
        ),
    ]
)
def test_repeating_unsigned_values(
    bytestr, exp_bytes, exp_halfs, exp_dwords, exp_rest,
):
    data, rest = ArrayOfValues.parse(bytestr)
    assert data.byte_arr == exp_bytes
    assert data.half_arr == exp_halfs
    assert data.dword_arr == exp_dwords
    assert rest == exp_rest
