import logging
LOG = logging.getLogger('custom')

class InvalidSyntax(Exception):
    """Returned when the input syntax is not expected"""
    def __init__(self, *args):
        LOG.error("\n".join(args))
        super().__init__("\n".join(args))
