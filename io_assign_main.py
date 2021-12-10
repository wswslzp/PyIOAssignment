import argparse as ap
import json

from IO_assign.IOHelper import *
from IO_assign.IOAssignDef import *
from IO_assign.IOWriteFile import *

def run(args):
    with open(args.config) as f:
        config = json.load(f)
    
    LOGGER.verbose = args.verbose
    io_def = IOAssignDef()
    io_def.digital_pad.io.DIO = "__EMPTY__" # TODO: the io def should be compatible with different io cells, like input/output/inout cell.
    io_def.digital_pad.io.DIO_I = config["DataPadCell"]["inputCell"]["name"]
    io_def.digital_pad.io.DIO_O = config["DataPadCell"]["outputCell"]["name"]
    io_def.digital_pad.io.BDIO = config["DataPadCell"]["inoutCell"]["name"]
    io_def.digital_pad.supply.corner = config["PGPadCell"]["Corner"]
    io_def.digital_pad.supply.io_supply.VDD = config["PGPadCell"]["IOVDD"]
    io_def.digital_pad.supply.io_supply.VSS = config["PGPadCell"]["IOVSS"]
    io_def.digital_pad.supply.core_supply.VDD = config["PGPadCell"]["COREVDD"]
    io_def.digital_pad.supply.core_supply.VSS = config["PGPadCell"]["COREVSS"]
    io_def.driving_strength = config["DataPadCell"]["meta"]["drivingStrength"]
    io_def.smt_port_list = config["DataPadCell"]["meta"]["SMTPortList"] # The port that apply schmitt 

    # input_netlist = args.input_netlist
    ports = inputNetlist(args.input_netlist, config["TopModule"])
    print(ports)
    io_def.inputPorts(ports)
    io_def.setPGPad(
        io_sup_num=config["PowerGround"]["IOPGNum"],
        core_sup_num=config["PowerGround"]["CorePGNum"],
        core_p=config["PowerGround"]["CorePG"]["Power"],
        core_g=config["PowerGround"]["CorePG"]["Ground"],
        io_p=config["PowerGround"]["IOPG"]["Power"],
        io_g=config["PowerGround"]["IOPG"]["Ground"]
    )
    if args.output_io is not None:
        # TODO: Now the io file should be consider the different io cells, e.g. input/output/inout cell.
        io_def.writeIOFile(args.output_io)
    if args.output_netlist is not None:
        writeNetlist(args.output_netlist, io_def, config, ports)

parser = ap.ArgumentParser()
parser.add_argument('-c', "--config", type=str, help="input configure json file", required=True)
parser.add_argument('-i', "--input-netlist", type=str, help="input gate netlist", required=True)
parser.add_argument("-v", "--verbose", type=int, help="verbose level, 0 for only errors, 1 for waring and error and 2 for all", default=3)
parser.add_argument("--output-io", type=str, help="output io file")
parser.add_argument("--output-netlist", type=str, help="output netlist file")
args = parser.parse_args()
run(args)
