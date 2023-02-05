"""
Utility functions to help prepare mapped data.

Also being used to support mocking.
"""


from datetime import datetime


def get_now():
    """Wrapper to provide now(), mainly in support of code testing"""
    return datetime.now()
