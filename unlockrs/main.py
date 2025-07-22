import sys
import os


# Add the project root directory to the Python path to resolve the module.
# This makes the script runnable directly.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
from unlockrs.pve.start import *
from unlockrs.pve.status import *
from unlockrs.config import *
from unlockrs.tokens import *

def main():
    TrueNas_Boot()
    #TODO Impliment the TrueNAS Components for unlocking the system
    exit()


def TrueNas_Boot():
    status = pve_vmstatus(PVE_Endpoint, PVE_Port, PVE_Node, TrueNas_VMID, TruePVE_Token)
    if status == "running":
        print("System Running")
    elif status == "stopped":
        print("System Stopped")
        pve_vmpost(PVE_Endpoint, PVE_Port, PVE_Node, TrueNas_VMID, "start", TruePVE_Token)
        if loop_protect == False:
            loop_protect = True
            TrueNas_Boot()
        if loop_protect == True:
            exit()
    else:
        print("ERROR: Unknown Status")
        exit()



if __name__ == "__main__":
    main()