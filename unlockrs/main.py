import sys
import os
import asyncio

# Add the project root directory to the Python path to resolve the module.
# This makes the script runnable directly.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
from unlockrs.config import *
from unlockrs.tokens import *
from unlockrs.pve.start import *
from unlockrs.pve.status import *
from unlockrs.TrueNas.unlock import *


async def main():
    await TrueNas_Boot()
    # TODO Impliment the TrueNAS Components for unlocking the system
    await TrueNas_Unlock()
    exit()


async def TrueNas_Boot():
    global status
    global check
    if "status" not in globals():
        status = pve_vmstatus(
            PVE_Endpoint, PVE_Port, PVE_Node, TrueNas_VMID, TrueNas_Token
        )
        # Debugging Component to Force, if bellow
        # status = "stopped"
        await TrueNas_Boot()
    elif status == "running" and "check" not in globals():
        print("TrueNas Virtual Machine is already Running")
        return ()
    elif status == "running" and check == "start":
        print("TrueNas Virtual Machine has Booted")
        return ()
    elif status == "stopped" and "check" not in globals():
        print("Virtaul Machine is Stopped")
        check = pve_vmpost(
            PVE_Endpoint, PVE_Port, PVE_Node, TrueNas_VMID, "start", TrueNas_Token
        )
        # Debugging Component to Force, if bellow
        # status = "stopped"
        await TrueNas_Boot()
    elif status == "stopped" and check == "start":
        for i in range(5):
            status = pve_vmstatus(
                PVE_Endpoint, PVE_Port, PVE_Node, TrueNas_VMID, TrueNas_Token
            )
            if status == "running":
                print("TrueNas Virtual Machine has Booted")
                print(f"after {i} amount of checks")
            else:
                print("System Failed to Boot")
                print("CHECK PVE SERVER")
    else:
        print("ERROR: Unknown Status")
        exit()


async def TrueNas_Unlock():
    print("DEBUG: TrueNAS Unlock Starts Here")
    await unlock_dataset(
        endpoint=TrueNas_IP,
        dataset=TrueNas_dataset,
        passphrase=TrueNas_passphrase,
        username=TrueNas_Username,
        password=TrueNas_Password,
    )


if __name__ == "__main__":
    asyncio.run(main())
