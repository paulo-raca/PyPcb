# PyPcb

Have you noticed how boring it is to draw PCB schematics?

1. Find each component in a list,
2. Place it somewhere in the drawing
3. Connect each of the hundreds of wires
4. Try to keep it all tidy (And fail at it)
5. Copy-Paste (Many, many times)

Although these are all important things to do on a PCB design, they should be postponed to the layout. Indeed, the only thing the layout editor uses from the schematic is the [netlist](https://en.wikipedia.org/wiki/Netlist).

To me, _drawing_ schematics sound very much like programming with Ladder logic or Scratch: Fun and Educative, but too inefficient for real life.

Fortunately, I've had the chance to learn [VHDL](https://en.wikipedia.org/wiki/VHDL), and I found that describing hardware components with a programming language is great!

I've looked for other [HDL targetting PCBs](https://en.wikipedia.org/wiki/Hardware_description_language#HDLs_for_printed_circuit_board_design), but wasn't impressed by any of the existing projects and decided to try on creating my own.

# Quick Start

```python
from pcb import *

# Declare the components you are going to use
# Importing existing components from KiCad/Eagle/etc is in my TODO list ;)
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

# Create a microcontroller.
microcontroller = Microcontroller()

# Plug the power to the microcontroller. `Power.GND` and `Power.VCC` are pre-defined nets for convenience.
microcontroller.vcc = Power.VCC
microcontroller.gnd = Power.GND


# Let's connect a few LEDs to the microcontroller ports!

# We can connect the pins after creation
led1 = Led("Led1")
r1 = Resistor("R1")
r1.A = Power.GND
r1.B = led1.anode
led1.cathode = microcontroller.pb1

# Or using named arguments during creation
led2 = Led("Led2", cathode=microcontroller.pb2)
r2 = Resistor("R2", A=Power.GND, B=led2.anode)

# This also works, but is hard to read
Led("Led3", anode=Resistor("R3", A=Power.GND).B, cathode=microcontroller.pb3)


# schematic is done! Print the circuit netlist
# This netlist is not in any standard format and is only for debugging.
microcontroller.print_netlist()
```

# Project Status

This Project is only a quick'n'dirty Proof-Of-Concept.

__It has no pratical use yet.__

If I do find the time and willpower to continue working on it, the next steps are:

- Import component library from other tools
- Export netlist that can be parsed by other tools 
- Support hierarchical components
- Support Numbered Buses: PB[8] instead of [PB0, PB1, PB2, etc]
- Support Named Buses: Serial1 instead of [GND, RX1, TX1]
- Support parametric components

Other tools to integrate to:
- KiCad
- Eagle
- Proteus
- Razen
- Spice
- ...?
