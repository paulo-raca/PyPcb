from .component import Component
from .interconnection import Wire

def Power(v):
    if v not in Power._cache:
        Power._cache[v] = Wire(("%+f" % v).rstrip('0').rstrip('.') + "V", Power._root)
    return Power._cache[v]
Power._root = Component("Power")
Power._cache = {0: Wire("GND", Power._root)}
Power.GND = Power(0)
Power.VCC = Power(5)
