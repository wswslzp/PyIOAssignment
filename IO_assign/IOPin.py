from IO_assign.IOAttrTree import IOAttrLeaf, IOAttrTree


class IOPinLocal(IOAttrLeaf):
    # define some variables shared in IOpin field

    def __init__(self):
        IOAttrLeaf.__init__(self, head="locals")
        self._setSingleRow()

    def setSide(self, side):
        # Specifies the side of the I/O pin. This can be:
        # top | north, left | west, right | east, bottom | south
        self._addAttr("side", side)
        return self

    def setEdgeNum(self, edge_num):
        self._addAttr("edge num", edge_num)
        return self 

    def setSpace(self, space):
        self._addAttr("space", space)
        return self


class IOPinInst(IOAttrLeaf):
    
    def __init__(self):
        IOAttrLeaf.__init__(self, head="pin")
        self._setSingleRow()

    def setName(self, name):
        self._addAttr("name", '"' + str(name) + '"')
        return self

    def setLayer(self, layer):
        self._addAttr("layer", layer)
        return self

    def setWidth(self, width):
        self._addAttr("width", width)
        return self

    def setDepth(self, depth):
        self._addAttr("depth", depth)
        return self

    def setUp(self, up):
        self._addAttr("up", up)
        return self

    def setX(self, x):
        self._addAttr("x", x)
        return self

    def setY(self, y):
        self._addAttr("y", y)
        return self

    def setPlaceStatus(self, place_status):
        self._addAttr("place_status", place_status)
        return self

    def setOffset(self, offset):
        self._addAttr("offset", offset)
        return self



class IOPinSide(IOAttrTree):

    def __init__(self, side):
        IOAttrTree.__init__(self, root=side)


class IOPin(IOAttrTree):
    
    def __init__(self):
        IOAttrTree.__init__(self, root="iopin")
        print(
            "# Recommend to use Innovus to assign pin"
        )