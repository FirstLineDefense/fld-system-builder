class BaseOptimizer:
    name = "base"

    capabilities = []

    description = ""

    version = "1.0"

    def metadata(self):
        return {
            "name": self.name,
            "capabilities": self.capabilities,
            "description": self.description,
            "version": self.version,
        }

    def optimize(self, requirements):
        raise NotImplementedError
