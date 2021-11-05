from IO_assign.IOParser import IOParser

class IOPortsGeoConstraint(object):
    def __init__(self):
        self.hw_ratio = None
        self.die_height = None
        self.die_width = None
        self.io_height = None
        self.io_width = None 
        self.io_pitch = 0
        self.port_position = {}
        
    def check_constraint(self):
        return not ((self.hw_ratio == None) and (self.die_width == None or self.die_height == None or self.io_height == None or self.io_width == None))

class IOPortsContainer(object):
    def __init__(self):
        self.top = [] 
        self.left = [] 
        self.right = [] 
        self.bottom = [] 
        self.ptr = [0, 0, 0, 0]
        # self.full = [0, 0, 0, 0]
        self.step = 0

    def set_ports_num(self, t:int, l:int, r:int, b:int):
        self.top = ["unused" for x in range(t)]
        self.left = ["unused" for x in range(l)]
        self.right = ["unused" for x in range(r)]
        self.bottom = ["unused" for x in range(b)]
        return self

    def add_port(self, position:str, port):
        if position == "top":
            if self.ptr[0] < len(self.top):
                print(self.ptr[0])
                self.top[self.ptr[0]] = port
                self.ptr[0] += 1
            else:
                self.step += 1
                assert self.step < 4, "No Legal position for port {}".format(port["name"])
                self.add_port("right", port)
        elif position == "left":
            if self.ptr[1] < len(self.left):
                self.left[self.ptr[1]] = port
                self.ptr[1] += 1
            else:
                self.step += 1
                assert self.step < 4, "No Legal position for port {}".format(port["name"])
                self.add_port("top", port)
        elif position == "right":
            if self.ptr[2] < len(self.right):
                self.right[self.ptr[2]] = port
                self.ptr[2] += 1
            else:
                self.step += 1
                assert self.step < 4, "No Legal position for port {}".format(port["name"])
                self.add_port("bottom", port)
        elif position == "bottom":
            if self.ptr[3] < len(self.bottom):
                self.bottom[self.ptr[3]] = port
                self.ptr[3] += 1
            else:
                self.step += 1
                assert self.step < 4, "No Legal position for port {}".format(port["name"])
                self.add_port("left", port)
        elif position == "any":
            self.add_port("top", port)
        else:
            assert False, "Wrong position {}! legal position is top, left, right and bottom".format(position)

        self.step = 0
        return self

    def remove_unuse_slot(self):
        try:
            while True:
                self.top.remove("unused")
        except:
            ...
        try:
            while True:
                self.left.remove("unused")
        except:
            ...
        try:
            while True:
                self.right.remove("unused")
        except:
            ...
        try:
            while True:
                self.bottom.remove("unused")
        except:
            ...


class IOPortsDrawer(object):
    def __init__(self, io_parser: IOParser):
        self.ports = io_parser.build_ports().uniquify_ports().port_struct
        self.port_container = IOPortsContainer()
        self.geo_constraint = IOPortsGeoConstraint()
        for p in self.ports:
            p["position"] = ""

    def set_hw_ratio(self, hw_ratio):
        self.geo_constraint.hw_ratio = hw_ratio
        return self

    def set_die_size(self, h, w):
        self.geo_constraint.die_height = h
        self.geo_constraint.die_width = w
        return self

    def set_io_cell_size(self, io_height, io_width):
        self.geo_constraint.io_height = io_height
        self.geo_constraint.io_width = io_width
        return self

    def set_io_pitch(self, pitch):
        self.geo_constraint.io_pitch = pitch
        return self

    def set_port_prefer_position(self, position:str, *port_name_pat:str):
    # def set_port_prefer_position(self, port_name_pat:str, position:str):
        import re
        assert position in ["top", "left", "right", "bottom"], "Illegal position!"
        self.geo_constraint.port_position[position] = port_name_pat
        for idx in range( len( self.ports ) ):
            for pat_id in range( len( port_name_pat ) ):
                if re.match(port_name_pat[pat_id], self.ports[idx]["name"]):
                    self.ports[idx]["position"] = position
        return self 

    def define_port_container(self):
        import math
        assert self.geo_constraint.check_constraint(), "The geometry constraint of port is incomplete."
        port_amount = len(self.ports)
        if self.geo_constraint.die_height != None:
            self.geo_constraint.hw_ratio = self.geo_constraint.io_height / self.geo_constraint.io_width

        w_num = math.ceil(
            port_amount / (2 * (self.geo_constraint.hw_ratio + 1))
        )
        h_num = math.ceil(
            w_num * self.geo_constraint.hw_ratio
        )

        if self.geo_constraint.io_width != None:
            w_len = w_num * max(self.geo_constraint.io_width, self.geo_constraint.io_pitch)
            h_len = h_num * max(self.geo_constraint.io_width, self.geo_constraint.io_pitch)
            if w_len > self.geo_constraint.die_width or h_len > self.geo_constraint.die_height:
                print("This assignment may be illegal! w_len = {w_num} * {io_w} = {w_len} > {die_w}; h_len = {h_num} * {io_w} = {h_len} > {die_h}".format(
                    w_num = w_num,
                    io_w = max(self.geo_constraint.io_width, self.geo_constraint.io_pitch),
                    w_len = w_len,
                    die_w = self.geo_constraint.die_width,
                    h_num = h_num,
                    h_len = h_len,
                    die_h = self.geo_constraint.die_height
                ))
                print("The default setting may be little pessimistic because the slots of the port container are more than actually need.")
        self.port_container.set_ports_num(w_num, h_num, h_num, w_num)

        return self 
    
    def assign_ports(self):
        # the port container contains more slots than needed
        import re
        for pos in self.geo_constraint.port_position:
            for port_name in self.geo_constraint.port_position[pos]:
                for port in self.ports:
                    if re.match(port_name, port["name"]):
                        self.port_container.add_port(pos, port)

        for port in self.ports:
            if port["position"] == "":
                self.port_container.add_port("any", port)

        self.port_container.remove_unuse_slot()

    def generate(self):
        self.define_port_container().assign_ports()
    
    def print_pin_position(self):
        print("Top:")
        for p in self.port_container.top:
            print('\t', p["name"])
        print("Left:")
        for p in self.port_container.left:
            print('\t', p["name"])
        print("Right:")
        for p in self.port_container.right:
            print('\t', p["name"])
        print("Bottom:")
        for p in self.port_container.bottom:
            print('\t', p["name"])