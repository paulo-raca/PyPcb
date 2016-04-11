from pcb.component import *
from pcb.interconnection import *
from pcb.power import *

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