from nommy import parser, string, le_u8, flag


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
    assert flags.magic == 'MZ'
    assert flags.flag1
    assert flags.flag2
    assert flags.flag3
    assert flags.flag4
    flags, rest = Flags.parse(b'MZ\x0f\x00')
    assert flags.magic == 'MZ'
    assert not flags.flag1
    assert not flags.flag2
    assert not flags.flag3
    assert not flags.flag4
    flags, rest = Flags.parse(b'MZ\xcf\x00')
    assert flags.magic == 'MZ'
    assert flags.flag1
    assert flags.flag2
    assert not flags.flag3
    assert not flags.flag4
    flags, rest = Flags.parse(b'MZ\x1f\x00')
    assert flags.magic == 'MZ'
    assert not flags.flag1
    assert not flags.flag2
    assert not flags.flag3
    assert flags.flag4
