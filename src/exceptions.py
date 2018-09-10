class NSException(BaseException):
    pass


class NSParserException(NSException):
    pass


class NSLoaderException(NSException):
    pass


class HTMLException(BaseException):
    pass


class HTMLParserException(HTMLException):
    pass


class HTMLLoaderException(HTMLException):
    pass
