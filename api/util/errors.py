class MessagedError(Exception):  # 500
    """Exception with message field"""
    def __init__(self, message):
        self.message = message
        super().__init__()


class NotFoundError(MessagedError):  # 404
    """Raised when value was not found"""
    pass


class EntryNotFoundError(NotFoundError):
    """Raised when value with corresponding key was not found"""

    def __init__(self, key, message):
        self.key = key
        super().__init__(message if message is not None else f"Entry with key '{key}' was not found")


class ForbiddenError(MessagedError):  # 403
    """Raised when operation is forbidden"""
    pass


class BadFormatError(MessagedError):  # 400
    """Raised when operation's format was invalid"""
    pass
