from nommy import (
    parser, flag, le_u, le_u8, repeating, string, repeating_until_null,
)


@parser
class SomeStruct:
    # Total size, 1 byte.
    some_flag1: flag
    some_flag2: flag
    some_flag3: flag
    some_flag4: flag
    some_four_bit_nibble: le_u(4)


@parser
class HasRepeats:
    name_ct: le_u8
    names: repeating(string(None), 'name_ct')
    struct_ct: le_u8
    structs: repeating(SomeStruct, 'struct_ct')
    labels: repeating_until_null(string(4))


def main():
    data, rest = HasRepeats.parse(
        # 4 names, null terminated strings
        b'\x04foo\0bar\0baz\0quux\0'
        # 2 structs, 1 byte each
        # First is \xff, so all true flags and 15 value nibble
        # Second is \x0a, so all false flags and 10 value nibble
        b'\x02\xff\x0a'
        # Labels keep going until they hit a null byte
        b'ALFA'
        b'BETA'
        b'GAMA'
        b'DLTA'
        b'\x00'
        b'the rest!'
    )
    print(f'data.names: {data.names!r}')
    print(f'data.structs[0]: {data.structs[0]!r}')
    print(f'data.structs[1]: {data.structs[1]!r}')
    print(f'data.labels: {data.labels!r}')
    print(f'rest: {rest!r}')


if __name__ == '__main__':
    main()
