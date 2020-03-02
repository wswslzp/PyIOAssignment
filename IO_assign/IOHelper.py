import re
import math

def commentDelete(verilog_netlist):
    comment_pattern1 = re.compile(
        r"(//.*\n|/\*[.|\n]*\*/)"
    )
    netlist_without_comment = re.sub(comment_pattern1, '', verilog_netlist)
    return netlist_without_comment

def inputNetlist(netlist_file, top_module):

    try:
        with open(netlist_file, "r") as f:
            ports = []
            verilog_netlist = f.read()
            verilog_netlist = commentDelete(verilog_netlist)
            re_module = re.compile(r"module\s*" + top_module)
            re_module_match = re_module.search(verilog_netlist)
            if re_module_match:
                re_module_start = re_module_match.start()
                re_endmodule = re.compile(r"endmodule")
                re_module_end = re_endmodule.search(verilog_netlist[re_module_start:]).end()
                verilog_netlist = verilog_netlist[re_module_start:re_module_start + re_module_end]# should only have one top module
                # port search
                # port_pattern_1 = re.compile(
                #     r"\([\s\n]*((input|output|inout)\s*(\[\d+:\d+\])?\s*([\s\w,\n\[:\]]+)[\s\n]*)+\);"
                # )
                # portdec_match = port_pattern_1.match(verilog_netlist)
                # ports_match_results_1 = port_pattern_1.findall(verilog_netlist)


                # port_pattern_2 = re.compile(
                #     r"(input|output|inout)\s*(\[\d+:\d+\])?\s*([\s\w,\n\[:\]]+)[;,]"
                # )
                # ports_match_results = port_pattern_2.findall(verilog_netlist)
                # for width_section in ports_match_results:
                #     port_name_list = width_section[2]
                #     name_sep = re.compile(r"[\s,\n]+")
                #     port_name_list = name_sep.split(port_name_list)
                #     for port_name_dims in port_name_list:
                #         name_dims_pattern = re.compile(
                #             r"(\w+)(\[\d:\d\])*"
                #         )
                #         name_dims = name_dims_pattern.findall(port_name_dims)
                #         name_dims = name_dims[0]
                #         ports.append(
                #             {
                #                 "direction": width_section[0],
                #                 "width": width_section[1],
                #                 "name": name_dims[0],
                #                 "dims": name_dims[1]
                #             }
                #         )
                port_pattern_2 = re.compile(
                    r"(input|output|inout)\s+([\s\w,\n]+);"
                )
                # ports_match_result = re.findall(r"(input|output|inout)\s+([\s\w,\n]+);", verilog_netlist)
                ports_match_result = port_pattern_2.findall(verilog_netlist)
                verilog_netlist = port_pattern_2.sub("@", verilog_netlist)
                for idx in range(0, len(ports_match_result)):
                    name_list = re.split(r"[,\s\n]+", ports_match_result[idx][1])
                    for name in name_list:
                        ports.append(
                            {
                                "direction": ports_match_result[idx][0],
                                "width": "",
                                "name": name,
                                "dims": ""
                            }
                        )

                port_pattern_1 = re.compile(
                    r"\s*(input|output|inout)\s*(\[\d+:\d+\])?\s+(\w+)\s*(\[\d+:\d+\])?\s*"
                )
                # ports_match_result = re.findall(r"\s*(input|output|inout)\s*(\[\d+:\d+\])?\s+(\w+)\s*(\[\d+:\d+\])?\s*", verilog_netlist)
                ports_match_result = port_pattern_1.findall(verilog_netlist)
                verilog_netlist = port_pattern_1.sub("@", verilog_netlist)
                for idx in range(0, len(ports_match_result)):
                    ports.append(
                        {
                            "direction": ports_match_result[idx][0],
                            "width": ports_match_result[idx][1],
                            "name": ports_match_result[idx][2],
                            "dims": ports_match_result[idx][3]
                        }
                    )
                return ports
            else:
                print("Top Module: " + top_module + "does not exist!")
                return 
    except FileNotFoundError :
        print("Netlist not found")

