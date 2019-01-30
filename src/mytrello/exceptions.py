import requests.exceptions


class HTTPError(requests.exceptions.RequestException):
    """
    Custom Exception to show error
    """
