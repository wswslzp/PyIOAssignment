# What below is the digital pad part.
class DigitalIO(object):
    def __init__(self, DIO = None, BDIO = None, DIO_I=None, DIO_O=None):
        self.DIO = DIO
        self.DIO_I = DIO_I 
        self.DIO_O = DIO_O
        self.BDIO = BDIO

class DigitalCoreSupply(object):
    def __init__(self, VDD = None, VSS = None):
        self.VDD = VDD
        self.VSS = VSS

class DigitalIOSupply(object):
    def __init__(self, VDD = None, VSS = None):
        self.VDD = VDD
        self.VSS = VSS

class DigitalMacroSupply(object):
    def __init__(self, VDD = None, VSS = None):
        self.VDD = VDD
        self.VSS = VSS

class DigitalPowerOn(object):
    def __init__(self, POC = None):
        self.POC = POC

class DigitalGNDConnect(object):
    def __init__(self, ConnectGNDCell = None):
        self.ConnectGNDCell = ConnectGNDCell

class CornerRail(object):
    def __init__(self, Corner = None):
        self.Corner = Corner

class DigitalSupply(object):
    def __init__(self):
        self.core_supply = DigitalCoreSupply()
        self.io_supply = DigitalIOSupply()
        self.macro_supply = DigitalMacroSupply()
        self.poweron = DigitalPowerOn()
        self.gnd_connect = DigitalGNDConnect()
        self.corner = None

class DigitalPad(object):
    def __init__(self):
        self.io = DigitalIO()
        self.supply = DigitalSupply()

class AnalogIO(object):
    def __init__(self, AIO):
        self.AIO = AIO
