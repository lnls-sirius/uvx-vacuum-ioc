import serial
import threading
from pcaspy import Driver, Alarm, Severity, SimpleServer

group = { ("A","R1") : ("Canhao", "LMV_01A"), ("A", "R2") : ("Tripleto", "LMV_03A"), ("A", "R4") : ("Espectrometro", "LMV_05A"), \
          ("D","R1") : ("AEB09B", "AMV_09B"), ("D", "R2") : ("AEB10B"  , "AMV_10A"), ("D", "R4") : ("ADI11", "AMV_11C"), \
          ("E","R1") : ("AEB07B", "AMV_07B"), ("E", "R2") : ("AEB08B"  , "AMV_08A"), ("E", "R4") : ("AMV_09C", "AMV_09C"), \
          ("F","R1") : ("AEB05C", "AMV_05C"), ("F", "R2") : ("AEB06B"  , "AMV_06A"), ("F", "R4") : ("ACR05A", "ARFA"), \
          ("G","R1") : ("AEB04B", "AMV_04A"), ("G", "R4") : ("ACR05B"  , "AMV_05B"), \
          # ("H","R1") : ("AEB02B", "AMV_02A"), ("H", "R2") : ("AEB03B"  , "AMV_03A"), ("H", "R4") : ("Espelho", "Cam:Espelho:DFE"), \
          # ("I","R1") : ("AEB11B", "AMV_11B"), ("I", "R2") : ("AEB12B"  , "AMV_12"),  ("I", "R4") : ("AWB01", "AMV_01A"), \
          # ("J","R1") : ("AWB11" , "AMV_11A"), ("J", "R2") : ("AEB01B"  , "AMV_01B"), ("J", "R4") : ("ADI01", "AMV_01C"), \
          ("K","R1") : ("AWB07" , "AMV_07A"), ("K", "R2") : ("AWB09"   , "AMV_09A"), ("K", "R4") : ("AMV_09C", "AMV_09C"), \
          ("L","R1") : ("SCR07", "SRFPRES"), ("L", "R2") : ("SKC12"    , "SMV_12A"), ("L", "R4") : ("XSI01", "XMV_01A"), \
          ("M","R1") : ("YSI03", "YMV_03A"), ("M", "R2") : ("SKC02A"   , "SMV_02A"), ("M", "R4") : ("SDI02", "SMV_02B"), \
          ("N","R1") : ("XSG02", "XMV_02A"), ("N", "R2") : ("XSG05"    , "XMV_05A"), ("N", "R4") : ("XSI06", "XMV_06A") }

prefix = "VAC:"

pvs = {}

for key in group.keys ():
    pvs[group[key][0]] = {"type" : "float", "unit" : "pbar", "precision" : 3}

# This class inherits from Driver
class VacuumDriver(Driver):

    def __init__(self):

        Driver.__init__(self)
        
        self.serial = serial.Serial ("/dev/ttyUSB0", baudrate = 9600, \
                                     parity = serial.PARITY_EVEN, \
                                     bytesize = 8, stopbits = 1)

        self.scanThread = threading.Thread (target = self.scan)

        self.scanThread.start ()


    def scan (self):

        while True:

            c = self.serial.read ()

            if c == "$":

                # Reads identification
                id = self.serial.read ()
                # Reads channel
                ch = self.serial.read (2)

                print (id, ch)

                if (id, ch) in group.keys ():

                    # discards CR
                    self.serial.read ()

                    # reads pressure                  
                    s = ""
                    c = self.serial.read ()
                    while c != '\x0d':

                       s = s + c
                       c = self.serial.read ()

                    print s

                    try:
                        self.setParam(group [(id, ch)][0], float (s) * 1e9)
                        print str (float (s) * 1e9)
                    except ValueError:
                        print "Not a number read = " + s

                    self.updatePVs()

# Main function. Instantiates a new server and a new driver.
if __name__ == "__main__":

    CAserver = SimpleServer()
    CAserver.createPV(prefix, pvs)
    driver = VacuumDriver()

    # Processes request each 100 ms
    while (True):
        CAserver.process(0.1)


