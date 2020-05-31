from enum import Enum

from nommy import le_enum, parser, le_u16, flag, le_u


@le_enum(1)
class QR(Enum):
    query = 0
    response = 1


@le_enum(4)
class Opcode(Enum):
    standard_query = 0


@le_enum(8)
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


@le_enum(4)
class RCode(Enum):
    no_error = 0
    format_error = 1
    server_failure = 2
    name_error = 3
    not_impl = 4
    refused = 5


@parser
class DNSHeader:
    id: le_u16
    qr: QR
    opcode: Opcode
    aa: flag
    tc: flag
    rd: flag
    ra: flag
    z: le_u(3)
    rcode: RCode
    qdcount: le_u16
    ancount: le_u16
    nscount: le_u16
    arcount: le_u16


def main():
    hdr, rest = DNSHeader.parse(
        b'\xff\x00'  # ID field, 255
        b'\x05'  # should be 0 QR 0 Opcode AA=True RD=True
        b'\x80'  # RA=True rcode=no_error
        b'\x02\x00'  # 2 qdcount
        b'\x10\x00'  # 16 ancount
        b'\x00\x00'  # 0 nscount
        b'\x00\x00'  # 0 arcount
        b'\xff\xff\xff\xff\xff\xff...'  # just something to drop into rest
    )
    print(f'DNS Header is: {hdr!r}')


if __name__ == '__main__':
    main()
