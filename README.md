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
ports = inputNetlist("Top_Remcm_mini_sram_post_dc.sv", "Top_Remcm_mini_sram") 
...
# set the power ground pad
# there are 4 pairs of IO supply pads and 4 pairs 
# of core supply pads. 
io_def.setPGPad(4, 4, "CORE_VCCK", "CORE_GNDK", "IO_VCCK", "IO_GNDK")
...
# write the IO assignment file into result directory
io_def.writeIOFile("result/remcm_s.io")
...
# write the pad-wrapped netlist into result directory
netlist = writeNetlist("result/remcm_top_with_io_s.v", io_def, "Top_Remcm_mini_sram", ports)
```


### 2. Run the script

```bash
# enter the root directory
# create a directory to store generated files
mkdir result

./io_assign.py
```

## Notice 

The module that has ports' width or dimension declared with parameters cannot be parse by `inputNetlist` function. 

Any module that own such port declaration must first be synthesized and input the post-synthesis netlist file.