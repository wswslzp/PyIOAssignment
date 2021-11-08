import argparse as ap
import json

from IO_assign.IOHelper import *
from IO_assign.IOAssignDef import *
from IO_assign.IOWriteFile import *

def run(args):
    config = json.load(args.config)
    
    io_def = IOAssignDef()
    io_def.digital_pad.io.DIO = config["PadCell"]["DigitalIO"]
    io_def.digital_pad.supply.corner = config["PadCell"]["Corner"]
    io_def.digital_pad.supply.io_supply.VDD = config["Padcell"]["IOVDD"]
    io_def.digital_pad.supply.io_supply.VSS = config["PadCell"]["IOVSS"]
    io_def.digital_pad.supply.core_supply.VDD = config["PadCell"]["CORECDD"]
    io_def.digital_pad.supply.core_supply.VSS = config["PadCell"]["COREVSS"]
    io_def.driving_strength = config["DrivingStrength"]
    io_def.smt_port_list = config["SMTPortList"]

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
        io_def.writeIOFile(args.output_io)
    if args.output_netlist is not None:
        writeNetlist(args.output_netlist, io_def, config["TopModule"], ports)

parser = ap.ArgumentParser()
parser.add_argument('-c', "--config", type=str, help="input configure json file", required=True)
parser.add_argument('-i', "--input-netlist", type=str, help="input gate netlist", required=True)
parser.add_argument("--output-io", type=str, help="output io file")
parser.add_argument("--output-netlist", type=str, help="output netlist file")
args = parser.parse_args()
run(args)

# io_def = IOAssignDef()
# io_def.digital_pad.io.DIO = "PBCD16R"
# io_def.digital_pad.supply.corner = "PVDD1RESD"
# io_def.digital_pad.supply.io_supply.VDD = "PVDD2R"
# io_def.digital_pad.supply.io_supply.VSS = "PVSS2R"
# io_def.digital_pad.supply.core_supply.VDD = "PVDD1R"
# io_def.digital_pad.supply.core_supply.VSS = "PVSS1R"
# io_def.driving_strength = "011"
# io_def.smt_port_list = ["rst_n"]

# ports = inputNetlist("post_dc_CSHM_PR_v1_FIR_CSHM_v2.v", "FIR_CSHM_v2")
# print(ports)


# io_def.inputPorts(ports)
# io_def.setPGPad(4, 8, "CORE_VCCK", "CORE_GNDK", "IO_VCCK", "IO_GNDK")

# io_def.writeIOFile("FIR_CSHM_v2.io")

# writeNetlist("FIR_CSHM_v2_withio.v", io_def, "FIR_CSHM_v2", ports)
#print(netlist)


