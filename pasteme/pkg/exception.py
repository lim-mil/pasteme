from pasteme.pkg.response import resp_401


class RecordTypeError(Exception):
    def __init__(self):
        super().__init__()
        self.msg = 'Recode type is error'


def handle_401(*args, **kwargs):
    return resp_401()
