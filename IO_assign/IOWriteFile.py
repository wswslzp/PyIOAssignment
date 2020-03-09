from IO_assign.IOHelper import *

def cellInst(port_direction,
                port_name,
                cell_inst_name,
                cell_name = "MDSDUIX16",
                ds = "111",
                smt = "",
                oen = "0",
                pd = "",
                pu = "",
                ie = ""):

    cell_inst = ""
    cell_inst += cell_name + '\t' + cell_inst_name + '_inst' + '\n(\n'
    cell_inst += "\t.DS0(" + ds[0] + "),\n"
    cell_inst += "\t.DS1(" + ds[1] + "),\n"
    cell_inst += "\t.DS2(" + ds[2] + "),\n"
    cell_inst += "\t.SMT(" + smt + "),\n"
    cell_inst += "\t.OEN(" + oen + "),\n"
    cell_inst += "\t.PU(" + pu + "),\n"
    cell_inst += "\t.PD(" + pd + "),\n"
    cell_inst += "\t.IE(" + ie + "),\n"
    if port_direction != "inout" :
        cell_inst += "\t.A(" + port_name + "_A),\n"
        cell_inst += "\t.D(" + port_name + "_D),\n"
        cell_inst += "\t.PAD()\n"
    else:
        cell_inst += "\t.A(),\n"
        cell_inst += "\t.D(),\n"
        cell_inst += "\t.PAD(" + port_name + ")\n"
    cell_inst += ");\n\n"
    return cell_inst

def cellInstNetlist(ports, 
                    pg_name_set,
                    cell_name = "MDSDUIX16",
                    ds = "111",
                    smt_port_list = [],
                    pad_pull_up = True,
                    enable = {
                        "smt" : True,
                        "oen" : False,
                        "ie" : True,
                        "pu" : True,
                        "pd" : True
                    }):

    port_count = countPorts(ports)
    port_total_num = len(port_count["ports"])
    content = ""

    smt = "1'b" + str(int(enable["smt"]))
    smt_iv = "1'b" + str(int(not enable["smt"]))
    oen = "1'b" + str(int(enable["oen"]))
    oen_iv = "1'b" + str(int(not enable["oen"]))
    ie = "1'b" + str(int(enable["ie"]))
    ie_iv = "1'b" + str(int(not enable["ie"]))
    pu = "1'b" + str(int(enable["pu"]))
    pu_iv = "1'b" + str(int(not enable["pu"]))
    pd = "1'b" + str(int(enable["pd"]))
    pd_iv = "1'b" + str(int(not enable["pd"]))

    for iii in range(0, port_total_num):
        port_dims = port_count["ports"][iii]["dims"]
        port_width = port_count["ports"][iii]["width"]
        for jjj in range(0, port_dims):
            posfix_jjj = "" if port_dims==1 else "_"+str(jjj)
            for kkk in range(0, port_width):
                posfix_kkk = "" if port_width==1 else "_"+str(kkk)
                posfix = posfix_jjj + posfix_kkk
                port_name = ports[iii]["name"] + "_PORT" + posfix
                port_direction = ports[iii]["direction"]
                cell_inst_name = cell_name + "_" + ports[iii]["name"] + posfix_jjj + posfix_kkk

                content += cell_name + '\t' + cell_inst_name + '_inst' + '\n(\n'
                content += "\t.DS0(" + "1'b" + ds[2] + "),\n"
                content += "\t.DS1(" + "1'b" + ds[1] + "),\n"
                content += "\t.DS2(" + "1'b" + ds[0] + "),\n"
                if ports[iii]["name"] in smt_port_list:
                    content += "\t.SMT(" + smt + "),\n"
                else:
                    content += "\t.SMT(" + smt_iv + "),\n"
                if port_direction == "inout" :
                    if pad_pull_up :
                        content += "\t.PU(" + pu + "),\n"
                        content += "\t.PD(" + pd_iv + "),\n"
                    else:
                        content += "\t.PU(" + pu_iv + "),\n"
                        content += "\t.PD(" + pd + "),\n"
                    content += "\t.OEN(" + oen + "),\n"# oen
                    content += "\t.IE(" + ie + "),\n"# ie
                    content += "\t.A(" + port_name + "_A),\n"
                    content += "\t.D(" + port_name + "_D),\n"
                elif port_direction == "input":
                    content += "\t.PU(" + pu_iv + "),\n"
                    content += "\t.PD(" + pd_iv + "),\n"
                    content += "\t.OEN(" + oen_iv + "),\n" # oen_iv
                    content += "\t.IE(" + ie + "),\n" # ie
                    content += "\t.A(1'b0),\n"
                    content += "\t.D(" + port_name + "_D),\n"
                elif port_direction == "output":
                    content += "\t.PU(" + pu_iv + "),\n"
                    content += "\t.PD(" + pd_iv + "),\n"
                    content += "\t.OEN(" + oen + "),\n" # oen
                    content += "\t.IE(" + ie_iv + "),\n" # ie_iv
                    content += "\t.A(" + port_name + "_A),\n"
                    content += "\t.D(1'b0),\n"
                else:
                    print("DIRECTION ERROR!")
                content += "\t.PAD(" + port_name + ")\n"
                # else:
                #     content += "\t.A(),\n"
                #     content += "\t.D(),\n"
                #     content += "\t.PAD(" + port_name + ")\n"
                content += ");\n\n"
    return content

                

