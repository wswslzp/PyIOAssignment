import re
import math

def commentDelete(verilog_netlist):
    comment_pattern1 = re.compile(
        r"(//.*\n|/\*([\s\S]*)\*/)"
    )
    netlist_without_comment = re.sub(comment_pattern1, '', verilog_netlist)
    return netlist_without_comment

def moduleSlice(verilog_netlist):
    # module_pattern = re.compile(
    #     r"module([\s\S]*)endmodule"
    # )
    modules = []
    module_pattern = re.compile(
        r"module[\s\n]+(\w+)([\s\S]*?)endmodule"
    )
    module_name_contents = module_pattern.findall(verilog_netlist)
    for mnc in module_name_contents:
        modules.append(
            {
                "name": mnc[0],
                "content": mnc[1]
            }
        )

    return modules

def parseParameter(verilog_netlist):
    modules = moduleSlice(verilog_netlist)
    module_parameters = []
    for module in modules:
        parameters = {
            "module": module["name"],
            "params": {}
        }

        single_module = module["content"]

        port_params_region = re.compile(
            r"#[\s\n]*\([\s\n]*([\s\n\w,=]*)\)"
        )
        port_params_region_part = port_params_region.findall(single_module)
        single_module = port_params_region.sub("@",single_module)
        
        local_params_pattern = re.compile(
            r"(parameter|localparam)[\s\n]+([\w=,\s\n]*);"
        )
        local_params_part = local_params_pattern.findall(single_module)
        single_module = local_params_pattern.sub("@", single_module)

        port_param_pattern = re.compile(
            r"(\w+)[\s\n]*=[\s\n]*(\d+)"
        )
        local_params_pattern = re.compile(
            r"(\w+)[\s\n]*=[\s\n]*(\d+)"
        )

        params_name_values = port_param_pattern.findall(port_params_region_part[0])
        for pnv in params_name_values:
            parameters["params"][pnv[0]] = pnv[1]

        for lpp in local_params_part:
            lpp_type_name_values = local_params_pattern.findall(lpp[1])
            for ltnv in lpp_type_name_values:
                parameters["params"][ltnv[0]] = ltnv[1]

        module_parameters.append(parameters)

    return module_parameters

def subsParameters(verilog_netlist, params):
    pass

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
    # inputNetlist("t1.v", "wrapper")
    with open("t1.v", "r") as f:
        verilog_netlist = f.read()
        modules = moduleSlice(verilog_netlist)
        params = parseParameter(verilog_netlist)
        print(params)