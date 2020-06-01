# checkstyle: noqa
'''
nommy

A python implementation of Rust's nom.
'''

__title__ = 'nommy'
__version__ = '0.3.3'
__all__ = (
    'parser', 'Data', 'repeating', 'repeating_until_null',
    'le_enum', 'be_enum',
    'NommyError', 'NommyUnpackError', 'NommyLShiftError',
    'NommyEnumValueError', 'NommyChompBitsError', 'NommyFieldError',
    'NommyDataError',
    'string', 'pascal_string', 'flag', 'char',
    'le_u', 'be_u',
    'le_u8', 'be_u8', 'le_i8', 'be_i8', 'bool8',
    'le_u16', 'be_u16', 'le_i16', 'be_i16',
    'le_u32', 'be_u32', 'le_i32', 'be_i32',
    'le_u64', 'be_u64', 'le_i64', 'be_i64',
    'le_float16', 'be_float16',
    'le_float32', 'be_float32',
    'le_float64', 'be_float64',
)
__author__ = 'Johan Nestaas <johannestaas@gmail.com'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2020 Johan Nestaas'

from .parser import (
    parser, Data, repeating, repeating_until_null,
    string, pascal_string, flag, char,
    le_u, be_u,
    le_u8, be_u8, le_i8, be_i8, bool8,
    le_u16, be_u16, le_i16, be_i16,
    le_u32, be_u32, le_i32, be_i32,
    le_u64, be_u64, le_i64, be_i64,
    le_float16, be_float16,
    le_float32, be_float32,
    le_float64, be_float64,
)
from .enum import le_enum, be_enum
from .exceptions import (
    NommyError, NommyUnpackError, NommyLShiftError, NommyChompBitsError,
    NommyEnumValueError, NommyFieldError, NommyDataError,
)


def main():
    pass
