class PcbObject:
    def __init__(self, name=None, parent=None):
        self._parent = parent
        self._name = name or self.__class__.__name__

    def symbol_prefix(self):
        return self.__class__.__name__.upper().strip("_")

    def __str__(self):
        pretty_path = self._name
        current = self._parent
        while current is not None:
            pretty_path = current._name + "»" + pretty_path
            current = current._parent

        return pretty_path
          
    def all_connections(self):
        return []
