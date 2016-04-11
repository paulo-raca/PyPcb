from .common import PcbObject

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
