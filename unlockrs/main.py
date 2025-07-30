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
    unlock = await TrueNas_Unlock()
    await VMBoot(unlock)
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
    tstatus = await port_check(endpoint=PVE_Endpoint, port=PVE_Port)
    assert tstatus == "online"


async def TrueNas_Boot():
    global tstatus
    global check
    if "tstatus" not in globals():
        tstatus = pve_vmstatus(
            Endpoint=PVE_Endpoint,
            Port=PVE_Port,
            Node=PVE_Node,
            vmid=TrueNas_VMID,
            token=PVE_Token,
        )
        # Debugging Component to Force, if bellow
        # tstatus = "stopped"
        await TrueNas_Boot()
    elif tstatus == "running" and "check" not in globals():
        print("TrueNas Virtual Machine is already Running")
        return ()
    elif tstatus == "running" and check == "start":
        print("TrueNas Virtual Machine has Booted")
        return ()
    elif tstatus == "stopped" and "check" not in globals():
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
        # tstatus = "stopped"
        await TrueNas_Boot()
    elif tstatus == "stopped" and check == "start":
        for i in range(5):
            tstatus = pve_vmstatus(
                Endpoint=PVE_Endpoint,
                Port=PVE_Port,
                Node=PVE_Node,
                vmid=TrueNas_VMID,
                token=PVE_Token,
            )
            if tstatus == "running":
                print("TrueNas Virtual Machine has Booted")
                print(f"after {i} amount of checks")
            else:
                print("System Failed to Boot")
                print("CHECK PVE SERVER")
    else:
        print("ERROR: Unknown Status")
        exit()


async def TrueNas_Unlock():
    unlock = await unlock_dataset(
        endpoint=TrueNas_Endpoint,
        username=TrueNas_Username,
        password=TrueNas_Password,
        dataset=TrueNas_dataset,
        passphrase=TrueNas_passphrase,
    )
    return unlock


async def VMBoot(unlock):  # STATUS: TODO
    VB = "VMBootLoop"
    for group in load[VB]:
    # Check if Variables exists and if they do not set the default value
        if "Reboot" in load[VB][group]:
            Reboot = bool(load[VB][group]["Reboot"])
        else:
            Reboot = False
        assert isinstance(Reboot, bool)
        if "GroupStart" in load[VB][group]:
            GroupStart = load[VB][group]["GroupStart"]
        else:
            GroupStart = int(1)
        print(GroupStart)
        assert isinstance(GroupStart, int)
        if "StartDelay" in load[VB][group]:
            StartDelay = int(load[VB][group]["StartDelay"])
        else:
            StartDelay = 0
        assert isinstance(StartDelay, int)
    # Assert Virtual Machines are Setup and if not crash program
        assert "VirtualMachines" in load[VB][group]
        VirtualMachines = list(load[VB][group]["VirtualMachines"])
        assert isinstance(VirtualMachines, list)
    # Run the concurrent routine for the virtual machine checking and starting
        tasks = [
            start_vm_async(sem=asyncio.Semaphore(GroupStart), group=group, vm=vm, delay=StartDelay, unlock=unlock)
            for vm in VirtualMachines
        ]
        await asyncio.gather(*tasks)


async def start_vm_async(sem, group, vm, delay, unlock):
    async with sem:
        vm = str(vm)  # Convert to String
        print(f"Checking VM Status: {vm}")
        status = pve_vmstatus(
            Endpoint=PVE_Endpoint,
            Port=PVE_Port,
            Node=PVE_Node,
            vmid=vm,
            token=PVE_Token,
        )
        reboot = "true"
        if status == "stopped":
            await asyncio.sleep(delay)
            print(f"Finished VM: {vm}")
        if status == "running" and unlock == "already" and reboot == "true":
            print(f"Finished VM: {vm} with unlock and reboot")


if __name__ == "__main__":
    asyncio.run(main())
