from pasteme.pkg.response import resp


class RecordTypeError(Exception):
    def __init__(self):
        super().__init__()
        self.msg = 'Recode type is error'


def handle_401(*args, **kwargs):
    return resp(code=401)
