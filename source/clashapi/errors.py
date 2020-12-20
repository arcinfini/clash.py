

class ClashException(Exception):
    pass

class ClashHTTPException(ClashException):
    """A base exception for an http response"""
    def __init__(self, status_code, message, data):
        self.status_code = status_code
        self.message = message
        self._data = data
        super().__init__(message)
        print(status_code, data)