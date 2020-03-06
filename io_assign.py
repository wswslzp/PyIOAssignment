from IO_assign.IOGlobal import IOGlobal
from IO_assign.IOPad import IOPad, IOPadInst, IOPadSide, IOPadLocal
from IO_assign.IOHelper import inputNetlist, powerRing, powerStripe, countPorts, powerPlanDesign, powerIO, commentDelete
from IO_assign.IOAssignDef import IOAssignDef, PadDef, PadListDef, PadRingDef
from IO_assign.IOWriteFile import writeNetlist

if __name__ == "__main__":

    io_def = IOAssignDef()
    io_def.digital_pad.io.DIO = "MDSDUSX16"
    io_def.digital_pad.io.BDIO = "MDSDUSX16"
    io_def.digital_pad.supply.corner = "MCORNERS"
    io_def.digital_pad.supply.io_supply.VDD = "VDD2DGZS"
    io_def.digital_pad.supply.io_supply.VSS = "VSS2DGZS"
    io_def.digital_pad.supply.core_supply.VDD = "VDD1DGZS"
    io_def.digital_pad.supply.core_supply.VSS = "VSS1DGZS"

    wr = 0

    if wr == 1:
        ports = inputNetlist("tmp/wrapper.v", "wrapper")
    else:
        ports = inputNetlist("tmp/Top_Remcm_mini_sram_post_dc.sv", "Top_Remcm_mini_sram")


    # count = countPorts(ports)
    io_def.inputPorts(ports)
    io_def.setPGPad(4, 4, "CORE_VCCK", "CORE_GNDK", "IO_VCCK", "IO_GNDK")
    
    # print(str(io_global) + '\n' + str(io_def))
    if wr == 1:
        io_def.writeIOFile("result/wrapper.io")
    else:
        io_def.writeIOFile("result/remcm_s.io")
    power_io_plan = powerIO(300e-3, 3.3, 108e-3, 88, 5)
    # print(power_io_plan)
    
    # pad1 = PadDef()
    # pad1.setName("a1").setCell("PADI")
    # pad2 = PadDef()
    # pad2.setName("a1").setCell("PADI")

    if wr == 1:
        netlist = writeNetlist("result/wrapper_top_io.v", io_def, "wrapper", ports)
    else:
        netlist = writeNetlist("result/remcm_top_with_io_s.v", io_def, "Top_Remcm_mini_sram", ports)
    #print(netlist)

    ppd = powerPlanDesign(total_power=300e-3, vdd=1.2, k=2, max_current_density=7.8e3, ring_num=1, metal_pitch=.11e-6, vertical_pitch=.26e-6, 
                    min_nand_width=.78e-6, stdcell_height=1.8e-6, chip_height=1.3e-3, chip_width=1.3e-3, IR_drop=.05, res_square_h=.022, 
                    res_square_v=.022, v_pad=3.3, i_pad=108e-3, total_port_num=100)
    print(ppd)
