import sys
import os
import asyncio

# Add the project root directory to the Python path to resolve the module.
# This makes the script runnable directly.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
from unlockrs.yaml_conf import *
from unlockrs.checks.is_docker import *
from unlockrs.systemcheck import *
from unlockrs.pve.start import *
from unlockrs.pve.status import *
from unlockrs.TrueNas.unlock import *

async def main():
    await SetupConfig()
    await SystemCheck()
    await TrueNas_Boot()
    unlock = await TrueNas_Unlock()
    await VMBoot(unlock)
    exit()


async def SetupConfig():
# Confirm if running in contianer or as application is standalone
    dir_path = is_docker(PROJECT_ROOT=_PROJECT_ROOT)
    # Import the TrueNas Global Variables
    global load
    global PVE_Endpoint, PVE_Port, PVE_Node, PVE_Token
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
    assert status == "online" or "offline"
    if status == "offline":
        exit()


async def TrueNas_Boot():
    vm = TrueNas_VMID
    status, agent, name = pve_vmstatus(
        Endpoint=PVE_Endpoint,
        Port=PVE_Port,
        Node=PVE_Node,
        vmid=TrueNas_VMID,
        token=PVE_Token,
    )
    # Debugging Component to Force, if bellow
    assert status == "running" or status == "stopped"
    if status == "running":
        print(f"Virtual Machine: {name} ID: {vm} is already running")
        return ()
    elif status == "stopped":
        print("Virtaul Machine is Stopped")
        check = pve_vmpost(
            Endpoint=PVE_Endpoint,
            Port=PVE_Port,
            Node=PVE_Node,
            vmid=TrueNas_VMID,
            api_command="start",
            token=PVE_Token,
        )
    assert check == "start"
    if status == "stopped" and check == "start":
        for i in range(1, 6):
            status, agent, name = pve_vmstatus(
                Endpoint=PVE_Endpoint,
                Port=PVE_Port,
                Node=PVE_Node,
                vmid=TrueNas_VMID,
                token=PVE_Token,
            )
            if status == "running":
                print(f"Virtual Machine: {name} ID: {vm} is already running")
                print(f"after {i} amount of checks")
                return ()
            elif status == "stopped" and i == 4:
                print(f"Virtual Machine: {name} ID: {vm} has failed to boot")
                print("CHECK PVE SERVER")
                return ()
            elif i == 4:
                print("Fatel Error")
                exit()


async def TrueNas_Unlock():
    status = await port_check(endpoint=TrueNas_Endpoint, port=TrueNas_Port)
    assert status == "online" or "offline"
    if status == "offline":
        exit()
    unlock = await unlock_dataset(
        endpoint=TrueNas_Endpoint,
        username=TrueNas_Username,
        password=TrueNas_Password,
        dataset=TrueNas_dataset,
        passphrase=TrueNas_passphrase,
    )
    if unlock == "error":
        exit()
    return unlock


async def VMBoot(unlock):
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
        sem = asyncio.Semaphore(GroupStart)
        tasks = [
            start_vm_async(
                sem,
                endpoint=PVE_Endpoint,
                port=PVE_Port,
                node=PVE_Node,
                token=PVE_Token,
                group=group,
                vm=vm,
                delay=StartDelay,
                unlock=unlock,
            )
            for vm in VirtualMachines
        ]
        await asyncio.gather(*tasks)
        print(f"BootGroup: {group} Finished")


async def start_vm_async(sem, endpoint, port, node, token, group, vm, delay, unlock):
    async with sem:
        vm = str(vm)  # Convert to String
        status, agent, name = pve_vmstatus(
            Endpoint=endpoint,
            Port=port,
            Node=node,
            vmid=vm,
            token=token,
        )
        assert status == "running" or "stopped"
        # First System Check if allready running or start virtual machine
        reboot = "true"
        # status = "stopped"
        if status == "running" and unlock == "already" and reboot == "false":
            print(f"Virtual Machine: {name} ID: {vm} is already running")
            return ()
        elif status == "running" and unlock == "already" and reboot == "true":
            print(f"Virtual Machine: {name} ID: {vm} is already running")
            return ()
        elif status == "stopped":
            check = pve_vmpost(
                Endpoint=endpoint,
                Port=port,
                Node=node,
                vmid=vm,
                api_command="start",
                token=token,
            )
            print(f"Starting VM: {vm}")
        assert check == "start" or "rebooted"
        # Check the status of the booting virtual machine
        if status == "stopped" and check == "start":
            for i in range(1, 10):
                status, agent, name = pve_vmstatus(
                    Endpoint=endpoint,
                    Port=port,
                    Node=node,
                    vmid=vm,
                    token=token,
                )
                if status == "running":
                    print(f"Virtual Machine: {name} ID: {vm} has Started")
                    print(f"after {i} checks")
                    await asyncio.sleep(
                        delay
                    )  # Delay Between each virtual machine start
                elif status == "stopped" and i == 4:
                    print(f"Virtual Machine: {name} ID: {vm} has failed to boot")
                    print("CHECK PVE SERVER")
                    return ()
                elif i == 4:
                    print("Fatel Error")
                    exit()
                else:
                    await asyncio.sleep(i)




if __name__ == "__main__":
    asyncio.run(main())
