from IO_assign.IOGlobal import IOGlobal
from IO_assign.IOPad import IOPad, IOPadInst, IOPadSide, IOPadLocal
from IO_assign.IOHelper import inputNetlist, powerRing, powerStripe, countPorts, powerPlanDesign, powerIO, commentDelete
from IO_assign.IOAssignDef import IOAssignDef, PadDef, PadListDef, PadRingDef
from IO_assign.IOWriteFile import writeNetlist

if __name__ == "__main__":

    io_def = IOAssignDef()
    io_def.digital_pad.io.DIO = "MDSDUIX16"
    io_def.digital_pad.io.BDIO = "MDSDUIX16"
    io_def.digital_pad.supply.corner = "MCORNERI"
    io_def.digital_pad.supply.io_supply.VDD = "VDD2DGZI"
    io_def.digital_pad.supply.io_supply.VSS = "VSS2DGZI"
    io_def.digital_pad.supply.core_supply.VDD = "VDD1DGZI"
    io_def.digital_pad.supply.core_supply.VSS = "VSS1DGZI"

    wr = 0

    if wr == 1:
        ports = inputNetlist("wrapper.v", "wrapper")
    else:
        ports = inputNetlist("Top_remcm_mini_CCS102050_post_dc.v", "Top_remcm_mini")


    # count = countPorts(ports)
    io_def.inputPorts(ports)
    io_def.setPGPad(4, 4, "CORE_VCCK", "CORE_GNDK", "IO_VCCK", "IO_GNDK")
    
    # print(str(io_global) + '\n' + str(io_def))
    if wr == 1:
        io_def.writeIOFile("result/wrapper_io.txt")
    else:
        io_def.writeIOFile("result/remcm_io.txt")
    power_io_plan = powerIO(300e-3, 3.3, 108e-3, 88, 5)
    
    # pad1 = PadDef()
    # pad1.setName("a1").setCell("PADI")
    # pad2 = PadDef()
    # pad2.setName("a1").setCell("PADI")

    if wr == 1:
        netlist = writeNetlist("result/wrapper_top_io.v", io_def, "wrapper", ports)
    else:
        netlist = writeNetlist("result/remcm_top_with_io.v", io_def, "Top_remcm_mini", ports)
    print(netlist)
