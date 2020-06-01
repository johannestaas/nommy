from nommy import parser, repeating, le_u8, string

@parser
class Header:
    id: le_u8
    payload_ct: le_u8

@parser
class Payload:
    name: string(None)

@parser
class Message:
    header: Header
    string_ct: le_u8
    strings: repeating(string(None), 'string_ct')
    payloads: repeating(Payload, 'header.payload_ct')


def main():
    data, rest = Message.parse(
        b'\xff\x02\x03foo\0bar\0bazzz\0name1\0name2\0the rest'
    )
    print(f'Message: {data!r}')
    print(f'rest: {rest!r}')


if __name__ == '__main__':
    main()
