import sys

from pyvit.proto.obdii import ObdInterface
from pyvit.hw.cantact import CantactDev
from pyvit.dispatch import Dispatcher

if len(sys.argv) != 2 and len(sys.argv) != 4:
    print("usage: %s CANtact_device [tx_arb_id] [rx_arb_id]" %
          sys.argv[0])
    sys.exit(1)

# set up a CANtact device
dev = CantactDev(sys.argv[1])
dev.set_bitrate(500000)

# create our dispatcher and OBD interface
disp = Dispatcher(dev)

# if we were given tx and rx ids, set them, otherwise use defaults
if len(sys.argv) > 4:
    tx_arb_id = int(sys.argv[4], 0)
    rx_arb_id = int(sys.argv[5], 0)
else:
    # functional address
    tx_arb_id = 0x7DF
    # physical response ID of ECM ECU, responses from other ECUs will be ignored
    rx_arb_id = 0x7E8

obd = ObdInterface(disp, tx_arb_id, rx_arb_id)

# setting debug to true will print all frames sent and received
obd.debug = False
disp.start()

print("Supported PIDs (mode 1):", obd.get_supported_pids(1))
print("Supported PIDs (mode 9):", obd.get_supported_pids(9))

disp.stop()
