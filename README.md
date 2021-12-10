# IO Wrapper Script

## Requirement

* Python 2/3;
* Netlist file of top level module, written in Verilog/SystemVerilog, with non-parametric ports definition.

## Overview

The help description of the script.
```
usage: io_assign_main.py [-h] -c CONFIG -i INPUT_NETLIST [-v VERBOSE]
                         [--output-io OUTPUT_IO]
                         [--output-netlist OUTPUT_NETLIST]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        input configure json file
  -i INPUT_NETLIST, --input-netlist INPUT_NETLIST
                        input gate netlist
  -v VERBOSE, --verbose VERBOSE
                        verbose level, 0 for only errors, 1 for waring and
                        error and 2 for all
  --output-io OUTPUT_IO
                        output io file
  --output-netlist OUTPUT_NETLIST
                        output netlist file
```

Example
```shell
python3 ./io_assign_main.py -v 1 -c io_config.json -i wrapper.v --output-io wrapper.io --output-netlist wrapper_io.v
```

The `verbose` option controls the message reporting level. 

### Config file 

The script needs user to provide the IO configuration file in `JSON` format, in which user define the information like the name of the top module, the data pad cell's name and ports, pg pad cell names, the meta info including pull up/pull down/schmitt, etc. User needs to fill in the specific value according to the used IO cell lib. The script will use the configuration file to generate the output files.

The example configuration file is `io_config.json` in the repo.

## Notice 

The module that has ports' width or dimension declared with parameters cannot be parse by `inputNetlist` function. 

Any module that own such port declaration must first be synthesized and input the post-synthesis netlist file.


Generated IO location file is only for Innovus.