class ConnectException(Exception):
    """A connection failed"""
    def __init__(self, err):
        self.message = err
        