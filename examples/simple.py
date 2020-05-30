from nommy import parser, string, le_u8


@parser
class Example:
    header: string(4)
    name: string(5)
    some_byte: le_u8


def main():
    example, rest = Example.parse(b'BUZZjohanA')
    print(f'example: {example!r}')
    print(f'rest: {rest!r}')


if __name__ == '__main__':
    main()
