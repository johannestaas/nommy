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

# Repeating

Sometimes a field in a structure specifies the number of repeating fields, such as in DNS you have
QDCOUNT and ANCOUNT for the number of queries and answers that will be in a following section.
Nommy supports this with the `repeating` class, which allows you to specify a data type that repeats
the number of times specified by a previous field, likely in the header.

The format is: `repeating(SomeDataType, 'field_that_represents_the_count')`

Example::

   from nommy import parser, repeating, flag, le_u, le_u16

   @parser
   class DNSHeader:
      id: le_u16
      qr: flag
      opcode: le_u(4)
      aa: flag
      tc: flag
      rd: flag
      ra: flag
      z: flag
      ad: flag
      cd: flag
      rcode: le_u(4)
      qdcount: le_u16
      ancount: le_u16
      nscount: le_u16
      arcount: le_u16

   @parser
   class DNSRequest:
      header: DNSHeader

See examples for more.


Release Notes
-------------

:0.2.0:
    Added enums.
:0.1.0:
    Works for major types, with strings and flags.
:0.0.1:
    Project created
