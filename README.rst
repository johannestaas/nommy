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


See examples for more.


Release Notes
-------------

:0.0.1:
    Project created
