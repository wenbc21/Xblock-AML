class Task:
    def __init__(self, strategy, **kwargs):
        self.strategy = strategy
        self.info = kwargs
        self.is_closed = False

    def push(self, node, edges: list, **kwargs):
        raise NotImplementedError()

    def pop(self):
        raise NotImplementedError()

    def close(self):
        self.is_closed = True
        self.strategy = None

