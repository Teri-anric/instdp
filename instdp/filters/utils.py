class FuncFilter(BaseFilter):
    def __init__(self, func):
        self.check = func
        super().__init__()