def countPorts(ports):
    count = {
        "total": 0,
        "ports": []
    }
    num_pattern = re.compile(r"\[(\d+):(\d+)\]")
    for port in ports:
        if num_pattern.match(port["width"]):
            port_width = int(num_pattern.findall(port["width"])[0][0]) - int(num_pattern.findall(port["width"])[0][1]) + 1
        else:
            port_width = 1

        if num_pattern.match(port["dims"]):
            port_dims = abs( int(num_pattern.findall(port["dims"])[0][0]) - int(num_pattern.findall(port["dims"])[0][1]) ) + 1
        else:
            port_dims = 1

        count["total"] += port_width * port_dims
        count["ports"].append(
            {
                "name": port["name"],
                "width": port_width,
                "dims": port_dims
            }
        )

    return count

def powerPlanDesign(total_power, 
                    vdd,
                    k,
                    max_current_density,
                    ring_num,
                    metal_pitch,
                    vertical_pitch,
                    min_nand_width,
                    stdcell_height,
                    chip_height,
                    chip_width,
                    IR_drop,
                    res_square_h,
                    res_square_v,
                    v_pad, i_pad,
                    total_port_num):
    return (
        powerRing(total_power, vdd, max_current_density, ring_num, k, metal_pitch),
        powerStripe(total_power, vdd, k, vertical_pitch, min_nand_width, stdcell_height, chip_height, 
                    chip_width,  IR_drop, res_square_v, res_square_h),
        powerIO(total_power, v_pad, i_pad, total_port_num, k)
    )

def powerIO(total_power,
            v_pad,
            i_pad,
            total_port_num,
            k):
    core_supply_n = total_power/(v_pad * i_pad) * k
    io_supply_nout_min, io_supply_nout_max = total_port_num/10, total_port_num/5
    io_supply_ncore = core_supply_n/2
    return {
        "core_supply": core_supply_n,
        "io_supply": (min(io_supply_nout_min, io_supply_ncore), max(io_supply_nout_max, io_supply_ncore))
    }

def powerRing(total_power,
              vdd,
              max_current_density,
              ring_num,
              k,
              metal_pitch):
    ring = {}
    Ip = total_power / vdd
    ring["width"] = Ip / (max_current_density*4*ring_num) * k
    ring["space"] = 2*metal_pitch
    ring["num"] = ring_num
    return ring 

def powerStripe(total_power, 
                vdd, 
                k,
                vertical_pitch,
                min_nand_width,
                stdcell_height,
                chip_height,
                chip_width,
                IR_drop,
                res_square_v,
                res_square_h):
    # stripe = {}
    I_total = total_power / vdd
    # stripe["vertical_width"] = 4 * min_nand_width - (4*min_nand_width % vertical_pitch)
    # stripe["horizontal_width"] = 2 * stdcell_height
    Wv = 4 * min_nand_width - (4*min_nand_width % vertical_pitch)
    Wh = 2 * stdcell_height
    Ih = chip_height / (chip_height + chip_width) * I_total
    Iv = chip_width / (chip_width + chip_height) * I_total
    Rev = .05 * (vdd/2)/Iv
    Reh = .05 * (vdd/2)/Ih
    Rsv = res_square_v * chip_height/Wv
    Rsh = res_square_h * chip_width/Wh
    N = Rsv/Rev
    M = Rsh/Reh
    SpaceV = chip_width/N
    SpaceH = chip_height/M

    return {
        "vertical_width": Wv,
        "horizontal_width": Wh,
        "vertical_space": SpaceV,
        "horizontal_space": SpaceH
    }

def multilineComment(*comment):
    cblock = ""
    cblock_width = 0
    for c in comment:
        cblock_width = 10 + len(c) if cblock_width < (10 + len(c)) else cblock_width
        cblock += '*' + 5*' ' + c + '\n'
    cblock_ub = '/' + cblock_width*'*' + '\n' + '*\n'
    cblock_db = '*\n' + cblock_width* '*' + '/'
    return cblock_ub + cblock + cblock_db + '\n'

if __name__ == "__main__":
    inputNetlist("t1.v", "wrapper")