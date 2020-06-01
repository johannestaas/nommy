from .parser import le_u, be_u
from .exceptions import NommyEnumValueError

# TODO DRY this up.


def le_enum(size):
    def _enum_decorator(enum):
        chomper = le_u(size)

        def _parser(data, **kwargs):
            val = chomper(data)
            return enum.map(val)

        dct = {}
        for key in enum:
            if key.value in dct:
                raise NommyEnumValueError(
                    f'{enum!r} has value {key.value!r}, which isnt unique'
                )
            dct[key.value] = key

        def _map(v):
            return enum._val_dict.get(v)

        enum._val_dict = dct
        enum.map = _map
        enum.parse = _parser
        enum._is_parser = True

        return enum

    return _enum_decorator


def be_enum(size):
    def _enum_decorator(enum):
        chomper = be_u(size)

        def _parser(data, **kwargs):
            val = chomper(data)
            return enum.map(val)

        dct = {}
        for key in enum:
            if key.value in dct:
                raise NommyEnumValueError(
                    f'{enum!r} has value {key.value!r}, which isnt unique'
                )
            dct[key.value] = key

        def _map(v):
            return enum._val_dict.get(v)

        enum._val_dict = dct
        enum.map = _map
        enum.parse = _parser
        enum._is_parser = True

        return enum

    return _enum_decorator
