# import IO_assign.IOHelper
import re
from IO_assign.IOHelper import *
# from IOHelper import *

class IOParser(object):
    def __init__(self, netlist, top_module):
        self.netlist: str = netlist
        self.top_module: str = top_module
        self.port_struct = []

    def build_ports(self):
        return self

    def uniquify_ports(self):
        new_ports = self.port_struct.copy()
        for ports in self.port_struct:
            if ports['width'] != '': 
                new_ports.remove(ports)
                width_range = re.findall(
                    r"\[(\d+):(\d+)\]", ports['width']
                )[0]
                for w in range(int( width_range[1] ), int(width_range[0])):
                    new_ports.append(
                        {
                            "direction": ports["direction"],
                            "width": "",
                            "name": ports["name"] + "_{}".format(w),
                            "dims": "" # dim in ports is not synthesizable
                        }
                    )
        self.port_struct = new_ports
        return self

    def print_ports(self):
        for port in self.port_struct:
            print(port)


class VerilogIOParser(IOParser):
    def __init__(self, netlist, top_module):
        IOParser.__init__(self, netlist, top_module)

    def build_ports(self):
        try:
            with open(self.netlist, "r") as f:
                ports = []
                verilog_netlist = f.read()
                verilog_netlist = commentDelete(verilog_netlist)
                re_module = re.compile(r"module\s*" + self.top_module)
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
                    self.port_struct = ports
                    return self
                else:
                    print("Top Module: " + self.top_module + "does not exist!")
                    return self
        except FileNotFoundError :
            print("Netlist not found")


class VHDLIOParser(IOParser):
    def __init__(self, netlist, top_module):
        IOParser.__init__(self, netlist, top_module)
        
        
if __name__ == "__main__":
    viop = VerilogIOParser("wrapper_net.v", "wrapper")
    viop.build_ports()
    viop.uniquify_ports()
    viop.print_ports()
