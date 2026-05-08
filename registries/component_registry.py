class ComponentRegistry:
    def __init__(self):
        self._components = {}

    def register(self, category, name, component):
        category_bucket = self._components.setdefault(category, {})

        category_bucket[name] = component

    def get(self, category, name):
        return self._components.get(category, {}).get(name)

    def get_category(self, category):
        return self._components.get(category, {})

    def categories(self):
        return sorted(self._components.keys())

    def snapshot(self):
        return self._components


registry = ComponentRegistry()
