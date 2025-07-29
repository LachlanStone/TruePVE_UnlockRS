import sys
import os
import asyncio

# Add the project root directory to the Python path to resolve the module.
# This makes the script runnable directly.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
from unlockrs.yaml_conf import *
from unlockrs.systemcheck import *
from unlockrs.pve.start import *
from unlockrs.pve.status import *
from unlockrs.TrueNas.unlock import *

# Global Variables


# TODO: Encryption / Read USB Key
# The usb key will store the file that contains the encryption key

# TODO: Config File
# Need to define the variables


# TODO: Virtual Machine Booting
# Impliment Array to store all the Settings and Virtual Machines booted after
# Impliment Looping Startup of Virtual Machines with checking of VM State


async def main():
    await SetupConfig()
    await SystemCheck()
    await TrueNas_Boot()
    await TrueNas_Unlock()
    await VMBoot()
    exit()


async def SetupConfig():
    # Set the default location for the project root files
    dir_path = _PROJECT_ROOT
    # Import the TrueNas Global Variables
    global PVE_Endpoint, PVE_Port, PVE_Node, PVE_Token, load
    global TrueNas_Endpoint, TrueNas_Port, TrueNas_VMID, TrueNas_dataset, TrueNas_passphrase, TrueNas_FilePath, TrueNas_Username, TrueNas_Password, TrueNas_Token
    load = await setup_configfile(dir_path=dir_path)
    TrueNas_Endpoint = load["TrueNas"]["Endpoint"]
    TrueNas_Port = load["TrueNas"]["Port"]
    TrueNas_VMID = load["TrueNas"]["vmid"]
    TrueNas_dataset = load["TrueNas"]["DataSet"]["Name"]
    TrueNas_passphrase = load["TrueNas"]["DataSet"]["PassPhrase"]
    TrueNas_FilePath = load["TrueNas"]["DataSet"]["FilePath"]
    TrueNas_Username = load["TrueNas"]["Auth"]["Username"]
    TrueNas_Password = load["TrueNas"]["Auth"]["Password"]
    TrueNas_Token = load["TrueNas"]["Auth"]["API_Token"]
    PVE_Endpoint = load["PVE"]["Endpoint"]
    PVE_Port = load["PVE"]["Port"]
    PVE_Node = load["PVE"]["Node"]
    PVE_Token = load["PVE"]["Token"]


async def SystemCheck():
    status = await port_check(endpoint=PVE_Endpoint, port=PVE_Port)
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
            token=PVE_Token,
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
            token=PVE_Token,
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
                token=PVE_Token,
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
        username=TrueNas_Username,
        password=TrueNas_Password,
        dataset=TrueNas_dataset,
        passphrase=TrueNas_passphrase,
    )


async def VMBoot():  # STATUS: TODO
    VB = "VMBootLoop"
    for group in load[VB]:
        for VirtualMachines in load[VB][group]["VirtualMachines"]:
            StartDelay = load[VB][group]["StartDelay"]
            GroupStart = load[VB][group]["GroupStart"]
            VirtualMachines = load[VB][group]["VirtualMachines"]
            for vm in VirtualMachines:
                # Convert this to multi Procesing for the GroupStart
                print(GroupStart)
                # Make this the VM Start funtion
                print(vm)
                # Nested For loop for the status
                print(vm)
                if isinstance(StartDelay, int):
                    time.sleep(StartDelay)


if __name__ == "__main__":
    asyncio.run(main())
