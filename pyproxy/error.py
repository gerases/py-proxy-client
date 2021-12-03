"""Module with custom exceptions"""


class ProxyProtocolError(Exception):
    """Class for implementing custom exceptions"""
    def __init__(self, message, cause):
        """
        Represents a generic error that occurs in the proxy protocol
        :param message: String message describing the error
        :param cause:   Actual exception which occurred
        """
        super().__init__(message)
        self.message = message
        self.cause = cause
