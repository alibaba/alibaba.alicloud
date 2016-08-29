class ACSConnectionError(RuntimeError):
    def __init__(self, reason, **args):
        self.reason = reason
        self.args = args

class ECSResponseError(RuntimeError):
    def __init__(self, status, body=None):
        self.status = status
        self.body = body