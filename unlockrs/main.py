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
from unlockrs.systemcheck import *
from unlockrs.TrueNas.unlock import *


#TODO: Encryption / Read USB Key
# The usb key will store the file that contains the encryption key

#TODO: Config File
# Need to define the variables


#TODO: Virtual Machine Booting
# Impliment Array to store all the Settings and Virtual Machines booted after
# Impliment Looping Startup of Virtual Machines with checking of VM State

async def main():
    await SystemCheck()
    await TrueNas_Boot()
    await TrueNas_Unlock()
    await VMBoot()
    exit()

async def SystemCheck():
    status = await port_check(endpoint=PVE_Endpoint, port=8006)
    assert status == "online"
async def TrueNas_Boot():
    global status
    global check
    if "status" not in globals():
        status = pve_vmstatus(
            Endpoint=PVE_Endpoint,
            Port=PVE_Port,
            Node=PVE_Node,
            vmid=TrueNas_VMID,
            token=TrueNas_Token,
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
            Endpoint=PVE_Endpoint,
            Port=PVE_Port,
            Node=PVE_Node,
            vmid=TrueNas_VMID,
            api_command="start",
            token=TrueNas_Token,
        )
        # Debugging Component to Force, if bellow
        # status = "stopped"
        await TrueNas_Boot()
    elif status == "stopped" and check == "start":
        for i in range(5):
            status = pve_vmstatus(
                Endpoint=PVE_Endpoint,
                Port=PVE_Port,
                Node=PVE_Node,
                vmid=TrueNas_VMID,
                token=TrueNas_Token,
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
    await unlock_dataset(
        endpoint=TrueNas_Endpoint,
        dataset=TrueNas_dataset,
        username=TrueNas_Username,
        passphrase=TrueNas_passphrase,
        password=TrueNas_Password,
    )

async def VMBoot(): # STATUS: TODO
    print("DEBUG: VM Boot Starts Here")


if __name__ == "__main__":
    asyncio.run(main())
