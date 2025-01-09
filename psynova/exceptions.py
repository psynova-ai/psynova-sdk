from typing import Dict, Any, Optional


class PsynovaAPIError(Exception):
    """Exception raised when Psynova API request fails.

    Args:
        message (str): Error message describing what went wrong
        errors (Optional[Dict[str, Any]]): Additional error details from the API response

    Attributes:
        errors (Optional[Dict[str, Any]]): Additional error details from the API response
    """

    def __init__(self, message: str, errors: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.errors = errors
