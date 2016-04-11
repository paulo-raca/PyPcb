from collections import OrderedDict, deque

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


#------------------------------------------------------------------------------


class Interconnection(PcbObject):
    pass

class Wire(Interconnection):
    def __init__(self, name=None, parent=None):
        super().__init__(name, parent)
        self._wire_root = self
        self._wire_connections = [self]
      
    def root(self):
        if self._wire_root is self:
            return self
        else:
            self._wire_root = self._wire_root.root()
            return self._wire_root
          
    def all_wires(self):
        yield from self.root()._wire_connections
          
    def all_connections(self):
        for wire in self.all_wires():
            if wire._parent is not None:
                yield wire._parent

    def __add__(self, other):
        my_root = self.root()
        other_root = other.root()
        if my_root is not other_root:
            my_root._wire_connections += other_root._wire_connections
            del other_root._wire_connections
            other_root._wire_root = my_root
        return self

    def __eq__(self, other):
        return type(other) is type(self) and self.root() is other.root()

    def __hash__(self):
        return id(self.root())

    def __str__(self):
        return "Interconnection: %s" % str([PcbObject.__str__(x) for x in self.all_wires()])

class Bus(Interconnection): 
    """
    Array of Wires
    
    It should support slicing assignment. E.g.: 
        Bus[0] = vcc
        Bus[1] = gnd
        bus[2:10] = data
    """
    pass #TODO

class NamedBus(Interconnection):
    """
    Set of named Interconnections.
    
    E.g.: 
        Serial: VCC, GND, RX, TX
        I2C>: VCC, GND, SDA, SCL
        CHARLCD: VCC, GND, RS, RW, EN, DATA[8], Backlight
    """
    pass #TODO


#------------------------------------------------------------------------------


class InterconnectionAttribute:
    def create(self, name, parent):
        raise NotImplementedError

class WireAttribute(InterconnectionAttribute):
    def create(self, name, parent):
        return Wire(name, parent)

class BusAttribute(InterconnectionAttribute):
    def create(self, name, parent):
        return Bus(name, parent)

class NamedBusAttribute(InterconnectionAttribute):
    def create(self, name, parent):
        return NamedBus(name, parent)


#------------------------------------------------------------------------------


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


#------------------------------------------------------------------------------


def Power(v):
    if v not in Power._cache:
        Power._cache[v] = Wire(("%+f" % v).rstrip('0').rstrip('.') + "V", Power._root)
    return Power._cache[v]
Power._root = Component("Power")
Power._cache = {0: Wire("GND", Power._root)}
Power.GND = Power(0)
Power.VCC = Power(5)


###############################################################################
# Little test code
###############################################################################


class Led(Component):
    anode = WireAttribute()
    cathode = WireAttribute()

class Resistor(Component):
    A = WireAttribute()
    B = WireAttribute()

class Microcontroller(Component):
    vcc = WireAttribute()
    gnd = WireAttribute()
    pb1 = WireAttribute()
    pb2 = WireAttribute()
    pb3 = WireAttribute()

microcontroller = Microcontroller(vcc=Power.VCC, gnd=Power.GND)

led1 = Led("Led1", anode=Resistor("R1", A=Power.GND).B, cathode=microcontroller.pb1)
led2 = Led("Led2", anode=Resistor("R2", A=Power.GND).B, cathode=microcontroller.pb2)
led3 = Led("Led3", anode=Resistor("R3", A=Power.GND).B, cathode=microcontroller.pb3)

microcontroller.print_netlist()