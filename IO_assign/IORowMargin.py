from IO_assign.IOAttrTree import IOAttrLeaf, IOAttrTree


class IORow(IOAttrLeaf):
    
    def __init__(self):
        IOAttrLeaf.__init__(self, head="io_row")
        self._setSingleRow()

    def setRingNumber(self, ring_number):
        self._addAttr("ring_number", ring_number)
        return self

    def setMargin(self, margin):
        self._addAttr("margin", margin)
        return self


class RowMarginSide(IOAttrTree):

    def __init__(self, side):
        # side = top, bottom, left, right
        IOAttrTree.__init__(self, root=side)

class IORowMargin(IOAttrTree):
    
    def __init__(self):
        IOAttrTree.__init__(self, "row_margin")