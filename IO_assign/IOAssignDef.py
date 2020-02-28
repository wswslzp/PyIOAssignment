from IO_assign.IOHelper import countPorts
from IO_assign.PadClass import DigitalPad
from IO_assign.IOPad import IOPad, IOPadInst, IOPadSide
from IO_assign.IOGlobal import IOGlobal

class PadDef(IOPadInst):
    def __init__(self):
        IOPadInst.__init__(self)

class PadListDef(IOPadSide):
    def __init__(self,side):
        IOPadSide.__init__(self, side)
        self.row_max = 0

    @property
    def side(self):
        return self.root

    def addPad(self, pad):
        self.leaf_list.append(pad)
        return self

    def insertPad(self, pad, index):
        self.leaf_list.insert(index, pad)
        return self

    def setRowMax(self, ub):
        self.row_max = ub
        return self

    def isempty(self):
        return len(self.leaf_list) == 0

    def isfull(self):
        return len(self.leaf_list) == self.row_max


class PadRingDef(IOPad):
    def __init__(self):
        IOPad.__init__(self)
        self.setLeafList(
            [
                PadListDef("top"),
                PadListDef("left"),
                PadListDef("right"),
                PadListDef("bottom"),
                PadListDef("topleft"),
                PadListDef("topright"),
                PadListDef("bottomleft"),
                PadListDef("bottomright")
            ]
        )
        self.row_max = 0

    @property
    def top(self):
        return self.leaf_list[0]

    @property
    def left(self):
        return self.leaf_list[1]

    @property
    def right(self):
        return self.leaf_list[2]

    @property
    def bottom(self):
        return self.leaf_list[3]

    @property
    def topleft(self):
        return self.leaf_list[4]

    @property
    def topright(self):
        return self.leaf_list[5]

    @property
    def bottomleft(self):
        return self.leaf_list[6]

    @property
    def bottomright(self):
        return self.leaf_list[7]

    def setRowMax(self, ub):
        self.top.setRowMax(ub)
        self.left.setRowMax(ub)
        self.right.setRowMax(ub)
        self.bottom.setRowMax(ub)
        self.row_max = ub
        return self

    def checkStatus(self):
        if not self.left.isfull():
            return 1
        elif not self.top.isfull():
            return 2
        elif not self.right.isfull():
            return 3
        elif not self.bottom.isfull():
            return 4
        else: 
            return 0

    def addPad(self, pad):
        ring_status = self.checkStatus()
        if not ring_status:
            print("Ring Full!")
        elif ring_status == 1:
            self.left.addPad(pad)
        elif ring_status == 2:
            self.top.addPad(pad)
        elif ring_status == 3:
            self.right.addPad(pad)
        elif ring_status == 4:
            self.bottom.addPad(pad)
        else :
            print("Error")
        return self
    

