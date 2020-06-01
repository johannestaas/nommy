nommy
=====

A python byte and bit parser inspired by Rust's nom.

Installation
------------

From the project root directory::

    $ python setup.py install

From pip::

    $ pip install nommy

Usage
-----

# Parser

You specify a class wrapped with `@nommy.parser` that has type hints in the order
that variables occur in the bytes::

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

    example, rest_of_bytes = Example.parse(b'CAFEBABE\xff\x12\x34\x80')
    print(example.magic_str)  # prints "CAFEBABE"
    print(example.some_unsigned_byte)  # prints 255, from \xff
    print(hex(example.some_unsigned_16bit))  # prints 0x3412 , because little endian \x12\x34
    print(example.some_flag)  # "True" from first bit of \x80
    print(example.next_flag)  # "False" from next bit
    print(example.six_bit_unsigned)  # \x1f or 31


# Endianedness and Signedness

There are several little-endian and big-endian types to use, such as::

    @parser
    class LittleEndianUnsigned:
        eight_bit: le_u8
        sixteen_bit: le_u16
        thirtytwo_bit: le_u32
        sixtyfour_bit: le_u64
        one_bit: le_u(1)
        two_bit: le_u(2)
        ...
        seven_bit: le_u(7)

You also have signed sizes, like `le_i8`, `le_i16`, `le_i32`, and `le_i64`.
For each of those, you also have big-endian: `be_u16`, ...

# Strings

There are three string types you can parse.

You can parse a static length string::

    static_len: string(12)

You can parse a null-terminated string::

    null_term: string(None)

And you also can parse pascal strings::

    some_str: pascal_string

# Flag

You also can trivially extract a bit as a boolean variable::

    debug: nommy.flag

# Enum

You can also create an `le_enum` or `be_enum` if you want to parse something
like a DNS rtype, to have easy named values::

    from enum import Enum
    from nommy import le_enum, parser

    @le_enum(4)  # 4 bit size
    class DNSRType(Enum):
       A = 1
       NS = 2
       MD = 3
       MF = 4
       ...

    @parser
    class DNSRecord:
        rtype: DNSRType
        ...

    data, rest = DNSRecord.parse(b'\x10...')
    assert data == DNSRecord(rtype=DNSRType.A, ...)

# Nested Parser

Parsers can be split up into multiple classes, then combined::

    from nummy import parser, le_u8, string

    @parser
    class Header:
        id: le_u8
        recipient: string(None)
        sender: string(None)

    @parser
    class Body:
        subject: string(None)
        text: string(None)

    @parser
    class Email:
        header: Header
        body: Body

See `examples/nested.py`


# Repeating

Sometimes a field in a structure specifies the number of repeating fields, such as in DNS you have
QDCOUNT and ANCOUNT for the number of queries and answers that will be in a following section.
Nommy supports this with the `repeating` class, which allows you to specify a data type that repeats
the number of times specified by a previous field, likely in the header.

The format is: `repeating(SomeDataType, 'integer_field_name')`

We also have `repeating_until_null` so that you can handle items that keep repeating indefinitely
until a null byte is reached, for example, in DNS names that are repeating pascal strings essentially.

Examples::

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
    )

See `examples/readme_repeating_example.py`


You can even reference other parser values by splitting the field with a period like `header.payload_ct`::

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

See examples for more.

For a full example that shows nested parsers with repeating values that
closely matches an actual DNS parser, check `examples/dns.py`


Release Notes
-------------

:0.3.2:
    Fix readme and add `examples/readme_repeating_example.py`
:0.3.1:
    Add `repeating_until_null` to handle DNS names
:0.3.0:
    Added support for nested fields and repeating values.
:0.2.0:
    Added enums.
:0.1.0:
    Works for major types, with strings and flags.
:0.0.1:
    Project created
