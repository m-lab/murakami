"""
Common utility functions for Murakami.
"""


def is_enabled(toggle):
    """
    Check for string values that are common regarded as "True"
    """
    return str(toggle).lower() in ["true", "yes", "1", "y"]
