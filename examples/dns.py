from enum import Enum

from nommy import (
    be_enum, parser, be_u16, flag, le_u, repeating_until_null, pascal_string,
    repeating,
)


@be_enum(1)
class QR(Enum):
    query = 0
    response = 1


@be_enum(4)
class Opcode(Enum):
    standard_query = 0


@be_enum(4)
class RCode(Enum):
    no_error = 0
    format_error = 1
    server_failure = 2
    name_error = 3
    not_impl = 4
    refused = 5


@parser
class DNSHeader:
    id: be_u16
    qr: QR
    opcode: Opcode
    aa: flag
    tc: flag
    rd: flag
    ra: flag
    z: le_u(3)
    rcode: RCode
    qdcount: be_u16
    ancount: be_u16
    nscount: be_u16
    arcount: be_u16


@be_enum(16)
class RType(Enum):
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


@be_enum(16)
class RClass(Enum):
    IN = 1
    # There's more here too of course.


@parser
class Query:
    name: repeating_until_null(pascal_string)
    rtype: RType
    rclass: RClass


@parser
class DNSQuery:
    header: DNSHeader
    queries: repeating(Query, 'header.qdcount')


def main():
    hdr, rest = DNSQuery.parse(
        b'\x00\xff'  # ID field, 255
        b'\x05'  # should be 0 QR 0 Opcode AA=True RD=True
        b'\x80'  # RA=True rcode=no_error
        b'\x00\x02'  # 2 qdcount
        b'\x00\x00'  # 0 ancount
        b'\x00\x00'  # 0 nscount
        b'\x00\x00'  # 0 arcount
        b'\x07example\x03org\0'
        b'\x00\x01\x00\x01'
        b'\x03foo\x07example\x03org\0'
        b'\x00\x01\x00\x01'
        b'\xff\xff\xff\xff\xff\xff...'  # just something to drop into rest
    )
    print(f'DNS Header is: {hdr!r}')


if __name__ == '__main__':
    main()
