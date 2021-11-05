from IO_assign.IOAttrTree import IOAttrLeaf

class IOGlobal(IOAttrLeaf):
    
    def __init__(self):
        IOAttrLeaf.__init__(self, head="globals")
    
    def setVersion(self, version):
        # Specifies the beginning of a new I/O format
        self._addAttr("version", version)
        return self

    def setSpace(self, space):
        # Specifies the global I/O pin spacing, in μmeters.
        self._addAttr("space", space)
        return self

    def setTotalEdge(self, total_edge):
        # Specifies the number of edges for the rectilinear block design.
        # The edges are numbered starting from 0. For example, if the total_edge is
        # 4, then the edges are numbered as edge 0, edge 1, edge 2, and edge 3.
        self._addAttr("total_edge", total_edge)
        return self

    def setIOOrder(self, io_order):
        # Specifies the order of the I/O pads and pins. This can be:
        # clockwise, counterclockwise, default
        self._addAttr("io_order", io_order)
        return self

        