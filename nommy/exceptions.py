class NommyError(ValueError):
    pass


class NommyUnpackError(NommyError):
    pass


class NommyLShiftError(NommyError):
    pass


class NommyChompBitsError(NommyError):
    pass


class NommyEnumValueError(NommyError):
    pass


class NommyFieldError(NommyError):
    pass


class NommyDataError(NommyError):
    pass
