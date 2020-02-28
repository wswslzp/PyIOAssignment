from IO_assign.IOGlobal import IOGlobal
from IO_assign.IOPad import IOPad, IOPadInst, IOPadSide, IOPadLocal
from IO_assign.IOHelper import inputNetlist, powerRing, powerStripe, countPorts, powerPlanDesign, powerIO
from IO_assign.IOAssignDef import IOAssignDef, PadDef, PadListDef, PadRingDef

if __name__ == "__main__":
    # print(inputNetlist("prePlace.v", "Top_remcm_mini"))
    # ring = powerRing(
    #     total_power=100e-3,
    #     vdd=1.2,
    #     max_current_density=1.7e3,
    #     ring_num=2,
    #     k=2,
    #     metal_pitch=.2e-6
    # )
    # stripe = powerStripe(
    #     total_power=100e-3,
    #     vdd=1.2,
    #     k=2,
    #     vertical_pitch=.8e-6,
    #     min_nand_width=.78e-6,
    #     stdcell_height=1.8e-6,
    #     chip_height=885e-6,
    #     chip_width=885e-6,
    #     IR_drop=.05,
    #     res_square_h=.022,
    #     res_square_v=.022
    # )
    # # print(ring, stripe)

    # io_content = ""

    io_global = IOGlobal().setVersion(3).setIOOrder("clockwise").setTotalEdge(4)

    io_def = IOAssignDef()
    io_def.digital_pad.io.DIO = "PADI"
    io_def.digital_pad.io.BDIO = "MDSDUIX16"
    io_def.digital_pad.supply.corner = "MCORNERI"
    io_def.digital_pad.supply.io_supply.VDD = "VDD2DGZI"
    io_def.digital_pad.supply.io_supply.VSS = "VSS2DGZI"
    io_def.digital_pad.supply.core_supply.VDD = "VDD1DGZI"
    io_def.digital_pad.supply.core_supply.VSS = "VSS1DGZI"

    ports = inputNetlist("prePlace.v", "Top_remcm_mini")
    count = countPorts(ports)
    io_def.inputPorts(ports)
    io_def.setPGPad(4, 4, "CORE_VCCK", "CORE_GNDK", "IO_VCCK", "IO_GNDK")
    
    # print(str(io_global) + '\n' + str(io_def))
    io_def.writeIOFile("io_assign.txt")
    power_io_plan = powerIO(300e-3, 3.3, 108e-3, 88, 5)
    
    # pad1 = PadDef()
    # pad1.setName("a1").setCell("PADI")
    # pad2 = PadDef()
    # pad2.setName("a1").setCell("PADI")

