class ApiException(Exception):
    def __init__(self, code, msg):
        super().__init__(msg)
        self.code = code