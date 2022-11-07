

def _status_code(code: int):
    def inner(cls):
        cls.status_code = code
        return cls

    return inner


class ApplicationException(Exception):
    status_code: int
    message: str
    code: int
    error: str

    def __init__(self, message, code=None):
        self.message = message
        if hasattr(self, 'code') is False:
            self.code = code
        self.error = type(self).__name__
        super().__init__()

    def to_dict(self):
        return dict(message=self.message, code=self.code, error=self.error)


@_status_code(400)
class BadRequestException(ApplicationException):
    pass


@_status_code(401)
class UnauthorizedException(ApplicationException):
    pass


@_status_code(403)
class ForbiddenException(ApplicationException):
    pass


@_status_code(404)
class NotFoundException(ApplicationException):
    pass


class FileNotFoundException(NotFoundException):
    pass


class InvalidUsageException(BadRequestException):
    pass
