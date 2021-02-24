class RecordTypeError(Exception):
    def __init__(self):
        super().__init__()
        self.msg = 'Recode type is error'
