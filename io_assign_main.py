from IO_assign.IOHelper import *
from IO_assign.IOAssignDef import *
from IO_assign.IOWriteFile import *

if __name__ == "__main__":

    io_def = IOAssignDef()
    io_def.digital_pad.io.DIO = "MDSDUSX16"
    io_def.digital_pad.io.BDIO = "MDSDUSX16"
    io_def.digital_pad.supply.corner = "MCORNERS"
    io_def.digital_pad.supply.io_supply.VDD = "VDD2DGZS"
    io_def.digital_pad.supply.io_supply.VSS = "VSS2DGZS"
    io_def.digital_pad.supply.core_supply.VDD = "VDD1DGZS"
    io_def.digital_pad.supply.core_supply.VSS = "VSS1DGZS"

    ports = inputNetlist("clock_ctrl.v", "clock_ctrl")


    io_def.inputPorts(ports)
    io_def.setPGPad(1, 1, "CORE_VCCK", "CORE_GNDK", "IO_VCCK", "IO_GNDK")
    
    io_def.writeIOFile("clock_ctrl.io")

    writeNetlist("clock_ctrl_wrapped.v", io_def, "clock_ctrl_withio.v", ports)
    #print(netlist)


