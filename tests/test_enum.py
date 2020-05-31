from enum import Enum

from nommy import le_enum, parser, string



@le_enum(8)
class DNSRType(Enum):
    A = 1
    NS = 2
    MD = 3
    MF = 4
    CNAME = 5
    SOA = 6
    MB = 7
    MG = 8
    MR = 9
    NULL = 10
    # There's more of course.


@parser
class DNSRecord:
    magic: string(None)
    rtype: DNSRType
    foo: string(None)


def test_le_enum():
    data, rest = DNSRecord.parse(b'foo\0\4bar\0')
    assert data == DNSRecord(
        magic='foo',
        rtype=DNSRType.MF,
        foo='bar',
    )
    assert rest == b''

    data, rest = DNSRecord.parse(b'what\0\x0a\0hello world!')
    assert data == DNSRecord(
        magic='what',
        rtype=DNSRType.NULL,
        foo='',
    )
    assert rest == b'hello world!'
