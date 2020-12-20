from aiohttp import ClientResponse

class ClashException(Exception):
    pass

class HTTPException(ClashException):
    """A base exception for an http response"""
    def __init__(self, response:ClientResponse=None, data=None):
        self.status = response.status
        
        self.message = data.get('message')
        self.reason = data.get('reason', default='No reason')

        super().__init__("{0.message} (status: {0.status}): {0.reason}".format(self))
        

class InvalidParameters(HTTPException):
    pass

class Forbidden(HTTPException):
    pass

class NotFound(HTTPException):
    pass

class Maintenance:
    pass