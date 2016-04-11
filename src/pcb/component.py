from .common import PcbObject
from .interconnection import Interconnection, InterconnectionAttribute
from collections import deque

class Component(PcbObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        for attrname in dir(self.__class__):
            attr = getattr(self.__class__, attrname)
            if isinstance(attr, InterconnectionAttribute):
                super().__setattr__(attrname, attr.create(attrname, self))

        for attrname in kwargs:
            setattr(self, attrname, kwargs[attrname])
        
    def all_connections(self):
        for attrname in dir(self):
            attr = getattr(self, attrname)
            if isinstance(attr, PcbObject):
                yield attr

    def __setattr__(self, attr, value):
        if attr[0] != '_':
            value += getattr(self, attr)
        return super().__setattr__(attr, value)
      
    def netlist(self):
        symbol_count = {}
        symbols = {}
        components = []
        wires = []
        queue = deque([self])
        
        def append(x):
            if x in symbols:
                return

            symbol_prefix = x.symbol_prefix()
            symbol_num = symbol_count.get(symbol_prefix, 0) + 1
            symbol_count[symbol_prefix] = symbol_num
            symbols[x] = "%s_%d" % (symbol_prefix, symbol_num)

            queue.append(x)
            
            if isinstance(x, Interconnection):
                wires.append(x)
            else:
                components.append(x)
        
        while queue:
            e = queue.popleft()
            for connection in e.all_connections():
                append(connection)
            
        return symbols, components, wires
             
    def print_netlist(self):
        symbols, components, wires = self.netlist()
        print("Components:")
        for c in components:
            print("- %s  # %s" % (symbols[c], c))
            for attrname in dir(c):
                attr = getattr(c, attrname)
                if isinstance(attr, PcbObject):
                    print("  - %s => %s  # %s" % (attrname, symbols[attr], attr))
        #print("Wire:")
        #for w in wires:
            #print("- %s  # %s" % (symbols[w], w))
