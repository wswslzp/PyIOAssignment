from IO_assign.IOAttrTree import IOAttrLeaf, IOAttrTree


class IOPadLocal(IOAttrLeaf):
    # define some local variables shared in IOPad field
    
    def __init__(self):
        IOAttrLeaf.__init__(self, head='locals')
        self._setSingleRow()

    def setSpace(self, space):
        self._addAttr("space", space)
        return self

    def setRingNumber(self, ring_number):
        self._addAttr("ring_number", ring_number)
        return self

    def setRowName(self, row_name):
        self._addAttr("row_name", '"' + row_name + '"')
        return self


class IOPadInst(IOAttrLeaf):
    
    def __init__(self):
        IOAttrLeaf.__init__(self, head='inst')
        self._setSingleRow()

    def setName(self, name):
        self._addAttr("name", '"' + name + '"')
        return self

    def setX(self, x):
        self._addAttr("x", x)
        return self
    
    def setY(self, y):
        self._addAttr("y", y)
        return self

    def setSkip(self, skip):
        self._addAttr("skip", skip)
        return self

    def setSpace(self, space):
        self._addAttr("space", space)
        return self

    def setOffset(self, offset):
        self._addAttr("offset", offset)
        return self
    
    def setIndent(self, indent):
        self._addAttr("indent", indent)
        return self

    def setOrientation(self, orientation):
        self._addAttr("orientation", orientation)
        return self

    def setPlaceStatus(self, place_status):
        self._addAttr("place_status", place_status)
        return self

    def setKeepClear(self, keep_clear):
        self._addAttr("keep_clear", keep_clear)
        return self

    def setCell(self, cell):
        self._addAttr("cell", '"' + cell + '"')
        return self

    def setEndspaceGap(self, endspace_gap):
        self._addAttr("endspace_gap", endspace_gap)
        return self

    def deepCopy(self):
        import copy
        return copy.deepcopy(self)
        

class IOPadSide(IOAttrTree):
    
    def __init__(self, side):
        # [string]side: "Top", "left", "right", "bottom", or combination
        IOAttrTree.__init__(self, root=side)


class IOPad(IOAttrTree):
    
    def __init__(self):
        IOAttrTree.__init__(self, root="iopad")