def writeNetlist(netlist_file, io_assign_def, top_module_name, ports):
    # output the netlist_file with IO pad definition
    # [IOAssignDef] io_assign_def
    # [string] top_module_name
    import time
    localtime = time.asctime( time.localtime(time.time()) )
    with open(netlist_file, 'w') as f:
        content = multilineComment(
            "Module: " + top_module_name,
            "Date: " + localtime,
            "Generated by IO Assigner"
        )

        module_dec = lambda port_dec: "module " + top_module_name + "_withio" + '(\n' + port_dec + ');\n\n'


        # PG pad inst
        pg_pad_inst = ""
        core_vdd_cell = io_assign_def.digital_pad.supply.core_supply.VDD 
        core_vss_cell = io_assign_def.digital_pad.supply.core_supply.VSS 
        io_vdd_cell = io_assign_def.digital_pad.supply.io_supply.VDD 
        io_vss_cell = io_assign_def.digital_pad.supply.io_supply.VSS 
        corner_cell = io_assign_def.digital_pad.supply.corner
        pg_name_set = {
            "core_vdd": "",
            "core_vss": "",
            "io_vdd": "",
            "io_vss": "",
            "poc": "POC"
        }
        pg_idx = 0
        for pad_side in io_assign_def.pad_ring.leaf_list:
            for pad_inst in pad_side.leaf_list:
                pad_inst_cell = pad_inst.cell[1:-1]
                pad_inst_name = pad_inst.name[1:-1]
                last_idx = pad_inst_name.rfind("_")
                if pad_inst_cell == core_vdd_cell:
                    pg_name_set["core_vdd"] = pad_inst_name[:last_idx]
                elif pad_inst_cell == core_vss_cell:
                    pg_name_set["core_vss"] = pad_inst_name[:last_idx]
                elif pad_inst_cell == io_vdd_cell:
                    pg_name_set["io_vdd"] = pad_inst_name[:last_idx]
                elif pad_inst_cell == io_vss_cell:
                    pg_name_set["io_vss"] = pad_inst_name[:last_idx]
                else:
                    continue
        for pad_side in io_assign_def.pad_ring.leaf_list:
            for pad_inst in pad_side.leaf_list:
                pad_inst_cell = pad_inst.cell[1:-1]
                pad_inst_name = pad_inst.name[1:-1]
                if pad_inst_cell in [core_vdd_cell, core_vss_cell, io_vdd_cell, io_vss_cell]:
                    pg_pad_inst += pad_inst_cell + ' ' + pad_inst_cell + "_inst_" + str(pg_idx) + "\n(\n"
                    # pg_pad_inst += "\t.VDDIO(" + pg_name_set["io_vdd"] + "),\n"
                    # pg_pad_inst += "\t.VSSIO(" + pg_name_set["io_vss"] + "),\n"
                    # pg_pad_inst += "\t.VDD(" + pg_name_set["core_vdd"] + "),\n"
                    # pg_pad_inst += "\t.VSS(" + pg_name_set["core_vss"] + "),\n"
                    # pg_pad_inst += "\t.POC(" + pg_name_set["poc"] + ")\n"
                    pg_pad_inst += ");\n"
                    pg_idx += 1
                elif pad_inst_cell == corner_cell:
                    corner_position = pad_side.root
                    pg_pad_inst += pad_inst_cell+ ' ' + pad_inst_cell + '_' + corner_position + "_inst" + "\n(\n"
                    # pg_pad_inst += "\t.VDD(" + pg_name_set["core_vdd"] + "),\n"
                    # pg_pad_inst += "\t.VSS(" + pg_name_set["core_vss"] + ")"
                    pg_pad_inst += "\n);\n"
                else : 
                    continue


        # ports declaration
        port_count = countPorts(ports)
        port_total_num = len(port_count["ports"])
        port_dec = ""
        wire_inst_c2p, wire_inst_m2c, wire_inst_port, wire_inst_pin = "", "", "", ""
        port_merge = ""
        module_pin_assign = ""
        for ii in range(0, port_total_num):
            port_dims = port_count["ports"][ii]["dims"]
            port_width = port_count["ports"][ii]["width"]
            pin_name = ports[ii]["name"]
            wire_inst_pin += "wire\t" + ports[ii]["width"] + "\t" + pin_name + "\t" + ports[ii]["dims"] + ";\n"
            module_pin_assign += "\t." + pin_name + "(" + pin_name + ")" + ("\n" if ii == port_total_num-1 else ",\n")
            for jj in range(0, port_dims):
                posfix_jj = "" if port_dims==1 else "_"+str(jj)
                posfix_jj_bracket = "" if port_dims==1 else "[" + str(jj) + "]"
                for kk in range(0, port_width):
                    posfix_kk = "" if port_width==1 else "_"+str(kk)
                    posfix_kk_bracket = "" if port_width==1 else "["+str(kk) + "]"
                    posfix = posfix_jj + posfix_kk
                    posfix_bracket = posfix_jj_bracket + posfix_kk_bracket

                    port_name = ports[ii]["name"] + "_PORT" + posfix
                    port_direction = ports[ii]["direction"]

                    # declare wire
                    wire_name_m2cfix_inv = '_A' if (port_direction == "output") else '_D'
                    # wire_name_c2pfix = '_CELL2PORT_PAD' if (port_direction == "inout") else wire_name_c2pfix
                    wire_name_m2cfix = '_D' if (port_direction == "output") else '_A'
                    # wire_name_m2cfix = '_PIN2CELL_PAD' if (port_direction == "inout") else wire_name_m2cfix
                    # wire_inst_c2p += "wire\t" + port_name + wire_name_c2pfix + ";\n"
                    wire_inst_m2c += "wire\t" + port_name + wire_name_m2cfix + ";\n"
                    wire_inst_m2c += "wire\t" + port_name + wire_name_m2cfix_inv + ";\n"
                    wire_inst_port += "wire\t" + port_name + ";\n"
                    # wire_inst_pin += "wire\t" + posfix_kk_bracket + '\t' + pin_name + '\t' + posfix_jj_bracket + ";\n"

                    # cell to pad
                    # wire_c2p_name = port_name + wire_name_c2pfix
                    # if port_direction == "output": 
                    #     port_merge += "assign\t" + port_name + "\t=\t" + wire_c2p_name + ';\n'
                    # elif port_direction == "input":
                    #     port_merge += "assign\t" + wire_c2p_name + "\t=\t" + port_name + ';\n'
                    # else:
                    #     port_merge += "assign\t" + port_name + "\t=\t" + wire_c2p_name + ';\n'
                    # module to cell
                    # wire_m2c_name = port_name + wire_name_m2cfix
                    if port_direction == "output":
                        wire_m2c_name = port_name + "_A"
                        port_merge += "assign\t" + wire_m2c_name + "\t=\t" + ports[ii]["name"] + posfix_bracket + ';\n'
                    elif port_direction == "input":
                        wire_m2c_name = port_name + "_D"
                        port_merge += "assign\t" + ports[ii]["name"] + posfix_bracket + "\t=\t" + wire_m2c_name + ';\n'
                    else:
                        wire_m2c_name_in = port_name + "_D"
                        wire_m2c_name_out = port_name + "_A"
                        port_merge += "assign\t" + wire_m2c_name_out + "\t=\t" + ports[ii]["name"] + posfix_bracket + ';\n'
                        port_merge += "assign\t" + ports[ii]["name"] + posfix_bracket + "\t=\t" + wire_m2c_name_in + ';\n'

                    port_dec += '\t' + port_direction + '\t\t'+ port_name # cell to port
                    port_dec += '\n' if (ii==port_total_num-1) and (jj==port_dims-1) and (kk==port_width-1) else ',\n'

        
        # for pg_type in pg_name_set:
        #     port_dec = "\tinout\t\t" + pg_name_set[pg_type] + ',\n' + port_dec
        content += module_dec(port_dec)

        # content += multilineComment(
        #     "Port inst"
        # )

        # content += wire_inst_port + wire_inst_c2p + wire_inst_m2c + '\n\n'
        # content += multilineComment(
        #     "Port instance"
        # ) + wire_inst_port
        # content += multilineComment(
        #     "Cell to Port wire instance"
        # ) + wire_inst_c2p
        content += multilineComment(
            "Module to Cell wire instance"
        ) + wire_inst_m2c
        content += multilineComment(
            "Module pin wire instance"
        ) + wire_inst_pin

        # Ports merge into pins
        content += multilineComment(
            "Pin assignment"
        ) + '\n'
        content += port_merge + '\n\n'

        # Module inst : cell inst and original module inst
        # cell inst using another function: cellInstNetlist()
        cell_inst = cellInstNetlist(ports,
                                    pg_name_set, 
                                    cell_name=io_assign_def.digital_pad.io.DIO,
                                    smt_port_list=io_assign_def.smt_port_list,
                                    ds=io_assign_def.driving_strength)
        # cell_inst = cellInstNetlist(ports, io_assign_def.digital_pad.io.DIO, cell_pin)
        content += multilineComment(
            "Cell instance"
        ) + cell_inst + '\n\n'
        module_inst = lambda pin_assign: top_module_name + ' ' + top_module_name + '_inst\n(\n' + pin_assign + ');\n\n'

                    
        # content += multilineComment(
        #     "PG pad instance"
        # )
        # content += pg_pad_inst + '\n\n\n'


        # for ii in range(0, port_total_num):
        #     j
        content += multilineComment(
            "Module instance"
        ) + module_inst(module_pin_assign)

        content += "\nendmodule\n"

        f.write(content)
        return content