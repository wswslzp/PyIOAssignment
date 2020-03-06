# IO Assignment Script

## Requirement

* Python 2/3 with `re` and `math` module;
* Netlist file of top level module, written in Verilog/SystemVerilog, with non-parametric ports definition.

## Usage 

### 1. Modify the io_assign.py

```python
#!/bin/python
# import some class and function 
from IO_assign.IOHelper import *
from IO_assign.IOAssignDef import *
from IO_assign.IOWriteFile import *
...
# designate which pad cells to use 
io_def = IOAssignDef()
io_def.digital_pad.io.DIO = "MDSDUSX16"
io_def.digital_pad.io.BDIO = "MDSDUSX16"
io_def.digital_pad.supply.corner = "MCORNERS"
io_def.digital_pad.supply.io_supply.VDD = "VDD2DGZS"
io_def.digital_pad.supply.io_supply.VSS = "VSS2DGZS"
io_def.digital_pad.supply.core_supply.VDD = "VDD1DGZS"
io_def.digital_pad.supply.core_supply.VSS = "VSS1DGZS"
...
# input the nelist file and the top module name
# the function try to parse the port definition
ports = inputNetlist("clock_ctrl.v", "clock_ctrl") 
...
# set the power ground pad
# there are 4 pairs of IO supply pads and 4 pairs 
# of core supply pads. 
io_def.setPGPad(4, 4, "CORE_VCCK", "CORE_GNDK", "IO_VCCK", "IO_GNDK")
...
# write the IO assignment file into result directory
io_def.writeIOFile("clock_ctrl.io")
...
# write the pad-wrapped netlist into result directory
netlist = writeNetlist("clock_ctrl_wrapped.v", io_def, "clock_ctrl_wrapped", ports)
```


### 2. Run the script

```bash
# enter the root directory
# create a directory to store generated files
chmod u+x ./io_assign_main.py
./io_assign_main.py
```

## Notice 

The module that has ports' width or dimension declared with parameters cannot be parse by `inputNetlist` function. 

Any module that own such port declaration must first be synthesized and input the post-synthesis netlist file.