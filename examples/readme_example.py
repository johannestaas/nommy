import nommy


@nommy.parser
class Example:
    magic_str: nommy.string(8)
    some_unsigned_byte: nommy.le_u8
    some_unsigned_16bit: nommy.le_u16
    some_flag: nommy.flag
    next_flag: nommy.flag
    six_bit_unsigned: nommy.le_u(6)
    ...


def main():
    example, rest_of_bytes = Example.parse(b'CAFEBABE\xff\x12\x34\x9f')
    print(example.magic_str)  # prints "CAFEBABE"
    print(example.some_unsigned_byte)  # prints 255, from \xff
    print(hex(example.some_unsigned_16bit))  # prints 0x3412 , because little endian \x12\x34
    # \x9f would be boolean 10011111
    # This splits into 2 flags at first, 1 and 0, True and False
    # Then it contains 011111 or 0x1f, the six bit unsigned int, so 31.
    print(example.some_flag)  # "True" from first bit of \x9f
    print(example.next_flag)  # "False" from next bit
    print(example.six_bit_unsigned)  # \x1f or 31


if __name__ == '__main__':
    main()
