from IO_assign.IOHelper import LOGGER


def boolToVerilogLiteral(value):
    """
    value could be True/False, 1/0, "1"/"0"
    """
    return "1'b" + str(int(value))

class IOCellBundle(object):
    def __init__(self, inputEnable="", outputEnable="", cellEnable="", chipPad="", pinToCore="", pinFromCore="", schmitt="", pullUp="", pullDown="", drivingStrength="", slewRate="") -> None:
        super().__init__()
        self.bundle = {
            "inputEnable": inputEnable,
            "outputEnable": outputEnable,
            "cellEnable":cellEnable,
            "chipPad":chipPad,
            "pinToCore":pinToCore,
            "pinFromCore":pinFromCore,
            "schmitt":schmitt,
            "pullUp":pullUp,
            "pullDown":pullDown,
            "drivingStrength":drivingStrength,
            "slewRate":slewRate
        }

    def setMetaInfo(self, meta):
        """
        The meta is from io config, io_config["DataPadCell"]["meta"]
        """
        self.bundle["drivingStrength"] = [boolToVerilogLiteral(c) for c in meta["drivingStrength"]]
        self.bundle["pullUp"] = boolToVerilogLiteral(meta["pullUp"])
        self.bundle["pullDown"] =  boolToVerilogLiteral(meta["pullDown"])
        self.bundle["slewRate"] =  boolToVerilogLiteral(meta["slewRate"])
        self.bundle["schmitt"] =  boolToVerilogLiteral(meta["schmitt"])
        return self

    def enableAsInput(self):
        self.bundle["cellEnable"] = boolToVerilogLiteral(True)
        self.bundle["inputEnable"] = boolToVerilogLiteral(True)
        self.bundle["outputEnable"] = boolToVerilogLiteral(False)
    def enableAsOutput(self):
        self.bundle["cellEnable"] = boolToVerilogLiteral(True)
        self.bundle["inputEnable"] = boolToVerilogLiteral(False)
        self.bundle["outputEnable"] = boolToVerilogLiteral(True)
    def setDirection(self, direction):
        if direction == "input":
            self.enableAsInput()
        elif direction == "output":
            self.enableAsOutput()
        else:
            LOGGER.reportWarn("Now we don't support inout direction setting. Please mannully set.")

class IOCell(object):
    def __init__(self, cellName) -> None:
        """
        self.ports: the keys are logical ports and the values are physical ports.
        """
        super().__init__()
        self.cellName = cellName
        self.ports = {# The comment port of all the input/output/inout pad cell
            "cellEnable": "",
            "chipPad": ""
        } 

    def getCellInstName(self, postfix) -> str:
        return self.cellName + postfix + "_inst"

    def setPortName(self, portConfig):
        """
        set the physical port's name according to the io config
        """
        for logicPort in self.ports:
            if portConfig[logicPort] != "":
                # print("warning, the port {k} is absence".format(k=logicPort))
                LOGGER.reportWarn("warning, the port {k} is absence".format(k=logicPort))
            self.ports[logicPort] = portConfig[logicPort]
        return self

    # logicPort: the key in the self.ports
    # value: the connected signal.
    def setPortToValue(self, logicPort, value, isFinal) -> str:
        """
        return the port connection string: ".port(value)"\n
        here the value is either a wire or a verilog literal `1'b1/1'b0`.
        """
        ret = ""
        ending = ")\n" if isFinal else "),\n"
        if type(self.ports[logicPort]) is str:
            ret = "\t."+self.ports[logicPort]+"(" + value + ending
        elif type(self.ports[logicPort]) is list:
            assert len(self.ports[logicPort]) <= len(value), "ERROR! the size of value is smaller than the port size."
            for ii in range(len(self.ports[logicPort])):
                ret += "\t."+self.ports[logicPort][ii]+"("+value[ii]+ending
        return ret
    
    def connect(self, bundle: IOCellBundle):
        """
        connect the cell port to the bundle, return the connection string.
        """
        ret = ""
        idx = 1
        portsLen = len(self.ports)
        for logicPort in self.ports:
            ret += self.setPortToValue(logicPort, bundle.bundle[logicPort], idx == portsLen)
            idx += 1
        return ret

class InputCell(IOCell):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.ports["inputEnable"] = ""
        self.ports["pinToCore"] = ""
        self.ports["schmitt"] = ""
        self.ports["pullUp"]  = ""
        self.ports["pullDown"]= ""

class OutputCell(IOCell):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.ports["outputEnable"] = ""
        self.ports["pinFromCore"] = ""
        self.ports["drivingStrength"] = []
        self.ports["slewRate"] = ""

class InoutCell(IOCell):
    def __init__(self, cellName) -> None:
        super().__init__(cellName)
        self.ports["inputEnable"] = ""
        self.ports["outputEnable"] = ""
        self.ports["schmitt"] = ""
        self.ports["pullUp"]  = ""
        self.ports["pullDown"]= ""
        self.ports["drivingStrength"] = []
        self.ports["slewRate"] = ""

class IOCellFactory(object):
    def __init__(self) -> None:
        super().__init__()

    def build(self, config, direction) -> IOCell:
        ret = None
        if direction == "input": 
            if config["inputCell"]["valid"]: # if there's an input io cell valid, then use it
                name = config["inputCell"]["name"]
                ret = InputCell(name).setPortName(config["inputCell"]["port"])
            else: # otherwise use the inout io cell
                name = config["inoutCell"]["name"]
                ret = InoutCell(name).setPortName(config["inoutCell"]["port"])
        elif direction == "output":
            if config["outputCell"]["valid"]:
                name = config["outputCell"]["name"]
                ret = OutputCell(name).setPortName(config["outputCell"]["port"])
            else:
                name = config["inoutCell"]["name"]
                ret = InoutCell(name).setPortName(config["inoutCell"]["port"])
        elif direction == "inout":
            name = config["inoutCell"]["name"]
            ret = InoutCell(name).setPortName(config["inoutCell"]["port"])
        else:
            LOGGER.reportError("ERROR direction detected.")
            ret = None
        return ret