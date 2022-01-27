"""
Custom exceptions
"""
import logging
log = logging.getLogger('custom')

class InvalidSyntax(Exception):
    """
    Exception returned when the input syntax is not expected
    """
    def __init__(self, *args):
        log.error("\n".join(args))
        super().__init__("\n".join(args))
