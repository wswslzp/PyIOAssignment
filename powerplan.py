from IO_assign.IOHelper import *
from IO_assign.IOPortsDrawer import *
from IO_assign.IOParser import *

if __name__ == "__main__":
    viop = VerilogIOParser("wrapper_net.v", "wrapper")
    drawer = IOPortsDrawer(viop)
    drawer.set_hw_ratio(1)
    drawer.set_port_prefer_position("left", "IDATA", "SVM_COEF", "SCORE_EFF")
    drawer.set_port_prefer_position("top", "GRAM_COEF")
    drawer.generate()
    drawer.print_pin_position()
    # print(
    #     powerPlanDesign(
    #         total_power=50e-3,
    #         vdd=1.1,
    #         k=4,
    #         max_current_density=9*(12*.9-.02)*1e-3/12e-6,
    #         ring_num=4,
    #         metal_pitch=.8e-6,
    #         vertical_pitch=.14e-6,
    #         min_nand_width=.56e-6,
    #         stdcell_height=1.26e-6,
    #         chip_height=3e-3,
    #         chip_width=6e-3,
    #         IR_drop=.05,
    #         res_square_h=.289,
    #         res_square_v=.289,
    #         v_pad=2.25,
    #         i_pad=16e-3,
    #         total_port_num=99
    #     )
    # )