class IOAssignDef(object):
    
    def __init__(self):
        self.pad_ring = PadRingDef()
        self.digital_pad = DigitalPad()
        self.ports = None

    def inputPorts(self, ports):
        import math
        port_count = countPorts(ports)
        total_num = port_count["total"]
        self.pad_ring.setRowMax(math.ceil(total_num/4))
        for ii in range(0, len(port_count["ports"])):
            pad_dims = port_count["ports"][ii]["dims"]
            pad_width = port_count["ports"][ii]["width"]
            for jj in range(0, pad_dims):
                posfix_jj = "" if pad_dims==1 else "_"+str(jj)
                for kk in range(0, pad_width):
                    posfix_kk = "" if pad_width==1 else "_"+str(kk)
                    posfix = posfix_jj + posfix_kk
                    pad_name = port_count["ports"][ii]["name"] + posfix
                    pad_cell = self.digital_pad.io.BDIO if ports[ii]["direction"] == "inout" else self.digital_pad.io.DIO
                    pad_def = PadDef()
                    pad_def.setName(pad_name).setCell(pad_cell)
                    self.pad_ring.addPad(pad_def)

    def setCorner(self):
        self.pad_ring.topleft.setRowMax(1).addPad(
            PadDef().setName("TL_CORNER").setCell(self.digital_pad.supply.corner)
        )
        self.pad_ring.topright.setRowMax(1).addPad(
            PadDef().setName("TR_CORNER").setCell(self.digital_pad.supply.corner)
        )
        self.pad_ring.bottomleft.setRowMax(1).addPad(
            PadDef().setName("BL_CORNER").setCell(self.digital_pad.supply.corner)
        )
        self.pad_ring.bottomright.setRowMax(1).addPad(
            PadDef().setName("BR_CORNER").setCell(self.digital_pad.supply.corner)
        )

    def setPGPad(self, io_sup_num, core_sup_num, core_p, core_g, io_p, io_g):
        import math
        core_sup_num_per_side = math.ceil(core_sup_num/4) * 2
        io_sup_num_per_side = math.ceil(io_sup_num/4) * 2
        row_max_num_without_pg = self.pad_ring.row_max
        row_max_num = row_max_num_without_pg + core_sup_num_per_side + io_sup_num_per_side
        self.pad_ring.setRowMax(row_max_num)
        # pg_pad_skip = row_max_num // (core_sup_num_per_side + io_sup_num_per_side) + 1
        pg_pad_skip = math.ceil(row_max_num/(core_sup_num_per_side + io_sup_num_per_side))
        insert_position = [x for x in range(pg_pad_skip-1, row_max_num, pg_pad_skip)]
        vdd_pad_io_supply = PadDef().setName(io_p).setCell(
            self.digital_pad.supply.io_supply.VDD
        )
        vss_pad_io_supply = PadDef().setName(io_g).setCell(
            self.digital_pad.supply.io_supply.VSS
        )
        vdd_pad_core_supply = PadDef().setName(core_p).setCell(
            self.digital_pad.supply.core_supply.VDD
        )
        vss_pad_core_supply = PadDef().setName(core_g).setCell(
            self.digital_pad.supply.core_supply.VSS
        )
        count = 0
        print("insert_position = ", insert_position)
        for idx in insert_position:
            if count % 2 == 0:
                self.pad_ring.top.insertPad(vdd_pad_io_supply, idx)
                self.pad_ring.top.insertPad(vss_pad_io_supply, idx+1)
                self.pad_ring.left.insertPad(vdd_pad_io_supply, idx)
                self.pad_ring.left.insertPad(vss_pad_io_supply, idx+1)
                self.pad_ring.bottom.insertPad(vdd_pad_io_supply, idx)
                self.pad_ring.bottom.insertPad(vss_pad_io_supply, idx+1)
                self.pad_ring.right.insertPad(vdd_pad_io_supply, idx)
                self.pad_ring.right.insertPad(vss_pad_io_supply, idx+1)
            else:
                self.pad_ring.top.insertPad(vdd_pad_core_supply, idx)
                self.pad_ring.top.insertPad(vss_pad_core_supply, idx+1)
                self.pad_ring.left.insertPad(vdd_pad_core_supply, idx)
                self.pad_ring.left.insertPad(vss_pad_core_supply, idx+1)
                self.pad_ring.bottom.insertPad(vdd_pad_core_supply, idx)
                self.pad_ring.bottom.insertPad(vss_pad_core_supply, idx+1)
                self.pad_ring.right.insertPad(vdd_pad_core_supply, idx)
                self.pad_ring.right.insertPad(vss_pad_core_supply, idx+1)
            count += 1

    # ???
    def setOrientation(self):
        pass
    
    def writeIOFile(self, io_file):
        io_global = IOGlobal().setVersion(3).setIOOrder("clockwise").setTotalEdge(4)
        self.setCorner()
        io_pad = str(self.pad_ring)
        io_content = str(io_global) + io_pad
        with open(io_file, "w") as f:
            f.write(io_content)


    def __str__(self):
        # io_global = IOGlobal().setVersion(3).setIOOrder("clockwise").setTotalEdge(4)
        return str(self.pad_ring)
                



