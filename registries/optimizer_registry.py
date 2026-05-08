class OptimizerRegistry:
    def __init__(self):
        self._optimizers = {}

    def register(self, name, optimizer):
        self._optimizers[name] = optimizer

    def get(self, name):
        return self._optimizers.get(name)

    def names(self):
        return sorted(self._optimizers.keys())

    def snapshot(self):
        return self._optimizers


optimizer_registry = OptimizerRegistry()
