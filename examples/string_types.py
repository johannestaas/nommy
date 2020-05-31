from nommy import parser, string, pascal_string


@parser
class StringTypes:
    static_len: string(4)
    nullterm: string(None)
    pascal: pascal_string


def main():
    data, rest = StringTypes.parse(b'tofuHello World!\0\5hello')
    print(repr(data))
    assert rest == b''
