"""The error types for Murakami."""


class Error(Exception):
    """Base class for Murakami exceptions"""


class ExporterError(Error):
    """Exception raised for an error caused by an exporter.

    Attributes:
        name -- The name of the runner
        message -- The error message
    """
    def __init__(self, name, message):
        super().__init__()
        self.name = name
        self.message = message


class RunnerError(Error):
    """Exception raised for an error caused by a runner.

    Attributes:
        name -- The name of the runner
        message -- The error message
    """
    def __init__(self, name, message):
        super().__init__()
        self.name = name
        self.message = message
    
    def __str__(self):
        return self.message
