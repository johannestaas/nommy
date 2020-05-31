from nommy import parser, string, pascal_string, le_u8, flag


@parser
class Simple:
    header: string(4)
    name: string(5)
    some_byte: le_u8


@parser
class JustString:
    name: string(12)


def test_simple():
    simple, rest = Simple.parse(b'BUZZjohanA')
    assert simple.header == 'BUZZ'
    assert simple.name == 'johan'
    assert simple.some_byte == 0x41
    assert rest == b''
    simple, rest = Simple.parse(b'BUZZjohanA    ')
    assert simple.header == 'BUZZ'
    assert simple.name == 'johan'
    assert simple.some_byte == 0x41
    assert rest == b'    '


def test_just_string():
    just, rest = JustString.parse(b'012345678912')
    assert just.name == '012345678912'
    assert rest == b''
    just, rest = JustString.parse(b'012345678912   ')
    assert just.name == '012345678912'
    assert rest == b'   '


@parser
class Flags:
    magic: string(2)
    flag1: flag
    flag2: flag
    flag3: flag
    flag4: flag


def test_flags():
    flags, rest = Flags.parse(b'MZ\xf0')
    assert flags == Flags(
        magic='MZ', flag1=True, flag2=True, flag3=True, flag4=True,
    )
    assert rest == b'\x00'

    flags, rest = Flags.parse(b'MZ\x0f\x00')
    assert flags == Flags(
        magic='MZ', flag1=False, flag2=False, flag3=False, flag4=False,
    )
    assert rest == b'\x0f\x00'

    flags, rest = Flags.parse(b'MZ\xcf\x00')
    assert flags == Flags(
        magic='MZ', flag1=True, flag2=True, flag3=False, flag4=False,
    )
    assert rest == b'\x0f\x00'

    flags, rest = Flags.parse(b'MZ\x1f\x00')
    assert flags == Flags(
        magic='MZ', flag1=False, flag2=False, flag3=False, flag4=True,
    )
    assert rest == b'\x0f\x00'


@parser
class PascalString:
    magic: string(2)
    first_name: pascal_string
    last_name: pascal_string


def test_pascal_string():
    data, rest = PascalString.parse(b'AA\3joe\6schmoe')
    assert data == PascalString(
        magic='AA', first_name='joe', last_name='schmoe',
    )
    assert rest == b''

    data, rest = PascalString.parse(b'BB\x10abcdef0123456789\0\x0f\x0f')
    assert data == PascalString(
        magic='BB', first_name='abcdef0123456789', last_name='',
    )
    assert rest == b'\x0f\x0f'


@parser
class NullTermString:
    magic: string(4)
    first_name: string(None)
    last_name: string(None)


def test_null_term_string():
    data, rest = NullTermString.parse(b'foobHello\0World!\0\xff')
    assert data == NullTermString(
        magic='foob', first_name='Hello', last_name='World!',
    )
    assert rest == b'\xff'

    data, rest = NullTermString.parse(b'fooB\0testingtesting\0\0\0\0\0')
    assert data == NullTermString(
        magic='fooB', first_name='', last_name='testingtesting',
    )
    assert rest == b'\0\0\0\0'
